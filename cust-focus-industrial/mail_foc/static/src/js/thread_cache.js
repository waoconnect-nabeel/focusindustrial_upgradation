odoo.define('mail_foc/static/src/js/thread_cache.js', function (require) {

    const {
        registerInstancePatchModel,
    } = require('mail/static/src/model/model_core.js');

    registerInstancePatchModel('mail.thread_cache', 'mail_foc.thread', {
        _computeMessages() {
            var res = this._super.apply(this, arguments);
            if (res && res[0] && res[0][1]) {
                if (this.threadModel === 'res.partner') {
                    res[0][1] = res[0][1].filter(m => !m["author"] || m["author"] && m["author"]["id"] !== 2)
                }
            }
            return res
        }
    });
});
