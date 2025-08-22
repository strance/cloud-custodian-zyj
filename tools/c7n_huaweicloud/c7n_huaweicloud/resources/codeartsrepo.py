# Copyright The Cloud Custodian Authors.
# SPDX-License-Identifier: Apache-2.0

import json
import logging
import os

from c7n_huaweicloud.provider import resources
from c7n_huaweicloud.query import QueryResourceManager, TypeInfo
from c7n_huaweicloud.actions.base import HuaweiCloudBaseAction
from c7n.utils import type_schema, local_session

from huaweicloudsdkcodehub.v4 import ShowProjectWatermarkRequest, UpdateProjectWatermarkRequest, UpdateWatermarkDto
from huaweicloudsdkcore.exceptions import exceptions

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

    """
    schema = type_schema("open")

    def perform_action(self, resource):
        region = os.getenv("HUAWEI_DEFAULT_REGION")
        project_id = resource["id"]
        try:
            response = self.query_project_watermark_status(region, project_id)
            response = json.loads(str(response))
            is_open_watermark = response.get("watermark")
            if is_open_watermark:
                log.info(
                    "[actions]-{codehub-project-open-watermark} has open project watermark fro project_id: [%s], skip.",
                    project_id)
            else:
                can_update = response.get("can_update")
                if not can_update:
                    log.error(
                        "[actions]-{codehub-project-open-watermark} no permission open project watermark fro project_id: [%s], skip.",
                        project_id)
                else:
                    response = self.open_project_watermark(region, project_id)
                    log.info(
                        "[actions]-{codehub-project-open-watermark} open project watermark fro project_id: [%s] success.",
                        project_id)
        except exceptions.ClientRequestException as e:
            log.error("[actions]-{codehub-project-open-watermark} for project_id:[%s] failed.", project_id)
            raise
        return response

    def get_codehub_client(self, region):
        return local_session(self.manager.session_factory).client("codeartsrepo")

    def query_project_watermark_status(self, region, project_id):
        request = ShowProjectWatermarkRequest()
        request.project_id = project_id
        try:
            response = self.get_codehub_client(region).show_project_watermark(request)
            log.info(
                "[actions]-{codehub-project-open-watermark} with project_id: [%s]"
                "query project watermark success, response: [%s]",
                project_id, response)
        except exceptions.ClientRequestException as e:
            log.error(
                "[actions]-{codehub-project-open-watermark} with request:[%s]"
                "query project watermark status failed, cause: "
                "status_code[%s] request_id[%s] error_code[%s] error_msg[%s]",
                request, e.status_code, e.request_id, e.error_code, e.error_msg)
            raise
        return response

    def open_project_watermark(self, region, project_id):
        request = UpdateProjectWatermarkRequest()
        request.project_id = project_id
        request.body = UpdateWatermarkDto(
            watermark=True
        )
        try:
            response = self.get_codehub_client(region).update_project_watermark(request)
            log.info(
                "[actions]-{codehub-project-open-watermark} with project_id:[%s] "
                "open project watermark success.", project_id)
        except exceptions.ClientRequestException as e:
            log.error(
                "[actions]-{codehub-project-open-watermark} with request:[%s]"
                "open project watermark failed, cause: "
                "status_code[%s] request_id[%s] error_code[%s] error_msg[%s]",
                request, e.status_code, e.request_id, e.error_code, e.error_msg)
            raise
        return response
