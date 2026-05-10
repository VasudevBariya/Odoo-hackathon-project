# -*- coding: utf-8 -*-
# Import order matters: parent models must load before child models
# that reference them via Many2one.

from . import traveloop_user               # 1. Users (no dependencies)
from . import traveloop_trip               # 2. Trips  → User
from . import traveloop_stop               # 3. Stops  → Trip
from . import traveloop_activity           # 4. Activities → Stop, Trip
from . import traveloop_budget             # 5. Budget → Trip
from . import traveloop_expense            # 6. Expenses → Trip, Stop
from . import traveloop_packing_checklist  # 7. Checklist → Trip
from . import traveloop_trip_note          # 8. Notes → Trip, Stop
from . import traveloop_saved_trip         # 9. Saved trips → User, Trip
