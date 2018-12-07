# -*- coding: utf-8 -*-

from odoo import http
from datetime import date
from dateutil.relativedelta import relativedelta


class OrderRoute(http.Controller):

    @http.route('/timeline/statistics', type='json', auth='user')
    def get_timeline(self):
        today = date.today()
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
                content += '<br/>%s (%s)' % (building.name, building.date_quizaine)

            events.append({
                'date': '%s - %s' % (month.year, month.month),
                'content': content,
            })

        return {
            'myEvents': events
        }
