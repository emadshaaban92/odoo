/** @odoo-module **/
import { ActionContainer } from "../action_manager/action_manager";
const { Component, hooks } = owl;
import { NavBar } from "./navbar/navbar";
import { useService } from "../core/hooks";
export class WebClient extends Component {
  constructor(...args) {
    super(...args);
    this.menus = useService("menus");
    this.actionManager = useService("action_manager");
    this.title = useService("title");
    this.router = useService("router");
    this.user = useService("user");
    this.Components = odoo.mainComponentRegistry.getEntries();
    this.title.setParts({ zopenerp: "Odoo" }); // zopenerp is easy to grep
    hooks.onMounted(() => {
      this.env.bus.on("ROUTE_CHANGE", this, this.loadRouterState);
      this.env.bus.on("ACTION_MANAGER:UI-UPDATED", this, (mode) => {
        if (mode !== "new") {
          this.el.classList.toggle("o_fullscreen", mode === "fullscreen");
        }
      });
      this.loadRouterState();
    });
  }
  static getClass(config) {
    return this;
  }
  mounted() {
    // the chat window and dialog services listen to 'web_client_ready' event in
    // order to initialize themselves:
    this.env.bus.trigger("WEB_CLIENT_READY");
  }
  async loadRouterState() {
    const options = {
      clearBreadcrumbs: true,
    };
    const state = this.router.current.hash;
    let action = state.action;
    if (action && !Number.isNaN(action)) {
      action = parseInt(action, 10);
    }
    let menuId = state.menu_id ? parseInt(state.menu_id, 10) : undefined;
    const actionManagerHandles = await this.actionManager.loadState(state, options);
    if (!actionManagerHandles) {
      if (!action && menuId) {
        // determine action from menu_id key
        const menu = this.menus.getAll().find((m) => menuId === m.id);
        action = menu && menu.actionID;
      }
      if (action) {
        await this.actionManager.doAction(action, options);
      }
    }
    // Determine the app we are in
    if (!menuId && typeof action === "number") {
      const menu = this.menus.getAll().find((m) => m.actionID === action);
      menuId = menu && menu.appID;
    }
    if (menuId) {
      this.menus.setCurrentMenu(menuId);
    }
    if (!actionManagerHandles && !action) {
      return this._loadDefaultApp();
    }
  }
  async _loadDefaultApp() {
    const action = this.user.home_action_id;
    if (action) {
      // Don't know what to do here: should we set the menu
      // even if it's a guess ?
      return this.actionManager.doAction(action, { clearBreadcrumbs: true });
    }
    const root = this.menus.getMenu("root");
    const firstApp = root.children[0];
    if (firstApp) {
      return this.menus.selectMenu(firstApp);
    }
  }
}
WebClient.components = { ActionContainer, NavBar };
WebClient.template = "wowl.WebClient";
