/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            ModelAddon
        [ModelAddon/feature]
            hr_holidays
        [ModelAddon/model]
            ThreadViewComponent
        [ModelAddon/template]
            root
                outOfOffice
`;
