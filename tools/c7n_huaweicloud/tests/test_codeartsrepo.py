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