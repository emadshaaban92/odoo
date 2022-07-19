/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { ListController } from "@web/views/list/list_controller";
import { kanbanView } from "@web/views/kanban/kanban_view";
import { KanbanRenderer } from "@web/views/kanban/kanban_renderer";
import { KanbanController } from "@web/views/kanban/kanban_controller";
import { KanbanRecord } from "@web/views/kanban/kanban_record";
import { FileUploader } from "@web/views/fields/file_handler";

const { Component, useState } = owl;

class AccountFileUploader extends Component {
    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.attachmentIdsToProcess = [];
    }

    async onFileUploaded(file) {
        let att_data = {
            name: file.name,
            mimetype: file.type,
            datas: file.data,
        }
        const att_id = await this.orm.create("ir.attachment", att_data, {
            ...this.props.extraContext, ...this.env.searchModel.context,
        });
        this.attachmentIdsToProcess.push(att_id);
    }

    async onUploadComplete() {
        const action = await this.orm.call("account.journal", "create_document_from_attachment", ["", this.attachmentIdsToProcess], {
            context: {...this.props.extraContext, ...this.env.searchModel.context},
        });
        this.attachmentIdsToProcess = [];
        this.action.doAction(action);
    }
}
AccountFileUploader.components = {
    FileUploader,
}
AccountFileUploader.template = "account.AccountFileUploader";

class AccountDropZone extends Component {
    setup(){
        this.notificationService = useService("notification");
    }

    onDrop(ev) {
        const selector = '.account_file_uploader.o_input_file.o_hidden';
        // look for the closest uploader Input as it may have a context
        let uploadInput = ev.target.closest('.o_drop_area').parentElement.querySelector(selector) || document.querySelector(selector);
        let files = ev.dataTransfer ? ev.dataTransfer.files : false;
        if (uploadInput && !!files) {
            uploadInput.files = ev.dataTransfer.files;
            uploadInput.dispatchEvent(new Event("change"));
        } else {
            this.notificationService.add(
                this.env._t("Could not upload files"),
                {
                    type: "danger",
                });
        }
        this.props.hideZone();
    }
}
AccountDropZone.defaultProps = {
    hideZone: () => {},
}
AccountDropZone.template = "account.DropZone";

// Account Move List View
class AccountMoveUploadListRenderer extends ListRenderer {
    setup() {
        super.setup();
        this.state.dropzoneVisible = false;
    }
}
AccountMoveUploadListRenderer.template = "account.ListRenderer";
AccountMoveUploadListRenderer.components = {
    ...ListRenderer.components,
    AccountDropZone,
};

ListController.components = {
    ...ListController.components,
    AccountFileUploader,
}

const AccountMoveUploadListView = {
    ...listView,
    Renderer: AccountMoveUploadListRenderer,
    buttonTemplate: "account.ListView.Buttons",
};

// Account Move Kanban View
class AccountMoveUploadKanbanRenderer extends KanbanRenderer {
    setup() {
        super.setup();
        this.state.dropzoneVisible = false;
    }
}
AccountMoveUploadKanbanRenderer.template = "account.KanbanRenderer";
AccountMoveUploadKanbanRenderer.components = {
    ...KanbanRenderer.components,
    AccountDropZone
};

KanbanController.components = {
    ...KanbanController.components,
    AccountFileUploader
};

const AccountMoveUploadKanbanView = {
    ...kanbanView,
    Renderer: AccountMoveUploadKanbanRenderer,
    buttonTemplate: "account.KanbanView.Buttons",
};

// Accounting Dashboard
class DashboardKanbanRecord extends KanbanRecord {
    setup() {
        super.setup();
        this.state = useState({
            dropzoneVisible: false,
        });
    }
}
DashboardKanbanRecord.components = {
    ...DashboardKanbanRecord.components,
    AccountDropZone,
    AccountFileUploader,
}
DashboardKanbanRecord.template = "account.DashboardKanbanRecord";

class DashboardKanbanRenderer extends KanbanRenderer {}
DashboardKanbanRenderer.components = {
    ...KanbanRenderer.components,
    KanbanRecord: DashboardKanbanRecord,
};

const DashboardKanbanView = {
    ...kanbanView,
    Renderer: DashboardKanbanRenderer,
}

registry.category("views").add("account_tree", AccountMoveUploadListView);
registry.category("views").add("account_documents_kanban", AccountMoveUploadKanbanView);
registry.category("views").add("account_dashboard_kanban", DashboardKanbanView);
