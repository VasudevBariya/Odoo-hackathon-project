from odoo import models, fields, api
from odoo.exceptions import ValidationError


class TraveloopActivity(models.Model):
    _name = 'traveloop.activity'
    _description = 'Activity'

    activity_name = fields.Char(
        string='Activity Name',
        required=True
    )

    category = fields.Selection([
        ('sightseeing', 'Sightseeing'),
        ('adventure', 'Adventure'),
        ('food', 'Food'),
        ('other', 'Other')
    ],
        string='Category',
        default='other',
        required=True
    )

    estimated_cost = fields.Float(
        string='Estimated Cost',
        default=0.0
    )

    trip_id = fields.Many2one(
        'traveloop.trip',
        string='Trip',
        required=True,
        ondelete='cascade'
    )

    stop_id = fields.Many2one(
        'traveloop.stop',
        string='Stop',
        ondelete='cascade'
    )

    # -----------------------------
    # Validate Cost
    # -----------------------------
    @api.constrains('estimated_cost')
    def _check_cost(self):
        for rec in self:
            if rec.estimated_cost < 0:
                raise ValidationError(
                    'Estimated cost cannot be negative'
                )

    # -----------------------------
    # Validate Activity Name
    # -----------------------------
    @api.constrains('activity_name')
    def _check_name(self):
        for rec in self:
            if not rec.activity_name or not rec.activity_name.strip():
                raise ValidationError(
                    'Activity name cannot be empty'
                )

    # -----------------------------
    # Prevent Unrealistic Cost
    # -----------------------------
    @api.constrains('estimated_cost')
    def _check_max_cost(self):
        for rec in self:
            if rec.estimated_cost > 1000000:
                raise ValidationError(
                    'Estimated cost is too high'
                )