/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Field
        [Field/name]
            isActive
        [Field/model]
            ComposerSuggestionComponent
        [Field/type]
            attr
        [Field/target]
            Boolean
        [Field/default]
            false
`;
