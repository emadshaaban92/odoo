/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Element
        [Element/name]
            sidebar
        [Element/model]
            NotificationRequestComponent
        [Record/models]
            NotificationListItemComponent/sidebar
`;
