/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Element
        [Element/name]
            headerAutogrowSeparator
        [Element/model]
            ThreadPreviewComponent
        [web.Element/tag]
            span
        [Record/models]
            AutogrowComponent
`;
