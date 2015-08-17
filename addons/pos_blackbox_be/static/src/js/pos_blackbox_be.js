odoo.define('pos_blackbox_be.pos_blackbox_be', function (require) {
    var core    = require('web.core');
    var screens = require('point_of_sale.screens');
    var models = require('point_of_sale.models');
    var devices = require('point_of_sale.devices');
    var chrome = require('point_of_sale.chrome');
    var Class = require('web.Class');
    var PaymentScreenWidget = screens.PaymentScreenWidget;

    var _t      = core._t;

    models.Orderline = models.Orderline.extend({
        // generates a table of the form
        // {..., 'char_to_translate': translation_of_char, ...}
        _generate_translation_table: function() {
            var replacements = [
                ["ÄÅÂÁÀâäáàã", "A"],
                ["Ææ", "AE"],
                ["ß", "SS"],
                ["çÇ", "C"],
                ["ÎÏÍÌïîìí", "I"],
                ["€", "E"],
                ["ÊËÉÈêëéè", "E"],
                ["ÛÜÚÙüûúù", "U"],
                ["ÔÖÓÒöôóò", "O"],
                ["Œœ", "OE"],
                ["ñÑ", "N"],
                ["ýÝÿ", "Y"]
            ];

            var lowercase_to_uppercase = _.range("a".charCodeAt(0), "z".charCodeAt(0) + 1).map(function(lowercase_ascii_code) {
                return [String.fromCharCode(lowercase_ascii_code), String.fromCharCode(lowercase_ascii_code).toUpperCase()];
            });
            replacements = replacements.concat(lowercase_to_uppercase);

            var lookup_table = {};

            _.forEach(replacements, function(letter_group) {
                _.forEach(letter_group[0], function(special_char) {
                    lookup_table[special_char] = letter_group[1];
                });
            });

            return lookup_table;
        },

        _replace_hash_and_sign_chars: function(str) {
            if (typeof str !== 'string') {
                throw "Can only handle strings";
            }

            var translation_table = this._generate_translation_table();

            var replaced_char_array = _.map(str, function (char, index, str) {
                var translation = translation_table[char];
                if (translation) {
                    return translation;
                } else {
                    return char;
                }
            });

            return replaced_char_array.join("");
        },

        // for hash and sign the allowed range for DATA is:
        //   - A-Z
        //   - 0-9
        // and SPACE as well. We filter SPACE out here though, because
        // SPACE will only be used in DATA of hash and sign as description
        // padding
        _filter_allowed_hash_and_sign_chars: function(str) {
            if (typeof str !== 'string') {
                throw "Can only handle strings";
            }

            var filtered_char_array = _.filter(str, function (char) {
                var ascii_code = char.charCodeAt(0);

                if ((ascii_code >= "A".charCodeAt(0) && ascii_code <= "Z".charCodeAt(0)) ||
                    (ascii_code >= "0".charCodeAt(0) && ascii_code <= "9".charCodeAt(0))) {
                    return true;
                } else {
                    return false;
                }
            });

            return filtered_char_array.join("");
        },

        // for both amount and price
        // price should be in eurocents
        // amount should be in gram
        _prepare_number_for_plu: function(number, field_length) {
            number = Math.abs(number);
            number = Math.round(number); // todo jov: don't like this

            var number_string = number.toFixed(0);

            number_string = this._replace_hash_and_sign_chars(number_string);
            number_string = this._filter_allowed_hash_and_sign_chars(number_string);

            // get the required amount of least significant characters
            number_string = number_string.substr(-field_length);

            // pad left with 0 to required size
            while (number_string.length < field_length) {
                number_string = "0" + number_string;
            }

            return number_string;
        },

        _prepare_description_for_plu: function(description) {
            description = this._replace_hash_and_sign_chars(description);
            description = this._filter_allowed_hash_and_sign_chars(description);

            // get the 20 most significant characters
            description = description.substr(0, 20);

            // pad right with SPACE to required size of 20
            while (description.length < 20) {
                description = description + " ";
            }

            return description;
        },

        _get_amount_for_plu: function () {
            // three options:
            // 1. unit => need integer
            // 2. weight => need integer gram
            // 3. volume => need integer milliliter

            var amount = this.get_quantity();
            var uom = this.get_unit();

            if (uom.is_unit) {
                return amount;
            } else {
                if (uom.category_id[1] === "Weight") {
                    var uom_gram = _.find(this.pos.units_by_id, function (unit) {
                        return unit.category_id[1] === "Weight" && unit.name === "g";
                    });
                    amount = (amount / uom.factor) * uom_gram.factor;
                } else if (uom.category_id[1] === "Volume") {
                    var uom_milliliter = _.find(this.pos.units_by_id, function (unit) {
                        return unit.category_id[1] === "Volume" && unit.name === "Milliliter(s)";
                    });
                    amount = (amount / uom.factor) * uom_milliliter.factor;
                }

                return amount;
            }
        },

        _get_vat_letter: function () {
            var taxes = this.get_taxes()[0];
            var line_name = this.get_product().display_name;

            if (! taxes) {
                throw new Error(line_name + " has no tax associated with it.");
            }

            var vat_letter = taxes.identification_letter;

            if (! vat_letter) {
                throw new Error(line_name + " has an invalid tax amount. Only 21%, 12%, 6% and 0% are allowed.");
            }

            return vat_letter;
        },

        generate_plu_line: function () {
            // |--------+-------------+-------+-----|
            // | AMOUNT | DESCRIPTION | PRICE | VAT |
            // |      4 |          20 |     8 |   1 |
            // |--------+-------------+-------+-----|

            // steps:
            // 1. replace all chars
            // 2. filter out forbidden chars
            // 3. build PLU line

            var amount = this._get_amount_for_plu();
            var description = this.get_product().display_name;
            var price_in_eurocents = this.get_display_price() * 100;
            var vat_letter = this._get_vat_letter();

            amount = this._prepare_number_for_plu(amount, 4);
            description = this._prepare_description_for_plu(description);
            price_in_eurocents = this._prepare_number_for_plu(price_in_eurocents, 8);

            return amount + description + price_in_eurocents + vat_letter;
        }
    });

    models.Order = models.Order.extend({
        _hash_and_sign_string: function() {
            var order_str = "";

            this.get_orderlines().forEach(function (current, index, array) {
                order_str += current.generate_plu_line();
            });

            return order_str;
        },

        get_base_price_in_eurocents_per_tax_letter: function () {
            var base_price_per_tax_letter = {
                'A': 0,
                'B': 0,
                'C': 0,
                'D': 0
            };

            this.get_orderlines().forEach(function (current, index, array) {
                var tax_letter = current._get_vat_letter();

                if (tax_letter) {
                    base_price_per_tax_letter[tax_letter] += Math.floor(current.get_price_without_tax() * 100);
                }
            });

            return base_price_per_tax_letter;
        },

        calculate_hash: function() {
            return Sha1.hash(this._hash_and_sign_string());
        }
    });

    var FDMPacketField = Class.extend({
        init: function (name, length, content, pad_character) {
            if (typeof content !== 'string') {
                throw "Can only handle string contents";
            }

            this.name = name;
            this.length = length;

            this.content = this._pad_left_to_length(content, pad_character);
        },

        _pad_left_to_length: function (content, pad_character) {
            if (content.length < this.length && ! pad_character) {
                throw "Can't pad without a pad character";
            }

            while (content.length < this.length) {
                content = pad_character + content;
            }

            return content;
        },

        to_string: function () {
            return this.content;
        }
    });

    var FDMPacket = Class.extend({
        init: function () {
            this.fields = [];
        },

        add_field: function (field) {
            this.fields.push(field);
        },

        from_string: function (packet_string) {
            // todo jov: parse FDM responses
        },

        to_string: function () {
            return _.map(this.fields, function (field) {
                return field.to_string();
            }).join("");
        },

        to_human_readable_string: function () {
            return _.map(this.fields, function (field) {
                return field.name + ": " + field.to_string();
            }).join("\n");
        }

        // todo jov: send: function () {}?
    });

    PaymentScreenWidget.include({
        _handle_fdm_errors: function (parsed_response) {
            var error_1 = parsed_response.error_1;
            var error_2 = parsed_response.error_2;

            if (error_1 === 0) { // no errors
                if (error_2 === 1) {
                    this.gui.show_popup("confirm", {
                        'title': _t("Fiscal Data Module"),
                        'body':  _t("PIN accepted."),
                    });
                }

                return true;
            } else if (error_1 === 1) { // warnings
                if (error_2 === 1) {
                    this.gui.show_popup("error", {
                        'title': _t("Fiscal Data Module warning"),
                        'body':  _t("Fiscal Data Module memory 90% full."),
                    });
                } else if (error_2 === 2) {
                    this.gui.show_popup("error", {
                        'title': _t("Fiscal Data Module warning"),
                        'body':  _t("Already handled request."),
                    });
                } else if (error_2 === 3) {
                    this.gui.show_popup("error", {
                        'title': _t("Fiscal Data Module warning"),
                        'body':  _t("No record."),
                    });
                } else if (error_2 === 99) {
                    this.gui.show_popup("error", {
                        'title': _t("Fiscal Data Module warning"),
                        'body':  _t("Unspecified warning."),
                    });
                }

                return true;
            } else { // errors
                if (error_2 === 1) {
                    this.gui.show_popup("error", {
                        'title': _t("Fiscal Data Module error"),
                        'body':  _t("No Vat Signing Card or Vat Signing Card broken."),
                    });
                } else if (error_2 === 2) {
                    this.gui.show_popup("error", {
                        'title': _t("Fiscal Data Module error"),
                        'body':  _t("Vat Signing Card not initialized with PIN."),
                    });
                } else if (error_2 === 3) {
                    this.gui.show_popup("error", {
                        'title': _t("Fiscal Data Module error"),
                        'body':  _t("Vat Signing Card blocked."),
                    });
                } else if (error_2 === 4) {
                    this.gui.show_popup("error", {
                        'title': _t("Fiscal Data Module error"),
                        'body':  _t("Invalid PIN."),
                    });
                } else if (error_2 === 5) {
                    this.gui.show_popup("error", {
                        'title': _t("Fiscal Data Module error"),
                        'body':  _t("Fiscal Data Module memory full."),
                    });
                } else if (error_2 === 6) {
                    this.gui.show_popup("error", {
                        'title': _t("Fiscal Data Module error"),
                        'body':  _t("Unknown identifier."),
                    });
                } else if (error_2 === 7) {
                    this.gui.show_popup("error", {
                        'title': _t("Fiscal Data Module error"),
                        'body':  _t("Invalid data in message."),
                    });
                } else if (error_2 === 8) {
                    this.gui.show_popup("error", {
                        'title': _t("Fiscal Data Module error"),
                        'body':  _t("Fiscal Data Module not operational."),
                    });
                } else if (error_2 === 9) {
                    this.gui.show_popup("error", {
                        'title': _t("Fiscal Data Module error"),
                        'body':  _t("Fiscal Data Module real time clock corrupt."),
                    });
                } else if (error_2 === 10) {
                    this.gui.show_popup("error", {
                        'title': _t("Fiscal Data Module error"),
                        'body':  _t("Vat Signing Card not compatible with Fiscal Data Module."),
                    });
                } else if (error_2 === 99) {
                    this.gui.show_popup("error", {
                        'title': _t("Fiscal Data Module error"),
                        'body':  _t("Unspecified error."),
                    });
                }

                return false;
            }
        },

        validate_order: function (force_validation) {
            var self = this;
            var payment_screen_super = this._super.bind(self);

            var order = self.pos.get_order();
            this.pos.proxy.request_fdm_hash_and_sign(order).then(function (response) {
                if (! response) {
                    self.gui.show_popup("error", {
                        'title': _t("Fiscal Data Module error"),
                        'body':  _t("Could not connect to the Fiscal Data Module."),
                    });
                } else {
                    // todo jov: deal with error codes
                    var parsed_response = self.pos.proxy.parse_fdm_hash_and_sign_response(response);
                    console.log(response);
                    console.log(parsed_response);

                    if (self._handle_fdm_errors(parsed_response)) {
                        // payment_screen_super(force_validation);
                    }
                }
            });
        }
    });

    devices.ProxyDevice.include({
        sequence_number: 0,

        _increment_sequence_number: function () {
            this.sequence_number = (this.sequence_number + 1) % 100;
        },

        build_request: function (id) {
            var packet = new FDMPacket();

            packet.add_field(new FDMPacketField("id", 1, id));
            packet.add_field(new FDMPacketField("sequence number", 2, this.sequence_number.toString(), "0"));
            packet.add_field(new FDMPacketField("retry number", 1, "0"));
            this._increment_sequence_number();

            return packet;
        },

        _parse_fdm_common_response: function (response) {
            return {
                identifier: response[0],
                sequence_number: parseInt(response.substr(1, 2), 10),
                retry_counter: parseInt(response[3], 10),
                error_1: parseInt(response[4], 10),
                error_2: parseInt(response.substr(5, 2), 10),
                error_3: parseInt(response.substr(7, 3), 10),
                fdm_unique_production_number: response.substr(10, 11),
            };
        },

        parse_fdm_identification_response: function (response) {
            return _.extend(this._parse_fdm_common_response(response),
                            {
                                fdm_firmware_version_number: response.substr(21, 20),
                                fdm_communication_protocol_version: response[41],
                                vsc_identification_number: response.substr(42, 14),
                                vsc_version_number: parseInt(response.substr(56, 3), 10)
                            });
        },

        parse_fdm_hash_and_sign_response: function (response) {
            return _.extend(this._parse_fdm_common_response(response),
                            {
                                vsc_identification_number: response.substr(21, 14),
                                date: response.substr(35, 8),
                                time: response.substr(43, 6),
                                event_label: response.substr(49, 2),
                                vsc_ticket_counter: parseInt(response.substr(51, 9)),
                                vsc_total_ticket_counter: parseInt(response.substr(60, 9)),
                                signature: response.substr(69, 40)
                            });
        },

        _build_fdm_identification_request: function () {
            return this.build_request("I");
        },

        // todo jov: p77
        _build_fdm_hash_and_sign_request: function (order) {
            var packet = this.build_request("H");
            var insz_or_bis_number = this.pos.get_cashier().insz_or_bis_number;

            if (! insz_or_bis_number) {
                throw new Error("INSZ or BIS number not set for current cashier.");
            }

            packet.add_field(new FDMPacketField("ticket date", 8, moment().format("YYYYMMDD")));
            packet.add_field(new FDMPacketField("ticket time", 6, moment().format("HHmmss")));
            packet.add_field(new FDMPacketField("insz or bis number", 11, insz_or_bis_number));

            // todo jov:
            // they want PPPPPPP to uniquely identify users, don't think we can do that
            // id   cert license-key
            // BXXX CCC  PPPPPPP
            packet.add_field(new FDMPacketField("production number POS", 14, "0", "0"));

            // todo jov:
            // this should be truly sequential (so always +1) also across sessions
            // so probably just add a field on the point_of_sale
            packet.add_field(new FDMPacketField("ticket number", 6, order.sequence_number.toString(), "0"));

            // todo jov:
            // p3 pdf
            // most normal thing is normal sales => NS
            // but there's also the training and pro forma (implement?)
            packet.add_field(new FDMPacketField("event label", 2, "NS"));

            packet.add_field(new FDMPacketField("total amount to pay in eurocent", 11, (order.get_due() * 100).toString(), " "));

            var tax_amounts = order.get_base_price_in_eurocents_per_tax_letter();
            packet.add_field(new FDMPacketField("tax percentage 1", 4, "2100"));
            packet.add_field(new FDMPacketField("amount at tax percentage 1 in eurocent", 11, tax_amounts['A'].toString(), " "));
            packet.add_field(new FDMPacketField("tax percentage 2", 4, "1200"));
            packet.add_field(new FDMPacketField("amount at tax percentage 2 in eurocent", 11, tax_amounts['B'].toString(), " "));
            packet.add_field(new FDMPacketField("tax percentage 3", 4, " 600"));
            packet.add_field(new FDMPacketField("amount at tax percentage 3 in eurocent", 11, tax_amounts['C'].toString(), " "));
            packet.add_field(new FDMPacketField("tax percentage 4", 4, " 000"));
            packet.add_field(new FDMPacketField("amount at tax percentage 4 in eurocent", 11, tax_amounts['D'].toString(), " "));
            packet.add_field(new FDMPacketField("PLU hash", 40, order.calculate_hash()));

            console.log(order._hash_and_sign_string());
            console.log(order.calculate_hash());

            return packet;
        },

        request_fdm_identification: function () {
            var self = this;

            return this.message('request_blackbox', {
                'high_layer': self._build_fdm_identification_request().to_string(),
                'response_size': 59
            });
        },

        request_fdm_hash_and_sign: function (order) {
            var self = this;

            return this.message('request_blackbox', {
                'high_layer': self._build_fdm_hash_and_sign_request(order).to_string(),
                'response_size': 109
            });
        }
    });

    var _posmodelproto = models.PosModel.prototype;
    models.PosModel = models.PosModel.extend({
        // todo jov: use exports.load_fields = function(model_name, fields) {
        initialize: function (session, attributes) {
            var user_model = _.find(this.models, function (model) {
                return model.model === "res.users" && _.find(model.fields, function (field) {
                    return field === "pos_security_pin";
                });
            });
            user_model.fields.push("insz_or_bis_number");

            var tax_model = _.find(this.models, function (model) {
                return model.model === "account.tax";
            });
            tax_model.fields.push("identification_letter");

            _posmodelproto.initialize.apply(this, arguments);
        }
    });

    chrome.DebugWidget.include({
        start: function () {
            var self = this;
            this._super();

            this.$('.button.request-fdm-identification').click(function () {
                console.log("Sending identification request to controller...");

                self.pos.proxy.request_fdm_identification().then(function (response) {
                    console.log(response);
                    console.log(self.pos.proxy.parse_fdm_identification_response(response));
                });
            });

            this.$('.button.build-hash-and-sign-request').click(function () {
                console.log(self.pos.proxy._build_fdm_hash_and_sign_request(self.pos.get_order()).to_human_readable_string());
            });
        }
    });

    return {
        'FDMPacketField': FDMPacketField,
        'FDMPacket': FDMPacket
    };
});
