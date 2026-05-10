from odoo import models, fields, api
from odoo.exceptions import ValidationError


class TraveloopSavedTrip(models.Model):
    _name = 'traveloop.saved.trip'
    _description = 'Saved Trip'

    user_id = fields.Many2one(
        'traveloop.user',
        string='User',
        required=True,
        ondelete='cascade'
    )

    trip_id = fields.Many2one(
        'traveloop.trip',
        string='Trip',
        required=True,
        ondelete='cascade'
    )

    saved_date = fields.Datetime(
        string='Saved Date',
        default=fields.Datetime.now,
        readonly=True
    )

    # -----------------------------
    # Prevent Duplicate Save
    # -----------------------------
    @api.constrains('user_id', 'trip_id')
    def _check_duplicate_save(self):
        for rec in self:

            if not rec.user_id or not rec.trip_id:
                raise ValidationError(
                    'User and Trip are required'
                )

            existing = self.search([
                ('user_id', '=', rec.user_id.id),
                ('trip_id', '=', rec.trip_id.id),
                ('id', '!=', rec.id)
            ], limit=1)

            if existing:
                raise ValidationError(
                    'Trip already saved by this user'
                )