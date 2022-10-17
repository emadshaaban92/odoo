/** @odoo-module **/

import OnboardingStepFormController from "@onboarding/views/form/onboarding_step_form_controller";


export default class AccountCommonOnboardingCompanyFormController extends OnboardingStepFormController {
    /**
     * @override
     */
    getStepConfig() {
        return {
            ...super.getStepConfig(),
            stepName: "action_save_account_common_onboarding_company_step",
        };
    }
}
