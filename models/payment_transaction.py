# -*- coding: utf-8 -*-
# Copyright 2016 SYLEAM Info Services
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api, fields
from odoo.tools import float_round


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    @api.multi
    def create_account_payment(self):
        self.ensure_one()
        if self.acquirer_id.payment_term_id:
            totlines = self.acquirer_id.payment_term_id.with_context(
                currency_id=self.currency_id.id
            ).compute(
                float_round(self.amount, 2),
                fields.Date.context_today(self)
            )[0]
            for payment_date, amount in sorted(totlines):
                payment_data = self._prepare_payment_data()
                payment_data.update(
                    payment_date=payment_date,
                    amount=amount,
                    payment_difference_handling='open',
                )
                self.env['account.payment'].create(payment_data).post()
        else:
            super(PaymentTransaction, self).create_account_payment()
        return True

