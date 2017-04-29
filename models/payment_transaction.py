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
                self.env['account.payment'].create({
                    'payment_date': payment_date,
                    'payment_type': 'inbound',
                    'amount': amount,
                    'currency_id': self.currency_id.id,
                    'journal_id': self.acquirer_id.journal_id.id,
                    'partner_type': 'customer',
                    'partner_id': self.partner_id.id,
                    'payment_reference': self.reference,
                    'payment_method_id': self.env.ref('account.account_payment_method_manual_in').id,
                    'transaction_id': self.id,
                }).post()
        else:
            super(PaymentTransaction, self).create_account_payment()
        return True

