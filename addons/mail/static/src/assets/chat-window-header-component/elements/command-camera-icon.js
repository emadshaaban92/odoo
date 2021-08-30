/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Element
        [Element/name]
            commandCameraIcon
        [Element/model]
            ChatWindowHeaderComponent
        [web.Element/tag]
            i
        [web.Element/class]
            fa
            fa-video-camera
`;
