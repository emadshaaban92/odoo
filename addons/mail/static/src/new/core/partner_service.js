/** @odoo-module */

import { Partner } from "@mail/new/core/partner_model";

export class PartnerService {
    constructor(env, store) {
        this.env = env;
        /** @type {import("@mail/new/core/store_service").Store} */
        this.store = store;
    }

    /**
     * @param {import("@mail/new/core/partner_model").Data} data
     * @returns {import("@mail/new/core/partner_model").Partner}
     */
    static insert(data) {
        let partner = this.store.partners[data.id];
        if (!partner) {
            partner = new Partner();
            partner._store = this.store;
            this.store.partners[data.id] = partner;
            // Get reactive version.
            partner = this.store.partners[data.id];
        }
        const {
            id = partner.id,
            name = partner.name,
            im_status = partner.im_status,
            email = partner.email,
        } = data;
        Object.assign(partner, {
            id,
            name,
            im_status,
            email,
        });
        if (
            partner.im_status !== "im_partner" &&
            !partner.is_public &&
            !this.store.registeredImStatusPartners.includes(partner.id)
        ) {
            this.store.registeredImStatusPartners.push(partner.id);
        }
        // return reactive version
        return partner;
    }
}

export const partnerService = {
    dependencies: ["mail.store"],
    start(env, { "mail.store": store }) {
        return new PartnerService(env, store);
    },
};
