odoo.define('website_event.ticket_qty_selection', require => {
'use strict';

const publicWidget = require('web.public.widget');
const core = require('web.core');

/**
 * This widget can be hooked to a select tag in order to send an
 * "event_ticket_quantity_change" event each time the selection is changed.
 * The event payload contains ticketId:{integer}, quantity:{integer}.
 *
 * @param ticketId id of the ticket to which the selection refers
 */
const EventTicketQuantitySelectionWidget = publicWidget.Widget.extend({
    selector: '.o_event_ticket_quantity_selection',
    events: {
        'change': '_onQuantityChange',
    },

    start: function () {
        this.ticketId = this.$el.data('ticketId');
        // Some browser keeps the value of the selection when refreshing the page. As it would be hard to send the event
        // when other components listening to the event are ready, we give an initial value known of other components.
        this.$el.val('0');
    },

    _onQuantityChange: function (ev) {
        core.bus.trigger('event_ticket_quantity_change', {
            ticketId: this.ticketId,
            quantity: parseInt(ev.target.value)
        });
    },
});

publicWidget.registry.EventTicketQuantitySelectionWidget = EventTicketQuantitySelectionWidget;

return EventTicketQuantitySelectionWidget;

});
