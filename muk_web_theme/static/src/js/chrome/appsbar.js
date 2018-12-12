/**********************************************************************************
*
*    Copyright (C) 2017 MuK IT GmbH
*
*    This program is free software: you can redistribute it and/or modify
*    it under the terms of the GNU Affero General Public License as
*    published by the Free Software Foundation, either version 3 of the
*    License, or (at your option) any later version.
*
*    This program is distributed in the hope that it will be useful,
*    but WITHOUT ANY WARRANTY; without even the implied warranty of
*    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*    GNU Affero General Public License for more details.
*
*    You should have received a copy of the GNU Affero General Public License
*    along with this program.  If not, see <http://www.gnu.org/licenses/>.
*
**********************************************************************************/

odoo.define('muk_web_theme.AppsBar', function (require) {
"use strict";

var core = require('web.core');
var config = require("web.config");

var Widget = require('web.Widget');

var _t = core._t;
var QWeb = core.qweb;

var AppsBar = Widget.extend({
	events: _.extend({}, Widget.prototype.events, {
        'click .nav-link': '_onAppsMenuItemClicked',
    }),
	template: "muk_web_theme.AppsBarMenu",
	init: function (parent, menu) {
        this._super.apply(this, arguments);
        this._apps = _.map(menu.children, function (app) {
            return {
                actionID: parseInt(app.action.split(',')[1]),
                web_icon_data: app.web_icon_data,
                menuID: app.id,
                name: app.name,
                xmlID: app.xmlid,
            };
        });
    },
    getApps: function () {
        return this._apps;
    },
    _openApp: function (app) {
        this.trigger_up('app_clicked', {
            action_id: app.actionID,
            menu_id: app.menuID,
        });
    },
    _onAppsMenuItemClicked: function (ev) {
        var $target = $(ev.currentTarget);
        var actionID = $target.data('action-id');
        var menuID = $target.data('menu-id');
        var app = _.findWhere(this._apps, { actionID: actionID, menuID: menuID });
        this._openApp(app);
    },
});

return AppsBar;

});
