/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Action
        [Action/name]
            RtcCallViewerComponent/_setTileLayout
        [Action/behavior]
            :rect
                {web.Element/getBoundingClientRect}
                    @record
                    .{RtcCallViewerComponent/grid}
            :width
                @rect
                .{Dict/get}
                    width
            :height
                @rect
                .{Dict/get}
                    height
            :tessellation
                {RtcCallViewerComponent/_computeTessellation}
                    [aspectRatio]
                        @record
                        .{RtcCallViewerComponent/rtcCallViewer}
                        .{RtcCallViewer/aspectRatio}
                    [containerHeight]
                        @height
                    [containerWidth]
                        @width
                    [tileCount]
                        @record
                        .{RtcCallViewerComponent/grid}
                        .{web.Element/children}
                        .{Collection/length}
            :tileWidth
                @tessellation
                .{Dict/get}
                    tileWidth
            :tileHeight
                @tessellation
                .{Dict/get}
                    tileHeight
            :columnCount
                @tessellation
                .{Dict/get}
                    columnCount
            {Record/update}
                [0]
                    @record
                [1]
                    [tileWidth]
                        @tileWidth
                    [tileHeight]
                        tileHeight
                    [columnCount]
                        columnCount
`;
