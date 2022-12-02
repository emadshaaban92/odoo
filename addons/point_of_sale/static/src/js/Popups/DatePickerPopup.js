/** @odoo-module */

import AbstractAwaitablePopup from "@point_of_sale/js/Popups/AbstractAwaitablePopup";
import Registries from "@point_of_sale/js/Registries";
import { _lt } from "@web/core/l10n/translation";

const { onMounted, useRef, useState } = owl;

class DatePickerPopup extends AbstractAwaitablePopup {
    setup() {
        super.setup();
        this.state = useState({shippingDate: new Date().toISOString().split('T')[0]});
        this.inputRef = useRef('input');
        onMounted(this.onMounted);
    }
    onMounted() {
        this.inputRef.el.focus();
    }
    getPayload() {
        return this.state.shippingDate < this.today() ? false : this.state.shippingDate;
    }
    today() {
        return new Date().toISOString().split('T')[0]
    }
    
}
DatePickerPopup.template = 'DatePickerPopup';
DatePickerPopup.defaultProps = {
    confirmText: _lt('Confirm'),
    cancelText: _lt('Discard'),
    title: _lt('DatePicker'),
};

Registries.Component.add(DatePickerPopup);

export default DatePickerPopup;
