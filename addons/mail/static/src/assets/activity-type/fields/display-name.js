/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Field
        [Field/name]
            displayName
        [Field/model]
            ActivityType
        [Field/type]
            attr
        [Field/target]
            String
`;
