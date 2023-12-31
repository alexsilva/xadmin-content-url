$(function () {
    var ContentUrl = function ($el, options) {
        this.$el = $el;
        this.options = options;
        this.icons = {
            loading: "fa fa-spin fa-spinner mr-2",
            error: "fa fa-exclamation-triangle mr-2",
        }
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
            var for_name = self.$el.data("for_name"),
                retry = modal.retry_action(for_name, $.proxy(self.init, self));
            modal.fail(retry);
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
            this.$btnInsert.attr("data-dismiss", function (_, value) {
                return value !== undefined ? value : 'modal';
            });
        }
        return this.$btnInsert
    }

    ContentUrl.prototype.get_modal_footer = function () {
        if (!this.$modalFooter) {
            this.$modalFooter = this.modal.find(".modal-footer");
        }
        return this.$modalFooter
    }

    ContentUrl.prototype.get_selection = function () {
        return this.modal.find("form.xdm_ct_url_form #id_xdm-content").val();
    }

    /* Mount the url to the initial form */
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
        var self = this,
            $form = this.modal.find("form.xdm_ct_url_form"),
            $icon = $form.find("button.btn-content-select").find('i'),
            $sel = $form.find("#id_xdm-content"),
            url = this.get_rest_url($sel.val()),
            $table_wrapper = $form.find(".xdm_ct_url_table_wrapper").removeClass('d-none'),
            $table = $form.find("table.xdm_ct_url_table").removeClass('d-none'),
            params = {plugin: "xd_ct_url", 'format': 'datatables'};


        if (!this.$dt) {
            this.$dt = $table.DataTable({
                	dom: "<'row align-items-center'<'col-sm-12 col-md-6 p-1'l><'col-sm-12 col-md-6 p-1'f>>"
                        + "<'row'<'col-sm-12'tr>>"
                        + "<'row mt-3'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
                ajax: {
                    url: url,
                    data: params,
                    error: function (jqXHR, textStatus, errorThrown) {
                        var data = (jqXHR.responseJSON || {}).data,
                            text = textStatus || '';
                        $icon.removeClass(self.icons.loading);
                        $icon.addClass(self.icons.error);
                        $icon.attr("title", data ? data.detail || text: text);
                    },
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
            this.$dt.on('preXhr', function () {
                $icon.addClass(self.icons.loading).removeAttr("title");
            });
            this.$dt.on('draw', function () {
                $icon.removeClass(self.icons.loading).removeClass(self.icons.error);
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
            this.modal = xadmin.bs_modal({
                header: {tag: 'h5', title: gettext("Content URL")},
                modal: {size: 'modal-lg', id: "xd_content_url_modal"},
                cancel_button: {'class': 'd-none'},
                confirm_button: {
                    'class': 'sticky-bottom xd_ct_insert',
                    'text': gettext("Insert selected")
                }
            });

            this.get_modal_footer().addClass('sticky-bottom');

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