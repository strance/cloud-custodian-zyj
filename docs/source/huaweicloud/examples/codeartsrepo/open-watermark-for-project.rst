CodeArtsRepo - open watermark for project
========================

.. code-block:: yaml

  policies:
    - name: CodeArtsRepo-Project-Open-Watermark
      description: open watermark for project
      resource: huaweicloud.codeartsrepo-project
      filters:
        - type: value
          key: id
          value: "project_id"
      actions:
        - type: open