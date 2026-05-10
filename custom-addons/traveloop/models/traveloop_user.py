from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re


class TraveloopUser(models.Model):
    _name = 'traveloop.user'
    _description = 'Traveloop User'

    name = fields.Char(
        string='Name',
        required=True
    )

    email = fields.Char(
        string='Email',
        required=True
    )

    phone = fields.Char(
        string='Phone'
    )

    city = fields.Char(
        string='City'
    )

    user_id = fields.Many2one(
        'res.users',
        string='Odoo User',
        default=lambda self: self.env.user
    )

    # -----------------------------
    # Validate Name
    # -----------------------------
    @api.constrains('name')
    def _check_name(self):
        for rec in self:
            if not rec.name or not rec.name.strip():
                raise ValidationError(
                    'Name cannot be empty'
                )

    # -----------------------------
    # Validate Email
    # -----------------------------
    @api.constrains('email')
    def _check_email(self):
        for rec in self:

            if not rec.email:
                raise ValidationError(
                    'Email is required'
                )

            pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

            if not re.match(pattern, rec.email):
                raise ValidationError(
                    'Please enter a valid email address'
                )

    # -----------------------------
    # Validate Phone Number
    # -----------------------------
    @api.constrains('phone')
    def _check_phone(self):
        for rec in self:
            if rec.phone:

                if not rec.phone.isdigit():
                    raise ValidationError(
                        'Phone number must contain digits only'
                    )

                if len(rec.phone) != 10:
                    raise ValidationError(
                        'Phone number must be 10 digits'
                    )

    # -----------------------------
    # Prevent Duplicate Email
    # -----------------------------
    @api.constrains('email')
    def _check_duplicate_email(self):
        for rec in self:

            existing = self.search([
                ('email', '=', rec.email),
                ('id', '!=', rec.id)
            ])

            if existing:
                raise ValidationError(
                    'Email already exists'
                )