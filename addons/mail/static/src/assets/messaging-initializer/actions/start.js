/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Dev/comment}
        Fetch messaging data initially to populate the store specifically for
        the current user. This includes pinned channels for instance.
    {Record/insert}
        [Record/models]
            Action
        [Action/name]
            MessagingInitializer/start
        [Action/params]
            record
                [type]
                    MessagingInitializer
        [Action/behavior]
            {Record/update}
                [0]
                    @env
                [1]
                    [Env/history]
                        {Record/insert}
                            [Record/models]
                                Thread
                            [Thread/id]
                                history
                            [Thread/isServerPinned]
                                true
                            [Thread/model]
                                mail.box
                            [Thread/name]
                                {Locale/text}
                                    History
                    [Env/inbox]
                        {Record/insert}
                            [Record/models]
                                Thread
                            [Thread/id]
                                inbox
                            [Thread/isServerPinned]
                                true
                            [Thread/model]
                                mail.box
                            [Thread/name]
                                {Locale/text}
                                    Inbox
                    [Env/starred]
                        {Record/insert}
                            [Record/models]
                                Thread
                            [Thread/id]
                                starred
                            [Thread/isServerPinned]
                                true
                            [Thread/model]
                                mail.box
                            [Thread/name]
                                {Locale/text}
                                    Starred
            {Device/start}
            {ChatWindowManager/start}
            :data
                {Record/doAsync}
                    [0]
                        @record
                    [1]
                        @env
                        .{Env/owlEnv}
                        .{Dict/get}
                            services
                        .{Dict/get}
                            rpc
                        .{Function/call}
                            [0]
                                [route]
                                    /mail/init_messaging
                                [params]
                                    [context]
                                        @context
                            [1]
                                [shadow]
                                    true
            {Record/doAsync}
                [0]
                    @record
                [1]
                    {MessagingInitializer/_init}
                        [0]
                            @record
                        [1]
                            @data
            {if}
                {Discuss/discussView}
            .{then}
                {Discuss/openInitThread}
            {if}
                {Env/autofetchPartnerImStatus}
            .{then}
                {Partner/startLoopFetchImStatus}
            {if}
                {Env/currentUser}
            .{then}
                {MessagingInitializer/_loadMessageFailures}
                    @record
`;
