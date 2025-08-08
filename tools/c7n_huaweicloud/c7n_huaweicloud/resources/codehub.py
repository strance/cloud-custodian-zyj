# Copyright The Cloud Custodian Authors.
# SPDX-License-Identifier: Apache-2.0

import logging
from huaweicloudsdkcore.exceptions import  exceptions
from c7n_huaweicloud.provider import resources
from c7n_huaweicloud.query import QueryResourceManager, TypeInfo
from huaweicloudsdkcodehub.v3 import CreateCommitRequest, CreateCommitRequestBody, CommitAction
from c7n_huaweicloud.actions.base import HuaweiCloudBaseAction
from c7n.utils import type_schema

log = logging.getLogger("custodian.huaweicloud.resources.repo-commit")

@resources.register("codehub-commit")
class CodeHubCommit(QueryResourceManager):
    class resource_type(TypeInfo):
        service = "repo"
        enum_spec = ("list_commits", "request", "page")
        id = "repo_id"


@CodeHubCommit.action_registry.register("create")
class CodeHubCommitCreate(HuaweiCloudBaseAction):
    """ Create a new repo commit

    :Example:

    .. code-block:: yaml

        policies:
          - name: create-codehub-commit
          resource: huaweicloud.codehub-commit
          filters:
            - type: value
              key: id
              value: ${repo_id}
          actions:
            - type: create
              file_path: ${file_path}
              commit_message: ${commit_message}
              branch: ${branch_name}
    """

    schema = type_schema("create", action={'type': 'string'}, file_path={'type': 'string'}, commit_message={'type': 'string'},
                         branch={'type': 'string'})

    def perform_action(self, resource):
        client = self.manager.get_client()
        request = CreateCommitRequest()
        request.repo_id = resource.get("id")
        listActionsbody = [
            CommitAction(
                action= self.data.get("action"),
                file_path=self.data.get("file_path"),
            )
        ]
        request.body = CreateCommitRequestBody(
            actions=listActionsbody,
            commit_message=self.data.get("commit_message"),
            branch=self.data.get("branch")
        )
        try:
            response = client.create_commit(request)
        except exceptions.ClientRequestException as e:
            log.error("[actions]-{codehub-commit} The resource:[codehub-commit] with request:[%s]"
                      "create codehub-commit failed, cause: "
                      "status_code[%s] request_id[%s] error_code[%s] error_msg[%s]",
                      request, e.status_code, e.request_id, e.error_code, e.error_msg)
            raise
        return response
