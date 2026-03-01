# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools
from odoo import Command, modules


class RecurringEntriesWizard(models.TransientModel):
    """wizard for generating journal entries for recurring entries"""

    _name = 'recurring.entries.wizard'
    _description = 'Recurring Entries Wizard'

    starting_date = fields.Date(string='Starting Date', required=True)
    ending_date = fields.Date(string='Ending Date', required=True)
    recurring_payment_ids = fields.Many2many('recurring.template','payments',  string='Recurring Entries')

    @api.onchange('starting_date', 'ending_date')
    def _onchange_date(self):
        """filters recurring entries based on starting date and ending date"""
        self.recurring_payment_ids = self.env['recurring.template'].search([('state','=','running'),('start_date','>=',self.starting_date),('end_date','<=',self.ending_date)])
        print("rrr",self.recurring_payment_ids)


    def action_generate_entries(self):
        """generate entries for recurring entries"""
        print('Generating Recurring Entries')
        print(self.recurring_payment_ids)

        for rec in self.recurring_payment_ids:
           print("oooo",rec)
           print("amount",rec.amount)
           print("name",rec.name)
           rec.env['account.move'].create({
               'move_type': 'entry',
               'journal_id': rec.journal_id.id,
               'ref':rec.name,
               'amount_total_signed': rec.amount,
               'line_ids': [
                    Command.create({'debit': 0.0, 'credit':rec.amount, 'account_id': rec.credit_account_id.id}),
                    Command.create({'debit': rec.amount, 'credit': 0.0, 'account_id':  rec.debit_account_id.id}),
                ],
                })















