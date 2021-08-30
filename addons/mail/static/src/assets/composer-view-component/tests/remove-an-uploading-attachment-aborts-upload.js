/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Test
        [Test/name]
            remove an uploading attachment aborts upload
        [Test/model]
            ComposerViewComponent
        [Test/assertions]
            1
        [Test/scenario]
            :testEnv
                {Record/insert}
                    [Record/models]
                        Env
            @testEnv
            .{Record/insert}
                [Record/models]
                    mail.channel
                [mail.channel/id]
                    20
            :server
                {Record/insert}
                    [Record/models]
                        Server
                    [Server/data]
                        @record
                        .{Test/data}
                    [Server/mockFetch]
                        {Record/insert}
                            [Record/models]
                                Function
                            [Function/in]
                                resource
                                init
                                original
                            [Function/out]
                                {if}
                                    @resource
                                    .{=}
                                        /mail/attachment/upload
                                .{then}
                                    {Dev/comment}
                                        simulates uploading indefinitely
                                    {Promise/await}
                                @original
            :thread
                @testEnv
                .{Record/findById}
                    [Thread/id]
                        20
                    [Thread/model]
                        mail.channel
            :composerComponent
                @testEnv
                .{Record/insert}
                    [Record/models]
                        ComposerViewComponent
                    [ComposerViewComponent/composer]
                        @thread
                        .{Thread/composer}
            :file
                @testEnv
                .{Record/insert}
                    [Record/models]
                        web.File
                    [web.File/content]
                        hello, world
                    [web.File/contentType]
                        text/plain
                    [web.File/name]
                        text.txt
            @testEnv
            .{Component/afterNextRender}
                @testEnv
                .{UI/inputFiles}
                    [0]
                        @composerComponent
                        .{ComposerComponent/composerView}
                        .{ComposerView/fileUploader}
                        .{FileUploader/fileInput}
                    [1]
                        @file
            {Test/assert}
                []
                    @thread
                    .{Thread/composer}
                    .{Composer/attachments}
                    .{Collection/length}
                    .{=}
                        1
                []
                    should contain an attachment
            @testEnv
            .{UI/afterEvent}
                [eventName]
                    o-attachment-upload-abort
                [func]
                    @testEnv
                    .{UI/click}
                        @thread
                        .{Thread/composer}
                        .{Composer/attachments}
                        .{Collection/first}
                        .{Attachment/attachmentCards}
                        .{Collection/first}
                        .{AttachmentCard/attachmentCardComponents}
                        .{Collection/first}
                        .{AttachmentCardComponent/asideItemUnlink}
                [message]
                    attachment upload request should have been aborted
                [predicate]
                    {Record/insert}
                        [Record/models]
                            Function
                        [Function/in]
                            attachment
                        [Function/out]
                            @attachment
                            .{=}
                                @thread
                                .{Thread/composer}
                                .{Composer/attachments}
                                .{Collection/first}
`;
