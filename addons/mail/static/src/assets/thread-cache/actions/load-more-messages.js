/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Action
        [Action/name]
            ThreadCache/loadMoreMessages
        [Action/params]
            threadCache
                [type]
                    ThreadCache
        [Action/behavior]
            {if}
                @threadCache
                .{ThreadCache/isAllHistoryLoaded}
                .{|}
                    @threadCache
                    .{ThreadCache/isLoading}
            .{then}
                {break}
            {if}
                @threadCache
                .{ThreadCache/isLoaded}
                .{isFalsy}
            .{then}
                {Record/update}
                    [0]
                        @threadCache
                    [1]
                        [ThreadCache/isCacheRefreshRequested]
                            true
                {break}
            {Record/update}
                [0]
                    @threadCache
                [1]
                    [ThreadCache/isLoadingMore]
                        true
            :messageIds
                @threadCache
                .{ThreadCache/fetchedMessages}
                .{Collection/map}
                    {Record/insert}
                        [Record/models]
                            Function
                        [Function/in]
                            item
                        [Function/out]
                            @item
                            .{Message/id}
            :limit
                30
            {try}
                :fetchedMessages
                    {ThreadCache/_loadMessages}
                        [0]
                            @threadCache
                        [1]
                            [limit]
                                @limit
                            [maxId]
                                {Math/min}
                                    @messageIds
                :success
                    true
            .{catch}
                :success
                    false
            {if}
                {Record/exists}
                    @threadCache
                .{isFalsy}
            .{then}
                {break}
            {if}
                @success
            .{then}
                {if}
                    @fetchedMessages
                    .{Collection/length}
                    .{<}
                        @limit
                .{then}
                    {Record/update}
                        [0]
                            @threadCache
                        [1]
                            [ThreadCache/isAllHistoryLoaded]
                                true
                {foreach}
                    @threadCache
                    .{ThreadCache/threadViews}
                .{as}
                    threadView
                .{do}
                    {ThreadView/addComponentHint}
                        [0]
                            @threadView
                        [1]
                            more-messages-loaded
                        [2]
                            [fetchedMessages]
                                @fetchedMessages
            {Record/update}
                [0]
                    @threadCache
                [1]
                    [ThreadCache/isLoadingMore]
                        false
`;
