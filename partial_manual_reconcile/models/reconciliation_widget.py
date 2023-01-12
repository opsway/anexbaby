import logging
from odoo import api, models


_logger = logging.getLogger(__name__)


class AccountReconciliation(models.AbstractModel):
    _inherit = 'account.reconciliation.widget'

    def get_counterpart_vals(self, values: list) -> dict:
        prepared_vals = dict()
        for rec in values:
            prepared_vals.update({rec['counterpart_aml_id']: {'debit': rec['debit'], 'credit': rec['credit']}})

            # Write partial residual amount
            acmvl = self.env['account.move.line'].browse(rec['counterpart_aml_id'])
            if rec['debit'] != 0:
                acmvl.partial_amount_residual = rec['debit']
            if rec['credit'] != 0:
                acmvl.partial_amount_residual = rec['credit'] * -1
        return prepared_vals

    @api.model
    def partial_process_move_lines(self, data, values):
        _logger.info('partial_process_move_lines function call')

        self.get_counterpart_vals(values[0]['counterpart_aml_dicts'])

        Partner = self.env['res.partner']
        Account = self.env['account.account']

        for datum in data:
            if len(datum['mv_line_ids']) >= 1 or len(datum['mv_line_ids']) + len(datum['new_mv_line_dicts']) >= 2:
                self._process_move_lines(datum['mv_line_ids'], datum['new_mv_line_dicts'])

            if datum['type'] == 'partner':
                partners = Partner.browse(datum['id'])
                partners.mark_as_reconciled()
