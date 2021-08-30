/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Action
        [Action/name]
            Rtc/_toggleVideoBroadcast
        [Action/params]
            trackOptions
                [type]
                    Object
            record
                [type]
                    Rtc
        [Action/behavior]
            {if}
                @record
                .{Rtc/channel}
                .{isFalsy}
            .{then}
                {break}
            {Rtc/_toggleLocalVideoTrack}
                [0]
                    @record
                [1]
                    @trackOptions
            {foreach}
                @record
                .{Rtc/_peerConnections}
            .{as}
                item
            .{do}
                :token
                    @item
                    .{Collection/first}
                :peerConnection
                    @item
                    .{Collection/second}
                {Rtc/_updateRemoteTrack}
                    [0]
                        @record
                    [1]
                        @peerConnection
                    [2]
                        video
                    [3]
                        [token]
                            @token
            {if}
                @record
                .{Rtc/currentRtcSession}
                .{isFalsy}
            .{then}
                {break}
            {RtcSession/updateAndBroadcast}
                [0]
                    @record
                    .{Rtc/currentRtcSession}
                [1]
                    [isScreenSharingOn]
                        @record
                        .{Rtc/sendDisplay}
                        .{isTruthy}
                    [isCameraOn]
                        @record
                        .{Rtc/sendUserVideo}
                        .{isTruthy}
`;
