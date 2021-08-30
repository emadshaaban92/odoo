/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Element
        [Element/name]
            buttonLogNote
        [Element/model]
            ChatterTopbarComponent
        [web.Element/tag]
            button
        [web.Element/type]
            button
        [Record/models]
            ChatterTopbarComponent/button
            Hoverable
        [web.Element/class]
            btn
            btn-link
        [Element/isPresent]
            @record
            .{ChatterTopbarComponent/chatter}
            .{Chatter/threadView}
        [web.Element/isDisabled]
            @record
            .{ChatterTopbarComponent/chatter}
            .{Chatter/isDisabled}
        [Element/onClick]
            {Chatter/onClickLogNote}
                [0]
                    @record
                    .{ChatterTopbarComponent/chatter}
                [1]
                    @ev
        [web.Element/textContent]
            {Locale/text}
                Log note
        [web.Element/style]
            {if}
                @record
                .{ChatterTopbarComponent/isButtonLogActive}
            .{then}
                [web.scss/color]
                    {scss/$o-brand-odoo}
                [web.scss/background-color]
                    {scss/lighten}
                        {scss/gray}
                            300
                        7%
                [web.scss/border-right-color]
                    {scss/$border-color}
                {web.scss/selector}
                    [0]
                        &:not(:first-of-type)
                    [1]
                        [web.scss/border-left-color]
                            {scss/$border-color}
                {if}
                    @record
                    .{ChatterTopbarComponent/chatter}
                    .{Chatter/hasExternalBorder}
                .{then}
                    {web.scss/selector}
                        [0]
                            &:first-of-type
                        [1]
                            [web.scss/border-left-color]
                                {scss/$border-color}
                    [web.scss/border-top-color]
                        {scss/$border-color}
                {if}
                    @field
                    .{web.Element/isHover}
                .{then}
                    [web.scss/background-color]
                        {scss/gray}
                            300
                    [web.scss/color]
                        {scss/$link-hover-color}
`;
