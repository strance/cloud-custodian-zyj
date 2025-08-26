CodeArtsRepo - create protected branch for project
========================

.. code-block:: yaml

  policies:
    - name: CodeArtsRepo-Project-create-protected-branches
      description: create protected branch for project
      resource: huaweicloud.codeartsrepo-project
      filters:
        - type: value
          key: id
          value: "${project_id}"
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


.. code-block:: yaml

  policies:
    - name: CodeArtsRepo-Project-create-protected-branches
      description: create protected branch for projects
      resource: huaweicloud.codeartsrepo-project
      filters:
        - type: value
          op: not-equal
          value: ""
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


.. code-block:: yaml

  policies:
    - name: CodeArtsRepo-Project-create-protected-branches
      description: create protected branch for projects
      resource: huaweicloud.codeartsrepo-project
      filters:
        - type: value
          op: in
          value: ["$project_id1", "${project_id2}"]
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