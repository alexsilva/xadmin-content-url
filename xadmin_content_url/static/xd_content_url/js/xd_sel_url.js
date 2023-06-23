$(function () {
    var Modal = function (options) {
        this.$modal = $("#nunjucks-modal-main").template_render$(options);
    }
    Modal.prototype.loading = function () {
        return this.set_content('<h1 style="text-align:center;"><i class="fa-spinner fa-spin fa fa-large"></i></h1>');
    }
    Modal.prototype.find = function (selector){
        return this.$modal.find(selector)
    }
    Modal.prototype.set_content = function (html) {
        return this.find(".modal-body").html(html)
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
        var self = this,
            modal = this.get_modal();
        this.get_btn_insert().prop("disabled", true);
        modal.loading();
        $.ajax({
            url: this.$el.data('url')
        }).done(function (html) {
            self.reload(html);
        }).fail(function () {
            modal.set_content("Fail!");
        });
        modal.show();
    }

    /* Initializes the modal and prepares for a new table load */
    ContentUrl.prototype.reload = function (html) {
        var $form, ajax_table,
            modal = this.get_modal();
        modal.set_content(html);
        ajax_table = $.proxy(this.ajax_table, this);
        $form = modal.$modal.find("form.xdm_ct_url_form");
        $form.find("button.btn-content-select").click(ajax_table);
        if (this.$dt) {
            this.$dt.destroy();
            this.$dt = null;
        }
    }

    ContentUrl.prototype.get_btn_insert = function () {
        if (!this.$btnInsert) {
            this.$btnInsert = this.modal.find("button.xd_ct_insert");
        }
        return this.$btnInsert
    }

    ContentUrl.prototype.get_selection = function () {
        return this.modal.find("form.xdm_ct_url_form #id_xdm-content").val();
    }

    ContentUrl.prototype.get_rest_url = function (model_label) {
        var url;
        if (window.Urls) {
            url = Urls["xadmin:" + model_label.replace(".", "_") + "_rest"]()
        } else {
            url = xadmin.path_prefix + model_label.replace(".", "/") + "/rest"
        }
        return url;
    }
    ContentUrl.prototype.ajax_table = function () {
        var $form = this.modal.find("form.xdm_ct_url_form"),
            $sel = $form.find("#id_xdm-content"),
            url = this.get_rest_url($sel.val()),
            $table = $form.find("table.xdm_ct_url_table").removeClass('d-none'),
            params = {plugin: "xd_ct_url", 'format': 'datatables'};

        if (!this.$dt) {
            this.$dt = $table.DataTable({
                ajax: {
                    url: url,
                    data: params
                },
                select: {
                    info: false,
                    style: 'single'
                },
                processing: true,
                language: {
                    url: $table.data('language-url'),
                },
            });
            this.$dt.on('select', $.proxy(this.dt_row_selected, this));
            this.$dt.on('deselect', $.proxy(this.dt_row_deselected, this));
        } else {
            this.$dt.ajax.url(url).load();
        }
    }

    ContentUrl.prototype.dt_row_selected = function (e, dt, type, indexes) {
        if (type === 'row') {
            this.get_btn_insert().prop("disabled", false);
        }
    }
    ContentUrl.prototype.dt_row_deselected = function (e, dt, type, indexes) {
        if (type === 'row') {
            this.get_btn_insert().prop("disabled", true);
        }
    }

    ContentUrl.prototype.insert = function () {
        var data = this.$dt.rows( { selected: true } ).data(),
            data_id = data.pluck('id'),
            data_url = data.pluck('url'),
            model_label = this.get_selection(),
            $input = $("form input[name='" + this.$el.data('for_name') +"']"),
            $selInput = $("form input[name='sel_" + this.$el.data('for_name') +"']"),
            ctype = model_label.replace(".", ":") + ":" + data_id[0];
        $selInput.val(data_url[0])
        $input.val(ctype);
    }

    ContentUrl.prototype.get_modal = function () {
        if (!this.modal) {
            this.modal = new Modal({
                modal: {size: 'modal-lg', id: "xd_content_url_modal"},
                cancel_button: {
                    'class': 'btn-sm xd_ct_insert',
                    'text': gettext("Insert selected")
                }
            });
            this.modal.appendTo('body');
            var $btn = this.get_btn_insert().prop("disabled", true);
            $btn.click($.proxy(this.insert, this));
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