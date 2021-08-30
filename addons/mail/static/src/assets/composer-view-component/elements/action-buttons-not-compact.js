/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Element
        [Element/name]
            actionButtonsNotCompact
        [Element/model]
            ComposerViewComponent
        [Record/models]
            ComposerViewComponent/actionButtons
        [Element/isPresent]
            @record
            .{ComposerViewComponent/isCompact}
`;
