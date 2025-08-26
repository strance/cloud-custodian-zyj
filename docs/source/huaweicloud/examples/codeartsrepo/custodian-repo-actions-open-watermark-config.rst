CodeArtsRepo - open watermark for project and set project watermark inherit settings
========================

.. code-block:: yaml

  policies:
    - name: CodeArtsRepo-Project-Open-Watermark
      description: open watermark for project
      resource: huaweicloud.codeartsrepo-project
      filters:
        - type: value
          key: id
          value: "a8833a48b02540a2becc254f35b1f21e"
      actions:
        - type: open-watermark
    - name: CodeArtsRepo-Project-set-project-watermark-settings
      description: set project settings(watermark) for project
      resource: huaweicloud.codeartsrepo-project
      filters:
        - type: value
          key: id
          value: "a8833a48b02540a2becc254f35b1f21e"
      actions:
        - type: set-project-inherit-settings
          name: "watermark"
          inherit_mod: "force_inherit"