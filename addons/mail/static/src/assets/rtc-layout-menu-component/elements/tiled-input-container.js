/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Element
        [Element/name]
            tiledInputContainer
        [Element/model]
            RtcLayoutMenuComponent
        [Record/models]
            RtcLayoutMenuComponent/inputContainer
`;
