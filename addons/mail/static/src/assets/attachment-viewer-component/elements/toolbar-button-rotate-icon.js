/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Element
        [Element/name]
            toolbarButtonRotateIcon
        [Element/model]
            AttachmentViewerComponent
        [web.Element/tag]
            i
        [web.Element/class]
            fa
            fa-fw
            fa-repeat
        [web.Element/role]
            img
`;
