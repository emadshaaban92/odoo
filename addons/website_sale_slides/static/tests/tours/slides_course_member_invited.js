/** @odoo-module **/

import tour from 'web_tour.tour';

function fail(errorMessage) {
    tour._consume_tour(tour.running_tour, errorMessage);
}

tour.register('course_payment_members_only_invited_logged', {
    test: true
}, [
{
    trigger: 'a:contains("Add to Cart")',
    run: function () {
        if ($('.o_wslides_js_course_join_link').length !== 0) {
            fail("The course should not be joinable before buying");
        }
    } // check that the course is buyable, but not joinable
},
{
    trigger: '.o_wslides_slides_list_slide:contains("Home Gardening")',
    run: function () {
        if ($(this.$anchor[0]).find('a').length !== 0) {
            fail("Invited member should not access non-preview slides");
        }
    } // non preview slides are not accessible
},
{
    trigger: 'a:contains("Gardening: The Know-How")',
    run: function () {} // check that preview slides are accessible
},
]);


tour.register('course_payment_members_only_invited_public', {
    test: true
}, [
{
    trigger: 'a:contains("Add to Cart")',
    run: function () {
        if ($('.o_wslides_js_course_join_link').length !== 0) {
            fail("The course should not be joinable before buying");
        }
    } // check that the course is buyable, but not joinable
},
{
    trigger: '.o_wslides_slides_list_slide:contains("Gardening: The Know-How")',
    run: function () {
        if ($(this.$anchor[0]).find('a').length !== 0) {
            fail("The preview should not allow the public user to browse slides");
        }
    }
},
]);
