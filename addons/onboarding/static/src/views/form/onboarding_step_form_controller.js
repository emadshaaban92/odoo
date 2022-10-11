/** @odoo-module **/

import { FormController } from "@web/views/form/form_controller";
import { useService } from "@web/core/utils/hooks";

/**
 * Controller to use for an onboarding step dialog, not the
 * onboarding.onboarding.step form view itself.
 */
export default class OnboardingStepFormController extends FormController {
    setup() {
        super.setup();
        this.orm = useService('orm');
    }
    /**
     * Returns the name of the onboarding step to validate after the dialog
     * record is saved and whether to reload the page (useful if the current
     * view needs to be updated or if the banner is not automatically reloaded).
     *
     * @returns {{ String, boolean }} stepName, reloadOnFirstValidation
     */
    getStepConfig() {
        return {
            stepName: "",
            reloadOnFirstValidation: false
        };
    }
    /**
     * Overridden to mark the onboarding step as completed and reload the view.
     *
     * @override
     */
    async saveButtonClicked() {
        await super.saveButtonClicked();
        const { stepName, reloadOnFirstValidation } = this.getStepConfig();
        const wasFirstValidation = await this.orm.call(
            'onboarding.onboarding.step',
            stepName
        );
        this.env.dialogData.close();
        if (reloadOnFirstValidation && wasFirstValidation) {
            window.location.reload();
        }
    }
    /**
     * Close modal on discard.
     *
     * @override
     */
    async discard() {
        await super.discard();
        this.env.dialogData.close();
    }
}
