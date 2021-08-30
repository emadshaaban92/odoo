/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Action
        [Action/name]
            Rtc/handleNotification
        [Action/params]
            sender
                [type]
                    Number
                    .{|}
                        String
                [description]
                    id of the session that sent the notification
            content
                [type]
                    String
                [description]
                    JSON
            record
                [type]
                    Rtc
        [Action/behavior]
            :json
                {JSON/parse}
                    @content
            :rtcSession
                {Record/findById}
                    [RtcSession/id]
                        @sender
            {if}
                @rtcSession
                .{isFalsy}
                .{|}
                    @rtcSession
                    .{RtcSession/channel}
                    .{!=}
                        @record
                        .{Rtc/channel}
            .{then}
                {Dev/comment}
                    does handle notifications targeting a different session
                {break}
            {if}
                @record
                .{Rtc/isClientRtcCompatible}
                .{isFalsy}
            .{then}
                {break}
            {if}
                @record
                .{Rtc/_peerConnections}
                .{Collection/get}
                    @sender
                .{isFalsy}
                .{&}
                    @json
                    .{Dict/get}
                        channelId
                    .{isFalsy}
                    .{|}
                        @record
                        .{Rtc/channel}
                        .{isFalsy}
                    .{|}
                        @json
                        .{Dict/get}
                            channelId
                        .{!=}
                            @record
                            .{Rtc/channel}
                            .{Thread/id}
            .{then}
                {break}
            {switch}
                @json
                .{Dict/get}
                    event
            .{case}
                [offer]
                    {Rtc/_addLogEntry}
                        [0]
                            @record
                        [1]
                            @sender
                        [2]
                            received notification: 
                            .{+}
                                @event
                        [3]
                            [step]
                                received offer
                    {Rtc/_handleRtcTransactionOffer}
                        [0]
                            @record
                        [1]
                            @rtcSession
                            .{RtcSession/peerToken}
                        [2]
                            @json
                            .{Dict/get}
                                payload
                [answer]
                    {Rtc/_addLogEntry}
                        [0]
                            @record
                        [1]
                            @sender
                        [2]
                            received notification: 
                            .{+}
                                @event
                        [3]
                            [step]
                                received answer
                    {Rtc/_handleRtcTransactionAnswer}
                        [0]
                            @record
                        [1]
                            @rtcSession
                            .{RtcSession/peerToken}
                        [2]
                            @json
                            .{Dict/get}
                                payload
                [ice-candidate]
                    {Rtc/_handleRtcTransactionICECandidate}
                        [0]
                            @record
                        [1]
                            @rtcSession
                            .{RtcSession/peerToken}
                        [2]
                            @json
                            .{Dict/get}
                                payload
                [disconnect]
                    {Rtc/_addLogEntry}
                        [0]
                            @record
                        [1]
                            @sender
                        [2]
                            received notification: 
                            .{+}
                                @event
                        [3]
                            [step]
                                peer cleanly disconnected
                    {Rtc_removePeer}
                        [0]
                            @record
                        [1]
                            @rtcSession
                            .{RtcSession/peerToken}
                [trackChange]
                    {Rtc/_handleTrackChange}
                        [0]
                            @record
                        [1]
                            @rtcSession
                        [2]
                            @json
                            .{Dict/get}
                                payload
`;
