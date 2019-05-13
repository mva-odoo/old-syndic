odoo.define('timeline.dashboard', function (require) {
"use strict";
var AbstractAction = require('web.AbstractAction');
var ControlPanelMixin = require('web.ControlPanelMixin');
var core = require('web.core');

var qweb = core.qweb;

var Dashboard = AbstractAction.extend(ControlPanelMixin, {
	template: 'dashboardTimeline',

	events: {
        'click .building_btn': '_openBuilding',
    },

	willStart: function(){
		var self = this;
        var statsDef = this._rpc({route: '/timeline/statistics'}).then(function (stats) {
            self.stats = stats;
        });

				var buildingsDef = this._rpc({route: '/dashboard/buildings'}).then(function (buildings) {
					self.buildings = buildings;
				});

        var superDef = this._super.apply(this, arguments);

        return $.when(buildingsDef, statsDef, superDef);
	},

	start: function(){
        var superDef = this._super.apply(this, arguments);
        this._renderButtons();

        return superDef.then(
					this._updateControlPanel()).then(
							this._render_building.bind(this)).then(
								this._render_meetings.bind(this)
							);
	},

	_render_building: function(){
		var new_this = this;
		this.buildings.buildings.forEach(function(values, key) {
			new_this.$('.my-buildings').append('<p><a href="javascript:;" class="building_btn" data-id='+values.id+'>'+values.name+'</a></p>');
		})

	},

	_render_meetings: function(){
		var new_this = this;

		this.stats.myEvents.forEach(function(value) {
			var $div = $("<div>", {id: value.date, "class": "col-2"}).css('text-align', 'center');
			$div.html('<h2 class="header-month">'+value.date+'</h2>');
			new_this.$('.row.meeting_date').append($div);
			
			var $body_premier = $("<div>", {id: "premier"+value.date, "class": "col-2"}).css('text-align', 'center');
			new_this.$('.row.meeting_building1').append($body_premier);

			value.premier.forEach(function(element) {
				$body_premier.html('<h3 class="premier">'+element+'</h3>');
				new_this.$('.row.meeting_building1').append($body_premier);
			});

			var $body_deuxieme = $("<div>", {id: "deuxieme"+value.date, "class": "col-2"}).css('text-align', 'center');
			new_this.$('.row.meeting_building2').append($body_deuxieme);

			value.deuxieme.forEach(function(element) {
				$body_deuxieme.html('<h3 class="deuxieme">'+element+'</h3>');
				new_this.$('.row.meeting_building2').append($body_deuxieme);
			});
		});

	},

	_openBuilding: function (event) {
		var building_id = $(event.currentTarget).data('id');

		return this.do_action({
				res_id: building_id,
				name: 'Immeuble',
				res_model: 'syndic.building',
				type: 'ir.actions.act_window',
				views: [[false, 'form']],
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
