/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Dev/comment}
        Creates and setup a RTCPeerConnection.
    {Record/insert}
        [Record/models]
            Action
        [Action/name]
            Rtc/_createPeerConnection
        [Action/params]
            token
                [type]
                    String
            record
                [type]
                    Rtc
        [Action/returns]
            RTCPeerConnection
        [Action/behavior]
            :peerConnection
                {Record/insert}
                    [Record/models]
                        RTCPeerConnection
                    [iceServers]
                        @record
                        .{Rtc/iceServers}
            {Rtc/_addLogEntry}
                [0]
                    @record
                [1]
                    @token
                [2]
                    RTCPeerConnection create
                [3]
                    [step]
                        peer connection created
            {Record/update}
                [0]
                    @peerConnection
                [1]
                    [RTCPeerConnection/onicecandidate]
                        {Record/insert}
                            [Record/models]
                                Function
                            [Function/in]
                                event
                            [Function/out]
                                {if}
                                    @event
                                    .{Dict/get}
                                        candidate
                                    .{isFalsy}
                                .{then}
                                    {break}
                                {Rtc/_notifyPeers}
                                    [0]
                                        @record
                                    [1]
                                        token
                                    [2]
                                        [event]
                                            ice-candidate
                                        [payload]
                                            [candidate]
                                                @event
                                                .{Dict/get}
                                                    candidate
                    [RTCPeerConnection/oniceconnectionstatechange]
                        {Record/insert}
                            [Record/models]
                                Function
                            [Function/in]
                                event
                            [Function/out]
                                {Rtc/_onICEConnectionStateChange}
                                    [0]
                                        @record
                                    [1]
                                        @peerConnection
                                        .{RTCPeerConnection/iceConnectionState}
                                    [2]
                                        @token
                    [RTCPeerConnection/onconnectionstatechange]
                        {Record/insert}
                            [Record/models]
                                Function
                            [Function/in]
                                event
                            [Function/out]
                                {Rtc/_onConnectionStateChange}
                                    [0]
                                        @record
                                    [1]
                                        @peerConnection
                                        .{RtcPeerConnection/connectionState}
                                    [2]
                                        @token
                [RTCPeerConnection/onicecandidateerror]
                    {Record/insert}
                        [Record/models]
                            Function
                        [Function/in]
                            error
                        [Function/out]
                            {Rtc/_addLogEntry}
                                [0]
                                    @record
                                [1]
                                    @token
                                [2]
                                    ice candidate error
                            {Rtc/_recoverConnection}
                                [0]
                                    @record
                                [1]
                                    @token
                                [2]
                                    [delay]
                                        @record
                                        .{Rtc/recoveryTimeout}
                                    [reason]
                                        ice candidate error
                [RTCPeerConnection/onnegotiationneeded]
                    {Record/insert}
                        [Record/models]
                            Function
                        [Function/in]
                            event
                        [Function/out]
                            :offer
                                {RTCPeerConnection/createOffer}
                                    @peerConnection
                            {try}
                                {RTCPeerConnection/setLocalDescription}
                                    [0]
                                        @peerConnection
                                    [1]
                                        @offer
                            .{catch}
                                {Record/insert}
                                    [Record/models]
                                        Function
                                    [Function/in]
                                        error
                                    [Function/out]
                                        {Dev/comment}
                                            Possibly already have a remote offer here: cannot set local description
                                        {Rtc/_addLogEntry}
                                            [0]
                                                @record
                                            [1]
                                                @token
                                            [2]
                                                couldn't setLocalDescription
                                            [3]
                                                [error]
                                                    @error
                                        {break}
                            {Rtc/_addLogEntry}
                                [0]
                                    @record
                                [1]
                                    @token
                                [2]
                                    sending notification: offer
                                [3]
                                    [step]
                                        sending offer
                            {Rtc/_notifyPeers}
                                [0]
                                    @record
                                [1]
                                    @token
                                [2]
                                    [event]
                                        offer
                                    [payload]
                                        [sdp]
                                            @peerConnection
                                            .{RTCPeerConnection/localDescription}
                [RTCPeerConnection/ontrack]
                    {Record/insert}
                        [Record/models]
                            Function
                        [Function/in]
                            transceiver
                            track
                        [Function/out]
                            {Rtc/_addLogEntry}
                                [0]
                                    @record
                                [1]
                                    @token
                                [2]
                                    received 
                                    .{+}
                                        @track
                                        .{Track/kind}
                                    .{+}
                                         track
                            {Rtc/_updateExternalSessionTrack}
                                [0]
                                    @record
                                [1]
                                    @track
                                [2]
                                    @token
            :dataChannel
                {RTCPeerConnection/createDataChannel]
                    [0]
                        @peerConnection
                    [1]
                        notifications
                    [2]
                        [negotiated]
                            true
                        [id]
                            1
            {Record/update}
                [0]
                    @dataChannel
                [1]
                    [DataChannel/onmessage]
                        {Record/insert}
                            [Record/models]
                                Function
                            [Function/in]
                                event
                            [Function/out]
                                {Rtc/handleNotification}
                                    [0]
                                        @record
                                    [1]
                                        @token
                                    [2]
                                        @event
                                        .{Dict/get}
                                            data
                    [DataChannel/onopen]
                        {Record/insert}
                            [Record/models]
                                Function
                            [Function/out]
                                {Dev/comment}
                                    FIXME? it appears that the track yielded by the
                                    peerConnection's 'ontrack' event is always enabled,
                                    even when it is disabled on the sender-side.
                                {try}
                                    {Rtc/_notifyPeers}
                                        [0]
                                            @record
                                        [1]
                                            @token
                                        [2]
                                            [event]
                                                trackChange
                                            [type]
                                                peerToPeer
                                            [payload]
                                                [type]
                                                    audio
                                                [state]
                                                    [isTalking]
                                                        {Rtc/audioTrack}
                                                        .{&}
                                                            {Rtc/audioTrack}
                                                            .{AudioTrack/enabled}
                                                    [isSelfMuted]
                                                        @record
                                                        .{Rtc/currentRtcSession}
                                                        .{RtcSession/isSelfMuted}
                                .{catch}
                                    {Record/insert}
                                        [Record/models]
                                            Function
                                        [Function/in]
                                            e
                                        [Function/out]
                                            {if}
                                                @e
                                                .{instanceof}
                                                    DOMException
                                                .{isFalsy}
                                                .{|}
                                                    @e
                                                    .{Error/name}
                                                    .{!=}
                                                        OperationError
                                            .{then}
                                                {Error/raise}
                                                    @e
                                            {Rtc/_addLogEntry}
                                                [0]
                                                    @record
                                                [1]
                                                    @token
                                                [2]
                                                    failed to send on datachannel; dataChannelInfo: 
                                                    .{+}
                                                        {Rtc/_serializeRTCDataChannel}
                                                            [0]
                                                                @record
                                                            [1]
                                                                @dataChannel
                                                [3]
                                                    [error]
                                                        @error
            {Record/update}
                [0]
                    @record
                    .{Rtc/_peerConnections}
                [1]
                    {entry}
                        [key]
                            @token
                        [value]
                            @peerConnection
            {Record/update}
                [0]
                    @record
                    .{Rtc/_dataChannels}
                [1]
                    {entry}
                        [key]
                            @token
                        [value]
                            @dataChannel
            @peerConnection
`;
