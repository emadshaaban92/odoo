/** @odoo-module */

import wTourUtils from 'website.tour_utils';

wTourUtils.registerWebsitePreviewTour('website_image_quality', {
    test: true,
    url: '/',
    edition: true,
}, [
    wTourUtils.dragNDrop({
        id: 's_text_image',
        name: 'Text - Image',
    }),
    {
        content: "Replace image",
        trigger: 'iframe .s_text_image img',
        run: 'dblclick',
    },
    {
        content: "Pick replacement image",
        trigger: '.o_select_media_dialog img[title="s_banner_default_image.jpg"]',
        run: 'click',
    },
    {
        content: "Open Width dropdown",
        trigger: 'we-customizeblock-options:has(we-title:contains("Image")) we-select:has(we-title:contains("Width")) we-toggler',
        run: 'click',
    },
    {
        content: "Select Original Width",
        trigger: 'we-customizeblock-options:has(we-title:contains("Image")) we-select:has(we-title:contains("Width")) we-button:contains("Original")',
        run: 'click',
    },
    {
        content: "Wait for selected image update",
        trigger: 'iframe .s_text_image img[src$="YFB//Z"]',
        run: () => {}, // It is a check.
    },
    {
        content: "Check image size",
        trigger: 'we-customizeblock-options:has(we-title:contains("Image")) .o_we_image_weight:contains("214.3 kb")',
        run: () => {}, // It is a check.
    },
    {
        content: "Set low quality",
        trigger: 'we-customizeblock-options:has(we-title:contains("Image")) we-range[data-set-quality] input',
        run: 'range 5',
    },
    {
        content: "Wait for image update: NOT original image",
        trigger: 'iframe .s_text_image img:not([src$="YFB//Z"])',
        run: () => {}, // It is a check.
    },
    {
        content: "Check image size",
        trigger: 'we-customizeblock-options:has(we-title:contains("Image")) .o_we_image_weight:contains("31.4 kb")',
        run: () => {}, // It is a check.
    },
    {
        content: "Set high quality",
        trigger: 'we-customizeblock-options:has(we-title:contains("Image")) we-range[data-set-quality] input',
        run: 'range 99',
    },
    {
        content: "Wait for image update: back to original image",
        trigger: 'iframe .s_text_image img[src$="YFB//Z"]',
        run: () => {}, // It is a check.
    },
    {
        content: "Check image size",
        trigger: 'we-customizeblock-options:has(we-title:contains("Image")) .o_we_image_weight:contains("214.3 kb")',
        run: () => {}, // It is a check.
    },
    ...wTourUtils.clickOnSave(),
]);
