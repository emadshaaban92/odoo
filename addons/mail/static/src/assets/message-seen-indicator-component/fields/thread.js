/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Field
        [Field/name]
            thread
        [Field/model]
            MessageSeenIndicatorComponent
        [Field/type]
            one
        [Field/target]
            Thread
        [Field/isRequired]
            true
`;
