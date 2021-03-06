from sqlalchemy_utils import URLType, UUIDType
from .. import db


statuses = [

    "uploaded",

    "registered",

    "georeferenced",

    "classified"
]


class PlanModel(db.Model):

    id = db.Column(UUIDType(), primary_key=True)
    user = db.Column(UUIDType())
    pathname = db.Column(db.UnicodeText)
    layer_name = db.Column(db.UnicodeText)
    status = db.Column(db.Unicode(20))
    create_stamp = db.Column(db.DateTime)
    edit_stamp = db.Column(db.DateTime)
