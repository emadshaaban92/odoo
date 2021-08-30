/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Element
        [Element/name]
            followingLabel
        [Element/model]
            FollowButtonComponent
        [web.Element/tag]
            span
        [Element/isPresent]
            @record
            .{FollowButtonComponent/isUnfollowButtonHighlighted}
        [web.Element/textContent]
            {Locale/text}
                Following
`;
