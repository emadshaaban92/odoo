odoo.define('website_form_project.tour', function(require) {
    'use strict';

    const wTourUtils = require("website.tour_utils");

    const enterEditMode = function () {
        return [{
            content: "Select the contact us form by clicking on an input field",
            trigger: "iframe #wrap.o_editable section.s_website_form",
            extra_trigger: "iframe body.editor_enable",
        }, {
            content: "Verify that the form editor appeared",
            trigger: '.o_we_customize_panel .snippet-option-WebsiteFormEditor',
            run: () => null,
        }];
    };
    
    const createProjectFromView = function (name) {
        return [{
            content: "Give a name to the new project",
            trigger: 'div[name="name"] input',
            run: `text ${name}`,
        }, {
            content: "Save the new project",
            trigger: 'button.o_form_button_save',
        }, {
            content: "Go back to the contactus page",
            auto:true,
            trigger: '.o_form_view:not(:has(.o_form_button_save))',
            run: function () {
                window.location.href = window.location.origin + '/@/contactus';
            },
        }];
    };

    const websiteFormNoProject = [
        ...enterEditMode(),
    {
        content: "Open the action select",
        trigger: `we-select:has(we-button:contains("Send an E-mail")) we-toggler`,
    }, {
        content: "Click on the option",
        trigger: `we-select we-button:contains("Create a Task")`,
    }, {
        id: "error_popup",
        content: "Click on the 'Cancel' button in the dialog pop-up",
        trigger: `.modal-dialog .modal-content .modal-footer .btn span:contains("Cancel")`,
    }, {
        content: "Save the page",
        trigger: 'button[data-action=save]',
    }, {
        content: 'Wait for reload',
        trigger: 'body:not(.editor_enable)',
    }];

    wTourUtils.registerWebsitePreviewTour('website_form_no_project_tour', {
        test: true,
        edition: true,
        url: '/contactus',
    }, websiteFormNoProject);

    const formErrorStepIndex = websiteFormNoProject.findIndex(s => s.id && s.id === 'error_popup');

    const formErrorCreateProject = [{
        content: "Click on the 'Create Project' button in the dialog pop-up",
        trigger: `.btn span:contains("Create Project")`,
    },
        ...createProjectFromView("test project"), 
    {
        content: 'Enter in edit mode again',
        trigger: '.o_edit_website_container > a',
    }, 
        ...enterEditMode(),
    {
        content: "Open the action select",
        trigger: `we-select:has(we-button:contains("Send an E-mail")) we-toggler`,
    }, {
        content: "Click on the option",
        trigger: `we-select we-button:contains("Create a Task")`,
    }, {
        content: "Save the page",
        trigger: 'button[data-action=save]',
    }, {
        content: 'Wait for reload',
        trigger: 'body:not(.editor_enable)',
    }
];

    wTourUtils.registerWebsitePreviewTour('website_form_error_create_project', {
        test: true,
        edition: true,
        url: '/contactus',
    }, websiteFormNoProject.slice(0, formErrorStepIndex).concat(formErrorCreateProject));


    const websiteFormButtonCreateProject = [
        ...enterEditMode(), 
    {
        content: "Click on the create action button next to the action select drop-down",
        trigger: 'we-button.o_we_user_value_widget[title="Create new"]'
    }, {
        content: "Click the discard option in the confirmation pop-up",
        trigger: `button.btn span:contains("Discard")`,
    },
        ...createProjectFromView("test project 2"),
    {
        content: 'Enter in edit mode again',
        trigger: '.o_edit_website_container > a',
    },
        ...enterEditMode(),
    {
        content: "Open the project select",
        trigger: `we-select:has(we-button:contains("test project")) we-toggler`,
    }, {
        content: "Click on the correct project option",
        trigger: `we-select we-button:contains("test project 2")`,
    }, {
        content: "Save the page",
        trigger: 'button[data-action=save]',
    }, {
        content: 'Wait for reload',
        trigger: 'body:not(.editor_enable)',
    }];   

    wTourUtils.registerWebsitePreviewTour('website_form_button_create_project', {
        test: true,
        edition: true,
        url: '/contactus',
    }, websiteFormButtonCreateProject);

    return {};
});
