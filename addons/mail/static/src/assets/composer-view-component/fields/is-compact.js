/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Field
        [Field/name]
            isCompact
        [Field/model]
            ComposerViewComponent
        [Field/type]
            attr
        [Field/target]
            Boolean
        [Field/default]
            true
`;
