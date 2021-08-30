/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Action
        [Action/name]
            UserSetting/_onSaveGlobalSettingsTimeout
        [Action/params]
            record
                [type]
                    UserSetting
        [Action/behavior]
            {if}
                {Record/exists}
                    @record
                .{isFalsy}
            .{then}
                {break}
            {Record/update}
                [0]
                    @record
                [1]
                    [UserSetting/globalSettingsTimeout]
                        {Record/empty}
            {Env/owlEnv}
            .{Dict/get}
                services
            .{Dict/get}
                rpc
            .{Function/call}
                [0]
                    [model]
                        res.users.settings
                    [method]
                        set_res_users_settings
                    [args]
                        [0]
                            {Env/currentUser}
                            .{User/resUsersSettingsId}
                        [1]
                            [push_to_talk_key]
                                @record
                                .{UserSetting/pushToTalkKey}
                            [use_push_to_talk]
                                @record
                                .{UserSetting/usePushToTal}
                            [voice_active_duration]
                                @record
                                .{UserSetting/voiceActiveDuration}
                [1]
                    [shadow]
                        true
`;
