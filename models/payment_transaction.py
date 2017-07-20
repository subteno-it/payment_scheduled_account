# -*- coding: utf-8 -*-
##############################################################################
#
#    payment_scheduled_account module for OpenERP, Allows to create multiple account payments for the same transaction
#    Copyright (C) 2016 SYLEAM Info Services (<http://www.syleam.fr>)
#              Sebastien LANGE <sebastien.lange@syleam.fr>
#
#    This file is a part of payment_scheduled_account
#
#    payment_scheduled_account is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    payment_scheduled_account is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, api, fields
from openerp.tools import float_round


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
                payment_data.update(payment_date=payment_date, amount=amount)
                self.env['account.payment'].create(payment_data).post()
        else:
            super(PaymentTransaction, self).create_account_payment()
        return True


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
