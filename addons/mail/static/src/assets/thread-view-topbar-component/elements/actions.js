/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Element
        [Element/name]
            actions
        [Element/model]
            ThreadViewTopbarComponent
        [web.Element/class]
            d-flex
            align-items-center
            ml-1
`;