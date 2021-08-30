/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Field
        [Field/name]
            members
        [Field/model]
            ChannelMemberListMemberListComponent
        [Field/type]
            many
        [Field/target]
            Partner
`;
