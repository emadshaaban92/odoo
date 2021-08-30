/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Lifecycle
        [Lifecycle/name]
            onUpdate
        [Lifecycle/model]
            WelcomeViewComponent
        [Lifecycle/behavior]
            {WelcomeView/onComponentUpdate}
                @record
                .{WelcomeViewComponent/welcomeView}
`;
