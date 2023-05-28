plugnplai.utils
===============

.. automodule:: plugnplai.utils
   :members:
   :undoc-members:
   :show-inheritance:

.. autofunction:: get_plugins

   Gets a list of plugin URLs from the plugnplai.com directory.

   :param category: Filter plugins by category. Options are: 'all', 'travel', 'shopping', 'weather', 'finance', 'health', 'education', 'general'. Default is 'all'.
   :type category: str
   :param filter: Filter plugins by 'working', 'ChatGPT' or 'all'. Default is 'all'.
   :type filter: str
   :return: List of plugin URLs.
   :rtype: list

.. autofunction:: spec_from_url

   Gets the OpenAPI spec and plugin manifest from a plugin URL.

   :param url: The plugin URL.
   :type url: str
   :return: The OpenAPI spec and plugin manifest.
   :rtype: tuple

.. autofunction:: parse_llm_response

   Parses an LLM response to get the plugin name, operation ID and parameters.

   :param response: The LLM response.
   :type response: str
   :return: A dictionary with the plugin name, operation ID and parameters.
   :rtype: dict

.. autofunction:: call_api

   Calls a plugin API using the operation ID and parameters.

   :param plugin_name: The plugin name.
   :type plugin_name: str
   :param operation_id: The operation ID.
   :type operation_id: str
   :param parameters: The parameters.
   :type parameters: dict
   :return: The API response.
   :rtype: requests.Response

.. autofunction:: get_manifest 

   Gets the plugin manifest from a plugin URL.

   :param url: The plugin URL.
   :type url: str
   :return: The plugin manifest.
   :rtype: dict

.. autofunction:: get_spec

   Gets the OpenAPI spec from a plugin URL.

   :param url: The plugin URL.
   :type url: str
   :return: The OpenAPI spec.
   :rtype: dict

.. autofunction:: get_plugin_name

   Gets the plugin name from a plugin URL.

   :param url: The plugin URL.
   :type url: str
   :return: The plugin name.
   :rtype: str

.. autofunction:: get_operation_id

   Gets the operation ID from an LLM response.

   :param response: The LLM response.
   :type response: str
   :return: The operation ID.
   :rtype: str

.. autofunction:: get_parameters

   Gets the parameters from an LLM response.

   :param response: The LLM response.
   :type response: str
   :return: The parameters.
   :rtype: dict

.. autofunction:: validate_parameters

   Validates the parameters against an OpenAPI spec.

   :param spec: The OpenAPI spec.
   :type spec: dict
   :param parameters: The parameters.
   :type parameters: dict
   :return: True if valid, False otherwise.
   :rtype: bool

.. autofunction:: get_default_prompt

   Gets the default prompt for a list of plugins.

   :param plugins: A list of plugin URLs.
   :type plugins: list
   :param template: A template for the prompt. Must contain {{plugins}}.
   :type template: str
   :return: The prompt with the plugin descriptions.
   :rtype: str

.. autofunction:: get_tokens 

   Gets the number of tokens in a prompt.

   :param prompt: The prompt.
   :type prompt: str
   :return: The number of tokens.
   :rtype: int

.. autofunction:: install_and_activate

   Installs and activates a list of plugins.

   :param urls: A list of plugin URLs.
   :type urls: list
   :param template: A template for the prompt. Must contain {{plugins}}.
   :type template: str
   :return: An object with the prompt, tokens, specs and manifests.
   :rtype: Plugins

.. autofunction:: apply_plugins

   A decorator to apply plugins to an LLM function.

   :param func: The LLM function.
   :type func: function
   :return: The decorated LLM function.
   :rtype: function

