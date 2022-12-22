odoo.define('website_event_sale.ticket_details', function (require) {
    var publicWidget = require('web.public.widget');
    var ticketDetailsWidget = require('website_event.ticket_details');

    ticketDetailsWidget.include({
        /**
         * Overriding the method to toggle the tickets registration
         * pricelist dropdown visibility on ticket details click
         */
        _onTicketDetailsClick: function(ev) {
            this._super(...arguments);
            if (this.foldedByDefault){
                $(ev.currentTarget).siblings('#o_wevent_tickets_pricelist').toggleClass('collapse');
            }
        }
    });

return publicWidget.registry.ticketDetailsWidget;
});
