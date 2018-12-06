odoo.define('timeline.dashboard', function (require) {
"use strict";
var AbstractAction = require('web.AbstractAction');
var ControlPanelMixin = require('web.ControlPanelMixin');
var core = require('web.core');

var qweb = core.qweb;

var Dashboard = AbstractAction.extend(ControlPanelMixin, {
	template: 'dashboardTimeline',

	willStart: function(){
		var self = this;
        var statsDef = this._rpc({route: '/timeline/statistics'}).then(function (stats) {
            self.stats = stats;
        });
        var superDef = this._super.apply(this, arguments);
        return $.when(statsDef, superDef);
	},

	start: function(){
        var superDef = this._super.apply(this, arguments);
        this._renderButtons();
        return superDef.then(this._updateControlPanel()).then(this._render_timeline.bind(this));
	},

	_render_timeline: function(){
  		// console.log(template_timeline);
		this.$('.my-timeline').roadmap(this.stats.myEvents, {
			eventTemplate: '<div class="event">' + '<div class="event__date">####DATE###</div>' + '<div class="event__content">####CONTENT###</div>' + '</div>',
			eventsPerSlide: 5,
			orientation: 'horizontal'
		});
	},

    do_show: function () {
        this._super.apply(this, arguments);
        this._updateControlPanel();
    },

    _renderButtons: function () {
        // this.$buttons = $(qweb.render('timeline.Buttons'));
        // this.$buttons.on('click', '.o_new_orders_btn', this._get_timeline.bind(this));
    },

    _updateControlPanel: function () {
        this.update_control_panel({
            cp_content: {
               $buttons: this.$buttons,
            },
        });
    },

});


core.action_registry.add('timeline.dashboard', Dashboard);

return Dashboard;

});
