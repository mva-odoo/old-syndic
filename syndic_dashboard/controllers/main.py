# -*- coding: utf-8 -*-

from odoo import http
from datetime import date, datetime


class OrderRoute(http.Controller):

    @http.route('/timeline/statistics', type='json', auth='user')
    def get_timeline(self):
        current_month = datetime.now().month
        buildings = http.request.env['syndic.building'].search(
            [
                ('date_mois', '!=', False),
                ('date_mois', '<=', int(current_month) + 3),
                ('date_mois', '>=', int(current_month) - 2),

            ],
            order='date_mois'
        )

        events = []
        for month in range(int(current_month) - 2, int(current_month) + 3):
            events.append({
                'date': '%s' % (month),
                'content': ', '.join(buildings.filtered(lambda s: s.date_mois == month).mapped('name')),
            })

        return {
            'myEvents': events
        }
