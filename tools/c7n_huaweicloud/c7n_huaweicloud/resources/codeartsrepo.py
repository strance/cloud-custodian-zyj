# Copyright The Cloud Custodian Authors.
# SPDX-License-Identifier: Apache-2.0

import logging
from huaweicloudsdkcore.exceptions import  exceptions
from c7n_huaweicloud.provider import resources
from c7n_huaweicloud.query import QueryResourceManager, TypeInfo
from huaweicloudsdkcodehub.v3 import CreateCommitRequest, CreateCommitRequestBody, CommitAction
from c7n_huaweicloud.actions.base import HuaweiCloudBaseAction
from c7n.utils import type_schema

log = logging.getLogger("custodian.huaweicloud.resources.codeartsrepo-repository")

@resources.register("codeartsrepo-repository")
class CodeaArtsRepoRepository(QueryResourceManager):
    class resource_type(TypeInfo):
        service = "codeartsrepo-repository"
        enum_spec = ("get_all_repository_by_project_id", "result.repositorys", "pagesize", 10)
        id = "id"


@CodeaArtsRepoRepository.action_registry.register("create")
class CodeaArtsRepoRepositoryOpenWaterMark(HuaweiCloudBaseAction):
    """ CodeArtsRepo open watermark for repository.

    :Example:

    .. code-block:: yaml

        policies:
          - name: CodeArtsRepo-repository-open-watermark
          resource: huaweicloud.codeartsrepo-repository
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

    schema = type_schema("create", action={'type': 'string'}, file_path={'type': 'string'}, commit_message={'type': 'string'},
                         branch={'type': 'string'}, repo_id={'type': 'integer'})

    def perform_action(self, resource):
        client = self.manager.get_client()
        request = CreateCommitRequest()
        request.repo_id = self.data.get("repo_id")
        log.info("codehub perform_action data [%s]", self.data)
        listActionsbody = [
            CommitAction(
                action= self.data.get("action"),
                file_path=self.data.get("file_path"),
            )
        ]
        request.body = CreateCommitRequestBody(
            branch=self.data.get("branch"),
            commit_message=self.data.get("commit_message"),
            actions=listActionsbody,
        )
        log.info("codehub perform_action request [%s]", request)
        try:
            log.info("codehub perform_action before request.")
            response = client.create_commit(request)
            log.info("codehub perform_action before response [%s].", response)
        except exceptions.ClientRequestException as e:
            log.error("[actions]-{codehub-commit} The resource:[codehub-commit] with request:[%s]"
                      "create codehub-commit failed, cause: "
                      "status_code[%s] request_id[%s] error_code[%s] error_msg[%s]",
                      request, e.status_code, e.request_id, e.error_code, e.error_msg)
            raise
        return response


@resources.register("codeartsrepo-watermark")
class CodeArtsRepoWaterMark(QueryResourceManager):
    class resource_type(TypeInfo):
        service = "codeartsrepo-watermark"
        enum_spec = ("get_all_watermark", "*", None)