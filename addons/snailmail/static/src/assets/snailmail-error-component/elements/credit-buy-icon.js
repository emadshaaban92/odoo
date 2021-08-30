/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Element
        [Element/name]
            creditBuyIcon
        [Element/model]
            SnailmailErrorComponent
        [web.Element/tag]
            i
        [web.Element/class]
            fa
            fa-arrow-right
`;
