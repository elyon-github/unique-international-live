// SAWT Report
odoo.define('bir_module.PrintHistory', function(require) {
    "use strict";
    
    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var Dialog = require('web.Dialog');
    var Session = require('web.session');
    var Widget = require('web.Widget');
    
    var PrintHistory = AbstractAction.extend({
        contentTemplate: 'print_history',
    
        start: function(){
            this._rpc({
                model: 'account.move',
                method: 'fetch_print_types',
                args: [''],
            }).then(function(data){
                $("#_print_type").append(construct_print_types(data));
            });

            // var type = $("#_print_type").find(":selected").val();

            this._rpc({
                model: 'account.move',
                method: 'fetch_print_history',
                args: ['', 'all'],
            }).then(function(dat){
                $("#print_history").html(construct_print_history(dat));
                $('#print_history_datatable').DataTable();
                $('.dataTables_length').addClass('bs-select');
            });
        },
    
        events: {
            "change #_print_type": function(e){
                var type = this.$("#_print_type").find(":selected").val();
    
                this._rpc({
                    model: 'account.move',
                    method: 'fetch_print_history',
                    args: ['', type],
                }).then(function(dat){
                    $("#print_history").html(construct_print_history(dat));
                    $('#print_history_datatable').DataTable();
                    $('.dataTables_length').addClass('bs-select');
                });
            },

            "click .print_details_btn":function(e){
                var x = $(e.target).get(0);
                var cell = $(x).closest('button').get(0);
                var cell_val = $(cell).val()
                
                this._rpc({
                    model: 'account.move',
                    method: 'fetch_print_history_details',
                    args: ['', cell_val],
                }).then(function(dat){
                    $("#_print_details").html(construct_print_details(dat));
                    $('#print_history_line_datatable').DataTable();
                    $('.dataTables_length').addClass('bs-select');
                });
            },

            "click .preview_details_btn":function(e){
                var x = $(e.target).get(0);
                var cell = $(x).closest('button').get(0);
                var cell_val = $(cell).val()

                this._rpc({
                    model: 'account.move',
                    method: 'get_reprint_trans',
                    args: ['', cell_val],
                }).then(function(dat){
                    var url = "";
                    if(dat[0] == "2550M"){
                        url = "/report/pdf/bir_module.form_2550M?month="+dat[1]+"&trans=2550M&trigger=reprint&tranid="+cell_val;
                    } else if(dat[0] == "2550Q"){
                        url = "/report/pdf/bir_module.form_2550Q?month="+dat[1]+"&trans=2550Q&trigger=reprint&tranid="+cell_val;
                    } else if(dat[0] == "2307-Transactional"){
                        var url = "/report/pdf/bir_module.form_2307_preview/?id=none&month="+dat[1]+"&type="+dat[0]+"&tranid="+cell_val;
                    } else if(dat[0] == "2307-Quarterly"){
                        var url = "/report/pdf/bir_module.form_2307_preview/?id=none&month="+dat[1]+"&type="+dat[0]+"&tranid="+cell_val;
                    }
                    // alert(dat);

                    $("#print_preview_frame").attr("src", url);
                });            
            }
        },
    });
    
    core.action_registry.add('print_history_page', PrintHistory);
    
    return {
        PrintHistory: PrintHistory,
    };
    
    });
    