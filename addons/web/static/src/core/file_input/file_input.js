/** @odoo-module **/

import { useService } from "@web/core/utils/hooks";

const { Component, onMounted, useRef } = owl;

/**
 * Gets dataURL (base64 data) from the given file or blob.
 * Technically wraps FileReader.readAsDataURL in Promise.
 *
 * @param {Blob | File} file
 * @returns {Promise} resolved with the dataURL, or rejected if the file is
 *  empty or if an error occurs.
 */
function getDataURLFromFile(file) {
    if (!file) {
        return Promise.reject();
    }
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.addEventListener("load", () => resolve(reader.result));
        reader.addEventListener("abort", reject);
        reader.addEventListener("error", reject);
        reader.readAsDataURL(file);
    });
}

/**
 * Custom file input
 *
 * Component representing a customized input of type file. It takes a sub-template
 * in its default t-slot and uses it as the trigger to open the file upload
 * prompt.
 * @extends Component
 *
 * Props:
 * @param {string} [props.acceptedFileExtensions='*'] Comma-separated
 *      list of authorized file extensions (default to all).
 * @param {string} [props.route='/web/binary/upload'] Route called when
 *      a file is uploaded in the input.
 * @param {string} [props.resId]
 * @param {string} [props.resModel]
 * @param {string} [props.multiUpload=false] Whether the input should allow
 *      to upload multiple files at once.
 */
export class FileInput extends Component {
    setup() {
        this.http = useService("http");
        this.fileInputRef = useRef("file-input");

        onMounted(() => {
            if (this.props.autoOpen) {
                this.onTriggerClicked();
            }
        });
    }

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * Upload an attachment to the given route with the given parameters:
     * - ufile: list of files contained in the file input
     * - csrf_token: CSRF token provided by the odoo global object
     * - resModel: a specific model which will be given when creating the attachment
     * - resId: the id of the resModel target instance
     */
    async onFileInputChange() {
        const { resId, resModel, route, shouldUpload } = this.props;
        if (shouldUpload) {
            const params = {
                csrf_token: odoo.csrf_token,
                ufile: [...this.fileInputRef.el.files],
            };
            if (resModel) {
                params.model = resModel;
            }
            if (resId) {
                params.id = resId;
            }
            const fileData = await this.http.post(route, params, "text");
            const parsedFileData = JSON.parse(fileData);
            if (parsedFileData.error) {
                throw new Error(parsedFileData.error);
            }
            this.props.onUpload(parsedFileData);
        } else {
            for (const file of this.fileInputRef.el.files) {
                const data = await getDataURLFromFile(file);
                if (!file.size) {
                    this.props.onError(file);
                }
                this.props.onUpload({
                    name: file.name,
                    size: file.size,
                    type: file.type,
                    data: data.split(",")[1],
                    objectUrl: file.type === "application/pdf" ? URL.createObjectURL(file) : null,
                });
            }
        }
    }

    /**
     * Redirect clicks from the trigger element to the input.
     */
    onTriggerClicked() {
        this.fileInputRef.el.click();
    }
}

FileInput.defaultProps = {
    acceptedFileExtensions: "*",
    hidden: false,
    multiUpload: false,
    onError: () => {},
    onUpload: () => {},
    route: "/web/binary/upload_attachment",
    shouldUpload: true,
};
FileInput.props = {
    acceptedFileExtensions: { type: String, optional: true },
    autoOpen: { type: Boolean, optional: true },
    hidden: { type: Boolean, optional: true },
    multiUpload: { type: Boolean, optional: true },
    onError: { type: Function, optional: true },
    onUpload: { type: Function, optional: true },
    resId: { type: Number, optional: true },
    resModel: { type: String, optional: true },
    route: { type: String, optional: true },
    shouldUpload: { type: Boolean, optional: true },
    "*": true,
};
FileInput.template = "web.FileInput";
