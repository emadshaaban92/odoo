/** @odoo-module **/

import { Listener } from '@mail/model/model_listener';

import { onRendered, onWillDestroy, onWillRender, useComponent } from '@odoo/owl';

/**
 * This hook provides support for automatically re-rendering when used records
 * or fields changed.
 *
 * Components that use this hook must be instantiated after messaging service is
 * started. However there is no restriction on the messaging record (coming from
 * the modelManager of the messaging service) being already initialized or even
 * created.
 */
export function useModels() {
    const component = useComponent();
    const listener = new Listener({
        name: `useModels() of ${component}`,
        type: 'useModels',
        onChange: () => component.render(),
    });
    onWillRender(() => {
        component.env.services.messaging.modelManager.startListening(listener);
    });
    onRendered(() => {
        component.env.services.messaging.modelManager.stopListening(listener);
    });
    onWillDestroy(() => {
        component.env.services.messaging.modelManager.removeListener(listener);
    });
    component.env.services.messaging.modelManager.created.then(() => {
        component.render();
    });
}
