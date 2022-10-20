/** @odoo-module **/

import { one, Model } from '@mail/model';

Model({
    name: 'ThirdManager',
    fields: {
        thirdView: one('ThirdView', {
            default: {},
            inverse: 'thirdManager',
            isCausal: true,
        }),
    },
});
