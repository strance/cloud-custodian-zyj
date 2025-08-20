# Copyright The Cloud Custodian Authors.
# SPDX-License-Identifier: Apache-2.0

import logging
from huaweicloudsdkcore.exceptions import  exceptions
from c7n_huaweicloud.provider import resources
from c7n_huaweicloud.query import QueryResourceManager, TypeInfo
from c7n_huaweicloud.actions.base import HuaweiCloudBaseAction
from c7n.utils import type_schema

log = logging.getLogger("custodian.huaweicloud.resources.codeartsrepo-project")

@resources.register("codeartsrepo-project")
class CodeaArtsRepoProject(QueryResourceManager):
    class resource_type(TypeInfo):
        service = "codeartsrepo-project"
        enum_spec = ("list_projects_v4", "projects", "offset")
        id = "project_id"
        tag_resource_type = "codeartsrepo"


@CodeaArtsRepoProject.action_registry.register("open")
class CodeaArtsRepoProjectOpenWaterMark(HuaweiCloudBaseAction):
    """ CodeArtsRepo open watermark for project.

    :Example:

    .. code-block:: yaml

        policies:
          - name: CodeArtsRepo-project-open-watermark
          resource: huaweicloud.codeartsrepo-project
          filters:
            - type: value
              key: id
              value: ${id}
          actions:
            - type: open
              file_path: ${file_path}
              commit_message: ${commit_message}
              branch: ${branch_name}
    """
    schema =  type_schema("open")

    def perform_action(self, resource):

        request = ""
        try:
            log.info("is test open watermark action.")
        except exceptions.ClientRequestException as e:
            log.error("[actions]-{codehub-commit} The resource:[codehub-commit] with request:[%s]"
                      "create codehub-commit failed, cause: "
                      "status_code[%s] request_id[%s] error_code[%s] error_msg[%s]",
                      request, e.status_code, e.request_id, e.error_code, e.error_msg)
            raise
        return