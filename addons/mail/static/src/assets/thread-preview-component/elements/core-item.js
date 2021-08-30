/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Element
        [Element/name]
            coreItem
        [Element/model]
            ThreadPreviewComponent
        [Record/models]
            NotificationListItemComponent/coreItem
`;
