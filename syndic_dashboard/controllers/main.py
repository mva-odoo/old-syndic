# -*- coding: utf-8 -*-

from odoo import http
from datetime import date, datetime


class OrderRoute(http.Controller):

    @http.route('/timeline/statistics', type='json', auth='user')
    def get_timeline(self):
        current_month = datetime.now().month
        buildings = http.request.env['syndic.building'].search(
            [
                ('meeting_month', '!=', False),
                ('meeting_month', '<=', int(current_month) + 3),
                ('meeting_month', '>=', int(current_month) - 2),

            ],
            order='meeting_month'
        )

        events = []
        for month in range(int(current_month) - 2, int(current_month) + 3):
            events.append({
                'date': '%s' % (month),
                'content': ', '.join(buildings.filtered(lambda s: s.meeting_month == month).mapped('name')),
            })

        return {
            'myEvents': events
        }
