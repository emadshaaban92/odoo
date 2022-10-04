/** @odoo-module **/

import { registerModel } from '@mail/model/model_core';
import { attr, one } from '@mail/model/model_field';
import { clear, increment } from '@mail/model/model_field_command';

import { qweb } from 'web.core';
import { Markup } from 'web.utils';

registerModel({
    name: 'Chatbot',
    recordMethods: {
        /**
         * Add message posted by the bot into the conversation.
         * This allows not having to wait for the bus (since we run checks based on messages in the
         * conversation, having the result be there immediately eases the process).
         *
         * It also helps while running test tours since those don't have the bus enabled.
         */
        addMessage(message, options) {
            message.body = Markup(message.body);
            this.global.PublicLivechatGlobal.livechatButtonView.addMessage(message, options);
            if (this.global.PublicLivechatGlobal.publicLivechat.isFolded || !this.global.PublicLivechatGlobal.chatWindow.publicLivechatView.widget.isAtBottom()) {
                this.global.PublicLivechatGlobal.publicLivechat.update({ unreadCounter: increment() });
            }

            if (!options || !options.skipRenderMessages) {
                this.global.PublicLivechatGlobal.chatWindow.renderMessages();
            }
        },
        /**
         * Once the script ends, adds a visual element at the end of the chat window allowing to restart
         * the whole script.
         */
        endScript() {
            if (
                this.currentStep &&
                this.currentStep.data &&
                this.currentStep.data.conversation_closed
            ) {
                // don't touch anything if the user has closed the conversation, let the chat window
                // handle the display
                return;
            }
            this.global.PublicLivechatGlobal.chatWindow.widget.$('.o_composer_text_field').addClass('d-none');
            this.global.PublicLivechatGlobal.chatWindow.widget.$('.o_livechat_chatbot_end').show();
            this.global.PublicLivechatGlobal.chatWindow.widget.$('.o_livechat_chatbot_restart').one('click', this.global.PublicLivechatGlobal.livechatButtonView.onChatbotRestartScript);
        },
        onKeydownInput() {
            if (
                this.currentStep &&
                this.currentStep.data &&
                this.currentStep.data.chatbot_step_type === 'free_input_multi'
            ) {
                this.debouncedAwaitUserInput();
            }
        },
        /**
         * When the user first interacts with the bot, we want to make sure to actually post the welcome
         * messages into the conversation.
         *
         * Indeed, before that, they are 'virtual' messages that are not tied to mail.messages, see
         * #_sendWelcomeChatbotMessage() for more information.
         *
         * Posting them as real messages allows to have a cleaner model and conversation, that will be
         * kept intact when changing page on the website.
         *
         * It also allows tying any first response / question_selection choice to a chatbot.message
         * that has a linked mail.message.
         */
        async postWelcomeMessages() {
            const welcomeMessages = this.global.PublicLivechatGlobal.welcomeMessages;

            if (welcomeMessages.length === 0) {
                // we already posted the welcome messages, nothing to do
                return;
            }

            const postedWelcomeMessages = await this.global.Messaging.rpc({
                route: '/chatbot/post_welcome_steps',
                params: {
                    channel_uuid: this.global.PublicLivechatGlobal.publicLivechat.uuid,
                    chatbot_script_id: this.scriptId,
                },
            });

            const welcomeMessagesIds = welcomeMessages.map(welcomeMessage => welcomeMessage.id);
            this.global.PublicLivechatGlobal.update({
                messages: this.global.PublicLivechatGlobal.messages.filter((message) => {
                    !welcomeMessagesIds.includes(message.id);
                }),
            });

            postedWelcomeMessages.reverse();
            postedWelcomeMessages.forEach((message) => {
                this.addMessage(message, {
                    prepend: true,
                    skipRenderMessages: true,
                });
            });

            this.global.PublicLivechatGlobal.chatWindow.renderMessages();
        },
        /**
         * Processes the step, depending on the current state of the script and the author of the last
         * message that was typed into the conversation.
         *
         * This is a rather complicated process since we have many potential states to handle.
         * Here are the detailed possible outcomes:
         *
         * - Check if the script is finished, and if so end it.
         *
         * - If a human operator has taken over the conversation
         *   -> enable the input and let the operator handle the visitor.
         *
         * - If the received step is of type expecting an input from the user
         *   - the last message if from the user (he has already answered)
         *     -> trigger the next step
         *   - otherwise
         *     -> enable the input and let the user type
         *
         * - Otherwise
         *   - if the the step is of type 'question_selection' and we are still waiting for the user to
         *     select one of the options
         *     -> don't do anything, wait for the user to click one of the options
         *   - otherwise
         *     -> trigger the next step
         */
        processStep() {
            if (this.shouldEndScript) {
                this.endScript();
            } else if (
                this.currentStep.data.chatbot_step_type === 'forward_operator' &&
                this.currentStep.data.chatbot_operator_found
            ) {
                this.global.PublicLivechatGlobal.chatWindow.enableInput();
            } else if (this.isExpectingUserInput) {
                if (this.global.PublicLivechatGlobal.isLastMessageFromCustomer) {
                    // user has already typed a message in -> trigger next step
                    this.setIsTyping();
                    this.update({
                        nextStepTimeout: setTimeout(
                            this.triggerNextStep,
                            this.messageDelay,
                        ),
                    });
                } else {
                    this.global.PublicLivechatGlobal.chatWindow.enableInput();
                }
            } else {
                let triggerNextStep = true;
                if (this.currentStep.data.chatbot_step_type === 'question_selection') {
                    if (!this.global.PublicLivechatGlobal.isLastMessageFromCustomer) {
                        // if there is no last message or if the last message is from the bot
                        // -> don't trigger the next step, we are waiting for the user to pick an option
                        triggerNextStep = false;
                    }
                }

                if (triggerNextStep) {
                    let nextStepDelay = this.messageDelay;
                    if (this.global.PublicLivechatGlobal.chatWindow.widget.$('.o_livechat_chatbot_typing').length !== 0) {
                        // special case where we already have a "is typing" message displayed
                        // can happen when the previous step did not trigger any message posted from the bot
                        // e.g: previous step was "forward_operator" and no-one is available
                        // -> in that case, don't wait and trigger the next step immediately
                        nextStepDelay = 0;
                    } else {
                        this.setIsTyping();
                    }

                    this.update({
                        nextStepTimeout: setTimeout(
                            this.triggerNextStep,
                            nextStepDelay,
                        ),
                    });
                }
            }

            if (!this.hasRestartButton) {
                this.global.PublicLivechatGlobal.chatWindow.widget.$('.o_livechat_chatbot_main_restart').addClass('d-none');
            }
        },
        /**
         * See 'Chatbot/saveSession'.
         *
         * We retrieve the livechat uuid from the session cookie since the livechat Widget is not yet
         * initialized when we restore the chatbot state.
         *
         * We also clear any older keys that store a previously saved chatbot session.
         * (In that case we clear the actual browser's local storage, we don't use the localStorage
         * object as it does not allow browsing existing keys, see 'local_storage.js'.)
         */
        restoreSession() {
            const browserLocalStorage = window.localStorage;
            if (browserLocalStorage && browserLocalStorage.length) {
                for (let i = 0; i < browserLocalStorage.length; i++) {
                    const key = browserLocalStorage.key(i);
                    if (key.startsWith('im_livechat.chatbot.state.uuid_') && key !== this.sessionCookieKey) {
                        browserLocalStorage.removeItem(key);
                    }
                }
            }
            const chatbotState = localStorage.getItem(this.sessionCookieKey);
            if (chatbotState) {
                this.update({ currentStep: { data: this.localStorageState._chatbotCurrentStep } });
            }
        },
        /**
         * Register current chatbot step state into localStorage to be able to resume if the visitor
         * goes to another website page or if he refreshes his page.
         *
         * (Will not work if the visitor switches browser but his livechat session will not be restored
         *  anyway in that case, since it's stored into a cookie).
         */
        saveSession() {
            localStorage.setItem('im_livechat.chatbot.state.uuid_' + this.global.PublicLivechatGlobal.publicLivechat.uuid, JSON.stringify({
                '_chatbot': this.data,
                '_chatbotCurrentStep': this.currentStep.data,
            }));
        },
        /**
         * Adds a small "is typing" animation into the chat window.
         *
         * @param {boolean} [isWelcomeMessage=false]
         */
        setIsTyping(isWelcomeMessage = false) {
            if (this.global.PublicLivechatGlobal.livechatButtonView.isTypingTimeout) {
                clearTimeout(this.global.PublicLivechatGlobal.livechatButtonView.isTypingTimeout);
            }
            this.global.PublicLivechatGlobal.chatWindow.disableInput('');
            this.global.PublicLivechatGlobal.livechatButtonView.update({
                isTypingTimeout: setTimeout(
                    () => {
                        this.global.PublicLivechatGlobal.chatWindow.widget.$('.o_mail_thread_content').append(
                            $(qweb.render('im_livechat.legacy.chatbot.is_typing_message', {
                                'chatbotImageSrc': `/im_livechat/operator/${
                                    this.global.PublicLivechatGlobal.publicLivechat.operator.id
                                }/avatar`,
                                'chatbotName': this.name,
                                'isWelcomeMessage': isWelcomeMessage,
                            }))
                        );
                        this.global.PublicLivechatGlobal.chatWindow.publicLivechatView.widget.scrollToBottom();
                    },
                    this.messageDelay / 3,
                ),
            });
        },
        /**
         * Triggers the next step of the script by calling the associated route.
         * This will receive the next step and call step processing.
         */
        async triggerNextStep() {
            let triggerNextStep = true;
            if (
                this.currentStep &&
                this.currentStep.data &&
                this.currentStep.data.chatbot_step_type === 'question_email'
            ) {
                triggerNextStep = await this.validateEmail();
            }

            if (!triggerNextStep) {
                return;
            }

            const nextStep = await this.global.Messaging.rpc({
                route: '/chatbot/step/trigger',
                params: {
                    channel_uuid: this.global.PublicLivechatGlobal.publicLivechat.uuid,
                    chatbot_script_id: this.scriptId,
                },
            });

            if (nextStep) {
                if (nextStep.chatbot_posted_message) {
                    this.addMessage(nextStep.chatbot_posted_message);
                }

                this.update({ currentStep: { data: nextStep.chatbot_step } });

                this.processStep();
            } else {
                // did not find next step -> end the script
                this.currentStep.data.chatbot_step_is_last = true;
                this.global.PublicLivechatGlobal.chatWindow.renderMessages();
                this.endScript();
            }

            this.saveSession();

            return nextStep;
        },
        /**
         * A special case is handled for email steps, where we first validate the email (server side)
         * and we allow the user to try again in case the format is incorrect.
         *
         * The validation is made server-side to have the same test when we validate here and when we
         * register the answer, but also to easily post a message as the bot ("Sorry, try again...").
         *
         * Returns a boolean stating whether the email was valid or not.
         */
        async validateEmail() {
            let emailValidResult = await this.global.Messaging.rpc({
                route: '/chatbot/step/validate_email',
                params: { channel_uuid: this.global.PublicLivechatGlobal.publicLivechat.uuid },
            });

            if (emailValidResult.success) {
                this.currentStep.data.is_email_valid = true;
                this.saveSession();

                return true;
            } else {
                // email is not valid, let the user try again
                this.global.PublicLivechatGlobal.chatWindow.enableInput();
                if (emailValidResult.posted_message) {
                    this.addMessage(emailValidResult.posted_message);
                }

                return false;
            }
        },
        /**
         * This method will be transformed into a 'debounced' version (see init).
         *
         * The purpose is to handle steps of type 'free_input_multi', that will let the user type in
         * multiple lines of text before the bot goes to the next step.
         *
         * Every time a 'keydown' is detected into the input, or every time a message is sent, we call
         * this debounced method, which will give the user about 10 seconds to type more text before
         * the next step is triggered.
         *
         * First we check if the last message was sent by the user, to make sure we always let him type
         * at least one message before moving on.
         */
        awaitUserInput() {
            if (this.global.PublicLivechatGlobal.isLastMessageFromCustomer) {
                if (this.shouldEndScript) {
                    this.endScript();
                } else {
                    this.setIsTyping();
                    this.update({
                        nextStepTimeout: setTimeout(
                            this.triggerNextStep,
                            this.messageDelay,
                        )
                    });
                }
            }
        },
    },
    fields: {
        awaitUserInputDebounceTime: attr({
            compute() {
                return 10000;
            },
        }),
        data: attr({
            compute() {
                if (this.global.PublicLivechatGlobal.isTestChatbot) {
                    return this.global.PublicLivechatGlobal.testChatbotData.chatbot;
                }
                if (this.state === 'init') {
                    return this.global.PublicLivechatGlobal.rule.chatbot;
                }
                if (this.state === 'welcome') {
                    return this.global.PublicLivechatGlobal.livechatInit.rule.chatbot;
                }
                if (
                    this.state === 'restore_session' &&
                    this.localStorageState
                ) {
                    return this.localStorageState._chatbot;
                }
                return clear();
            },
        }),
        currentStep: one('ChatbotStep', {
            inverse: 'chabotOwner',
        }),
        debouncedAwaitUserInput: attr({
            compute() {
                // debounced to let the user type several sentences, see 'Chatbot/awaitUserInput' for details
                return _.debounce(
                    this.awaitUserInput,
                    this.awaitUserInputDebounceTime,
                );
            },
        }),
        hasRestartButton: attr({
            /**
             * Will display a "Restart script" button in the conversation toolbar.
             *
             * Side-case: if the conversation has been forwarded to a human operator, we don't want to
             * display that restart button.
             */
            compute() {
                return Boolean(
                    !this.currentStep ||
                    (
                        this.currentStep.data.chatbot_step_type !== 'forward_operator' ||
                        !this.currentStep.data.chatbot_operator_found
                    )
                );
            },
            default: false,
        }),
        isActive: attr({
            compute() {
                if (this.global.PublicLivechatGlobal.isTestChatbot) {
                    return true;
                }
                if (this.global.PublicLivechatGlobal.rule && this.global.PublicLivechatGlobal.rule.chatbot) {
                    return true;
                }
                if (this.global.PublicLivechatGlobal.livechatInit && this.global.PublicLivechatGlobal.livechatInit.rule.chatbot) {
                    return true;
                }
                if (this.state === 'welcome') {
                    return true;
                }
                if (this.localStorageState) {
                    return true;
                }
                return clear();
            },
            default: false,
        }),
        isExpectingUserInput: attr({
            compute() {
                if (!this.currentStep) {
                    return clear();
                }
                return [
                    'question_phone',
                    'question_email',
                    'free_input_single',
                    'free_input_multi',
                ].includes(this.currentStep.data.chatbot_step_type);
            },
            default: false,
        }),
        isRedirecting: attr({
            default: false,
        }),
        lastWelcomeStep: attr({
            compute() {
                if (!this.welcomeSteps) {
                    return clear();
                }
                return this.welcomeSteps[this.welcomeSteps.length - 1];
            },
        }),
        localStorageState: attr({
            compute() {
                if (!this.global.PublicLivechatGlobal.sessionCookie) {
                    return clear();
                }
                const data = localStorage.getItem(this.sessionCookieKey);
                if (!data) {
                    return clear();
                }
                return JSON.parse(data);
            },
        }),
        name: attr({
            compute() {
                if (!this.data) {
                    return clear();
                }
                return this.data.name;
            },
        }),
        nextStepTimeout: attr(),
        messageDelay: attr({
            compute() {
                return clear();
            },
            default: 3500, // in milliseconds
        }),
        publicLivechatGlobalOwner: one('PublicLivechatGlobal', {
            identifying: true,
            inverse: 'chatbot',
        }),
        scriptId: attr({
            compute() {
                if (!this.data) {
                    return clear();
                }
                return this.data.chatbot_script_id;
            },
        }),
        serverUrl: attr(),
        sessionCookieKey: attr({
            compute() {
                if (!this.global.PublicLivechatGlobal.sessionCookie) {
                    return clear();
                }
                return 'im_livechat.chatbot.state.uuid_' + JSON.parse(this.global.PublicLivechatGlobal.sessionCookie).uuid;
            },
        }),
        shouldEndScript: attr({
            /**
             * Compute method that checks if the script should be ended or not.
             * If the user has closed the conversation -> script has ended.
             *
             * Otherwise, there are 2 use cases where we want to end the script:
             *
             * If the current step is the last one AND the conversation was not taken over by a human operator
             *   1. AND we expect a user input (or we are on a selection)
             *       AND the user has already answered
             *   2. AND we don't expect a user input
             */
            compute() {
                if (!this.currentStep) {
                    return clear();
                }
                if (this.currentStep.data.conversation_closed) {
                    return true;
                }
                if (this.currentStep.data.chatbot_step_is_last &&
                    (this.currentStep.data.chatbot_step_type !== 'forward_operator' ||
                    !this.currentStep.data.chatbot_operator_found)
                ) {
                    if (this.currentStep.data.chatbot_step_type === 'question_email'
                        && !this.currentStep.data.is_email_valid
                    ) {
                        // email is not (yet) valid, let the user answer / try again
                        return false;
                    } else if (
                        (this.isExpectingUserInput ||
                        this.currentStep.data.chatbot_step_type === 'question_selection') &&
                        this.global.PublicLivechatGlobal.messages.length !== 0
                    ) {
                        if (this.global.PublicLivechatGlobal.lastMessage.authorId !== this.global.PublicLivechatGlobal.publicLivechat.operator.id) {
                            // we are on the last step of the script, expect a user input and the user has
                            // already answered
                            // -> end the script
                            return true;
                        }
                    } else if (!this.isExpectingUserInput) {
                        // we are on the last step of the script and we do not expect a user input
                        // -> end the script
                        return true;
                    }
                }
                return false;
            },
            default: false,
        }),
        state: attr({
            compute() {
                if (this.global.PublicLivechatGlobal.rule && !!this.global.PublicLivechatGlobal.rule.chatbot) {
                    return 'init';
                }
                if (this.global.PublicLivechatGlobal.livechatInit && this.global.PublicLivechatGlobal.livechatInit.rule.chatbot) {
                    return 'welcome';
                }
                if (
                    !this.global.PublicLivechatGlobal.rule &&
                    this.global.PublicLivechatGlobal.history !== null &&
                    this.global.PublicLivechatGlobal.history.length !== 0 &&
                    this.sessionCookieKey &&
                    localStorage.getItem(this.sessionCookieKey)
                ) {
                    return 'restore_session';
                }
                return clear();
            },
        }),
        welcomeMessageTimeout: attr(),
        welcomeSteps: attr({
            compute() {
                if (!this.data) {
                    return clear();
                }
                return this.data.chatbot_welcome_steps;
            },
        }),
    },
});
