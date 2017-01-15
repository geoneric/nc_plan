import datetime
import uuid
from marshmallow import fields, post_dump, post_load, pre_load, ValidationError
from .. import ma
from .model import PlanModel, statuses


def must_not_be_blank(
        data):
    if not data:
        raise ValidationError("Data not provided")


def must_be_one_of(
        values):

    def validator(
            data):
        if not data in values:
            raise ValidationError(
                "Value must be one of: {}".format(", ".join(values)))

    return validator


class PlanSchema(ma.Schema):

    class Meta:
        # Fields to include in the serialized result.
        fields = ("user", "pathname", "status", "wms", "_links")

    id = fields.UUID(dump_only=True)
    user = fields.UUID(required=True)
    pathname = fields.Str(required=True, validate=must_not_be_blank)
    status = fields.Str(required=True, validate=must_be_one_of(statuses))
    create_stamp = fields.DateTime(dump_only=True,
        missing=datetime.datetime.utcnow().isoformat())
    edit_stamp = fields.DateTime(dump_only=True,
        missing=datetime.datetime.utcnow().isoformat())
    # wms = fields.URL(required=False)

    # Only available after a plan is registered.
    wms = fields.Str(required=False)

    _links = ma.Hyperlinks({
        "self": ma.URLFor("api.plan", user_id="<user>", plan_id="<id>"),
        "collection": ma.URLFor("api.plans", user_id="<user>")
    })


    def key(self,
            many):
        return "plans" if many else "plan"


    @pre_load(
        pass_many=True)
    def unwrap(self,
            data,
            many):
        key = self.key(many)

        if key not in data:
            raise ValidationError(
                "Input data must have a {} key".format(key))

        return data[key]


    @post_dump(
        pass_many=True)
    def wrap(self,
            data,
            many):

        # Move wms uri to _links.
        if not many:
            if data["wms"] is not None:
                data["_links"]["wms"] = data["wms"]
                del data["wms"]
        else:
            for plan in data:
                if plan["wms"] is not None:
                    plan["_links"]["wms"] = plan["wms"]
                    del plan["wms"]

        key = self.key(many)

        return {
            key: data
        }


    @post_load
    def make_object(self,
            data):

        return PlanModel(
            id=uuid.uuid4(),
            user=data["user"],
            pathname=data["pathname"],
            status=data["status"],
            create_stamp=datetime.datetime.utcnow(),
            edit_stamp=datetime.datetime.utcnow(),
            wms=data.get("wms")
        )
