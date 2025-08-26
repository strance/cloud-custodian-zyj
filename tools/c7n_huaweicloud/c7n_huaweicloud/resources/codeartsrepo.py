# Copyright The Cloud Custodian Authors.
# SPDX-License-Identifier: Apache-2.0

import json
import logging

from c7n_huaweicloud.provider import resources
from c7n_huaweicloud.query import QueryResourceManager, TypeInfo
from c7n_huaweicloud.actions.base import HuaweiCloudBaseAction
from c7n.utils import type_schema, local_session

from huaweicloudsdkcodehub.v4 import ShowProjectWatermarkRequest, UpdateProjectWatermarkRequest, UpdateWatermarkDto, \
    ListProjectProtectedBranchesRequest, CreateProjectProtectedBranchesRequest, ProtectedBranchBodyApiDto, \
    ProtectedActionBasicApiDto, ShowProjectSettingsInheritCfgRequest, UpdateProjectSettingsInheritCfgRequest, \
    SettingsInheritCfgBodyApiDto, ProjectSettingsInheritCfgDto
from huaweicloudsdkcore.exceptions import exceptions

log = logging.getLogger("custodian.huaweicloud.resources.codeartsrepo-project")


@resources.register("codeartsrepo-project")
class CodeaArtsRepoProject(QueryResourceManager):
    class resource_type(TypeInfo):
        service = "codeartsrepo-project"
        enum_spec = ("list_projects_v4", "projects", "offset")
        id = "project_id"
        tag_resource_type = "codeartsrepo"


@CodeaArtsRepoProject.action_registry.register("open-watermark")
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
            - type: open-watermark

    """
    schema = type_schema("open-watermark")

    def perform_action(self, resource):
        project_id = resource["id"]
        try:
            response = self.query_project_watermark_status(project_id)
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
                    response = self.open_project_watermark(project_id)
                    log.info(
                        "[actions]-{codehub-project-open-watermark} open project watermark fro project_id: [%s] success.",
                        project_id)
        except exceptions.ClientRequestException as e:
            log.error("[actions]-{codehub-project-open-watermark} for project_id:[%s] failed.", project_id)
            raise
        return response

    def get_codehub_client(self):
        return local_session(self.manager.session_factory).client("codeartsrepo")

    def query_project_watermark_status(self, project_id):
        request = ShowProjectWatermarkRequest()
        request.project_id = project_id
        try:
            response = self.get_codehub_client().show_project_watermark(request)
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

    def open_project_watermark(self, project_id):
        request = UpdateProjectWatermarkRequest()
        request.project_id = project_id
        request.body = UpdateWatermarkDto(
            watermark=True
        )
        try:
            response = self.get_codehub_client().update_project_watermark(request)
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


@CodeaArtsRepoProject.action_registry.register("create-protected-branches")
class CodeaArtsRepoProjectCreateProtectedBranches(HuaweiCloudBaseAction):
    """ CodeArtsRepo create protected branches for project.

    :Example:

    .. code-block:: yaml

        policies:
          - name: CodeArtsRepo-project-create-protected-branches
          resource: huaweicloud.codeartsrepo-project
          filters:
            - type: value
              key: id
              value: ${id}
          actions:
            - type: create-protected-branches
              branch_name: *
              push_action: push
              push_user_ids: []
              push_user_team_ids: []
              push_related_role_ids: []
              merge_action: merge
              merge_user_ids: []
              merge_user_team_ids: []
              merge_related_role_ids: []
    """

    schema = type_schema("create-protected-branches", branch_name={'type': 'string'}, push_action={'type': 'string'},
                         push_enable={"type": "boolean"}, push_user_ids={"type": "array"},
                         push_user_team_ids={"type": "array"}, push_related_role_ids={"type": "array"},
                         merge_action={'type': 'string'}, merge_enable={"type": "boolean"},
                         merge_user_ids={"type": "array"},
                         merge_user_team_ids={"type": "array"}, merge_related_role_ids={"type": "array"})

    def perform_action(self, resource):
        response = {}
        project_id = resource["id"]
        branch_name = self.data.get("branch_name")
        push_action = self.data.get("push_action")
        push_enable = self.data.get("push_enable")
        push_user_ids = self.data.get("push_user_ids")
        push_user_team_ids = self.data.get("push_user_team_ids")
        push_related_role_ids = self.data.get("push_related_role_ids")
        merge_action = self.data.get("merge_action")
        merge_enable = self.data.get("merge_enable")
        merge_user_ids = self.data.get("merge_user_ids")
        merge_user_team_ids = self.data.get("merge_user_team_ids")
        merge_related_role_ids = self.data.get("merge_related_role_ids")

        try:
            protected_branches = self.query_project_protected_branches(project_id)
            if not self.need_create_protected_branches(protected_branches):
                log.info(
                    "[actions]-{codehub-project-create-protected-branches} has protected branches fro project_id: [%s], skip.",
                    project_id)
            else:
                list_actions_body = [
                    ProtectedActionBasicApiDto(
                        action=push_action,
                        enable=push_enable,
                        user_ids=push_user_ids,
                        user_team_ids=push_user_team_ids,
                        related_role_ids=push_related_role_ids
                    ),
                    ProtectedActionBasicApiDto(
                        action=merge_action,
                        enable=merge_enable,
                        user_ids=merge_user_ids,
                        user_team_ids=merge_user_team_ids,
                        related_role_ids=merge_related_role_ids
                    )
                ]
                response = self.create_project_protected_branches(project_id, list_actions_body, branch_name)
                log.info(
                    "[actions]-{codehub-project-create-protected-branches} create protected branches fro project_id: [%s] success.",
                    project_id)
        except exceptions.ClientRequestException as e:
            log.error("[actions]-{codehub-project-create-protected-branches} for project_id:[%s] failed.", project_id)
            raise
        return response

    def get_codehub_client(self):
        return local_session(self.manager.session_factory).client("codeartsrepo")

    def need_create_protected_branches(self, protected_branches):
        if len(protected_branches) > 0:
            for branch in protected_branches:
                if branch.get("name") == "*":
                    return False
            return True
        else:
            return True

    def query_project_protected_branches(self, project_id):
        request = ListProjectProtectedBranchesRequest()
        request.project_id = project_id
        request.user_actions = True
        protected_branches = []
        offset = 0
        limit = 20
        while True:
            request.offset = offset
            request.limit = limit
            try:
                response = self.get_codehub_client().list_project_protected_branches(request)
                log.info(
                    "[actions]-{codehub-project-create-protected-branches} with project_id: [%s]"
                    "query project protected branches success, response: [%s]",
                    project_id, response)
                response = json.loads(str(response))
                if response.get("body") is None:
                    break
                if len(protected_branches) == 0:
                    protected_branches = response.get("body")
                else:
                    protected_branches.extend(response.get("body"))
                if len(protected_branches) < limit:
                    break
                offset += limit
            except exceptions.ClientRequestException as e:
                log.error(
                    "[actions]-{codehub-project-create-protected-branches} with request:[%s]"
                    "query project protected branches failed, cause: "
                    "status_code[%s] request_id[%s] error_code[%s] error_msg[%s]",
                    request, e.status_code, e.request_id, e.error_code, e.error_msg)
                raise
        return protected_branches

    def create_project_protected_branches(self, project_id, list_actions_body, branch_name):
        request = CreateProjectProtectedBranchesRequest()
        request.project_id = project_id

        request.body = ProtectedBranchBodyApiDto(
            actions=list_actions_body,
            name=branch_name
        )
        try:
            response = self.get_codehub_client().create_project_protected_branches(request)
            log.info(
                "[actions]-{codehub-project-create-protected-branches} with project_id:[%s] "
                "create project protected branches success.", project_id)
        except exceptions.ClientRequestException as e:
            log.error(
                "[actions]-{codehub-project-create-protected-branches} with request:[%s]"
                "create project protected branches failed, cause: "
                "status_code[%s] request_id[%s] error_code[%s] error_msg[%s]",
                request, e.status_code, e.request_id, e.error_code, e.error_msg)
            raise
        return response


@CodeaArtsRepoProject.action_registry.register("set-project-inherit-settings")
class CodeaArtsRepoProjectSetSettings(HuaweiCloudBaseAction):
    """ CodeArtsRepo set project settings.

    :Example:

    .. code-block:: yaml

        policies:
          - name: CodeArtsRepo-project-set-settings
          resource: huaweicloud.codeartsrepo-project
          filters:
            - type: value
              key: id
              value: ${id}
          actions:
            - type: set-project-inherit-settings
              name: protected_branches
              inherit_mod: force_inherit

    """
    schema = type_schema("set-project-inherit-settings", name={'type': 'string'}, inherit_mod={'type': 'string'})

    def perform_action(self, resource):
        project_id = resource["id"]
        name = self.data.get("name")
        inherit_mod = self.data.get("inherit_mod")
        self.verify(name, inherit_mod)

        settings = self.query_project_settings(project_id)
        setting = self.find_setting_by_name(settings, name)
        if setting is None:
            log.error(
                "[actions]-{codehub-project-set-settings} with project_id: [%s]"
                "query project settings failed, not found name: [%s], please check your name.",
                project_id, name)
            return settings
        if setting["inherit_mod"] == "force_inherit":
            log.info(
                "[actions]-{codehub-project-set-settings} has force_inherit name: [%s] fro project_id: [%s], skip.",
                name, project_id)
            return settings
        list_data_body = [
            ProjectSettingsInheritCfgDto(
                name=name,
                inherit_mod=inherit_mod,
            )
        ]
        try:
            response = self.set_project_settings(project_id, list_data_body)
            log.info(
                "[actions]-{codehub-project-set-settings} set settings name: [%s] fro project_id: [%s] success.",
                name, project_id)
        except exceptions.ClientRequestException as e:
            log.error("[actions]-{codehub-project-set-settings} set settings name: [%s] for project_id:[%s] failed.",
                      name, project_id)
            raise
        return response

    def get_codehub_client(self):
        return local_session(self.manager.session_factory).client("codeartsrepo")

    def verify(self, name, inherit_mod):
        name_list = ["protected_branches", "watermark"]
        inherit_mod_list = ["force_inherit", "custom"]
        if name not in name_list:
            log.error("[actions]-{codehub-project-set-settings} verify name: [%s] failed."
                      "name must in [%s].",
                      name, name_list)
            raise
        if inherit_mod not in inherit_mod_list:
            log.error("[actions]-{codehub-project-set-settings} verify inherit_mod: [%s] failed."
                      " inherit_mod must in [%s].",
                      inherit_mod, inherit_mod_list)
            raise

    def query_project_settings(self, project_id):
        request = ShowProjectSettingsInheritCfgRequest()
        request.project_id = project_id
        try:
            response = self.get_codehub_client().show_project_settings_inherit_cfg(request)
            log.info(
                "[actions]-{codehub-project-set-settings} with project_id: [%s]"
                "query project settings success, response: [%s]",
                project_id, response)
        except exceptions.ClientRequestException as e:
            log.error(
                "[actions]-{codehub-project-set-settings} with request:[%s]"
                "query project settings failed, cause: "
                "status_code[%s] request_id[%s] error_code[%s] error_msg[%s]",
                request, e.status_code, e.request_id, e.error_code, e.error_msg)
            raise
        return response

    def find_setting_by_name(self, settings, name):
        settings = json.loads(str(settings))
        for setting in settings.get("body"):
            if setting["name"] == name:
                return setting
        return None

    def set_project_settings(self, project_id, list_data_body):
        request = UpdateProjectSettingsInheritCfgRequest()
        request.project_id = project_id

        request.body = SettingsInheritCfgBodyApiDto(
            data=list_data_body
        )
        try:
            response = self.get_codehub_client().update_project_settings_inherit_cfg(request)
            log.info(
                "[actions]-{codehub-project-set-settings} with project_id:[%s] "
                "set project settings success.", project_id)
        except exceptions.ClientRequestException as e:
            log.error(
                "[actions]-{codehub-project-set-settings} with request:[%s]"
                "set project settings failed, cause: "
                "status_code[%s] request_id[%s] error_code[%s] error_msg[%s]",
                request, e.status_code, e.request_id, e.error_code, e.error_msg)
            raise
        return response
