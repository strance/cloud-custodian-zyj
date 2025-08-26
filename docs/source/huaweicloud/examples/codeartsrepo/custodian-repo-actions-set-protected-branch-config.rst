CodeArtsRepo - open prtected branches for project and set project prtected branches inherit settings
========================

.. code-block:: yaml

  policies:
    - name: CodeArtsRepo-Project-create-protected-branches
      description: create protected branch for project
      resource: huaweicloud.codeartsrepo-project
      filters:
        - type: value
          key: id
          value: "a8833a48b02540a2becc254f35b1f21e"
      actions:
        - type: create-protected-branches
          branch_name: "*"
          push_action: "push"
          push_enable: True
          push_user_ids: []
          push_user_team_ids: []
          push_related_role_ids: []
          merge_action: "merge"
          merge_enable: True
          merge_user_ids: []
          merge_user_team_ids: []
          merge_related_role_ids: []
    - name: CodeArtsRepo-Project-set-project-protected-branches-settings
      description: set project settings(watermark) for project
      resource: huaweicloud.codeartsrepo-project
      filters:
        - type: value
          key: id
          value: "a8833a48b02540a2becc254f35b1f21e"
      actions:
        - type: set-project-inherit-settings
          name: "protected_branches"
          enable: True