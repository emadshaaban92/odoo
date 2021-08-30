/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Action
        [Action/name]
            ThreadView/_shouldMessageBeSquashed
        [Action/params]
            record
                [type]
                    ThreadView
            prevMessage
                [type]
                    Message
            message
                [type]
                    Message
        [Action/returns]
            Boolean
        [Action/behavior]
            {if}
                @record
                .{ThreadView/hasSquashCloseMessages}
                .{isFalsy}
            .{then}
                false
            .{elif}
                @message
                .{Message/parentMessage}
            .{then}
                false
            .{elif}
                @prevMessage
                .{isFalsy}
            .{then}
                false
            .{elif}
                @prevMessage
                .{Message/date}
                .{isFalsy}
                .{&}
                    @message
                    .{Message/date}
            .{then}
                false
            .{elif}
                @message
                .{Message/date}
                .{&}
                    @prevMessage
                    .{Message/date}
                .{&}
                    {Math/abs}
                        @message
                        .{Message/date}
                        .{Moment/diff}
                            @prevMessage
                            .{Message/date}
                    .{>}
                        60000
            .{then}
                {Dev/comment}
                    more than 1 min. elapsed
                false
            .{elif}
                @prevMessage
                .{Message/dateDay}
                .{!=}
                    @message
                    .{Message/dateDay}
            .{then}
                false
            .{elif}
                @prevMessage
                .{Message/type}
                .{!=}
                    comment
                .{|}
                    @message
                    .{Message/type}
                    .{!=}
                        comment
            .{then}
                false
            .{elif}
                @prevMessage
                .{Message/author}
                .{!=}
                    @message
                    .{Message/author}
                .{|}
                    @prevMessage
                    .{Message/guestAuthor}
                    .{!=}
                        @message
                        .{Message/guestAuthor}
            .{then}
                {Dev/comment}
                    from a different author
                false
            .{elif}
                @prevMessage
                .{Message/originThread}
                .{!=}
                    @message
                    .{Message/originThread}
            .{then}
                false
            .{elif}
                @prevMessage
                .{Message/notifications}
                .{Collection/length}
                .{>}
                    0
                .{|}
                    @message
                    .{Message/notifications}
                    .{Collection/length}
                    .{>}
                        0
            .{then}
                {Dev/comment}
                    visual about notifications is restricted to non-squashed messages
                false
            .{else}
                :prevOriginThread
                    @prevMessage
                    .{Message/originThread}
                :originThread
                    @message
                    .{Message/originThread}
                {if}
                    @prevOriginThread
                    .{&}
                        @originThread
                    .{&}
                        @prevOriginThread
                        .{Thread/model}
                        .{=}
                            @originThread
                            .{Thread/model}
                    .{&}
                        @originThread
                        .{Thread/model}
                        .{!=}
                            mail.channel
                    .{&}
                        @prevOriginThread
                        .{Thread/id}
                        .{!=}
                            @riginThread
                            .{Thread/id}
                .{then}
                    {Dev/comment}
                        messages linked to different document thread
                    false
                .{else}
                    true
`;
