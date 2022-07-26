/** @odoo-module **/

import '@mail/widgets/form_renderer/form_renderer'; // ensure mail overrides are applied first

import FormRenderer from 'web.FormRenderer';

export default FormRenderer.extend({
    _makeChatterContainerProps() {
        const props = this._super();
        return {
            ...props,
            hasActivities: false,
            hasFollowers: false,
            hasMessageList: true,
        };
    },
});
