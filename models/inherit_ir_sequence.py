from datetime import datetime, timedelta, date as _date

from odoo import models, fields


class InheritIrSequence(models.Model):
    _inherit = 'ir.sequence'

    date_range_interval = fields.Selection(
        string='Interval',
        selection=[
            ('yearly', 'Yearly'),
            ('monthly', 'Monthly'),
            ('weekly', 'Weekly'),
            ('daily', 'Daily'),
        ],
        default='yearly',
        required=True,
    )

    def last_day_of_month(self, any_day):
        next_month = any_day.replace(day=28) + timedelta(days=4)  # this will never fail
        return next_month - timedelta(days=next_month.day)

    def _create_date_range_seq(self, date):
        year = fields.Date.from_string(date).strftime('%Y')
        month = fields.Date.from_string(date).strftime('%m')

        date_from = '{}-01-01'.format(year)
        date_to = '{}-12-31'.format(year)

        if self.date_range_interval == 'monthly':
            date_from = '{year}-{month}-01'.format(year=year, month=month)
            date_to = '{}'.format(self.last_day_of_month(_date(int(year), int(month), 1, )))
        elif self.date_range_interval == 'weekly':
            date_from = fields.Date.from_string(date).strftime('%Y-%m-%d')
            date_to = datetime.strptime(date_from, '%Y-%m-%d') + timedelta(weeks=1)
        elif self.date_range_interval == 'daily':
            date_from = fields.Date.from_string(date).strftime('%Y-%m-%d')
            date_to = datetime.strptime(date_from, '%Y-%m-%d') + timedelta(days=1)

        date_range = self.env['ir.sequence.date_range'].search(
            [('sequence_id', '=', self.id), ('date_from', '>=', date), ('date_from', '<=', date_to)],
            order='date_from desc', limit=1)
        if date_range:
            date_to = datetime.strptime(date_range.date_from, '%Y-%m-%d') + timedelta(days=-1)
            date_to = date_to.strftime('%Y-%m-%d')
        date_range = self.env['ir.sequence.date_range'].search(
            [('sequence_id', '=', self.id), ('date_to', '>=', date_from), ('date_to', '<=', date)],
            order='date_to desc', limit=1)
        if date_range:
            date_from = datetime.strptime(date_range.date_to, '%Y-%m-%d') + timedelta(days=1)
            date_from = date_from.strftime('%Y-%m-%d')
        seq_date_range = self.env['ir.sequence.date_range'].sudo().create({
            'date_from': date_from,
            'date_to': date_to,
            'sequence_id': self.id,
        })
        return seq_date_range
