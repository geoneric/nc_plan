import datetime
import uuid
from marshmallow import fields, post_dump, post_load, pre_load, ValidationError
from marshmallow.validate import Length, OneOf
from .. import ma
from .model import PlanModel, statuses


class PlanSchema(ma.Schema):

    class Meta:
        # Fields to include in the serialized result.
        fields = ("user", "pathname", "layer_name", "status", "_links")

    id = fields.UUID(dump_only=True)
    user = fields.UUID(required=True)
    pathname = fields.Str(required=True, validate=Length(min=1))

    # Only available after a plan is registered.
    layer_name = fields.Str(required=False, validate=Length(min=1))

    status = fields.Str(required=True, validate=OneOf(statuses))
    create_stamp = fields.DateTime(dump_only=True,
        missing=datetime.datetime.utcnow().isoformat())
    edit_stamp = fields.DateTime(dump_only=True,
        missing=datetime.datetime.utcnow().isoformat())

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
            if data["status"] == "registered":
                data["_links"]["georeference"] = "{}/georeference".format(
                    data["_links"]["self"])
        else:
            for plan in data:
                if plan["status"] == "registered":
                    plan["_links"]["georeference"] = "{}/georeference".format(
                        plan["_links"]["self"])

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
            layer_name=data.get("layer_name", ""),
            status=data["status"],
            create_stamp=datetime.datetime.utcnow(),
            edit_stamp=datetime.datetime.utcnow()
        )
