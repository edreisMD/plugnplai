.. _Embeddings:

Embeddings
==============================

.. automodule:: plugnplai.embeddings
   :members:
   :inherited-members:
   :undoc-members:
   :show-inheritance:

.. _Utility Functions:

Utility Functions
==============================

.. automodule:: plugnplai.utils
   :members:
   :inherited-members:
   :undoc-members:
   :show-inheritance:

.. autofunction:: get_plugins
   Gets a list of plugins from the plugnplai directory

.. autofunction:: spec_from_url
   Gets a plugin manifest and OpenAPI spec from a plugin URL

.. autofunction:: parse_llm_response
   Parses an LLM response to get the plugin name, operation ID and parameters

.. autoclass:: Plugins
   :members: install_and_activate, call_api, prompt, tokens

.. automethod:: Plugins.install_and_activate
   Installs and activates plugins

.. automethod:: Plugins.call_api
   Calls a plugin API  

.. automethod:: Plugins.prompt
   Gets the prompt for the active plugins

.. automethod:: Plugins.tokens
   Gets the number of tokens in the prompt
