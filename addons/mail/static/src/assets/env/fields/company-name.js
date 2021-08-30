/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Field
        [Field/name]
            companyName
        [Field/model]
            Env
        [Field/type]
            attr
        [Field/target]
            String
`;
