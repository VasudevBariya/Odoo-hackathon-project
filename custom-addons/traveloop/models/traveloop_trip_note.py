from odoo import models, fields, api
from odoo.exceptions import ValidationError


class TraveloopTripNote(models.Model):
    _name = 'traveloop.trip.note'
    _description = 'Trip Note'

    title = fields.Char(
        string='Title',
        required=True
    )

    note = fields.Text(
        string='Note'
    )

    created_at = fields.Datetime(
        string='Created At',
        default=fields.Datetime.now,
        readonly=True
    )

    trip_id = fields.Many2one(
        'traveloop.trip',
        string='Trip',
        required=True
    )

    user_id = fields.Many2one(
        'traveloop.user',
        string='User'
    )

    # -----------------------------
    # Validate Title
    # -----------------------------
    @api.constrains('title')
    def _check_title(self):
        for rec in self:
            if not rec.title or not rec.title.strip():
                raise ValidationError(
                    'Title cannot be empty'
                )

    # -----------------------------
    # Validate Note
    # -----------------------------
    @api.constrains('note')
    def _check_note(self):
        for rec in self:
            if rec.note:
                if not rec.note.strip():
                    raise ValidationError(
                        'Note cannot be empty spaces'
                    )