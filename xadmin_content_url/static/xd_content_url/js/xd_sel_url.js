

$(function () {
    var ContentUrl = function ($el, options) {
        this.$el = $el;
    }

    $.fn.select_ct_url = function (options) {
        return this.each(function() {
            var $el = $(this).add('xd_sel_url');
            if (!$el.data('xd_content_url')) {
                $el.data('xd_content_url', new ContentUrl($el, options));
            }
            return $el.data('xd_content_url');
        });
    }

    $(".xd_content_url_sel_btn").select_ct_url();
})