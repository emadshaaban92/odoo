/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Element
        [Element/name]
            root
        [Element/model]
            MessageViewComponent
        [Record/models]
            Hoverable
        [Element/onClick]
            {if}
                @ev
                .{web.MouseEvent/target}
                .{web.Element/closest}
                    .o_channel_redirect
            .{then}
                {Env/openProfile}
                    [id]
                        @ev
                        .{web.MouseEvent/target}
                        .{web.Element/dataset}
                        .{web.Dataset/oeId}
                    [model]
                        mail.channel
                {Dev/comment}
                    avoid following dummy href
                {web.Event/preventDefault}
                    @ev
            .{elif}
                @ev
                .{web.MouseEvent/target}
                .{web.Element/tag}
                .{=}
                    A
            .{then}
                {if}
                    @ev
                    .{web.MouseEvent/target}
                    .{web.Element/dataset}
                    .{web.Dataset/oeId}
                    .{&}
                        @ev
                        .{web.MouseEvent/target}
                        .{web.Element/dataset}
                        .{web.Dataset/oeModel}
                .{then}
                    {Env/openProfile}
                        [id]
                            @ev
                            .{web.MouseEvent/target}
                            .{web.Element/dataset}
                            .{web.Dataset/oeId}
                        [model]
                            @ev
                            .{web.MouseEvent/target}
                            .{web.Element/dataset}
                            .{web.Dataset/oeModel}
                    {Dev/comment}
                        avoid following dummy href
                    {web.Event/preventDefault}
                        @ev
            .{elif}
                {Event/isHandled}
                    @ev
                    MessageViewComponent/onClickAuthorAvatar
                .{isFalsy}
                .{&}
                    {Event/isHandled}
                        @ev
                        MessageViewComponent/onClickAuthorName
                    .{isFalsy}
                .{&}
                    {Event/isHandled}
                        @ev
                        MessageViewComponent/onClickFailure
                    .{isFalsy}
                .{&}
                    {Event/isHandled}
                        [0]
                            @ev
                        [1]
                            MessageActionList/onClick
                    .{isFalsy}
                .{&}
                    {Event/isHandled}
                        [0]
                            @ev
                        [1]
                            MessageReactionGroup/onClick
                    .{isFalsy}
                .{&}
                    {Event/isHandled}
                        [0]
                            @ev
                        [1]
                            MessageInReplyToView/onClickMessageInReplyTo
                    .{isFalsy}
            .{then}
                {Record/update}
                    [0]
                        @record
                    [1]
                        [MessageViewComponent/isClicked]
                            @record
                            .{MessageViewComponent/isClicked}
                            .{isFalsy}
        [Element/onMouseenter]
            {Record/update}
                [0]
                    @record
                [1]
                    [MessageViewComponent/isHovered]
                        true
        [Element/onMouseleave]
            {Record/update}
                [0]
                    @record
                [1]
                    [MessageViewComponent/isHovered]
                        false
        [web.Element/data-message-local-id]
            @record
            .{MessageViewComponent/messageView}
            .{MessageView/message}
            .{Record/id}
        [web.Element/class]
            position-relative
            pt-1
            {if}
                @record
                .{MessageViewComponent/messageView}
                .{MessageView/isSquashed}
                .{isFalsy}
                .{&}
                    @record
                    .{MessageViewComponent/messageView}
                    .{MessageView/threadView}
            .{then}
                mt-3
        [web.Element/style]
            [web.scss/background-color]
                {scss/$white}
            [web.scss/transition]
                background-color
                .5s
                ease-out
            {if}
                @record
                .{MessageViewComponent/isActive}
            .{then}
                [web.scss/background-color]
                    {scss/gray}
                        100
            {if}
                @record
                .{MessageViewComponent/isClicked}
            .{then}
                {web.scss/selector}
                    [0]
                        .o-MessageViewComponent-commands
                    [1]
                        [web.scss/opacity]
                            1
                {if}
                    @record
                    .{MessageViewComponent/messageView}
                    .{MessageView/isSquashed}
                .{then}
                    {web.scss/selector}
                        [0]
                            .o-MessageViewComponent-sidebarItem
                        [1]
                            [web.scss/display]
                                flex
                    {web.scss/selector}
                        [0]
                            .o-MessageViewComponent-seenIndicator
                        [1]
                            [web.scss/display]
                                none
            {if}
                @field
                .{web.Element/isHover}
            .{then}
                {web.scss/selector}
                    [0]
                        .o-MessageViewComponent-commands
                    [1]
                        [web.scss/opacity]
                            1
                {if}
                    @record
                    .{MessageViewComponent/messageView}
                    .{MessageView/isSquashed}
                .{then}
                    {web.scss/selector}
                        [0]
                            .o-MessageViewComponent-sidebarItem
                        [1]
                            [web.scss/display]
                                flex
                    {web.scss/selector}
                        [0]
                            .o-MessageViewComponent-seenIndicator
                        [1]
                            [web.scss/display]
                                none
            {if}
                @record
                .{MessageViewComponent/messageView}
                .{MessageView/message}
                .{Message/isDiscussion}
                .{|}
                    @record
                    .{MessageViewComponent/messageView}
                    .{MessageView/message}
                    .{Message/isNotification}
            .{then}
                [web.scss/background-color]
                    {scss/gray}
                        100
                {if}
                    @record
                    .{MessageViewComponent/isActive}
                .{then}
                    [web.scss/background-color]
                        [0]
                            {web.scss/mix}
                                {scss/gray}
                                    100
                        [1]
                            {scss/gray}
                                200
                {web.scss/selector}
                    [0]
                        .o-MessageViewComponent-partnerImStatusIcon
                    [1]
                        [web.scss/color]
                            {scss/gray}
                                100
                                {Dev/comment}
                                    same color as background of parent
                {if}
                    @record
                    .{MessageViewComponent/isSelected}
                .{then}
                    [web.scss/border-bottom]
                        1px
                        solid
                        {scss/darken}
                            {scss/gray}
                                400
                            5%
            {if}
                @record
                .{MessageViewComponent/isSelected}
            .{then}
                [web.scss/background-color]
                    {scss/gray}
                        400
                {web.scss/selector}
                    [0]
                        .o-MessageViewComponent-partnerImStatusIcon
                    [1]
                        [web.scss/color]
                            {scss/gray}
                                400
            {if}
                @record
                .{MessageViewComponent/messageView}
                .{MessageView/message}
                .{Message/isStarred}
            .{then}
                {web.scss/selector}
                    [0]
                        .o-MessageViewComponent-commands
                    [1]
                        [web.scss/display]
                            flex
                {web.scss/selector}
                    [0]
                        .o-MessageViewComponent-commandStar
                    [1]
                        [web.scss/display]
                            flex
            {if}
                @record
                .{MessageViewComponent/threadView}
                .{&}
                    @record
                    .{MessageViewComponent/threadView}
                    .{ThreadView/replyingToMessageView}
            .{then}
                [web.scss/opacity]
                    0.5
                {if}
                    @record
                    .{MessageViewComponent/messageView}
                    .{MessageView/messageView}
                    .{MessageView/isHighlighted}
                .{then}
                    [web.scss/background-color]
                        {web.scss/rgba}
                            {scss/$o-brand-primary}
                            .1
`;
