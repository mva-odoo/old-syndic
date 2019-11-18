from odoo import http
from odoo.http import request
from odoo.addons.syndic_tools.syndic_tools import SyndicTools


import base64


class ReportController(http.Controller):
    @http.route([
        '/multi_report/<actions>/<docids>/<model>',
    ], type='http', auth='user', website=True)
    def multi_report_routes(self, actions, docids=None, model='', **data):
        if docids:
            docids = [int(i) for i in docids.split(',')]
        if actions:
            actions = [int(i) for i in actions.split(',')]
        pdf = []
        pdf_len = 0
        for action in request.env['ir.actions.report'].browse(actions):
            pdf_data = action.render_qweb_pdf(docids, data=data)[0]
            pdf.append(pdf_data)
            pdf_len += len(pdf_data)

        if model and model == 'letter.letter':
            for mymodel in request.env[model].browse(docids):
                if mymodel.is_merge:
                    for attachment in mymodel.piece_jointe_ids:
                        pdf_data = attachment._file_read(attachment.store_fname)
                        pdf.append(base64.b64decode(pdf_data))
                        pdf_len += len(pdf_data)

        pdf_merge = SyndicTools().merge_pdf(pdf)

        return request.make_response(pdf_merge, headers=[
            ('Content-Type', 'application/pdf'),
            ('Content-Length', len(pdf)),
        ])
