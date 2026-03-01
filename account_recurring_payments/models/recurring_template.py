# -*- coding: utf-8 -*-
from odoo import models,fields,api
from datetime import timedelta,datetime


class RecurringTemplate(models.Model):
    """ Recurring Template Model for Recurring Entries """
    _name = 'recurring.template'
    _rec_name = 'name'
    _description = 'Recurring Template'

    name = fields.Char(string="Name",required=True)
    state = fields.Selection(string='State', selection=[('draft', 'Draft'),('running', 'Running')],default='draft')
    pay_time = fields.Selection(string='Pay Time', selection=[('direct', 'Pay Directly'),('indirect', 'Pay Indirectly')])
    credit_account_id = fields.Many2one('account.account',string='Credit Account', required=True)
    debit_account_id = fields.Many2one('account.account', string='Debit Account', required=True)
    journal_id = fields.Many2one('account.journal', string='Journal', required=True,domain=[('type','=','general')])
    recurring_period = fields.Selection([('weeks', 'Weekly'), ('months', 'Monthly'), ('years', 'Yearly')],string='Recurring Period', required=True)
    recurring_interval = fields.Float(string='Recurring Interval', required=True)
    start_date = fields.Datetime(string='Start Date', required=True)
    next_date = fields.Datetime(string='Next Date',readonly=True)
    end_date = fields.Datetime(string='End Date', required=True)
    amount = fields.Monetary(string='Amount', required=True)
    currency_id = fields.Many2one("res.currency", string="Currency", tracking=True)
    generate_journal_as = fields.Char(string='Generate Journal As', required=True)
    description = fields.Char(string='Description')



    @api.constrains('recurring_period','recurring_interval','start_date')
    def _compute_next_date(self):
        """compute next date based on recurring interval,period and start date"""
        if self.recurring_period:
            period = str(self.recurring_period)
            print(period)
            interval = self.recurring_interval
            if period == 'weeks':
                 delta = timedelta(days = (7 * interval))
            elif period == 'months':
                 delta = timedelta(days=(30 * interval))
            else:
                delta = timedelta(days=(365 * interval))
            print(delta)


            self.next_date = (self.start_date+delta)
            print(self.start_date)
            print(self.next_date)
        else:
            self.next_date = None









