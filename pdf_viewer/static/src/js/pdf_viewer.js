odoo.define('odoo.pdf_viewer', function (require) {
    'use strict';

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var framework = require('web.framework');
    var ActionManager = require('web.ActionManager');
    var ControlPanelMixin = require('web.ControlPanelMixin');

    var Dashboard = AbstractAction.extend(ControlPanelMixin, {
        template: 'PDFViewer',
        init: function(parent, action) {
            this._super(parent);
            this.url = '';
            var context = action.context;

            if ((typeof context.report !== "undefined") && (typeof context.active_id !== "undefined")){
                if (typeof context.active_ids !== "undefined"){
                    this.url = '/report/pdf/'+context.report+'/'+context.active_ids;
                }
                else{
                   this.url = '/report/pdf/'+context.report+'/'+context.active_id;
                }
            }
        },
        start: function(){
              var superDef = this._super.apply(this, arguments);
              return superDef.then(this._updateControlPanel());
      	},

        do_show: function () {
            this._super.apply(this, arguments);
            this._updateControlPanel();
        },

        _updateControlPanel: function () {
            this.update_control_panel({
                cp_content: {
                   $buttons: this.$buttons,
                },
            });
        },

    });

    core.action_registry.add('pdf_viewer.homepage', Dashboard);

    var ActionManager = ActionManager.include({
      _triggerDownload: function (action, options, type){
        framework.blockUI();
        var self = this;

        var context = action.context;
        context.report = action.report_name;

        var actions = {
          'tag': 'pdf_viewer.homepage',
          'name': 'pdf_viewer',
          'type': "ir.actions.client",
          'context': context,
        };
        return this.doAction(actions,options).then(function(){
          framework.unblockUI();
        });
      },
    });
});
