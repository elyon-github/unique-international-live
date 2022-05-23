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
        var current = get_current();
        this.$("#_2307_month").val(current);

		this._rpc({
            model: 'account.move',
            method: 'fetch_BP',
            args: [''],
        }).then(function(data){
            $("#_2307_partner").append(construct_partners(data));

            var BP = $("#_2307_partner").find(":selected").val();

            var url = "/report/pdf/bir_module.form_2307/?id="+BP+"&month="+current+"&trigger=view";
            $("#2307_preview").attr("src", url);
        });
	},

	events: {
        "click #print_2307": function(){
            var current = this.$("#_2307_month").val();
            var BP = this.$("#_2307_partner").find(":selected").val();
            
            var self = this;

            this._rpc({
                model: 'account.move',
                method: 'x_2307_forms',
                args: ['', {'month': current, 'id': BP, 'trigger': 'print'}],
            }).then(function(data){
                self.do_action(data);
            });
        },

        "keypress #_2307_month": function(e){
            var current = this.$("#_2307_month").val()
            var BP = this.$("#_2307_partner").find(":selected").val();

            if(e.which == 13){
                var url = "/report/pdf/bir_module.form_2307/?id="+BP+"&month="+current+"&trigger=view";
                $("#2307_preview").attr("src", url);
            }
        },

        "change #_2307_partner": function(e){
            var current = this.$("#_2307_month").val()
            var BP = this.$("#_2307_partner").find(":selected").val();

            var url = "/report/pdf/bir_module.form_2307/?id="+BP+"&month="+current+"&trigger=view";
            $("#2307_preview").attr("src", url);
        },
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

        var url = "/report/pdf/bir_module.form_2550M?month="+current+"&trans=2550M&trigger=view";
        this.$("#2550M_preview").attr("src", url);
    },

    events: {
        "click #print_2550M": function(){
            var current = this.$("#_2550M_month").val()

            var self = this;

            this._rpc({
                model: 'account.move',
                method: 'x_2550_print_action',
                args: ['', {'month': current, 'trans': '2550M', 'trigger': 'print'}],
            }).then(function(data){
                self.do_action(data);
            });
        },

        "keypress #_2550M_month": function(e){
            if(e.which == 13){
                var current = this.$("#_2550M_month").val()

                var url = "/report/pdf/bir_module.form_2550M?month="+current+"&trans=2550M&trigger=view";
                this.$("#2550M_preview").attr("src", url);
            }
        },
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

        var url = "/report/pdf/bir_module.form_2550Q?month="+current+"&trans=2550Q&trigger=view";
        this.$("#2550Q_preview").attr("src", url);
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
                var current = this.$("#_2550Q_month").val()

                var url = "/report/pdf/bir_module.form_2550Q?month="+current+"&trans=2550Q&trigger=view";
                this.$("#2550Q_preview").attr("src", url);
            }
        },
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
