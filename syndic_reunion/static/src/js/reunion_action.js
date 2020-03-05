odoo.define('syndic.reunion', function (require) {
    "use strict";
    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var Dialog = require('web.Dialog');

    var Reunion = AbstractAction.extend({
        template: 'syndic_reunion',
        hasControlPanel: true,

        events: {
            'click .vote_btn': '_openvote',
            'click ._save_vote_btn': '_save_vote',
        },

        start: function(){
            var superDef = this._super.apply(this, arguments);
            return superDef.then(
                this._updateControlPanel());
        },
    
        do_show: function () {
            this._super.apply(this, arguments);
            this._updateControlPanel();
        },

        _openvote: function(){
            this.$el.append(core.qweb.render('vote.form'))
        },

        _test_test: function(test, test1, test2){
            debugger;
            console.log('Ceci est un test')
        },

        _save_vote: function(){
            var buttons = [{
                    text: "Ok",
                    close: true,
                    click: _.bind(this._test_test, this),
                },
                {
                    text: "Cancel",
                    close: true,
                },
            ];

            var dialog = new Dialog(this, {
                title: 'Ajouter un point',
                $content: core.qweb.render('ok_save'),
                buttons: buttons,
            });

            dialog.open();

        },

        _renderButtons: function () {
            this.$buttons = $(core.qweb.render('vote.Buttons'));
        },
    
        _updateControlPanel: function () {
            this._renderButtons();
            this.updateControlPanel({
                cp_content: {
                    $buttons: this.$buttons,
                },
            });
        },
    
    });
    
    core.action_registry.add('syndic.reunion', Reunion);
    
    return Reunion;
    
    });
    