/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Action
        [Action/name]
            Attachment/convertData
        [Action/params]
            data
        [Action/behavior]
            :data2
                {Record/insert}
                    [Record/models]
                        Dict
            {if}
                @data
                .{Dict/hasKey}
                    filename
            .{then}
                {Record/update}
                    [0]
                        @data2
                    [1]
                        [Attachment/filename]
                            @data
                            .{Dict/get}
                                filename
            {if}
                @data
                .{Dict/hasKey}
                    id
            .{then}
                {Record/update}
                    [0]
                        @data2
                    [1]
                        [Attachment/id]
                            @data
                            .{Dict/get}
                                id
            {if}
                @data
                .{Dict/hasKey}
                    is_main
            .{then}
                {Record/update}
                    [0]
                        @data2
                    [1]
                        [Attachment/isMain]
                            @data
                            .{Dict/get}
                                is_main
            {if}
                @data
                .{Dict/hasKey}
                    mimetype
            .{then}
                {Record/update}
                    [0]
                        @data2
                    [1]
                        [Attachment/mimetype]
                            @data
                            .{Dict/get}
                                mimetype
            {if}
                @data
                .{Dict/hasKey}
                    name
            .{then}
                {Record/update}
                    [0]
                        @data2
                    [1]
                        [Attachment/name]
                            @data
                            .{Dict/get}
                                name
            {Dev/comment}
                relation
            {if}
                @data
                .{Dict/hasKey}
                    res_id
                .{&}
                    @data
                    .{Dict/hasKey}
                        res_model
            .{then}
                {Record/update}
                    [0]
                        @data2
                    [1]
                        [Attachment/originThread]
                            {Record/insert}
                                [Record/models]
                                    Thread
                                [Thread/id]
                                    @data
                                    .{Dict/get}
                                        res_id
                                [Thread/model]
                                    @data
                                    .{Dict/get}
                                        res_model
            {if}
                @data
                .{Dict/hasKey}
                    originThread
            .{then}
                {Record/update}
                    [0]
                        @data2
                    [1]
                        [Attachment/originThread]
                            @data
                            .{Dict/get}
                                originThread
            @data2
`;
