/** @odoo-module **/

import tour from 'web_tour.tour';

function fail(errorMessage) {
    tour._consume_tour(tour.running_tour, errorMessage);
}

tour.register('course_member_invited_members_only_logged', {
    test: true
}, [
{
    trigger: 'a:contains("Gardening: The Know-How")',
    run: function () {} // check that preview are accessible
},
{
    trigger: '.o_wslides_slides_list_slide:contains("Home Gardening")',
    run: function () {
        const $slide = $('.o_wslides_slides_list_slide:contains("Home Gardening")');
        if ($slide.contents().find('a').length !== 0) {
            fail("Invited member should not see non-preview slides");
        } // other slides are not accessible
    }
},
{
    trigger: 'a:contains("Join this Course")',
},
{
    trigger: '.o_wslides_js_course_join:contains("You\'re enrolled")',
    run: function () {} // check membership
},
{
    trigger: '.o_wslides_js_slides_list_slide_link:contains("Home Gardening")',
    run: function () {} // check access is now given to the slides
},
]);


tour.register('course_member_invited_members_only_public', {
    test: true
}, [
{
    trigger: '.o_wslides_slides_list_slide:contains("Gardening: The Know-How")',
    run: function () {
        const $slide = $('.o_wslides_slides_list_slide:contains("Gardening: The Know-How")');
        if ($slide.contents().find('a').length !== 0) {
            fail("The preview should not allow the public user to browse slides");
        }
    }
},
{
    trigger: 'a:contains("Join this Course")',
},
{
    trigger: 'a:contains("login")',
},
{
    trigger: 'input[id="password"]',
    run: 'text portal',
},
{
    trigger: 'button:contains("Log in")',
},
{
    trigger: 'a:contains("Join this Course")',
},
{
    trigger: '.o_wslides_js_course_join:contains("You\'re enrolled")',
    run: function () {} // check membership
},
{
    trigger: '.o_wslides_js_slides_list_slide_link:contains("Gardening: The Know-How")',
    run: function () {} // check access is now given to the slides
}
]);
