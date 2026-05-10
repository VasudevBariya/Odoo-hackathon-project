from odoo import models, fields, api
from odoo.exceptions import ValidationError


class TraveloopTrip(models.Model):
    _name = 'traveloop.trip'
    _description = 'Trip'

    trip_name = fields.Char(
        string='Trip Name',
        required=True
    )

    destination = fields.Char(
        string='Destination'
    )

    start_date = fields.Date(
        string='Start Date'
    )

    end_date = fields.Date(
        string='End Date'
    )

    duration_days = fields.Integer(
        string='Duration (Days)',
        compute='_compute_duration',
        store=True
    )

    status = fields.Selection([
        ('draft', 'Draft'),
        ('planned', 'Planned'),
        ('completed', 'Completed')
    ],
        string='Status',
        default='draft'
    )

    total_budget = fields.Float(
        string='Total Budget'
    )

    total_spent = fields.Float(
        string='Total Spent',
        compute='_compute_total_spent',
        store=True
    )

    remaining_budget = fields.Float(
        string='Remaining Budget',
        compute='_compute_remaining_budget',
        store=True
    )

    user_id = fields.Many2one(
        'res.users',
        string='User',
        default=lambda self: self.env.user
    )

    stop_ids = fields.One2many(
        'traveloop.stop',
        'trip_id',
        string='Stops'
    )

    activity_ids = fields.One2many(
        'traveloop.activity',
        'trip_id',
        string='Activities'
    )

    expense_ids = fields.One2many(
        'traveloop.expense',
        'trip_id',
        string='Expenses'
    )

    # -----------------------------
    # Auto Calculate Total Spent
    # -----------------------------
    @api.depends('expense_ids.amount')
    def _compute_total_spent(self):
        for rec in self:
            rec.total_spent = sum(
                rec.expense_ids.mapped('amount')
            )

    # -----------------------------
    # Remaining Budget
    # -----------------------------
    @api.depends('total_budget', 'total_spent')
    def _compute_remaining_budget(self):
        for rec in self:
            rec.remaining_budget = (
                rec.total_budget - rec.total_spent
            )

    # -----------------------------
    # Auto Calculate Duration
    # -----------------------------
    @api.depends('start_date', 'end_date')
    def _compute_duration(self):
        for rec in self:
            if rec.start_date and rec.end_date:
                rec.duration_days = (
                    rec.end_date - rec.start_date
                ).days + 1
            else:
                rec.duration_days = 0

    # -----------------------------
    # Trip Name Validation
    # -----------------------------
    @api.constrains('trip_name')
    def _check_trip_name(self):
        for rec in self:
            if not rec.trip_name or not rec.trip_name.strip():
                raise ValidationError(
                    'Trip name cannot be empty'
                )

    # -----------------------------
    # Destination Validation
    # -----------------------------
    @api.constrains('destination')
    def _check_destination(self):
        for rec in self:
            if rec.destination:
                if not rec.destination.strip():
                    raise ValidationError(
                        'Destination cannot be empty'
                    )

    # -----------------------------
    # Date Validation
    # -----------------------------
    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for rec in self:
            if rec.start_date and rec.end_date:
                if rec.end_date < rec.start_date:
                    raise ValidationError(
                        'End date cannot be before start date'
                    )

    # -----------------------------
    # Budget Validation
    # -----------------------------
    @api.constrains('total_budget')
    def _check_budget(self):
        for rec in self:
            if rec.total_budget < 0:
                raise ValidationError(
                    'Budget cannot be negative'
                )

    # -----------------------------
    # Status Actions
    # -----------------------------
    def action_plan_trip(self):
        self.write({
            'status': 'planned'
        })

    def action_complete_trip(self):
        self.write({
            'status': 'completed'
        })

    def action_reset_trip(self):
        self.write({
            'status': 'draft'
        })