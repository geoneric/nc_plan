from werkzeug.exceptions import *
from flask_restful import Resource
from flask import request
from .. import db
from .model import PlanModel
from .schema import PlanSchema


plan_schema = PlanSchema()


class PlanResource(Resource):

    def get(self,
            user_id,
            plan_id):

        # user_id is not needed
        plan = PlanModel.query.get(plan_id)

        if plan is None or plan.user != user_id:
            raise BadRequest("Plan could not be found")


        data, errors = plan_schema.dump(plan)

        if errors:
            raise InternalServerError(errors)


        return data


class PlansResource(Resource):

    def get(self,
            user_id):

        plans = PlanModel.query.filter_by(user=user_id)
        data, errors = plan_schema.dump(plans, many=True)

        if errors:
            raise InternalServerError(errors)

        assert isinstance(data, dict), data


        return data


class PlansAllResource(Resource):


    # TODO Only call this from admin interface!
    def get(self):

        plans = PlanModel.query.all()
        data, errors = plan_schema.dump(plans, many=True)

        if errors:
            raise InternalServerError(errors)

        assert isinstance(data, dict), data


        return data


    def post(self):

        json_data = request.get_json()

        if json_data is None:
            raise BadRequest("No input data provided")


        # Validate and deserialize input.
        plan, errors = plan_schema.load(json_data)

        if errors:
            raise UnprocessableEntity(errors)


        # Write plan to database.
        db.session.add(plan)
        db.session.commit()


        # From record in database to dict representing a plan.
        data, errors = plan_schema.dump(PlanModel.query.get(plan.id))
        assert not errors, errors
        assert isinstance(data, dict), data


        return data, 201
