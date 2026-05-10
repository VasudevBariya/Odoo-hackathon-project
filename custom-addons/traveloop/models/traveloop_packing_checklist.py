from odoo import models, fields, api
from odoo.exceptions import ValidationError


class TraveloopPackingChecklist(models.Model):
    _name = 'traveloop.packing.checklist'
    _description = 'Packing Checklist'

    item_name = fields.Char(
        string='Item Name',
        required=True
    )

    quantity = fields.Integer(
        string='Quantity',
        default=1
    )

    is_packed = fields.Boolean(
        string='Packed',
        default=False
    )

    trip_id = fields.Many2one(
        'traveloop.trip',
        string='Trip',
        required=True,
        ondelete='cascade'
    )

    # -----------------------------
    # Validate Quantity
    # -----------------------------
    @api.constrains('quantity')
    def _check_quantity(self):
        for rec in self:
            if rec.quantity <= 0:
                raise ValidationError(
                    'Quantity must be greater than 0'
                )

    # -----------------------------
    # Validate Item Name
    # -----------------------------
    @api.constrains('item_name')
    def _check_item_name(self):
        for rec in self:
            if not rec.item_name or not rec.item_name.strip():
                raise ValidationError(
                    'Item name cannot be empty'
                )

    # -----------------------------
    # Prevent Very Large Quantity
    # -----------------------------
    @api.constrains('quantity')
    def _check_max_quantity(self):
        for rec in self:
            if rec.quantity > 100:
                raise ValidationError(
                    'Quantity cannot be greater than 100'
                )