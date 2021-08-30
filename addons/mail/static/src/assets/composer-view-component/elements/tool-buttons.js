/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Element
        [Element/name]
            toolButtons
        [Element/model]
            ComposerViewComponent
        [web.Element/style]
            [web.scss/display]
                flex
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
                .{ComposerViewComponent/isCompact}
                .{isFalsy}
            .{then}
                [web.scss/flex-direction]
                    row
                [web.scss/justify-content]
                    space-between
                [web.scss/flex]
                    100%
                [web.scss/border-bottom]
                    0
                [web.scss/border-radius]
                    initial
            [web.scss/background-color]
                {scss/$white}
            [web.scss/border-top]
                {scss/$border-width}
                solid
                {scss/$border-color}
            [web.scss/border-bottom]
                {scss/$border-width}
                solid
                {scss/$border-color}
            {if}
                @record
                .{ComposerViewComponent/hasCurrentPartnerAvatar}
                .{isFalsy}
            .{then}
                {web.scss/selector}
                    [0]
                        &:last-child
                    [1]
                        [web.scss/border-right]
                            {scss/$border-width}
                            solid
                            {scss/lighten}
                                {scss/gray}
                                    400
                                5%
`;
