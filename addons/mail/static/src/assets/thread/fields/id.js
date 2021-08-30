/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Field
        [Field/name]
            id
        [Field/model]
            Thread
        [Field/type]
            attr
        [Field/isReadonly]
            true
        [Field/isRequired]
            true
`;
