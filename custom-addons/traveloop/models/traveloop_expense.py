from odoo import models, fields, api
from odoo.exceptions import ValidationError


class TraveloopExpense(models.Model):
    _name = 'traveloop.expense'
    _description = 'Trip Expense'

    expense_name = fields.Char(
        string='Expense Name',
        required=True
    )

    category = fields.Selection([
        ('food', 'Food'),
        ('hotel', 'Hotel'),
        ('transport', 'Transport'),
        ('shopping', 'Shopping'),
        ('other', 'Other')
    ],
        string='Category',
        default='other',
        required=True
    )

    amount = fields.Float(
        string='Amount',
        required=True
    )

    expense_date = fields.Date(
        string='Expense Date',
        required=True
    )

    trip_id = fields.Many2one(
        'traveloop.trip',
        string='Trip',
        required=True,
        ondelete='cascade'
    )

    # -----------------------------
    # Validate Amount
    # -----------------------------
    @api.constrains('amount')
    def _check_amount(self):
        for rec in self:
            if rec.amount <= 0:
                raise ValidationError(
                    'Expense amount must be greater than 0'
                )

    # -----------------------------
    # Validate Expense Name
    # -----------------------------
    @api.constrains('expense_name')
    def _check_expense_name(self):
        for rec in self:
            if not rec.expense_name or not rec.expense_name.strip():
                raise ValidationError(
                    'Expense name cannot be empty'
                )

    # -----------------------------
    # Validate Expense Date
    # -----------------------------
    @api.constrains('expense_date')
    def _check_date(self):
        for rec in self:
            if not rec.expense_date:
                raise ValidationError(
                    'Please select expense date'
                )

    # -----------------------------
    # Prevent Unrealistic Amount
    # -----------------------------
    @api.constrains('amount')
    def _check_max_amount(self):
        for rec in self:
            if rec.amount > 1000000:
                raise ValidationError(
                    'Expense amount is too high'
                )