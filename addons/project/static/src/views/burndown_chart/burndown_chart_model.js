/** @odoo-module **/

import { GraphModel } from "@web/views/graph/graph_model";
import { useService } from "@web/core/utils/hooks";

const { onWillStart } = owl;


export class BurndownChartModel extends GraphModel {
    setup(params) {
        super.setup(params);

        onWillStart(async () => this.stageSequence = await this.fetchSequence());
    }

    /**
     * 
     * @returns {Object}
     */
    async fetchSequence() {
        const data = await this.orm.webSearchRead(
            "project.task.type",
            [["project_ids", "in", this.metaData.context.active_id]],
            ["name", "sequence"]
        );
        return data.records;
    }

    /**
     * @protected
     * @override
     */
    async _loadDataPoints(metaData) {
        metaData.measures.__count.string = this.env._t('# of Tasks');
        return super._loadDataPoints(metaData);
    }
}
