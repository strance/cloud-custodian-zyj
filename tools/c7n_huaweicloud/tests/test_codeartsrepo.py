from huaweicloud_common import BaseTest


class CodeArtsRepoTest(BaseTest):

    def test_project_query(self):
        factory = self.replay_flight_data("codeartsrepo_project_query")
        p = self.load_policy(
            {"name": "list_projects_v4", "resource": "huaweicloud.codeartsrepo-project"},
            session_factory=factory,
        )
        resources = p.run()
        self.assertEqual(len(resources), 1)

    def test_open_watermark(self):
        factory = self.replay_flight_data("codeartsrepo_open_watermark")
        p = self.load_policy(
            {
                "name": "codeartsrepo_open_watermark",
                "resource": "huaweicloud.codeartsrepo-project",
                "filters": [
                    {
                        "type": "value",
                        "key": "id",
                        "value": "f3754a7faff44f7e92e10caa4cf7ca0c",
                    }
                ],
                "actions": [{"type": "open"}],
            },
            session_factory=factory,
        )
        resources = p.run()
        self.assertEqual(resources[0]["project_id"], "f3754a7faff44f7e92e10caa4cf7ca0c")