import datetime
import unittest
import uuid
from nc_plan import create_app
from nc_plan.api.schema import *


class PlanSchemaTestCase(unittest.TestCase):


    def setUp(self):
        self.app = create_app("testing")

        self.app_context = self.app.app_context()
        self.app_context.push()

        self.client = self.app.test_client()
        self.schema = PlanSchema()


    def tearDown(self):
        self.schema = None

        self.app_context.pop()


    def test_empty1(self):
        client_data = {
        }
        data, errors = self.schema.load(client_data)

        self.assertTrue(errors)
        self.assertEqual(errors, {
            "_schema": ["Input data must have a plan key"]
        })


    def test_empty2(self):
        client_data = {
            "plan": {}
        }
        data, errors = self.schema.load(client_data)

        self.assertTrue(errors)
        self.assertEqual(errors, {
            "user": ["Missing data for required field."],
            "pathname": ["Missing data for required field."],
            "status": ["Missing data for required field."],
        })


    def test_invalid_user(self):
        client_data = {
            "plan": {
                "user": "blah",
                "pathname": "my_path/blah_plan.png",
                "status": "uploaded",
            }
        }
        data, errors = self.schema.load(client_data)

        self.assertTrue(errors)
        self.assertEqual(errors, {
            "user": ["Not a valid UUID."],
        })


    def test_empty_pathname(self):
        client_data = {
            "plan": {
                "user": uuid.uuid4(),
                "pathname": "",
                "status": "uploaded",
            }
        }
        data, errors = self.schema.load(client_data)

        self.assertTrue(errors)
        self.assertEqual(errors, {
            "pathname": ["Shorter than minimum length 1."]
        })


    def test_empty_layer_name(self):
        client_data = {
            "plan": {
                "user": uuid.uuid4(),
                "pathname": "/my_path",
                "layer_name": "",
                "status": "registered",
            }
        }
        data, errors = self.schema.load(client_data)

        self.assertTrue(errors)
        self.assertEqual(errors, {
            "layer_name": ["Shorter than minimum length 1."]
        })


    def test_invalid_status(self):
        client_data = {
            "plan": {
                "user": uuid.uuid4(),
                "pathname": "my_path/blah_plan.png",
                "status": "invalid",
            }
        }
        data, errors = self.schema.load(client_data)

        self.assertTrue(errors)
        self.assertEqual(errors, {
            "status": ["Not a valid choice."]
        })


    def test_usecase1(self):

        client_data = {
            "plan": {
                "user": uuid.uuid4(),
                "pathname": "my_path/blah_plan.png",
                "status": "uploaded",
            }
        }
        data, errors = self.schema.load(client_data)

        self.assertFalse(errors)

        self.assertTrue(hasattr(data, "id"))
        self.assertTrue(isinstance(data.id, uuid.UUID))

        self.assertTrue(hasattr(data, "user"))
        self.assertTrue(isinstance(data.user, uuid.UUID))

        self.assertTrue(hasattr(data, "pathname"))
        self.assertEqual(data.pathname, "my_path/blah_plan.png")

        self.assertTrue(hasattr(data, "layer_name"))
        self.assertEqual(data.layer_name, "")

        self.assertTrue(hasattr(data, "create_stamp"))
        self.assertTrue(isinstance(data.create_stamp, datetime.datetime))

        self.assertTrue(hasattr(data, "edit_stamp"))
        self.assertTrue(isinstance(data.edit_stamp, datetime.datetime))

        self.assertTrue(hasattr(data, "status"))
        self.assertEqual(data.status, "uploaded")

        data.id = uuid.uuid4()
        data, errors = self.schema.dump(data)

        self.assertFalse(errors)
        self.assertTrue("plan" in data)

        plan = data["plan"]

        self.assertTrue("id" not in plan)
        self.assertTrue("user" in plan)
        self.assertTrue("pathname" in plan)
        self.assertTrue("layer_name" in plan)
        self.assertTrue("status" in plan)
        self.assertTrue("create_stamp" not in plan)
        self.assertTrue("edit_stamp" not in plan)

        self.assertTrue("_links" in plan)

        links = plan["_links"]

        self.assertTrue("self" in links)
        self.assertTrue("collection" in links)


    def test_usecase2(self):

        client_data = {
            "plan": {
                "user": uuid.uuid4(),
                "pathname": "my_path/blah_plan.png",
                "status": "uploaded",
            }
        }
        data, errors = self.schema.load(client_data)

        self.assertFalse(errors)

        data.id = uuid.uuid4()
        data, errors = self.schema.dump(data)

        self.assertFalse(errors)
        self.assertTrue("plan" in data)

        plan = data["plan"]

        self.assertTrue("_links" in plan)

        links = plan["_links"]


if __name__ == "__main__":
    unittest.main()
