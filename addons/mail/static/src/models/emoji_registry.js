/** @odoo-module **/

import { insertAndReplace } from '@mail/model/model_field_command';
import { one, many } from '@mail/model/model_field';
import { registerModel } from '@mail/model/model_core';

registerModel({
    name: 'EmojiRegistry',
    identifyingFields: ['messaging'],
    fields: {
        allEmojis: many('Emoji', {
            inverse: 'emojiRegistry',
        }),
        '😊': one('Emoji', {
            default: insertAndReplace({ unicode: '😊', sources: [':)', ':-)', '=)', ':]'], description: ':)' }),
            readonly: true,
            required: true,
        }),
        '😃': one('Emoji', {
            default: insertAndReplace({ unicode: '😃', sources: [':D', ':-D', '=D'], description: ':D' }),
            readonly: true,
            required: true,
        }),
        '😆': one('Emoji', {
            default: insertAndReplace({ unicode: '😆', sources: ['xD', 'XD'], description: 'xD' }),
            readonly: true,
            required: true,
        }),
        '😂': one('Emoji', {
            default: insertAndReplace({ unicode: '😂', sources: ["x'D"], description: "x'D" }),
            readonly: true,
            required: true,
        }),
        '😉': one('Emoji', {
            default: insertAndReplace({ unicode: '😉', sources: [';)', ';-)'], description: ';)' }),
            readonly: true,
            required: true,
        }),
        '😎': one('Emoji', {
            default: insertAndReplace({ unicode: '😎', sources: ['B)', '8)', 'B-)', '8-)'], description: 'B)' }),
            readonly: true,
            required: true,
        }),
        '😜': one('Emoji', {
            default: insertAndReplace({ unicode: '😜', sources: [';p', ';P'], description: ';p' }),
            readonly: true,
            required: true,
        }),
        '😋': one('Emoji', {
            default: insertAndReplace({ unicode: '😋', sources: [':p', ':P', ':-p', ':-P', '=P'], description: ':p' }),
            readonly: true,
            required: true,
        }),
        '😝': one('Emoji', {
            default: insertAndReplace({ unicode: '😝', sources: ['xp', 'xP'], description: 'xp' }),
            readonly: true,
            required: true,
        }),
        '😳': one('Emoji', {
            default: insertAndReplace({ unicode: '😳', sources: ['o_o'], description: 'o_o' }),
            readonly: true,
            required: true,
        }),
        '😐': one('Emoji', {
            default: insertAndReplace({ unicode: '😐', sources: [':|', ':-|'], description: ':|' }),
            readonly: true,
            required: true,
        }),
        '😕': one('Emoji', {
            default: insertAndReplace({ unicode: '😕', sources: [':/', ':-/'], description: ':/' }),
            readonly: true,
            required: true,
        }),
        '😞': one('Emoji', {
            default: insertAndReplace({ unicode: '😞', sources: [':('], description: ':(' }),
            readonly: true,
            required: true,
        }),
        '😱': one('Emoji', {
            default: insertAndReplace({ unicode: '😱', sources: [':@'], description: ':@' }),
            readonly: true,
            required: true,
        }),
        '😲': one('Emoji', {
            default: insertAndReplace({ unicode: '😲', sources: [':O', ':-O', ':o', ':-o'], description: ':O' }),
            readonly: true,
            required: true,
        }),
        '😨': one('Emoji', {
            default: insertAndReplace({ unicode: '😨', sources: [":'o"], description: ":'o" }),
            readonly: true,
            required: true,
        }),
        '😠': one('Emoji', {
            default: insertAndReplace({ unicode: '😠', sources: ['3:(', '>:('], description: '3:(' }),
            readonly: true,
            required: true,
        }),
        '😈': one('Emoji', {
            default: insertAndReplace({ unicode: '😈', sources: ['3:)', '>:)'], description: '3:)' }),
            readonly: true,
            required: true,
        }),
        '😘': one('Emoji', {
            default: insertAndReplace({ unicode: '😘', sources: [':*', ':-*'], description: ':*' }),
            readonly: true,
            required: true,
        }),
        '😇': one('Emoji', {
            default: insertAndReplace({ unicode: '😇', sources: ['o:)'], description: 'o:)' }),
            readonly: true,
            required: true,
        }),
        '😢': one('Emoji', {
            default: insertAndReplace({ unicode: '😢', sources: [":'("], description: ":'(" }),
            readonly: true,
            required: true,
        }),
        '😭': one('Emoji', {
            default: insertAndReplace({ unicode: '😭', sources: [":'-(", ':"('], description: ":'-(" }),
            readonly: true,
            required: true,
        }),
        '❤️': one('Emoji', {
            default: insertAndReplace({ unicode: '❤️', sources: ['<3', '&lt;3', ':heart'], description: '<3' }),
            readonly: true,
            required: true,
        }),
        '💔': one('Emoji', {
            default: insertAndReplace({ unicode: '💔', sources: ['</3', '&lt;/3'], description: '</3' }),
            readonly: true,
            required: true,
        }),
        '😍': one('Emoji', {
            default: insertAndReplace({ unicode: '😍', sources: [':heart_eyes'], description: ':heart_eyes' }),
            readonly: true,
            required: true,
        }),
        '👳': one('Emoji', {
            default: insertAndReplace({ unicode: '👳', sources: [':turban'], description: ':turban' }),
            readonly: true,
            required: true,
        }),
        '👍': one('Emoji', {
            default: insertAndReplace({ unicode: '👍', sources: [':+1'], description: ':+1' }),
            readonly: true,
            required: true,
        }),
        '👎': one('Emoji', {
            default: insertAndReplace({ unicode: '👎', sources: [':-1'], description: ':-1' }),
            readonly: true,
            required: true,
        }),
        '👌': one('Emoji', {
            default: insertAndReplace({ unicode: '👌', sources: [':ok'], description: ':ok' }),
            readonly: true,
            required: true,
        }),
        '💩': one('Emoji', {
            default: insertAndReplace({ unicode: '💩', sources: [':poop'], description: ':poop' }),
            readonly: true,
            required: true,
        }),
        '🙈': one('Emoji', {
            default: insertAndReplace({ unicode: '🙈', sources: [':no_see'], description: ':no_see' }),
            readonly: true,
            required: true,
        }),
        '🙉': one('Emoji', {
            default: insertAndReplace({ unicode: '🙉', sources: [':no_hear'], description: ':no_hear' }),
            readonly: true,
            required: true,
        }),
        '🙊': one('Emoji', {
            default: insertAndReplace({ unicode: '🙊', sources: [':no_speak'], description: ':no_speak' }),
            readonly: true,
            required: true,
        }),
        '🐞': one('Emoji', {
            default: insertAndReplace({ unicode: '🐞', sources: [':bug'], description: ':bug' }),
            readonly: true,
            required: true,
        }),
        '😺': one('Emoji', {
            default: insertAndReplace({ unicode: '😺', sources: [':kitten'], description: ':kitten' }),
            readonly: true,
            required: true,
        }),
        '🐻': one('Emoji', {
            default: insertAndReplace({ unicode: '🐻', sources: [':bear'], description: ':bear' }),
            readonly: true,
            required: true,
        }),
        '🐌': one('Emoji', {
            default: insertAndReplace({ unicode: '🐌', sources: [':snail'], description: ':snail' }),
            readonly: true,
            required: true,
        }),
        '🐗': one('Emoji', {
            default: insertAndReplace({ unicode: '🐗', sources: [':boar'], description: ':boar' }),
            readonly: true,
            required: true,
        }),
        '🍀': one('Emoji', {
            default: insertAndReplace({ unicode: '🍀', sources: [':clover'], description: ':clover' }),
            readonly: true,
            required: true,
        }),
        '🌹': one('Emoji', {
            default: insertAndReplace({ unicode: '🌹', sources: [':sunflower'], description: ':sunflower' }),
            readonly: true,
            required: true,
        }),
        '🔥': one('Emoji', {
            default: insertAndReplace({ unicode: '🔥', sources: [':fire'], description: ':fire' }),
            readonly: true,
            required: true,
        }),
        '☀️': one('Emoji', {
            default: insertAndReplace({ unicode: '☀️', sources: [':sun'], description: ':sun' }),
            readonly: true,
            required: true,
        }),
        '⛅️': one('Emoji', {
            default: insertAndReplace({ unicode: '⛅️', sources: [':partly_sunny:'], description: ':partly_sunny:' }),
            readonly: true,
            required: true,
        }),
        '🌈': one('Emoji', {
            default: insertAndReplace({ unicode: '🌈', sources: [':rainbow'], description: ':rainbow' }),
            readonly: true,
            required: true,
        }),
        '☁️': one('Emoji', {
            default: insertAndReplace({ unicode: '☁️', sources: [':cloud'], description: ':cloud' }),
            readonly: true,
            required: true,
        }),
        '⚡️': one('Emoji', {
            default: insertAndReplace({ unicode: '⚡️', sources: [':zap'], description: ':zap' }),
            readonly: true,
            required: true,
        }),
        '⭐️': one('Emoji', {
            default: insertAndReplace({ unicode: '⭐️', sources: [':star'], description: ':star' }),
            readonly: true,
            required: true,
        }),
        '🍪': one('Emoji', {
            default: insertAndReplace({ unicode: '🍪', sources: [':cookie'], description: ':cookie' }),
            readonly: true,
            required: true,
        }),
        '🍕': one('Emoji', {
            default: insertAndReplace({ unicode: '🍕', sources: [':pizza'], description: ':pizza' }),
            readonly: true,
            required: true,
        }),
        '🍔': one('Emoji', {
            default: insertAndReplace({ unicode: '🍔', sources: [':hamburger'], description: ':hamburger' }),
            readonly: true,
            required: true,
        }),
        '🍟': one('Emoji', {
            default: insertAndReplace({ unicode: '🍟', sources: [':fries'], description: ':fries' }),
            readonly: true,
            required: true,
        }),
        '🎂': one('Emoji', {
            default: insertAndReplace({ unicode: '🎂', sources: [':cake'], description: ':cake' }),
            readonly: true,
            required: true,
        }),
        '🍰': one('Emoji', {
            default: insertAndReplace({ unicode: '🍰', sources: [':cake_part'], description: ':cake_part' }),
            readonly: true,
            required: true,
        }),
        '☕️': one('Emoji', {
            default: insertAndReplace({ unicode: '☕️', sources: [':coffee'], description: ':coffee' }),
            readonly: true,
            required: true,
        }),
        '🍌': one('Emoji', {
            default: insertAndReplace({ unicode: '🍌', sources: [':banana'], description: ':banana' }),
            readonly: true,
            required: true,
        }),
        '🍣': one('Emoji', {
            default: insertAndReplace({ unicode: '🍣', sources: [':sushi'], description: ':sushi' }),
            readonly: true,
            required: true,
        }),
        '🍙': one('Emoji', {
            default: insertAndReplace({ unicode: '🍙', sources: [':rice_ball'], description: ':rice_ball' }),
            readonly: true,
            required: true,
        }),
        '🍺': one('Emoji', {
            default: insertAndReplace({ unicode: '🍺', sources: [':beer'], description: ':beer' }),
            readonly: true,
            required: true,
        }),
        '🍷': one('Emoji', {
            default: insertAndReplace({ unicode: '🍷', sources: [':wine'], description: ':wine' }),
            readonly: true,
            required: true,
        }),
        '🍸': one('Emoji', {
            default: insertAndReplace({ unicode: '🍸', sources: [':cocktail'], description: ':cocktail' }),
            readonly: true,
            required: true,
        }),
        '🍹': one('Emoji', {
            default: insertAndReplace({ unicode: '🍹', sources: [':tropical'], description: ':tropical' }),
            readonly: true,
            required: true,
        }),
        '🍻': one('Emoji', {
            default: insertAndReplace({ unicode: '🍻', sources: [':beers'], description: ':beers' }),
            readonly: true,
            required: true,
        }),
        '👻': one('Emoji', {
            default: insertAndReplace({ unicode: '👻', sources: [':ghost'], description: ':ghost' }),
            readonly: true,
            required: true,
        }),
        '💀': one('Emoji', {
            default: insertAndReplace({ unicode: '💀', sources: [':skull'], description: ':skull' }),
            readonly: true,
            required: true,
        }),
        '👽': one('Emoji', {
            default: insertAndReplace({ unicode: '👽', sources: [':et', ':alien'], description: ':et' }),
            readonly: true,
            required: true,
        }),
        '🎉': one('Emoji', {
            default: insertAndReplace({ unicode: '🎉', sources: [':party'], description: ':party' }),
            readonly: true,
            required: true,
        }),
        '🏆': one('Emoji', {
            default: insertAndReplace({ unicode: '🏆', sources: [':trophy'], description: ':trophy' }),
            readonly: true,
            required: true,
        }),
        '🔑': one('Emoji', {
            default: insertAndReplace({ unicode: '🔑', sources: [':key'], description: ':key' }),
            readonly: true,
            required: true,
        }),
        '📌': one('Emoji', {
            default: insertAndReplace({ unicode: '📌', sources: [':pin'], description: ':pin' }),
            readonly: true,
            required: true,
        }),
        '📯': one('Emoji', {
            default: insertAndReplace({ unicode: '📯', sources: [':postal_horn'], description: ':postal_horn' }),
            readonly: true,
            required: true,
        }),
        '🎵': one('Emoji', {
            default: insertAndReplace({ unicode: '🎵', sources: [':music'], description: ':music' }),
            readonly: true,
            required: true,
        }),
        '🎺': one('Emoji', {
            default: insertAndReplace({ unicode: '🎺', sources: [':trumpet'], description: ':trumpet' }),
            readonly: true,
            required: true,
        }),
        '🎸': one('Emoji', {
            default: insertAndReplace({ unicode: '🎸', sources: [':guitar'], description: ':guitar' }),
            readonly: true,
            required: true,
        }),
        '🏃': one('Emoji', {
            default: insertAndReplace({ unicode: '🏃', sources: [':run'], description: ':run' }),
            readonly: true,
            required: true,
        }),
        '🚲': one('Emoji', {
            default: insertAndReplace({ unicode: '🚲', sources: [':bike'], description: ':bike' }),
            readonly: true,
            required: true,
        }),
        '⚽️': one('Emoji', {
            default: insertAndReplace({ unicode: '⚽️', sources: [':soccer'], description: ':soccer' }),
            readonly: true,
            required: true,
        }),
        '🏈': one('Emoji', {
            default: insertAndReplace({ unicode: '🏈', sources: [':football'], description: ':football' }),
            readonly: true,
            required: true,
        }),
        '🎱': one('Emoji', {
            default: insertAndReplace({ unicode: '🎱', sources: [':8ball'], description: ':8ball' }),
            readonly: true,
            required: true,
        }),
        '🎬': one('Emoji', {
            default: insertAndReplace({ unicode: '🎬', sources: [':clapper'], description: ':clapper' }),
            readonly: true,
            required: true,
        }),
        '🎤': one('Emoji', {
            default: insertAndReplace({ unicode: '🎤', sources: [':microphone'], description: ':microphone' }),
            readonly: true,
            required: true,
        }),
        '🧀': one('Emoji', {
            default: insertAndReplace({ unicode: '🧀', sources: [':cheese'], description: ':cheese' }),
            readonly: true,
            required: true,
        }),
    }
});
