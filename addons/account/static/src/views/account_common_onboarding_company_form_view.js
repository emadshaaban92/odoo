/** @odoo-module **/

import { formView } from "@web/views/form/form_view";
import { registry } from "@web/core/registry";

import AccountCommonOnboardingCompanyFormController from "./account_common_onboarding_company_form_controller.js";


const AccountCommonOnboardingCompanyFormView = {
    ...formView,
    Controller: AccountCommonOnboardingCompanyFormController,
};


registry.category("views").add("account_common_onboarding_company_form", AccountCommonOnboardingCompanyFormView);
