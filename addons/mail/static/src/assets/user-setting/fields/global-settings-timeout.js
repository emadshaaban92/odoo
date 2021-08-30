/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Field
        [Field/name]
            globalSettingsTimeout
        [Field/model]
            UserSetting
        [Field/type]
            attr
        [Field/target]
            Integer
`;
