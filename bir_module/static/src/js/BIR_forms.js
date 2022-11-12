// Form 2307
odoo.define('bir_module._2307Form', function(require) {
"use strict";

var AbstractAction = require('web.AbstractAction');
var core = require('web.core');
var Dialog = require('web.Dialog');
var Session = require('web.session');
var Widget = require('web.Widget');

var _2307Form = AbstractAction.extend({
	contentTemplate: 'form_2307_page',

	start: function(){
        self = this;
        var current = get_current();
        var BP = 0
        this.$("#_2307_month").val(current);

		this._rpc({
            model: 'account.move',
            method: 'fetch_BP',
            args: [''],
        }).then(function(data){
            $("#_2307_partner").append(construct_partners(data));

            BP = $("#_2307_partner").find(":selected").val();
            self.load_data();
        });
	},

	events: {
        "click #print_2307": function(){
            var current = this.$("#_2307_month").val();
            var BP = this.$("#_2307_partner").find(":selected").val();
            
            var self = this;

            // var ids = [];
            // var table = document.getElementById("bir_ammend_table");

            // var checkBoxes = table.getElementsByTagName("input");

            // for (var i = 0; i < checkBoxes.length; i++) {
            //     if (!checkBoxes[i].checked) {
            //         var row = checkBoxes[i].parentNode.parentNode.parentNode;
            //         ids.push(row.cells.item(0).innerHTML);
            //     }
            // }

            this._rpc({
                model: 'account.move',
                method: 'x_2307_forms',
                args: ['', {'month': current, 'id': BP, 'trigger': 'print', 'tranid': 'none'}],
            }).then(function(data){
                self.do_action(data);
            });
        },

        "keypress #_2307_month": function(e){
            if(e.which == 13){
                this.load_data();
            }
        },

        "change #_2307_partner": function(e){
            this.load_data();
        },

        // "click #apply_2307_ammend": function(e){
        //     var BP = this.$("#_2307_partner").find(":selected").val();
        //     var current = this.$("#_2307_month").val();

        //     var ids = [];
        //     var table = document.getElementById("bir_ammend_table");

        //     var checkBoxes = table.getElementsByTagName("input");

        //     for (var i = 0; i < checkBoxes.length; i++) {
        //         if (!checkBoxes[i].checked) {
        //             var row = checkBoxes[i].parentNode.parentNode.parentNode;
        //             ids.push(row.cells.item(0).innerHTML);
        //         }
        //     }

        //     var url = "/report/pdf/bir_module.form_2307/?id="+BP+"&month="+current+"&trigger=ammend_view&ids=" + encodeURIComponent(JSON.stringify(ids));
        //     $("#2307_preview").attr("src", url);
        // }
    },

    load_data: function(){
        var BP = this.$("#_2307_partner").find(":selected").val();
        var current = this.$("#_2307_month").val();

        var url = "/report/pdf/bir_module.form_2307/?id="+BP+"&month="+current+"&trigger=view";
        $("#2307_preview").attr("src", url);

        this._rpc({
            model: 'account.move',
            method: 'x_get_2307_data',
            args: ['', [[BP, current], 'not_transactional', 'table', '2307-Quarterly', 'none']],
        }).then(function(data){
            $("#2307_ammend_table").html(construct_ammendment_no_action(data));
            $('#bir_ammend_table').DataTable();
            $('.dataTables_length').addClass('bs-select');
        });
    },
});

core.action_registry.add('form_2307_page', _2307Form);

return {
    _2307Form: _2307Form,
};

});

// Form 2550M
odoo.define('bir_module._2550MForm', function(require) {
"use strict";

var AbstractAction = require('web.AbstractAction');
var core = require('web.core');
var Dialog = require('web.Dialog');
var Session = require('web.session');
var Widget = require('web.Widget');

var _2550MForm = AbstractAction.extend({
    contentTemplate: 'form_2550M_page',

    start: function(){
        var current = get_current();
        this.$("#_2550M_month").val(current);

        // var url = "/report/pdf/bir_module.form_2550M?month="+current+"&trans=2550M&trigger=view&tranid=none";
        // this.$("#2550M_preview").attr("src", url);

        this.load_data();
    },

    events: {
        "click #print_2550M": function(){
            var current = this.$("#_2550M_month").val()
            var self = this;

            var ids = [];
            var table = document.getElementById("bir_ammend_table");

            var checkBoxes = table.getElementsByTagName("input");

            for (var i = 0; i < checkBoxes.length; i++) {
                if (!checkBoxes[i].checked) {
                    var row = checkBoxes[i].parentNode.parentNode.parentNode;
                    ids.push(row.cells.item(0).innerHTML);
                }
            }

            this._rpc({
                model: 'account.move',
                method: 'x_2550_print_action',
                args: ['', {'month': current, 'trans': '2550M', 'trigger': 'exclude-print', 'ids': ids}],
            }).then(function(data){
                self.do_action(data);

                self.load_data();
            });
        },

        "click #apply_2550M_exclude": function(){
            var current = this.$("#_2550M_month").val()

            var ids = [];
            var table = document.getElementById("bir_ammend_table");

            var checkBoxes = table.getElementsByTagName("input");

            for (var i = 0; i < checkBoxes.length; i++) {
                if (!checkBoxes[i].checked) {
                    var row = checkBoxes[i].parentNode.parentNode.parentNode;
                    ids.push(row.cells.item(0).innerHTML);
                }
            }

            var url = "/report/pdf/bir_module.form_2550M?month="+current+"&trans=2550M&trigger=exclude-view&tranid=none&ids="+encodeURIComponent(JSON.stringify(ids));
            this.$("#2550M_preview").attr("src", url);
        },

        "keypress #_2550M_month": function(e){
            if(e.which == 13){
                // var current = this.$("#_2550M_month").val()

                // var url = "/report/pdf/bir_module.form_2550M?month="+current+"&trans=2550M&trigger=view&tranid=none";
                // this.$("#2550M_preview").attr("src", url);
                this.load_data();
            }
        },
    },

    load_data: function(){
        var current = this.$("#_2550M_month").val();

        var url = "/report/pdf/bir_module.form_2550M?month="+current+"&trans=2550M&trigger=view&tranid=none&ids=none";
        this.$("#2550M_preview").attr("src", url);

        this._rpc({
            model: 'account.move',
            method: 'fetch_2550_table_docs_data',
            args: ['', [current, '2550M', 'table']],
        }).then(function(data){
            $("#2550M_ammend_table").html(construct_ammendment(data));
            $('#bir_ammend_table').DataTable();
            $('.dataTables_length').addClass('bs-select');
        });
    },
});

core.action_registry.add('form_2550M_page', _2550MForm);

return {
    _2550MForm: _2550MForm,
};

});

// Form 2550Q
odoo.define('bir_module._2500QForm', function(require) {
"use strict";

var AbstractAction = require('web.AbstractAction');
var core = require('web.core');
var Dialog = require('web.Dialog');
var Session = require('web.session');
var Widget = require('web.Widget');

var _2500QForm = AbstractAction.extend({
    contentTemplate: 'form_2550Q_page',

    start: function(){
        var current = get_current();
        this.$("#_2550Q_month").val(current);

        // var url = "/report/pdf/bir_module.form_2550Q?month="+current+"&trans=2550Q&trigger=view&tranid=none";
        // this.$("#2550Q_preview").attr("src", url);
        this.load_data();
    },

    events: {
        "click #print_2550Q": function(){
            var current = this.$("#_2550Q_month").val()

            var self = this;
            
            this._rpc({
                model: 'account.move',
                method: 'x_2550_print_action',
                args: ['', {'month': current, 'trans': '2550Q', 'trigger': 'print'}],
            }).then(function(data){
                self.do_action(data);
            });
        },

        "keypress #_2550Q_month": function(e){
            if(e.which == 13){
                // var current = this.$("#_2550Q_month").val()

                // var url = "/report/pdf/bir_module.form_2550Q?month="+current+"&trans=2550Q&trigger=view&tranid=none";
                // this.$("#2550Q_preview").attr("src", url);
                this.load_data();
            }
        },
    },

    load_data: function(){
        var current = this.$("#_2550Q_month").val();

        var url = "/report/pdf/bir_module.form_2550Q?month="+current+"&trans=2550Q&trigger=view&tranid=none";
        this.$("#2550Q_preview").attr("src", url);

        this._rpc({
            model: 'account.move',
            method: 'fetch_2550_table_docs_data',
            args: ['', [current, '2550Q', 'table']],
        }).then(function(data){
            $("#2550Q_ammend_table").html(construct_ammendment_no_action(data));
            $('#bir_ammend_table').DataTable();
            $('.dataTables_length').addClass('bs-select');
        });
    },
});

core.action_registry.add('form_2550Q_page', _2500QForm);

return {
    _2500QForm: _2500QForm,
};

});


// Form 1601e
odoo.define('bir_module._1601EForm', function(require) {
"use strict";

var AbstractAction = require('web.AbstractAction');
var core = require('web.core');
var Dialog = require('web.Dialog');
var Session = require('web.session');
var Widget = require('web.Widget');

var _1601EForm = AbstractAction.extend({
    contentTemplate: 'form_1601e_page',

    start: function(){
        var current = get_current();
        this.$("#_1601e_month").val(current);

        var url = "/report/pdf/bir_module.form_1601e?month="+current;
        this.$("#1601e_preview").attr("src", url);
    },

    events: {
        "click #print_1601e": function(){
            var current = this.$("#_1601e_month").val()

            var self = this;
            
            this._rpc({
                model: 'account.move',
                method: 'x_1601e_print_action',
                args: ['', current],
            }).then(function(data){
                self.do_action(data);
            });
        },

        "keypress #_1601e_month": function(e){
            if(e.which == 13){
                var current = this.$("#_1601e_month").val()

                var url = "/report/pdf/bir_module.form_1601e?month="+current;
                this.$("#1601e_preview").attr("src", url);
            }
        },
    },
});

core.action_registry.add('form_1601e_page', _1601EForm);

return {
    _1601EForm: _1601EForm,
};

});
