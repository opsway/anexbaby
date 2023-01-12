from traceback import extract_stack
from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    partial_amount_residual = fields.Monetary(string='Partial Residual Amount', currency_field='company_currency_id')

    def is_partial_reconcile(self) -> bool:
        tb_stack = extract_stack()
        return bool(next((frame for frame in tb_stack if frame.name == 'partial_process_move_lines'), False))

    def auto_reconcile_lines(self):
        # Create list of debit and list of credit move ordered by date-currency
        debit_moves = self.filtered(lambda r: r.debit != 0 or r.amount_currency > 0)
        credit_moves = self.filtered(lambda r: r.credit != 0 or r.amount_currency < 0)
        debit_moves = debit_moves.sorted(key=lambda a: (a.date_maturity or a.date, a.currency_id))
        credit_moves = credit_moves.sorted(key=lambda a: (a.date_maturity or a.date, a.currency_id))
        # Compute on which field reconciliation should be based upon:
        if self[0].account_id.currency_id and self[0].account_id.currency_id != self[0].account_id.company_id.currency_id:
            field = 'amount_residual_currency'
        else:
            field = 'amount_residual'
        # if all lines share the same currency, use amount_residual_currency to avoid currency rounding error
        if self[0].currency_id and all([x.amount_currency and x.currency_id == self[0].currency_id for x in self]):
            field = 'amount_residual_currency'

        if self.is_partial_reconcile():
            field = 'partial_amount_residual'

        # Reconcile lines
        ret = self._reconcile_lines(debit_moves, credit_moves, field)
        return ret
