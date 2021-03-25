/** @odoo-module **/

import { click, getFixture, makeTestEnv, nextTick } from "../helpers/index";
import {
  ErrorDialog,
  Error504Dialog,
  RedirectWarningDialog,
  SessionExpiredDialog,
  WarningDialog,
  ClientErrorDialog,
} from "../../src/errors/error_dialogs";
import { Registry } from "../../src/core/registry";
import OdooError from "../../src/errors/odoo_error";
import { uiService } from "../../src/services/ui_service";
import { patch, unpatch } from "../../src/utils/patch";
import { browser } from "../../src/core/browser";

const { Component, mount, tags } = owl;
let target;
let env;
let parent;
let baseConfig;

QUnit.module("Error dialogs", {
  async beforeEach() {
    target = getFixture();
    const dialogContainer = document.createElement("div");
    dialogContainer.classList.add("o_dialog_container");
    target.append(dialogContainer);
    const serviceRegistry = new Registry();
    serviceRegistry.add("ui", uiService);
    baseConfig = { serviceRegistry };
  },
  async afterEach() {
    parent.unmount();
  },
});

QUnit.test("ErrorDialog with traceback", async (assert) => {
  var _a, _b, _c;
  assert.expect(11);
  class Parent extends Component {
    constructor() {
      super(...arguments);
      this.message = "Something bad happened";
      this.data = { debug: "Some strange unreadable stack" };
      this.name = "ERROR_NAME";
      this.traceback = "This is a tracback string";
    }
  }
  Parent.components = { ErrorDialog };
  Parent.template = tags.xml`<ErrorDialog traceback="traceback" name="name" message="message" data="data"/>`;
  assert.containsNone(target, ".o_dialog");
  env = await makeTestEnv(baseConfig);
  parent = await mount(Parent, { env, target });
  assert.containsOnce(target, "div.o_dialog_container .o_dialog");
  assert.strictEqual(
    (_a = target.querySelector("header .modal-title")) === null || _a === void 0
      ? void 0
      : _a.textContent,
    "Odoo Error"
  );
  const mainButtons = target.querySelectorAll("main button");
  assert.deepEqual(
    [...mainButtons].map((el) => el.textContent),
    ["Copy the full error to clipboard", "See details"]
  );
  assert.deepEqual(
    [...target.querySelectorAll("main .clearfix p")].map((el) => el.textContent),
    ["An error occurred", "Please use the copy button to report the error to your support service."]
  );
  assert.containsNone(target, "div.o_error_detail");
  assert.strictEqual(
    (_b = target.querySelector(".o_dialog footer button")) === null || _b === void 0
      ? void 0
      : _b.textContent,
    "Ok"
  );
  click(mainButtons[1]);
  await nextTick();
  assert.deepEqual(
    [...target.querySelectorAll("main .clearfix p")].map((el) => el.textContent),
    [
      "An error occurred",
      "Please use the copy button to report the error to your support service.",
      "Something bad happened",
    ]
  );
  assert.deepEqual(
    [...target.querySelectorAll("main .clearfix code")].map((el) => el.textContent),
    ["ERROR_NAME"]
  );
  assert.containsOnce(target, "div.o_error_detail");
  assert.strictEqual(
    (_c = target.querySelector("div.o_error_detail")) === null || _c === void 0
      ? void 0
      : _c.textContent,
    "This is a tracback string"
  );
});

QUnit.test("Client ErrorDialog with traceback", async (assert) => {
  var _a, _b, _c;
  assert.expect(11);
  class Parent extends Component {
    setup() {
      this.message = "Something bad happened";
      this.data = { debug: "Some strange unreadable stack" };
      this.name = "ERROR_NAME";
      this.traceback = "This is a tracback string";
    }
  }
  Parent.components = { ClientErrorDialog };
  Parent.template = tags.xml`<ClientErrorDialog traceback="traceback" name="name" message="message" data="data"/>`;
  assert.containsNone(target, ".o_dialog");
  env = await makeTestEnv(baseConfig);
  parent = await mount(Parent, { env, target });
  assert.containsOnce(target, "div.o_dialog_container .o_dialog");
  assert.strictEqual(
    (_a = target.querySelector("header .modal-title")) === null || _a === void 0
      ? void 0
      : _a.textContent,
    "Odoo Client Error"
  );
  const mainButtons = target.querySelectorAll("main button");
  assert.deepEqual(
    [...mainButtons].map((el) => el.textContent),
    ["Copy the full error to clipboard", "See details"]
  );
  assert.deepEqual(
    [...target.querySelectorAll("main .clearfix p")].map((el) => el.textContent),
    ["An error occurred", "Please use the copy button to report the error to your support service."]
  );
  assert.containsNone(target, "div.o_error_detail");
  assert.strictEqual(
    (_b = target.querySelector(".o_dialog footer button")) === null || _b === void 0
      ? void 0
      : _b.textContent,
    "Ok"
  );
  click(mainButtons[1]);
  await nextTick();
  assert.deepEqual(
    [...target.querySelectorAll("main .clearfix p")].map((el) => el.textContent),
    [
      "An error occurred",
      "Please use the copy button to report the error to your support service.",
      "Something bad happened",
    ]
  );
  assert.deepEqual(
    [...target.querySelectorAll("main .clearfix code")].map((el) => el.textContent),
    ["ERROR_NAME"]
  );
  assert.containsOnce(target, "div.o_error_detail");
  assert.strictEqual(
    (_c = target.querySelector("div.o_error_detail")) === null || _c === void 0
      ? void 0
      : _c.textContent,
    "This is a tracback string"
  );
});

QUnit.test("button clipboard copy error traceback", async (assert) => {
  assert.expect(1);
  const error = new OdooError("ERROR_NAME");
  error.message = "This is the message";
  error.traceback = "This is a traceback";
  patch(browser, "test.navigator", {
    navigator: {
      clipboard: {
        writeText: (value) => {
          assert.strictEqual(value, `${error.name}\n${error.message}\n${error.traceback}`);
        },
      },
    },
  });
  env = await makeTestEnv({ ...baseConfig });
  class Parent extends Component {
    constructor() {
      super(...arguments);
      this.message = error.message;
      this.name = "ERROR_NAME";
      this.traceback = "This is a traceback";
    }
  }
  Parent.components = { ErrorDialog };
  Parent.template = tags.xml`<ErrorDialog traceback="traceback" name="name" message="message" data="data"/>`;
  parent = await mount(Parent, { env, target });
  const clipboardButton = target.querySelector(".fa-clipboard");
  click(clipboardButton);
  await nextTick();
  unpatch(browser, "test.navigator");
});

QUnit.test("WarningDialog", async (assert) => {
  var _a, _b, _c;
  assert.expect(5);
  class Parent extends Component {
    constructor() {
      super(...arguments);
      this.name = "odoo.exceptions.UserError";
      this.message = "...";
      this.data = { arguments: ["Some strange unreadable message"] };
    }
  }
  Parent.components = { WarningDialog };
  Parent.template = tags.xml`<WarningDialog exceptionName="name" message="message" data="data"/>`;
  assert.containsNone(target, ".o_dialog");
  env = await makeTestEnv(baseConfig);
  parent = await mount(Parent, { env, target });
  assert.containsOnce(target, "div.o_dialog_container .o_dialog");
  assert.strictEqual(
    (_a = target.querySelector("header .modal-title")) === null || _a === void 0
      ? void 0
      : _a.textContent,
    "User Error"
  );
  assert.strictEqual(
    (_b = target.querySelector("main")) === null || _b === void 0 ? void 0 : _b.textContent,
    "Some strange unreadable message"
  );
  assert.strictEqual(
    (_c = target.querySelector(".o_dialog footer button")) === null || _c === void 0
      ? void 0
      : _c.textContent,
    "Ok"
  );
});

QUnit.test("RedirectWarningDialog", async (assert) => {
  var _a, _b;
  assert.expect(10);
  class Parent extends Component {
    constructor() {
      super(...arguments);
      this.data = {
        arguments: ["Some strange unreadable message", "buy_action_id", "Buy book on cryptography"],
      };
    }
    onDialogClosed() {
      assert.step("dialog-closed");
    }
  }
  Parent.components = { RedirectWarningDialog };
  Parent.template = tags.xml`<RedirectWarningDialog data="data" t-on-dialog-closed="onDialogClosed"/>`;
  const faceActionService = {
    name: "action",
    deploy() {
      return {
        doAction(actionId) {
          assert.step(actionId);
        },
      };
    },
  };
  baseConfig.serviceRegistry.add("action", faceActionService);
  env = await makeTestEnv(baseConfig);
  assert.containsNone(target, ".o_dialog");
  parent = await mount(Parent, { env, target });
  assert.containsOnce(target, "div.o_dialog_container .o_dialog");
  assert.strictEqual(
    (_a = target.querySelector("header .modal-title")) === null || _a === void 0
      ? void 0
      : _a.textContent,
    "Odoo Warning"
  );
  assert.strictEqual(
    (_b = target.querySelector("main")) === null || _b === void 0 ? void 0 : _b.textContent,
    "Some strange unreadable message"
  );
  let footerButtons = target.querySelectorAll("footer button");
  assert.deepEqual(
    [...footerButtons].map((el) => el.textContent),
    ["Buy book on cryptography", "Cancel"]
  );
  await click(footerButtons[0]); // click on "Buy book on cryptography"
  assert.verifySteps(["buy_action_id", "dialog-closed"]);

  await click(footerButtons[1]); // click on "Cancel"
  assert.verifySteps(["dialog-closed"]);
});

QUnit.test("Error504Dialog", async (assert) => {
  var _a, _b, _c;
  assert.expect(5);
  class Parent extends Component {}
  Parent.components = { Error504Dialog };
  Parent.template = tags.xml`<Error504Dialog/>`;
  assert.containsNone(target, ".o_dialog");
  env = await makeTestEnv(baseConfig);
  parent = await mount(Parent, { env, target });
  assert.containsOnce(target, "div.o_dialog_container .o_dialog");
  assert.strictEqual(
    (_a = target.querySelector("header .modal-title")) === null || _a === void 0
      ? void 0
      : _a.textContent,
    "Request timeout"
  );
  assert.strictEqual(
    (_b = target.querySelector("main p")) === null || _b === void 0 ? void 0 : _b.textContent,
    " The operation was interrupted. This usually means that the current operation is taking too much time. "
  );
  assert.strictEqual(
    (_c = target.querySelector(".o_dialog footer button")) === null || _c === void 0
      ? void 0
      : _c.textContent,
    "Ok"
  );
});

QUnit.test("SessionExpiredDialog", async (assert) => {
  var _a, _b;
  assert.expect(7);
  class Parent extends Component {}
  Parent.components = { SessionExpiredDialog };
  Parent.template = tags.xml`<SessionExpiredDialog/>`;
  patch(browser, "test.location", {
    location: {
      reload() {
        assert.step("location reload");
      },
    },
  });
  env = await makeTestEnv({ ...baseConfig });
  assert.containsNone(target, ".o_dialog");
  parent = await mount(Parent, { env, target });
  assert.containsOnce(target, "div.o_dialog_container .o_dialog");
  assert.strictEqual(
    (_a = target.querySelector("header .modal-title")) === null || _a === void 0
      ? void 0
      : _a.textContent,
    "Odoo Session Expired"
  );
  assert.strictEqual(
    (_b = target.querySelector("main p")) === null || _b === void 0 ? void 0 : _b.textContent,
    " Your Odoo session expired. The current page is about to be refreshed. "
  );
  const footerButton = target.querySelector(".o_dialog footer button");
  assert.strictEqual(footerButton.textContent, "Ok");
  click(footerButton);
  assert.verifySteps(["location reload"]);
  unpatch(browser, "test.location");
});
