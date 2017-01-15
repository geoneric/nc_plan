import os
from nc_plan import create_app


app = create_app(os.getenv("NC_PLAN_CONFIGURATION"))
