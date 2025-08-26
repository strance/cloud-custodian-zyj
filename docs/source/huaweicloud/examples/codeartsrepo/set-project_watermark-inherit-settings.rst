CodeArtsRepo - set project watermark settings for project
========================

.. code-block:: yaml

  policies:
    - name: CodeArtsRepo-Project-Set-Settings
      description: set project watermark settings for project
      resource: huaweicloud.codeartsrepo-project
      filters:
        - type: value
          key: id
          value: "${project_id}"
      actions:
       - type: set-project-inherit-settings
         name: "watermark"
         enable: True


.. code-block:: yaml

  policies:
    - name: CodeArtsRepo-Project-Set-Inherit-Settings
      description: set project watermark settings for projects
      resource: huaweicloud.codeartsrepo-project
      filters:
        - type: value
          key: id
          op: not-equal
          value: ""
      actions:
       - type: set-project-inherit-settings
         name: "watermark"
         enable: True


.. code-block:: yaml

  policies:
    - name: CodeArtsRepo-Project-Set-Inherit-Settings
      description: set project watermark settings for projects
      resource: huaweicloud.codeartsrepo-project
      filters:
        - type: value
          key: id
          op: in
          value: ["$project_id1", "${project_id2}"]
      actions:
       - type: set-project-inherit-settings
         name: "watermark"
         enable: True