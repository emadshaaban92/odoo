/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Element
        [Element/name]
            root
        [Element/model]
            ComposerViewComponent
        [Element/onKeydown]
            {if}
                @ev
                .{web.KeyboardEvent/key}
                .{!=}
                    Escape
            .{then}
                {break}
            {if}
                {Event/isHandled}
                    @ev
                    ComposerTextInputComponent.closeSuggestions
            .{then}
                {break}
            {if}
                {Event/isHandled}
                    @ev
                    ComposerViewComponent.closeEmojisPopover
            .{then}
                {break}
            {web.Event/preventDefault}
                @ev
            {ComposerView/discard}
                @record
                .{ComposerViewComponent/composerView}
        [web.Element/style]
            [web.scss/display]
                grid
            [web.scss/grid-template-areas]
                [0]
                    sidebar-header
                    core-header
                [1]
                    sidebar-main
                    core-main
                [2]
                    sidebar-footer
                    core-footer
            [web.scss/grid-template-columns]
                auto
                1fr
            [web.scss/grid-template-rows]
                auto
                1fr
                auto
            {if}
                @record
                .{ComposerViewComponent/hasCurrentPartnerAvatar}
            .{then}
                [web.scss/grid-template-columns]
                    50px
                    1fr
                [web.scss/padding]
                    [0]
                        {scss/map-get}
                            {scss/$spacers}
                            3
                    [1]
                        {scss/map-get}
                            {scss/$spacers}
                            3
                    [2]
                        {scss/map-get}
                            {scss/$spacers}
                            4
                    [3]
                        {web.scss/map-get}
                            {scss/$spacers}
                            1
                {if}
                    @record
                    .{ComposerViewComponent/hasFooter}
                    .{isFalsy}
                .{then}
                    [web.scss/padding-bottom]
                        {scss/map-get}
                            {scss/$spacers}
                            4
                {if}
                    @record
                    .{ComposerViewComponent/hasHeader}
                    .{isFalsy}
                .{then}
                    [web.scss/padding-top]
                        {scss/map-get}
                            {scss/$spacers}
                            4
                    {if}
                        @record
                        .{ComposerViewComponent/composerView}
                        .{ComposerView/threadView}
                    .{then}
                        [web.scss/padding-top]
                            {scss/map-get}
                                {scss/$spacers}
                                1
                        [web.scss/padding-bottom]
                            {scss/map-get}
                                {scss/$spacers}
                                1
            {if}
                @record
                .{ComposerViewComponent/composerView}
                .{ComposerView/messageViewInEditing}
                .{isFalsy}
            .{then}
                [web.scss/background-color]
                    {scss/gray}
                        100
            {if}
                @record
                .{ComposerViewComponent/composerView}
                .{ComposerView/threadView}
            .{then}
                [web.scss/background-color]
                    {scss/$white}
`;
