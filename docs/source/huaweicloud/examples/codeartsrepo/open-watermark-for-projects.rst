CodeArtsRepo - open watermark for projects
========================

.. code-block:: yaml

  policies:
    - name: CodeArtsRepo-Project-Open-Watermark
      description: open watermark for projects
      resource: huaweicloud.codeartsrepo-project
      filters:
        - type: value
          key: id
          op: not-equal
          value: ""
      actions:
        - type: open