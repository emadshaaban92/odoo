/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Field
        [Field/name]
            dateCreate
        [Field/model]
            Activity
        [Field/type]
            attr
        [Field/target]
            Date
`;
