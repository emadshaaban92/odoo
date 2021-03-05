/** @odoo-module **/
import { Dropdown } from "../../../components/dropdown/dropdown";
import { DropdownItem } from "../../../components/dropdown/dropdown_item";
import { FACET_ICONS } from "../search_utils";

const { Component } = owl;

export class ComparisonMenu extends Component {
  constructor() {
    super(...arguments);
    this.icon = FACET_ICONS.comparison;
    this.title = this.env._t("Comparison");
  }
  get items() {
    return this.props.searchModel.getSearchItems((searchItem) => searchItem.type === "comparison");
  }
  onDropdownItemSelected(ev) {
    const { itemId } = ev.detail.payload;
    this.props.searchModel.toggleSearchItem(itemId);
  }
}
ComparisonMenu.template = "wowl.ComparisonMenu";
ComparisonMenu.components = { Dropdown, DropdownItem };
