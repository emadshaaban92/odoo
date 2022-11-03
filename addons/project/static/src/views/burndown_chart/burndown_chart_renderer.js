/** @odoo-module **/

import { GraphRenderer, shortenLabel } from "@web/views/graph/graph_renderer";
import { useService } from "@web/core/utils/hooks";

const { onWillStart } = owl;


export class BurndownChartRenderer extends GraphRenderer {
    setup() {
        super.setup();
        this.orm = useService("orm");

        onWillStart(async () => this.stageSequence = await this.fetchSequence());
    }

    async fetchSequence() {
        const activeId = this.model.metaData.context.active_id;
        return await this.orm
            .webSearchRead(
                'project.task.type',
                [['project_ids', 'in', activeId]],
                ["name","sequence"]
            ).then((data) => {return data.records})
    }

    /**
     * @returns {Object}
     * @override
    **/
    getLegendOptions() {
        const legends = super.getLegendOptions();
        const { mode } = this.model.metaData;
        const referenceColor = mode === "bar" ? "backgroundColor" : "borderColor";
        legends.labels = {
            generateLabels: (chart) => {
                const { data } = chart;
                let labels = data.datasets.map((dataset, index) => {
                    let currentStage;
                    let currentIndex;
                    currentStage = this.stageSequence.find(item => item.name == dataset.label)
                    if (currentStage == null){
                        currentIndex = 1000
                    } else {
                        currentIndex = currentStage.sequence
                    }
                    return {
                        text: shortenLabel(dataset.label),
                        fullText: dataset.label,
                        fillStyle: dataset[referenceColor],
                        hidden: !chart.isDatasetVisible(index),
                        lineCap: dataset.borderCapStyle,
                        lineDash: dataset.borderDash,
                        lineDashOffset: dataset.borderDashOffset,
                        lineJoin: dataset.borderJoinStyle,
                        lineWidth: dataset.borderWidth,
                        strokeStyle: dataset[referenceColor],
                        pointStyle: dataset.pointStyle,
                        datasetIndex: currentIndex,
                    };
                });
                labels = labels.sort((a,b) => a.datasetIndex - b.datasetIndex)
                return labels;
            },
        };
        return legends;
    }
}