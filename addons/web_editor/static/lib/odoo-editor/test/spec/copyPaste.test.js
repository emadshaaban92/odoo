import {
    BasicEditor, customErrorMessage,
    testEditor
} from "../utils.js";

navigator.permissions.query({ name: "clipboard-write" }).then((result) => {
    if (result.state === "granted" || result.state === "prompt") {
        console.log("clipboard Write ok");
    } else {
        console.warn("clipboard Write Access bloqued !");
    }
});

const pasteData = async function (editor, text, type) {
    var fakeEvent = {
        dataType: 'text/plain',
        data: text,
        clipboardData: {
            getData: (datatype) => type === datatype ? text : null,
        },
        preventDefault: () => {},
    };
    await editor._onPaste(fakeEvent);
};

const pasteText = async (editor, text) => pasteData(editor, text, 'text/plain');
const pasteHtml = async (editor, html) => pasteData(editor, html, 'text/html');

describe('Copy and paste', () => {
    describe('Simple text', () => {
        describe('range collapsed', async () => {
            it('should paste a text in a p', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<p>ab[]cd</p>',
                    stepFunction: async editor => {
                        await pasteText(editor, 'x');
                    },
                    contentAfter: '<p>abx[]cd</p>',
                });
                await testEditor(BasicEditor, {
                    contentBefore: '<p>ab[]cd</p>',
                    stepFunction: async editor => {
                        await pasteText(editor, 'xyz 123');
                    },
                    contentAfter: '<p>abxyz 123[]cd</p>',
                });
                await testEditor(BasicEditor, {
                    contentBefore: '<p>ab[]cd</p>',
                    stepFunction: async editor => {
                        await pasteText(editor, 'x    y');
                    },
                    contentAfter: '<p>abx    y[]cd</p>',
                });
            });
            it('should paste a text in a span', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<p>a<span>b[]c</span>d</p>',
                    stepFunction: async editor => {
                        await pasteText(editor, 'x');
                    },
                    contentAfter: '<p>a<span>bx[]c</span>d</p>',
                });
            });
        });
        describe('range not collapsed', async () => {
            it('should paste a text in a p', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<p>a[bc]d</p>',
                    stepFunction: async editor => {
                        await pasteText(editor, 'x');
                    },
                    contentAfter: '<p>ax[]d</p>',
                });
                await testEditor(BasicEditor, {
                    contentBefore: '<p>a[bc]d</p>',
                    stepFunction: async editor => {
                        await pasteText(editor, 'xyz 123');
                    },
                    contentAfter: '<p>axyz 123[]d</p>',
                });
                await testEditor(BasicEditor, {
                    contentBefore: '<p>a[bc]d</p>',
                    stepFunction: async editor => {
                        await pasteText(editor, 'x    y');
                    },
                    contentAfter: '<p>ax    y[]d</p>',
                });
            });
            it('should paste a text in a span', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<p>a<span>b[cd]e</span>f</p>',
                    stepFunction: async editor => {
                        await pasteText(editor, 'x');
                    },
                    contentAfter: '<p>a<span>bx[]e</span>f</p>',
                });
            });
            it('should paste a text when selection across two span', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<p>a<span>b[c</span><span>d]e</span>f</p>',
                    stepFunction: async editor => {
                        await pasteText(editor, 'x');
                    },
                    contentAfter: '<p>a<span>bx[]e</span>f</p>',
                });
                await testEditor(BasicEditor, {
                    contentBefore: '<p>a<span>b[c</span>- -<span>d]e</span>f</p>',
                    stepFunction: async editor => {
                        await pasteText(editor, 'y');
                    },
                    contentAfter: '<p>a<span>by[]e</span>f</p>',
                });
            });
            it('should paste a text when selection across two p', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<div>a<p>b[c</p><p>d]e</p>f</div>',
                    stepFunction: async editor => {
                        await pasteText(editor, 'x');
                    },
                    contentAfter: '<div>a<p>bx[]e</p>f</div>',
                });
                await testEditor(BasicEditor, {
                    contentBefore: '<div>a<p>b[c</p>- -<p>d]e</p>f</div>',
                    stepFunction: async editor => {
                        await pasteText(editor, 'y');
                    },
                    contentAfter: '<div>a<p>by[]e</p>f</div>',
                });
            });
            it('should paste a text when selection leave a span', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<div>ab<span>c[d</span>e]f</div>',
                    stepFunction: async editor => {
                        await pasteText(editor, 'x');
                    },
                    contentAfter: '<div>ab<span>cx[]</span>f</div>',
                });
                await testEditor(BasicEditor, {
                    contentBefore: '<div>a[b<span>c]d</span>ef</div>',
                    stepFunction: async editor => {
                        await pasteText(editor, 'y');
                    },
                    contentAfter: '<div>ay[]<span>d</span>ef</div>',
                });
            });
            it('should paste a text when selection across two element', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<div>1a<p>b[c</p><span>d]e</span>f</div>',
                    stepFunction: async editor => {
                        await pasteText(editor, 'x');
                    },
                    contentAfter: '<div>1a<p>bx[]<span>e</span>f</p></div>',
                });
                await testEditor(BasicEditor, {
                    contentBefore: '<div>2a<span>b[c</span><p>d]e</p>f</div>',
                    stepFunction: async editor => {
                        await pasteText(editor, 'x');
                    },
                    contentAfter: '<div>2a<span>bx[]</span>e<br>f</div>',
                });
            });
        });
    });
    describe('Simple html', () => {
        const simpleHtmlCharX = '<span style="color: rgb(33, 37, 41); font-family: -apple-system, BlinkMacSystemFont, &quot;Segoe UI&quot;, Roboto, &quot;Helvetica Neue&quot;, Arial, &quot;Noto Sans&quot;, sans-serif, &quot;Apple Color Emoji&quot;, &quot;Segoe UI Emoji&quot;, &quot;Segoe UI Symbol&quot;, &quot;Noto Color Emoji&quot;; font-size: 16px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; white-space: normal; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; display: inline !important; float: none;">x</span>';
        describe('range collapsed', async () => {
            it('should paste a text in a p', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<p>ab[]cd</p>',
                    stepFunction: async editor => {
                        await pasteHtml(editor, simpleHtmlCharX);
                    },
                    contentAfter: '<p>abx[]cd</p>',
                });
            });
            it('should paste a text in a span', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<p>a<span>b[]c</span>d</p>',
                    stepFunction: async editor => {
                        await pasteHtml(editor, simpleHtmlCharX);
                    },
                    contentAfter: '<p>a<span>bx[]c</span>d</p>',
                });
            });
        });
        describe('range not collapsed', async () => {
            it('should paste a text in a p', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<p>a[bc]d</p>',
                    stepFunction: async editor => {
                        await pasteHtml(editor, simpleHtmlCharX);
                    },
                    contentAfter: '<p>ax[]d</p>',
                });
            });
            it('should paste a text in a span', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<p>a<span>b[cd]e</span>f</p>',
                    stepFunction: async editor => {
                        await pasteHtml(editor, simpleHtmlCharX);
                    },
                    contentAfter: '<p>a<span>bx[]e</span>f</p>',
                });
            });
            it('should paste a text when selection across two span', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<p>a<span>b[c</span><span>d]e</span>f</p>',
                    stepFunction: async editor => {
                        await pasteHtml(editor, simpleHtmlCharX);
                    },
                    contentAfter: '<p>a<span>bx[]e</span>f</p>',
                });
                await testEditor(BasicEditor, {
                    contentBefore: '<p>a<span>b[c</span>- -<span>d]e</span>f</p>',
                    stepFunction: async editor => {
                        await pasteHtml(editor, simpleHtmlCharX);
                    },
                    contentAfter: '<p>a<span>bx[]e</span>f</p>',
                });
            });
            it('should paste a text when selection across two p', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<div>1a<p>b[c</p><p>d]e</p>f</div>',
                    stepFunction: async editor => {
                        await pasteHtml(editor, simpleHtmlCharX);
                    },
                    contentAfter: '<div>1a<p>bx[]e</p>f</div>',
                });
                await testEditor(BasicEditor, {
                    contentBefore: '<div>2a<p>b[c</p>- -<p>d]e</p>f</div>',
                    stepFunction: async editor => {
                        await pasteHtml(editor, simpleHtmlCharX);
                    },
                    contentAfter: '<div>2a<p>bx[]e</p>f</div>',
                });
            });
            it('should paste a text when selection leave a span', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<div>ab<span>c[d</span>e]f</div>',
                    stepFunction: async editor => {
                        await pasteHtml(editor, simpleHtmlCharX);
                    },
                    contentAfter: '<div>ab<span>cx[]</span>f</div>',
                });
                await testEditor(BasicEditor, {
                    contentBefore: '<div>a[b<span>c]d</span>ef</div>',
                    stepFunction: async editor => {
                        await pasteHtml(editor, simpleHtmlCharX);
                    },
                    contentAfter: '<div>ax[]<span>d</span>ef</div>',
                });
            });
            it('should paste a text when selection across two element', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<div>1a<p>b[c</p><span>d]e</span>f</div>',
                    stepFunction: async editor => {
                        await pasteHtml(editor, simpleHtmlCharX);
                    },
                    contentAfter: '<div>1a<p>bx[]<span>e</span>f</p></div>',
                });
                await testEditor(BasicEditor, {
                    contentBefore: '<div>2a<span>b[c</span><p>d]e</p>f</div>',
                    stepFunction: async editor => {
                        await pasteHtml(editor, simpleHtmlCharX);
                    },
                    contentAfter: '<div>2a<span>bx[]</span>e<br>f</div>',
                });
                await testEditor(BasicEditor, {
                    contentBefore: '<div>3a<p>b[c</p><p>d]e</p>f</div>',
                    stepFunction: async editor => {
                        await pasteHtml(editor, simpleHtmlCharX);
                    },
                    contentAfter: '<div>3a<p>bx[]e</p>f</div>',
                });
            });
        });
    });
    describe('Complex html span', () => {
        const complexHtmlData = '<span style="color: rgb(33, 37, 41); font-family: -apple-system, BlinkMacSystemFont, &quot;Segoe UI&quot;, Roboto, &quot;Helvetica Neue&quot;, Arial, &quot;Noto Sans&quot;, sans-serif, &quot;Apple Color Emoji&quot;, &quot;Segoe UI Emoji&quot;, &quot;Segoe UI Symbol&quot;, &quot;Noto Color Emoji&quot;; font-size: 16px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; white-space: normal; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; display: inline !important; float: none;">1</span><b style="box-sizing: border-box; font-weight: bolder; color: rgb(33, 37, 41); font-family: -apple-system, BlinkMacSystemFont, &quot;Segoe UI&quot;, Roboto, &quot;Helvetica Neue&quot;, Arial, &quot;Noto Sans&quot;, sans-serif, &quot;Apple Color Emoji&quot;, &quot;Segoe UI Emoji&quot;, &quot;Segoe UI Symbol&quot;, &quot;Noto Color Emoji&quot;; font-size: 16px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; white-space: normal; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;">23</b><span style="color: rgb(33, 37, 41); font-family: -apple-system, BlinkMacSystemFont, &quot;Segoe UI&quot;, Roboto, &quot;Helvetica Neue&quot;, Arial, &quot;Noto Sans&quot;, sans-serif, &quot;Apple Color Emoji&quot;, &quot;Segoe UI Emoji&quot;, &quot;Segoe UI Symbol&quot;, &quot;Noto Color Emoji&quot;; font-size: 16px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; white-space: normal; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; display: inline !important; float: none;"><span> </span>4</span>';
        describe('range collapsed', async () => {
            it('should paste a text in a p', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<p>ab[]cd</p>',
                    stepFunction: async editor => {
                        await pasteHtml(editor, complexHtmlData);
                    },
                    contentAfter: '<p>ab1<b>23</b>&nbsp;4[]cd</p>',
                });
            });
            it('should paste a text in a span', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<p>a<span>b[]c</span>d</p>',
                    stepFunction: async editor => {
                        await pasteHtml(editor, complexHtmlData);
                    },
                    contentAfter: '<p>a<span>b1<b>23</b>&nbsp;4[]c</span>d</p>',
                });
            });
        });
        describe('range not collapsed', async () => {
            it('should paste a text in a p', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<p>a[bc]d</p>',
                    stepFunction: async editor => {
                        await pasteHtml(editor, complexHtmlData);
                    },
                    contentAfter: '<p>a1<b>23</b>&nbsp;4[]d</p>',
                });
            });
            it('should paste a text in a span', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<p>a<span>b[cd]e</span>f</p>',
                    stepFunction: async editor => {
                        await pasteHtml(editor, complexHtmlData);
                    },
                    contentAfter: '<p>a<span>b1<b>23</b>&nbsp;4[]e</span>f</p>',
                });
            });
            it('should paste a text when selection across two span', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<p>a<span>b[c</span><span>d]e</span>f</p>',
                    stepFunction: async editor => {
                        await pasteHtml(editor, complexHtmlData);
                    },
                    contentAfter: '<p>a<span>b1<b>23</b>&nbsp;4[]e</span>f</p>',
                });
                await testEditor(BasicEditor, {
                    contentBefore: '<p>a<span>b[c</span>- -<span>d]e</span>f</p>',
                    stepFunction: async editor => {
                        await pasteHtml(editor, complexHtmlData);
                    },
                    contentAfter: '<p>a<span>b1<b>23</b>&nbsp;4[]e</span>f</p>',
                });
            });
            it('should paste a text when selection across two p', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<div>a<p>b[c</p><p>d]e</p>f</div>',
                    stepFunction: async editor => {
                        await pasteHtml(editor, complexHtmlData);
                    },
                    contentAfter: '<div>a<p>b1<b>23</b>&nbsp;4[]e</p>f</div>',
                });
                await testEditor(BasicEditor, {
                    contentBefore: '<div>a<p>b[c</p>- -<p>d]e</p>f</div>',
                    stepFunction: async editor => {
                        await pasteHtml(editor, complexHtmlData);
                    },
                    contentAfter: '<div>a<p>b1<b>23</b>&nbsp;4[]e</p>f</div>',
                });
            });
            it('should paste a text when selection leave a span', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<div>ab<span>c[d</span>e]f</div>',
                    stepFunction: async editor => {
                        await pasteHtml(editor, complexHtmlData);
                    },
                    contentAfter: '<div>ab<span>c1<b>23</b>&nbsp;4[]</span>f</div>',
                });
                await testEditor(BasicEditor, {
                    contentBefore: '<div>a[b<span>c]d</span>ef</div>',
                    stepFunction: async editor => {
                        await pasteHtml(editor, complexHtmlData);
                    },
                    contentAfter: '<div>a1<b>23</b>&nbsp;4[]<span>d</span>ef</div>',
                });
            });
            it('should paste a text when selection across two element', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<div>1a<p>b[c</p><span>d]e</span>f</div>',
                    stepFunction: async editor => {
                        await pasteHtml(editor, complexHtmlData);
                    },
                    contentAfter: '<div>1a<p>b1<b>23</b>&nbsp;4[]<span>e</span>f</p></div>',
                });
                await testEditor(BasicEditor, {
                    contentBefore: '<div>2a<span>b[c</span><p>d]e</p>f</div>',
                    stepFunction: async editor => {
                        await pasteHtml(editor, complexHtmlData);
                    },
                    contentAfter: '<div>2a<span>b1<b>23</b>&nbsp;4[]</span>e<br>f</div>',
                });
                await testEditor(BasicEditor, {
                    contentBefore: '<div>3a<p>b[c</p><p>d]e</p>f</div>',
                    stepFunction: async editor => {
                        await pasteHtml(editor, complexHtmlData);
                    },
                    contentAfter: '<div>3a<p>b1<b>23</b>&nbsp;4[]e</p>f</div>',
                });
            });
        });
    });
    describe('Complex html p', () => {
        const complexHtmlData = '<p style="box-sizing: border-box; margin-top: 0px; margin-bottom: 1rem; color: rgb(33, 37, 41); font-family: -apple-system, BlinkMacSystemFont, &quot;Segoe UI&quot;, Roboto, &quot;Helvetica Neue&quot;, Arial, &quot;Noto Sans&quot;, sans-serif, &quot;Apple Color Emoji&quot;, &quot;Segoe UI Emoji&quot;, &quot;Segoe UI Symbol&quot;, &quot;Noto Color Emoji&quot;; font-size: 16px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; white-space: normal; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;">12</p><p style="box-sizing: border-box; margin-top: 0px; margin-bottom: 1rem; color: rgb(33, 37, 41); font-family: -apple-system, BlinkMacSystemFont, &quot;Segoe UI&quot;, Roboto, &quot;Helvetica Neue&quot;, Arial, &quot;Noto Sans&quot;, sans-serif, &quot;Apple Color Emoji&quot;, &quot;Segoe UI Emoji&quot;, &quot;Segoe UI Symbol&quot;, &quot;Noto Color Emoji&quot;; font-size: 16px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; white-space: normal; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;">34</p>';
        describe('range collapsed', async () => {
            it('should paste a text in a p', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<p>ab[]cd</p>',
                    stepFunction: async editor => {
                        await pasteHtml(editor, complexHtmlData);
                    },
                    contentAfter: '<p>ab12</p><p>34[]cd</p>',
                });
            });
            it('should paste a text in a span', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<p>a<span>b[]c</span>d</p>',
                    stepFunction: async editor => {
                        await pasteHtml(editor, complexHtmlData);
                    },
                    contentAfter: '<p>a<span>b12</span></p><p>34[]<span>c</span>d</p>',
                });
            });
        });
        describe('range not collapsed', async () => {
            it('should paste a text in a p', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<p>a[bc]d</p>',
                    stepFunction: async editor => {
                        await pasteHtml(editor, complexHtmlData);
                    },
                    contentAfter: '<p>a12</p><p>34[]d</p>',
                });
            });
            it('should paste a text in a span', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<p>a<span>b[cd]e</span>f</p>',
                    stepFunction: async editor => {
                        await pasteHtml(editor, complexHtmlData);
                    },
                    contentAfter: '<p>a<span>b12</span></p><p>34[]<span>e</span>f</p>',
                });
            });
            it('should paste a text when selection across two span (1)', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<p>1a<span>b[c</span><span>d]e</span>f</p>',
                    stepFunction: async editor => {
                        await pasteHtml(editor, complexHtmlData);
                    },
                    contentAfter: '<p>1a<span>b12</span></p><p>34[]<span>e</span>f</p>',
                });
            });
            it('should paste a text when selection across two span (2)', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<p>2a<span>b[c</span>- -<span>d]e</span>f</p>',
                    stepFunction: async editor => {
                        await pasteHtml(editor, complexHtmlData);
                    },
                    contentAfter: '<p>2a<span>b12</span></p><p>34[]<span>e</span>f</p>',
                });
            });
            it('should paste a text when selection across two p', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<div>a<p>b[c</p><p>d]e</p>f</div>',
                    stepFunction: async editor => {
                        await pasteHtml(editor, complexHtmlData);
                    },
                    contentAfter: '<div>a<p>b12</p><p>34[]e</p>f</div>',
                });
                await testEditor(BasicEditor, {
                    contentBefore: '<div>a<p>b[c</p>- -<p>d]e</p>f</div>',
                    stepFunction: async editor => {
                        await pasteHtml(editor, complexHtmlData);
                    },
                    contentAfter: '<div>a<p>b12</p><p>34[]e</p>f</div>',
                });
            });
            it('should paste a text when selection leave a span', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<div>1ab<span>c[d</span>e]f</div>',
                    stepFunction: async editor => {
                        await pasteHtml(editor, complexHtmlData);
                    },
                    contentAfter: '<div>1ab<span>c12<br>34[]</span>f</div>',
                });
                await testEditor(BasicEditor, {
                    contentBefore: '<div>2a[b<span>c]d</span>ef</div>',
                    stepFunction: async editor => {
                        await pasteHtml(editor, complexHtmlData);
                    },
                    contentAfter: '<div>2a12<br>34[]<span>d</span>ef</div>',
                });
            });
            it('should paste a text when selection leave a span (2)', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<p>1ab<span>c[d</span>e]f</p>',
                    stepFunction: async editor => {
                        await pasteHtml(editor, complexHtmlData);
                    },
                    contentAfter: '<p>1ab<span>c12</span></p><p>34[]f</p>',
                });
                await testEditor(BasicEditor, {
                    contentBefore: '<p>2a[b<span>c]d</span>ef</p>',
                    stepFunction: async editor => {
                        await pasteHtml(editor, complexHtmlData);
                    },
                    contentAfter: '<p>2a12</p><p>34[]<span>d</span>ef</p>',
                });
            });
            it('should paste a text when selection across two element (1)', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<div>1a<p>b[c</p><span>d]e</span>f</div>',
                    stepFunction: async editor => {
                        await pasteHtml(editor, complexHtmlData);
                    },
                    contentAfter: '<div>1a<p>b12</p>34[]<span>e</span>f</div>',
                });
            });
            it('should paste a text when selection across two element (2)', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<div>2a<span>b[c</span><p>d]e</p>f</div>',
                    stepFunction: async editor => {
                        await pasteHtml(editor, complexHtmlData);
                    },
                    contentAfter: '<div>2a<span>b1<b>23</b>&nbsp;4[]</span>e<br>f</div>',
                });
            });
        });
    });
    describe('Complex html p+i', () => {
        const complexHtmlData = '<p style="box-sizing: border-box; margin-top: 0px; margin-bottom: 1rem; color: rgb(33, 37, 41); font-family: -apple-system, BlinkMacSystemFont, &quot;Segoe UI&quot;, Roboto, &quot;Helvetica Neue&quot;, Arial, &quot;Noto Sans&quot;, sans-serif, &quot;Apple Color Emoji&quot;, &quot;Segoe UI Emoji&quot;, &quot;Segoe UI Symbol&quot;, &quot;Noto Color Emoji&quot;; font-size: 16px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; white-space: normal; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;">12</p><p style="box-sizing: border-box; margin-top: 0px; margin-bottom: 1rem; color: rgb(33, 37, 41); font-family: -apple-system, BlinkMacSystemFont, &quot;Segoe UI&quot;, Roboto, &quot;Helvetica Neue&quot;, Arial, &quot;Noto Sans&quot;, sans-serif, &quot;Apple Color Emoji&quot;, &quot;Segoe UI Emoji&quot;, &quot;Segoe UI Symbol&quot;, &quot;Noto Color Emoji&quot;; font-size: 16px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; white-space: normal; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;"><i style="box-sizing: border-box;">ii</i></p>';
        describe('range collapsed', async () => {
            it('should paste a text in a p', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<p>ab[]cd</p>',
                    stepFunction: async editor => {
                        await pasteHtml(editor, complexHtmlData);
                    },
                    contentAfter: '<p>ab12</p><p><i>ii[]</i>cd</p>',
                });
            });
            it('should paste a text in a span', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<p>a<span>b[]c</span>d</p>',
                    stepFunction: async editor => {
                        await pasteHtml(editor, complexHtmlData);
                    },
                    contentAfter: '<p>a<span>b12</span></p><p><i>ii[]</i><span>c</span>d</p>',
                });
            });
        });
        describe('range not collapsed', async () => {
            it('should paste a text in a p', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<p>a[bc]d</p>',
                    stepFunction: async editor => {
                        await pasteHtml(editor, complexHtmlData);
                    },
                    contentAfter: '<p>a12</p><p><i>ii[]</i>d</p>',
                });
            });
            it('should paste a text in a span', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<p>a<span>b[cd]e</span>f</p>',
                    stepFunction: async editor => {
                        await pasteHtml(editor, complexHtmlData);
                    },
                    contentAfter: '<p>a<span>b12</span></p><p><i>ii[]</i><span>e</span>f</p>',
                });
            });
            it('should paste a text when selection across two span', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<p>a<span>b[c</span><span>d]e</span>f</p>',
                    stepFunction: async editor => {
                        await pasteHtml(editor, complexHtmlData);
                    },
                    contentAfter: '<p>a<span>b12</span></p><p><i>ii[]</i><span>e</span>f</p>',
                });
                await testEditor(BasicEditor, {
                    contentBefore: '<p>a<span>b[c</span>- -<span>d]e</span>f</p>',
                    stepFunction: async editor => {
                        await pasteHtml(editor, complexHtmlData);
                    },
                    contentAfter: '<p>a<span>b12</span></p><p><i>ii[]</i><span>e</span>f</p>',
                });
            });
            it('should paste a text when selection across two p', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<div>a<p>b[c</p><p>d]e</p>f</div>',
                    stepFunction: async editor => {
                        await pasteHtml(editor, complexHtmlData);
                    },
                    contentAfter: '<div>a<p>b12</p><p><i>ii[]</i>e</p>f</div>',
                });
                await testEditor(BasicEditor, {
                    contentBefore: '<div>a<p>b[c</p>- -<p>d]e</p>f</div>',
                    stepFunction: async editor => {
                        await pasteHtml(editor, complexHtmlData);
                    },
                    contentAfter: '<div>a<p>b12</p><p><i>ii[]</i>e</p>f</div>',
                });
            });
            it('should paste a text when selection leave a span', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<div>ab<span>c[d</span>e]f</div>',
                    stepFunction: async editor => {
                        await pasteHtml(editor, complexHtmlData);
                    },
                    contentAfter: '<div>ab<span>c12</span></p><p><span><i>ii[]</i></span>f</div>',
                });
                await testEditor(BasicEditor, {
                    contentBefore: '<div>a[b<span>c]d</span>ef</div>',
                    stepFunction: async editor => {
                        await pasteHtml(editor, complexHtmlData);
                    },
                    contentAfter: '<div>a12</p><p><i>ii[]</i><span>d</span>ef</div>',
                });
            });
            it('should paste a text when selection across two element', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<div>a<p>b[c</p><span>d]e</span>f</div>',
                    stepFunction: async editor => {
                        await pasteHtml(editor, complexHtmlData);
                    },
                    contentAfter: '<div>a<p>b12</p><p><i>ii[]</i>e</p>f</div>',
                });
                await testEditor(BasicEditor, {
                    contentBefore: '<div>a<span>b[c</span><p>d]e</p>f</div>',
                    stepFunction: async editor => {
                        await pasteHtml(editor, complexHtmlData);
                    },
                    contentAfter: '<div>a<p>b12</span></p><p><span><i>ii[]</i>e</p>f</div>',
                });
            });
        });
    });
    describe('link', () => {
        describe('range collapsed', async () => {
            it('should paste and transform an URL in a p', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<p>ab[]cd</p>',
                    stepFunction: async editor => {
                        await pasteText(editor, 'http://www.xyz.com');
                    },
                    contentAfter: '<p>ab<a href="http://www.xyz.com">http://www.xyz.com</a>[]cd</p>',
                });
            });
            it('should paste and transform an URL in a span', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<p>a<span>b[]c</span>d</p>',
                    stepFunction: async editor => {
                        await pasteText(editor, 'http://www.xyz.com');
                    },
                    contentAfter: '<p>a<span>b<a href="http://www.xyz.com">http://www.xyz.com</a>[]c</span>d</p>',
                });
            });
            it('should paste and not transform an URL in a existing link', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<p>a<a href="http://existing.com">b[]c</a>d</p>',
                    stepFunction: async editor => {
                        await pasteText(editor, 'http://www.xyz.com');
                    },
                    contentAfter: '<p>a<a href="http://existing.com">bhttp://www.xyz.com[]c</a>d</p>',
                });
            });
        });
        describe('range not collapsed', async () => {
            it('should paste and transform an URL in a p', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<p>ab[xxx]cd</p>',
                    stepFunction: async editor => {
                        await pasteText(editor, 'http://www.xyz.com');
                    },
                    contentAfter: '<p>ab<a href="http://www.xyz.com">http://www.xyz.com</a>[]cd</p>',
                });
            });
            it('should paste and transform an URL in a span', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<p>a<span>b[x<a href="http://existing.com">546</a>x]c</span>d</p>',
                    stepFunction: async editor => {
                        await pasteText(editor, 'http://www.xyz.com');
                    },
                    contentAfter: '<p>a<span>b<a href="http://www.xyz.com">http://www.xyz.com</a>[]c</span>d</p>',
                });
            });
            it('should paste and not transform an URL in a existing link', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<p>a<a href="http://existing.com">b[qsdqsd]c</a>d</p>',
                    stepFunction: async editor => {
                        await pasteText(editor, 'http://www.xyz.com');
                    },
                    contentAfter: '<p>a<a href="http://existing.com">bhttp://www.xyz.com[]c</a>d</p>',
                });
            });
        });
    });
    describe('images', () => {
        describe('range collapsed', async () => {
            it('should paste and transform an image URL in a p', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<p>ab[]cd</p>',
                    stepFunction: async editor => {
                        await pasteText(editor, 'https://download.odoocdn.com/icons/website/static/description/icon.png');
                        // Ensure the powerbox is active
                        window.chai.expect(editor.commandBar._active).to.be.true;
                        // Force commandBar validation on the default first choice
                        await editor.commandBar._currentValidate();
                    },
                    contentAfter: '<p>ab<img src="https://download.odoocdn.com/icons/website/static/description/icon.png">[]cd</p>',
                });
            });
            it('should paste and transform an image URL in a span', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<p>a<span>b[]c</span>d</p>',
                    stepFunction: async editor => {
                        await pasteText(editor, 'https://download.odoocdn.com/icons/website/static/description/icon.png');
                        // Ensure the powerbox is active
                        window.chai.expect(editor.commandBar._active).to.be.true;
                        // Force commandBar validation on the default first choice
                        await editor.commandBar._currentValidate();
                    },
                    contentAfter: '<p>a<span>b<img src="https://download.odoocdn.com/icons/website/static/description/icon.png">[]c</span>d</p>',
                });
            });
            it('should paste and transform an image URL in an existing link', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<p>a<a href="http://existing.com">b[]c</a>d</p>',
                    stepFunction: async editor => {
                        await pasteText(editor, 'https://download.odoocdn.com/icons/website/static/description/icon.png');
                        // Ensure the powerbox is active
                        window.chai.expect(editor.commandBar._active).to.be.true;
                        // Force commandBar validation on the default first choice
                        await editor.commandBar._currentValidate();
                    },
                    contentAfter: '<p>a<a href="http://existing.com">b<img src="https://download.odoocdn.com/icons/website/static/description/icon.png">[]c</a>d</p>',
                });
            });
        });
        describe('range not collapsed', async () => {
            it('should paste and transform an image URL in a p', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<p>ab[xxx]cd</p>',
                    stepFunction: async editor => {
                        await pasteText(editor, 'https://download.odoocdn.com/icons/website/static/description/icon.png');
                        // Ensure the powerbox is active
                        window.chai.expect(editor.commandBar._active).to.be.true;
                        // Force commandBar validation on the default first choice
                        await editor.commandBar._currentValidate();
                    },
                    contentAfter: '<p>ab<img src="https://download.odoocdn.com/icons/website/static/description/icon.png">[]cd</p>',
                });
            });
            it('should paste and transform an image URL in a span', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<p>a<span>b[x<a href="http://existing.com">546</a>x]c</span>d</p>',
                    stepFunction: async editor => {
                        await pasteText(editor, 'https://download.odoocdn.com/icons/website/static/description/icon.png');
                        // Ensure the powerbox is active
                        window.chai.expect(editor.commandBar._active).to.be.true;
                        // Force commandBar validation on the default first choice
                        await editor.commandBar._currentValidate();
                    },
                    contentAfter: '<p>a<span>b<img src="https://download.odoocdn.com/icons/website/static/description/icon.png">[]c</span>d</p>',
                });
            });
            it('should paste and transform an image URL inside an existing link', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<p>a<a href="http://existing.com">b[qsdqsd]c</a>d</p>',
                    stepFunction: async editor => {
                        await pasteText(editor, 'https://download.odoocdn.com/icons/website/static/description/icon.png');
                        // Ensure the powerbox is active
                        window.chai.expect(editor.commandBar._active).to.be.true;
                        // Force commandBar validation on the default first choice
                        await editor.commandBar._currentValidate();
                    },
                    contentAfter: '<p>a<a href="http://existing.com">b<img src="https://download.odoocdn.com/icons/website/static/description/icon.png">[]c</a>d</p>',
                });
            });
        });
    });
    describe('youtube video', () => {
        describe('range collapsed', async () => {
            it('should paste and transform a youtube URL in a p', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<p>ab[]cd</p>',
                    stepFunction: async editor => {
                        await pasteText(editor, 'https://www.youtube.com/watch?v=dQw4w9WgXcQ');
                        // Ensure the powerbox is active
                        window.chai.expect(editor.commandBar._active).to.be.true;
                        // Force commandBar validation on the default first choice
                        await editor.commandBar._currentValidate();
                    },
                    contentAfter: '<p>ab<iframe width="560" height="315" src="https://www.youtube.com/embed/dQw4w9WgXcQ" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen="1"></iframe>[]cd</p>',
                });
            });
            it('should paste and transform a youtube URL in a span', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<p>a<span>b[]c</span>d</p>',
                    stepFunction: async editor => {
                        await pasteText(editor, 'https://youtu.be/dQw4w9WgXcQ');
                        // Ensure the powerbox is active
                        window.chai.expect(editor.commandBar._active).to.be.true;
                        // Force commandBar validation on the default first choice
                        await editor.commandBar._currentValidate();
                    },
                    contentAfter: '<p>a<span>b<iframe width="560" height="315" src="https://www.youtube.com/embed/dQw4w9WgXcQ" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen="1"></iframe>[]c</span>d</p>',
                });
            });
            it('should paste and not transform a youtube  URL in a existing link', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<p>a<a href="http://existing.com">b[]c</a>d</p>',
                    stepFunction: async editor => {
                        await pasteText(editor, 'https://youtu.be/dQw4w9WgXcQ');
                        // Ensure the powerbox is not active
                        window.chai.expect(editor.commandBar._active).to.be.false;
                    },
                    contentAfter: '<p>a<a href="http://existing.com">bhttps://youtu.be/dQw4w9WgXcQ[]c</a>d</p>',
                });
            });
        });
        describe('range not collapsed', async () => {
            it('should paste and transform a youtube URL in a p', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<p>ab[xxx]cd</p>',
                    stepFunction: async editor => {
                        await pasteText(editor, 'https://youtu.be/dQw4w9WgXcQ');
                        // Ensure the powerbox is active
                        window.chai.expect(editor.commandBar._active).to.be.true;
                        // Force commandBar validation on the default first choice
                        await editor.commandBar._currentValidate();
                    },
                    contentAfter: '<p>ab<iframe width="560" height="315" src="https://www.youtube.com/embed/dQw4w9WgXcQ" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen="1"></iframe>[]cd</p>',
                });
            });
            it('should paste and transform a youtube URL in a span', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<p>a<span>b[x<a href="http://existing.com">546</a>x]c</span>d</p>',
                    stepFunction: async editor => {
                        await pasteText(editor, 'https://www.youtube.com/watch?v=dQw4w9WgXcQ');
                        // Ensure the powerbox is active
                        window.chai.expect(editor.commandBar._active).to.be.true;
                        // Force commandBar validation on the default first choice
                        await editor.commandBar._currentValidate();
                    },
                    contentAfter: '<p>a<span>b<iframe width="560" height="315" src="https://www.youtube.com/embed/dQw4w9WgXcQ" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen="1"></iframe>[]c</span>d</p>',
                });
            });
            it('should paste and not transform a youtube URL in a existing link', async () => {
                await testEditor(BasicEditor, {
                    contentBefore: '<p>a<a href="http://existing.com">b[qsdqsd]c</a>d</p>',
                    stepFunction: async editor => {
                        await pasteText(editor, 'https://www.youtube.com/watch?v=dQw4w9WgXcQ');
                        // Ensure the powerbox is not active
                        window.chai.expect(editor.commandBar._active).to.be.false;
                    },
                    contentAfter: '<p>a<a href="http://existing.com">bhttps://www.youtube.com/watch?v=dQw4w9WgXcQ[]c</a>d</p>',
                });
            });
        });
    });
});
