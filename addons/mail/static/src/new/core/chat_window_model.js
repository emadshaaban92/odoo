/* @odoo-module */

export class ChatWindow {
    /**
     * @param {import("@mail/new/core/messaging").Messaging['state']} state
     * @param {Object} data
     * @returns {ChatWindow}
     */
    static insert(state, data) {
        const { thread } = data;
        const chatWindow = state.chatWindows.find((cw) => cw.thread.localId === thread.localId);
        if (!chatWindow) {
            const chatWindow = new ChatWindow(data);
            chatWindow._state = state;
            state.chatWindows.push(chatWindow);
        } else {
            chatWindow.folded = false;
            chatWindow.autofocus++;
        }
    }

    constructor(data) {
        const { thread } = data;
        Object.assign(this, { thread, autofocus: 1, folded: false });
    }

    close() {
        const index = this._state.chatWindows.findIndex(
            (cw) => cw.thread.localId === this.thread.localId
        );
        if (index > -1) {
            this._state.chatWindows.splice(index, 1);
        }
    }
}
