/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Element
        [Element/name]
            loading
        [Element/model]
            AttachmentViewerComponent
        [Element/isPresent]
            @record
            .{AttachmentViewerComponent/record}
            .{AttachmentViewer/isImageLoading}
        [web.Element/style]
            [web.scss/position]
                absolute
`;
