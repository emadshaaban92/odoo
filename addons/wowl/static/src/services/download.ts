import { NetworkErrorDialog, ServerErrorDialog } from "../crash_manager/error_dialogs";
import OdooError from "../crash_manager/odoo_error";
import parse from "../libs/content-disposition";
import download from "../libs/download";
import { Service } from "../types";

export interface DowloadFileOptionsFromForm {
  form: HTMLFormElement;
}

export interface DowloadFileOptionsFromParams {
  url: string;
  data: object;
}

export type DowloadFileOptions = DowloadFileOptionsFromForm | DowloadFileOptionsFromParams;

/**
 * Cooperative file download implementation, for ajaxy APIs.
 *
 * Requires that the server side implements an httprequest correctly
 * setting the `fileToken` cookie to the value provided as the `token`
 * parameter. The cookie *must* be set on the `/` path and *must not* be
 * `httpOnly`.
 *
 * It would probably also be a good idea for the response to use a
 * `Content-Disposition: attachment` header, especially if the MIME is a
 * "known" type (e.g. text/plain, or for some browsers application/json
 *
 * @param {Object} options
 * @param {String} [options.url] used to dynamically create a form
 * @param {Object} [options.data] data to add to the form submission. If can be used without a form, in which case a form is created from scratch. Otherwise, added to form data
 * @param {HTMLFormElement} [options.form] the form to submit in order to fetch the file
 * @param {Function} [options.success] callback in case of download success
 * @param {Function} [options.error] callback in case of request error, provided with the error body
 * @param {Function} [options.complete] called after both ``success`` and ``error`` callbacks have executed
 * @returns {Promise} file name if no problem, error object other wise
 */

export type Download = (options: DowloadFileOptions) => Promise<unknown>;

export const downloadService: Service<Download> = {
  name: "download",
  deploy(): Download {
    return async function (options: DowloadFileOptions) {
      return new Promise((resolve, reject) => {
        const xhr: XMLHttpRequest = new XMLHttpRequest();
        let data: FormData;
        if (options.hasOwnProperty("form")) {
          options = options as DowloadFileOptionsFromForm;
          xhr.open(options.form.method, options.form.action);
          data = new FormData(options.form);
        } else {
          options = options as DowloadFileOptionsFromParams;
          xhr.open("POST", options.url);
          data = new FormData();
          Object.entries(options.data).forEach((entry) => {
            const [key, value] = entry;
            data.append(key, value);
          });
        }
        data.append("token", "dummy-because-api-expects-one");
        if (odoo.csrf_token) {
          data.append("csrf_token", odoo.csrf_token);
        }
        // IE11 wants this after xhr.open or it throws
        xhr.responseType = "blob";
        xhr.onload = () => {
          const mimetype = xhr.response.type;
          if (xhr.status === 200 && mimetype !== "text/html") {
            // replace because apparently we send some C-D headers with a trailing ";"
            const header = (xhr.getResponseHeader("Content-Disposition") || "").replace(/;$/, "");
            const filename = header ? (parse(header).parameters as any).filename : null;
            download(xhr.response, filename, mimetype);
            return resolve(filename);
          } else {
            const decoder = new FileReader();
            decoder.onload = () => {
              const contents = decoder.result as string;
              const doc = new DOMParser().parseFromString(contents, "text/html");
              const nodes =
                doc.body.children.length === 0 ? doc.body.childNodes : doc.body.children;
              const error = new OdooError("XHR_SERVER_ERROR");
              error.Component = ServerErrorDialog;
              try {
                // Case of a serialized Odoo Exception: It is Json Parsable
                const node = nodes[1] || nodes[0];
                error.message = "Serialized Python Exception";
                error.traceback = JSON.parse(node.textContent!);
              } catch (e) {
                // Arbitrary uncaught python side exception
                error.message = "Arbitrary Uncaught Python Exception";
                error.traceback = `${xhr.status}
                          ${nodes.length > 0 ? nodes[0].textContent : ""}
                          ${nodes.length > 1 ? nodes[1].textContent : ""}
                      `;
              }
              reject(error);
            };
            decoder.readAsText(xhr.response);
          }
        };
        xhr.onerror = () => {
          const error = new OdooError("XHR_NETWORK_ERROR");
          error.Component = NetworkErrorDialog;
          reject(error);
        };
        xhr.send(data);
      });
    };
  },
};
