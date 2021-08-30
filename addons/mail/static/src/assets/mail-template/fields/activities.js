/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Field
        [Field/name]
            activities
        [Field/model]
            MailTemplate
        [Field/type]
            many
        [Field/target]
            Activity
        [Field/inverse]
            Activity/mailTemplates
`;
