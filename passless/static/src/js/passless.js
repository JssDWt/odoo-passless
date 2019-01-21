odoo.define('passless', function (require) {
    "use strict";
    
    var gui = require('point_of_sale.gui');
    var screens = require('point_of_sale.screens');
    var core = require('web.core');
    var ajax = require('web.ajax');
    var QWeb = core.qweb;
    var _t = core._t;
    
    var PasslessScreenWidget = screens.ReceiptScreenWidget.extend({
        template: 'PasslessScreenWidget',
        events: {
            'click .passless-button': function(e) {
                ajax.jsonRpc(
                    "/passless/send", 
                    "call", 
                    {
                        "receipt": this.get_receipt_render_env().receipt
                    })
                .then(function(data) {
                    var message = data['message'];
                    console.log(message);
                });
            }
        }
    });
    
    gui.define_screen({name:'receipt', widget: PasslessScreenWidget});
});


// odoo.passless = function(instance, module){
//     console.warn("odoo.passless called");
//     var _t = instance.web._t, 
//         _lt = instance.web._lt;
//     var QWeb = instance.web.qweb;
//     module = instance.point_of_sale;

//     module.ReceiptScreenWidget = module.ReceiptScreenWidget.extend({
//         init: function(parent, options) {
//             this._super(parent, options);
//             console.warn("Passless init called.");
//         }
//         // template: 'PasslessScreenWidget',
//         // start: function() {
//         //     console.log("Initializing passless"); 
//         // },
//         // events: {
//         //     "click .passless-button": function(e) {
//         //         console.log("Passless button clicked.")
//         //     },
//         // },
//         // close: function(){
//         //     this._super();
//         // }
//     });
// }