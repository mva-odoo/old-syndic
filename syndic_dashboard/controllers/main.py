# -*- coding: utf-8 -*-

from odoo import http
from datetime import date
from dateutil.relativedelta import relativedelta


class OrderRoute(http.Controller):

    @http.route('/timeline/statistics', type='json', auth='user')
    def get_timeline(self):
        today = date.today()
        Mois_fr = {
            1: 'Janvier',
            2: 'Fevrier',
            3: 'Mars',
            4: 'Avril',
            5: 'Mai',
            6: 'Juin',
            7: 'Juillet',
            8: 'Aout',
            9: 'Septembre',
            10: 'Octobre',
            11: 'Novembre',
            12: 'Decembre',
        }
        dates = []

        dates.append((today-relativedelta(months=2)))
        dates.append((today-relativedelta(months=1)))
        dates.append((today+relativedelta(months=0)))
        dates.append((today+relativedelta(months=1)))
        dates.append((today+relativedelta(months=2)))

        buildings = http.request.env['syndic.building'].search(
            [
                ('date_mois', '!=', False),
                ('date_mois', 'in', [month.month for month in dates]),
            ],
        )

        events = []
        for month in dates:
            content = ''
            for building in buildings.filtered(lambda s: s.date_mois == month.month):
                content += '<br/>%s (%s)' % (building.name, building.date_quinzaine)
            events.append({
                'date': '%s - %s' % (month.year, Mois_fr.get(month.month)),
                'content': content,
            })

        return {
            'myEvents': events
        }

    @http.route('/dashboard/buildings', type='json', auth='user')
    def get_buildings(self):
        uid = http.request.env['syndic.building']._context.get('uid')
        return {
            'buildings': http.request.env['syndic.building'].search_read(
                [('manager_id', '=', uid)],
                ['name']
            )
        }
