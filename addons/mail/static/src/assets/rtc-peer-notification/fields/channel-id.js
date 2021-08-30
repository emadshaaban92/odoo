/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Field
        [Field/name]
            channelId
        [Field/model]
            RtcPeerNotification
        [Field/isReadonly]
            true
        [Field/isRequired]
            true
`;
