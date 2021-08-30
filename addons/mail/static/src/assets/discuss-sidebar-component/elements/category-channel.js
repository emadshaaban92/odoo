/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Element
        [Element/name]
            categoryChannel
        [Element/model]
            DiscussSidebarComponent
        [Record/models]
            DiscussSidebarComponent/category
        [Field/target]
            DiscussSidebarCategoryComponent
        [DiscussSidebarCategoryComponent/category]
            @record
            .{DiscussSidebarComponent/discussView}
            .{DiscussView/discuss}
            .{Discuss/categoryChannel}
`;
