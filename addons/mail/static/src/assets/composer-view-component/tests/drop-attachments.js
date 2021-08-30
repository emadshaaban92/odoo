/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Test
        [Test/name]
            drop attachments
        [Test/model]
            ComposerViewComponent
        [Test/assertions]
            4
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
            @testEnv
            .{Record/insert}
                [Record/models]
                    Server
                [Server/data]
                    @record
                    .{Test/data}
            :thread
                @testEnv
                .{Record/findById}
                    [Thread/id]
                        20
                    [Thread/model]
                        mail.channel
            @testEnv
            .{Record/insert}
                [Record/models]
                    ComposerViewComponent
                [ComposerViewComponent/composer]
                    @thread
                    .{Thread/composer}
            :files
                {Record/insert}
                    [Record/models]
                        Collection
                    [0]
                        {Record/insert}
                            [Record/models]
                                web.File
                            [web.File/content]
                                hello, world
                            [web.File/contentType]
                                text/plain
                            [web.File/name]
                                text.txt
                    [1]
                        {Record/insert}
                            [Record/models]
                                web.File
                            [web.File/content]
                                hello, worlduh
                            [web.File/contentType]
                                text/plain
                            [web.File/name]
                                text2.txt
            @testEnv
            .{Component/afterNextRender}
                @testEnv
                .{Utils/dragenterFiles}
                    @thread
                    .{Thread/composer}
                    .{Composer/composerViewComponents}
                    .{Collection/first}
            {Test/assert}
                []
                    @thread
                    .{Thread/composer}
                    .{Composer/composerViewComponents}
                    .{Collection/first}
                    .{ComposerViewComponent/dropZone}
                []
                    should have a drop zone
            {Test/assert}
                []
                    @thread
                    .{Thread/composer}
                    .{Composer/attachments}
                    .{Collection/length}
                    .{=}
                        0
                []
                    should have no attachment before files are dropped

            @testEnv
            .{Component/afterNextRender}
                @testEnv
                .{Utils/dropFiles}
                    [0]
                        @thread
                        .{Thread/composer}
                        .{Composer/composerViewComponents}
                        .{Collection/first}
                        .{ComposerViewComponent/dropZone}
                    [1]
                        @files
            {Test/assert}
                []
                    @thread
                    .{Thread/composer}
                    .{Composer/attachments}
                    .{Collection/length}
                    .{=}
                        2
                []
                    should have 2 attachments in the composer after files dropped

            @testEnv
            .{Component/afterNextRender}
                @testEnv
                .{Utils/dragenterFiles}
                    @thread
                    .{Thread/composer}
                    .{Composer/composerViewComponents}
                    .{Collection/first}
            @testEnv
            .{Component/afterNextRender}
                @testEnv
                .{Utils/dropFiles}
                    [0]
                        @thread
                        .{Thread/composer}
                        .{Composer/composerViewComponents}
                        .{Collection/first}
                        .{ComposerViewComponent/dropZone}
                    [1]
                        {Record/insert}
                            [Record/models]
                                web.File
                            [web.File/content]
                                hello, world
                            [web.File/contentType]
                                text/plain
                            [web.File/name]
                                text3.txt
            {Test/assert}
                []
                    @thread
                    .{Thread/composer}
                    .{Composer/attachments}
                    .{Collection/length}
                    .{=}
                        3
                []
                    should have 3 attachments in the box after files dropped
`;
