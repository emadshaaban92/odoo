/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Element
        [Element/name]
            separatorLabelDate
        [Element/model]
            MessageListComponent:messageContainer
        [web.Element/tag]
            span
        [Record/models]
            MessageListComponent/separatorLabel
        [web.Element/textContent]
            @template
            .{Template/messageDay}
`;
