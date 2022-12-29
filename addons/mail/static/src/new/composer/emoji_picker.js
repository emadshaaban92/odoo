/* @odoo-module */

import { markEventHandled } from "@mail/new/utils/misc";

import {
    Component,
    onMounted,
    onWillStart,
    useEffect,
    useRef,
    useState,
    onPatched,
    onWillPatch,
} from "@odoo/owl";
import { getBundle, loadBundle } from "@web/core/assets";
import { usePopover } from "@web/core/popover/popover_hook";
import { memoize } from "@web/core/utils/functions";
import { escapeRegExp } from "@web/core/utils/strings";

/**
 *
 * @param {string} refName
 * @param {object} props
 * @param {function} [props.onSelect]
 * @param {function} [props.onClose]
 */
export function useEmojiPicker(refName, props) {
    const ref = useRef(refName);
    const popover = usePopover();
    let closePopover = false;
    const toggle = () => {
        if (closePopover) {
            closePopover();
            closePopover = false;
        } else {
            closePopover = popover.add(ref.el, EmojiPicker, props, {
                onClose: () => (closePopover = false),
                popoverClass: "o-fast-popover",
            });
        }
    };
    onMounted(() => {
        ref.el.addEventListener("click", toggle);
        ref.el.addEventListener("mouseenter", loadEmoji);
    });
    onWillPatch(() => {
        ref.el.removeEventListener("click", toggle);
        ref.el.removeEventListener("mouseenter", loadEmoji);
    });
    onPatched(() => {
        ref.el.addEventListener("click", toggle);
        ref.el.addEventListener("mouseenter", loadEmoji);
    });
}

const _loadEmoji = memoize(() => getBundle("mail.assets_emoji").then(loadBundle));

/**
 * @returns {import("@mail/new/composer/emoji_data")}
 */
export async function loadEmoji() {
    await _loadEmoji();
    return odoo.runtimeImport("@mail/new/composer/emoji_data");
}

export class EmojiPicker extends Component {
    static props = ["onSelect", "close", "onClose?"];
    static defaultProps = { onClose: () => {} };
    static template = "mail.emoji_picker";

    setup() {
        this.categories = null;
        this.emojis = null;
        this.inputRef = useRef("input");
        this.gridRef = useRef("emoji-grid");
        this.shouldScrollElem = null;
        this.state = useState({
            categoryId: null,
            searchStr: "",
        });
        onWillStart(async () => {
            const { categories, emojis } = await loadEmoji();
            this.categories = categories;
            this.emojis = emojis;
            this.state.categoryId = this.categories[0].sortId;
        });
        onMounted(() => {
            this.inputRef.el.focus();
            this.highlightActiveCategory();
        });
        onPatched(() => {
            if (this.shouldScrollElem) {
                this.shouldScrollElem = false;
                const getElement = () =>
                    this.gridRef.el.querySelector(
                        `.o-emoji-category[data-category="${this.state.categoryId}"`
                    );
                const elem = getElement();
                if (elem) {
                    elem.scrollIntoView();
                } else {
                    this.shouldScrollElem = getElement;
                }
            }
        });
        useEffect(
            () => {
                if (this.state.searchStr) {
                    this.state.categoryId = null;
                } else {
                    this.highlightActiveCategory();
                }
            },
            () => [this.state.searchStr]
        );
    }

    onClick(ev) {
        markEventHandled(ev, "emoji.selectEmoji");
    }

    onKeydown(ev) {
        if (ev.key === "Escape") {
            this.props.close();
            this.props.onClose();
            ev.stopPropagation();
        }
    }

    getEmojis() {
        const search = this.state.searchStr;
        if (search.length > 1) {
            const regexp = new RegExp(
                search
                    .split("")
                    .map((x) => escapeRegExp(x))
                    .join(".*")
            );
            return this.emojis.filter((emoji) =>
                [emoji.name, ...emoji.keywords, ...emoji.emoticons, ...emoji.shortcodes].some((x) =>
                    x.match(regexp)
                )
            );
        }
        return this.emojis;
    }

    selectCategory(ev) {
        const id = Number(ev.target.dataset.id);
        if (id) {
            this.state.searchStr = "";
            this.state.categoryId = id;
            this.shouldScrollElem = true;
        }
    }

    selectEmoji(ev) {
        const codepoints = ev.target.dataset.codepoints;
        if (codepoints) {
            this.props.onSelect(codepoints);
            this.props.close();
            this.props.onClose();
        }
    }

    highlightActiveCategory() {
        if (!this.gridRef || !this.gridRef.el) {
            return;
        }
        const coords = this.gridRef.el.getBoundingClientRect();
        const res = document.elementFromPoint(coords.x, coords.y);
        if (!res) {
            return;
        }
        this.state.categoryId = parseInt(res.dataset.category);
    }
}
