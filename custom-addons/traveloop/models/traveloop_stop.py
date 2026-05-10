from odoo import models, fields, api
from odoo.exceptions import ValidationError


class TraveloopStop(models.Model):
    _name = 'traveloop.stop'
    _description = 'Trip Stop'

    city_name = fields.Char(
        string='City Name',
        required=True
    )

    arrival_date = fields.Date(
        string='Arrival Date'
    )

    departure_date = fields.Date(
        string='Departure Date'
    )

    trip_id = fields.Many2one(
        'traveloop.trip',
        string='Trip',
        required=True,
        ondelete='cascade'
    )

    # -----------------------------
    # Validate Stop Dates
    # -----------------------------
    @api.constrains('arrival_date', 'departure_date')
    def _check_dates(self):
        for rec in self:
            if rec.arrival_date and rec.departure_date:
                if rec.departure_date < rec.arrival_date:
                    raise ValidationError(
                        'Departure date cannot be before arrival date'
                    )

    # -----------------------------
    # Validate City Name
    # -----------------------------
    @api.constrains('city_name')
    def _check_city(self):
        for rec in self:
            if not rec.city_name or not rec.city_name.strip():
                raise ValidationError(
                    'City name cannot be empty'
                )

    # -----------------------------
    # Validate Same Day Stop
    # -----------------------------
    @api.constrains('arrival_date', 'departure_date')
    def _check_stop_duration(self):
        for rec in self:
            if rec.arrival_date and rec.departure_date:
                if rec.departure_date == rec.arrival_date:
                    raise ValidationError(
                        'Arrival and departure date cannot be same'
                    )