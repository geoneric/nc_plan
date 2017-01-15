import os.path
import unittest
import uuid
from flask import current_app, json
from nc_plan import create_app, db
from nc_plan.api.schema import *


class PlanTestCase(unittest.TestCase):


    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

        self.user1 = uuid.uuid4()
        self.user2 = uuid.uuid4()
        self.user3 = uuid.uuid4()


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def post_plans(self):

        payloads = [
            {
                "user": self.user1,
                "pathname": "/some_path/plan1.png",
                "status": "uploaded",
            },
            {
                "user": self.user2,
                "pathname": "/some_path/plan2.png",
                "status": "registered",
                "wms": "assessment/geoserver/my_plan/wms/plan2"
            },
        ]

        for payload in payloads:
            response = self.client.post("/plans",
                data=json.dumps({"plan": payload}),
                content_type="application/json")
            data = response.data.decode("utf8")

            self.assertEqual(response.status_code, 201, "{}: {}".format(
                response.status_code, data))


    def test_get_all_plans1(self):
        # No plans posted.
        response = self.client.get("/plans")
        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 200, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("plans" in data)
        self.assertEqual(data["plans"], [])


    def test_get_all_plans2(self):
        # Some plans posted.
        self.post_plans()

        response = self.client.get("/plans")
        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 200, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("plans" in data)

        plans = data["plans"]

        self.assertEqual(len(plans), 2)


    def test_get_plan(self):
        self.post_plans()

        response = self.client.get("/plans")
        data = response.data.decode("utf8")
        data = json.loads(data)
        plans = data["plans"]
        plan = plans[0]
        uri = plan["_links"]["self"]
        response = self.client.get(uri)

        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 200, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("plan" in data)

        plan = data["plan"]

        self.assertEqual(data["plan"], plan)

        self.assertTrue("id" not in plan)
        self.assertTrue("create_stamp" not in plan)
        self.assertTrue("edit_stamp" not in plan)

        self.assertTrue("user" in plan)
        self.assertEqual(plan["user"], str(self.user1))

        self.assertTrue("pathname" in plan)
        self.assertEqual(plan["pathname"], "/some_path/plan1.png")

        self.assertTrue("status" in plan)
        self.assertEqual(plan["status"], "uploaded")

        self.assertTrue("_links" in plan)

        links = plan["_links"]

        self.assertTrue("self" in links)
        self.assertEqual(links["self"], uri)

        self.assertTrue("collection" in links)
        self.assertFalse("wms" in links)


    def test_get_unexisting_plan(self):
        self.post_plans()

        response = self.client.get("/plans")
        data = response.data.decode("utf8")
        data = json.loads(data)
        plans = data["plans"]
        plan = plans[0]
        uri = plan["_links"]["self"]
        # Invalidate uri
        uri = os.path.join(os.path.split(uri)[0], str(uuid.uuid4()))
        response = self.client.get(uri)

        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 400, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("message" in data)


    def test_post_plan(self):
        user_id = uuid.uuid4()
        payload = {
            "user": user_id,
            "pathname": "/some_path/plan.png",
            "status": "registered",
            "wms": "assessment/geoserver/my_plan/wms/plan"
        }
        response = self.client.post("/plans",
            data=json.dumps({"plan": payload}),
            content_type="application/json")
        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 201, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("plan" in data)

        plan = data["plan"]

        self.assertTrue("id" not in plan)
        self.assertTrue("create_stamp" not in plan)
        self.assertTrue("edit_stamp" not in plan)

        self.assertTrue("pathname" in plan)
        self.assertEqual(plan["pathname"], "/some_path/plan.png")

        self.assertTrue("_links" in plan)

        links = plan["_links"]

        self.assertTrue("self" in links)
        self.assertTrue("collection" in links)
        self.assertTrue("wms" in links)


    def test_post_bad_request(self):
        response = self.client.post("/plans")
        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 400, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("message" in data)


    def test_post_unprocessable_entity(self):
        payload = ""
        response = self.client.post("/plans",
            data=json.dumps({"plan": payload}),
            content_type="application/json")
        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 422, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("message" in data)


if __name__ == "__main__":
    unittest.main()
