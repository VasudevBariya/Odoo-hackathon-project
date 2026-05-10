from odoo import models, fields, api
from odoo.exceptions import ValidationError


class TraveloopBudget(models.Model):
    _name = 'traveloop.budget'
    _description = 'Budget'

    category = fields.Char(
        string='Category',
        required=True
    )

    amount = fields.Float(
        string='Amount',
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
                    'Budget amount must be greater than 0'
                )

    # -----------------------------
    # Validate Category
    # -----------------------------
    @api.constrains('category')
    def _check_category(self):
        for rec in self:
            if not rec.category or not rec.category.strip():
                raise ValidationError(
                    'Category cannot be empty'
                )

    # -----------------------------
    # Prevent Unrealistic Budget
    # -----------------------------
    @api.constrains('amount')
    def _check_max_budget(self):
        for rec in self:
            if rec.amount > 10000000:
                raise ValidationError(
                    'Budget amount is too high'
                )