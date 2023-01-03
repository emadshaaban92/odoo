/** @odoo-module **/

import { GraphModel } from "@web/views/graph/graph_model";
import { useService } from "@web/core/utils/hooks";

const { onWillStart } = owl;


export class BurndownChartModel extends GraphModel {

    /**
     * @protected
     * @override
     */
    _getData(dataPoints) {
        const { comparisonField, groupBy, mode } = this.metaData;

        let identify = false;
        if (comparisonField && groupBy.length && groupBy[0].fieldName === comparisonField) {
            identify = true;
        }
        const dateClasses = identify ? this._getDateClasses(dataPoints) : null;

        // dataPoints --> labels
        let labels = [];
        const labelMap = {};
        for (const dataPt of dataPoints) {
            const x = dataPt.labels.slice(0, mode === "pie" ? undefined : 1);
            const trueLabel = x.length ? x.join(SEP) : this.env._t("Total");
            if (dateClasses) {
                x[0] = dateClasses.classLabel(dataPt.originIndex, x[0]);
            }
            const key = JSON.stringify(x);
            if (labelMap[key] === undefined) {
                labelMap[key] = labels.length;
                if (dateClasses) {
                    if (mode === "pie") {
                        x[0] = dateClasses.classMembers(x[0]).join(", ");
                    } else {
                        x[0] = dateClasses.representative(x[0]);
                    }
                }
                const label = x.length ? x.join(SEP) : this.env._t("Total");
                labels.push(label);
            }
            dataPt.labelIndex = labelMap[key];
            dataPt.trueLabel = trueLabel;
        }

        // dataPoints + labels --> datasetsTmp --> datasets
        const datasetsTmp = {};
        const indexation = this.metaData.context.stage_seq;
        for (const dataPt of dataPoints) {
            const { domain, labelIndex, originIndex, trueLabel, value } = dataPt;
            const datasetLabel = this._getDatasetLabel(dataPt);
            if (!(datasetLabel in datasetsTmp)) {
                let dataLength = labels.length;
                if (mode !== "pie" && dateClasses) {
                    dataLength = dateClasses.arrayLength(originIndex);
                }
                datasetsTmp[datasetLabel] = {
                    data: new Array(dataLength).fill(0),
                    trueLabels: labels.slice(0, dataLength), // should be good // check this in case identify = true
                    domains: new Array(dataLength).fill([]),
                    label: datasetLabel,
                    originIndex: originIndex,
                };
            }
            datasetsTmp[datasetLabel].data[labelIndex] = value;
            datasetsTmp[datasetLabel].domains[labelIndex] = domain;
            datasetsTmp[datasetLabel].trueLabels[labelIndex] = trueLabel;
            datasetsTmp[datasetLabel].originIndex = indexation[datasetLabel];
        }
        // sort by origin
        let datasets = sortBy(Object.values(datasetsTmp), "originIndex");

        if (mode === "pie") {
            // We kinda have a matrix. We remove the zero columns and rows. This is a global operation.
            // That's why it cannot be done before.
            datasets = datasets.filter((dataset) => dataset.data.some((v) => Boolean(v)));
            const labelsToKeepIndexes = {};
            labels.forEach((_, index) => {
                if (datasets.some((dataset) => Boolean(dataset.data[index]))) {
                    labelsToKeepIndexes[index] = true;
                }
            });
            labels = labels.filter((_, index) => labelsToKeepIndexes[index]);
            for (const dataset of datasets) {
                dataset.data = dataset.data.filter((_, index) => labelsToKeepIndexes[index]);
                dataset.domains = dataset.domains.filter((_, index) => labelsToKeepIndexes[index]);
                dataset.trueLabels = dataset.trueLabels.filter(
                    (_, index) => labelsToKeepIndexes[index]
                );
            }
        }

        return { datasets, labels };
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
