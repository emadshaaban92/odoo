/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Element
        [Element/name]
            moreButtonIcon
        [Element/model]
            RtcControllerComponent
        [Record/models]
            RtcControllerComponent/buttonIcon
        [web.Element/class]
            fa-ellipsis-h
`;
