from . import api_restful
from .resource import *


# All plans.
# - Get all plans
# - Post plan by user-id
api_restful.add_resource(PlansAllResource,
    "/plans",
    endpoint="plans_all")

# Plan by user-id and plan-id.
# - Get plan by user-id and plan-id
# - Patch plan by user-id and plan-id
api_restful.add_resource(PlanResource,
    "/plans/<uuid:user_id>/<uuid:plan_id>",
    endpoint="plan")

# Plans by user-id.
# - Get plans by user-id
api_restful.add_resource(PlansResource,
    "/plans/<uuid:user_id>",
    endpoint="plans")
