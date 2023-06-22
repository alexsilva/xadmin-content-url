$(function () {
    var Modal = function () {
        this.$modal = $("#nunjucks-modal-main").template_render$({
            modal: {size: 'modal-lg', id: "xd_content_url_modal"},
            cancel_button: {'class': 'btn-sm'}
        });
    }
    Modal.prototype.loading = function () {
        return this.body_content('<h1 style="text-align:center;"><i class="fa-spinner fa-spin fa fa-large"></i></h1>');
    }
    Modal.prototype.body_content = function (html) {
        return this.$modal.find(".modal-body").html(html)
    }

    Modal.prototype.show = function () {
        return this.$modal.modal();
    }
    Modal.prototype.appendTo = function (selector) {
        return this.$modal.appendTo(selector);
    }

    var ContentUrl = function ($el, options) {
        this.$el = $el;
        this.options = options;
        $el.click($.proxy(this.init, this));
    }
    ContentUrl.prototype.init = function () {
        var self= this,
            modal = this.get_modal();
        modal.loading();
        $.ajax({
            url: this.$el.data('url')
        }).done(function (html) {
            modal.body_content(html);
            var $form = modal.$modal.find("form.xdm_ct_url_form"),
                load_table = $.proxy(self.ajax_table, self);
            $form.find("button.btn-content-select").click(load_table);
        }).fail(function () {
            modal.body_content("Fail!");
        });
        modal.show();
    }

    ContentUrl.prototype.ajax_table = function () {
        var $form = this.modal.$modal.find("form.xdm_ct_url_form"),
            $sel = $form.find("#id_xdm-content"),
            content = $sel.val(),
            url = Urls["xadmin:" + content.replace(".", "_") + "_rest"](),
            $table = $form.find("table.xdm_ct_url_table");
        var $dt = $table.DataTable({
            ajax: {
                url: url,
                data: {plugin: "xd_ct_url", 'format': 'datatables'}
            },
            processing: true,
            language: {
                url: $table.data('language-url'),
            },
        });
    }

    ContentUrl.prototype.get_modal = function () {
        if (!this.modal) {
            this.modal = new Modal();
            this.modal.appendTo('body');
        }
        return this.modal;
    }

    $.fn.select_ct_url = function (options) {
        return this.each(function () {
            var $el = $(this).add('xd_sel_url');
            if (!$el.data('xd_content_url')) {
                $el.data('xd_content_url', new ContentUrl($el, options));
            }
            return $el.data('xd_content_url');
        });
    }

    $(".xd_content_url_sel_btn").select_ct_url();
})