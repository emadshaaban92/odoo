/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Element
        [Element/name]
            headphoneButtonIconWrapper
        [Element/model]
            RtcControllerComponent
        [Record/models]
            RtcControllerComponent/buttonIconWrapper
`;
