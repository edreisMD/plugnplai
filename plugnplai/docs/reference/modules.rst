plugnplai.utils
=============

.. automodule:: plugnplai.utils
   :members:

get_openapi_spec
----------------

.. autofunction:: get_openapi_spec

Gets the OpenAPI spec for a plugin.

Parameters
----------
url : str
    The URL of the plugin.

Returns
-------
dict
    The OpenAPI spec for the plugin.

get_openapi_url
----------------  

.. autofunction:: get_openapi_url

Gets the OpenAPI URL for a plugin.

Parameters
----------
url : str
    The URL of the plugin.

Returns
-------
str
    The OpenAPI URL for the plugin.

get_plugin_manifest
-------------------

.. autofunction:: get_plugin_manifest  

Gets the manifest for a plugin.

Parameters
----------
url : str
    The URL of the plugin.

Returns
-------
dict
    The manifest for the plugin.

get_plugins
-----------

.. autofunction:: get_plugins

Gets plugins from the PlugnPlai API.

Parameters
----------
category : str, optional
    The category of plugins to get.

Returns
-------
list
    A list of plugin URLs.

spec_from_url
-------------

.. autofunction:: spec_from_url

Gets the OpenAPI spec from a URL.

Parameters
----------
url : str
    The URL of the OpenAPI spec.

Returns
-------
dict
    The OpenAPI spec.

get_category_names
------------------

.. autofunction:: get_category_names

Gets category names from the PlugnPlai API.

Returns 
-------
list
    A list of category names.

parse_llm_response
------------------

.. autofunction:: parse_llm_response  

Parses an LLM response to get the plugin call.

Parameters
----------
response : str
    The response from the LLM.

Returns
-------
dict
    A dictionary with the plugin name, operation ID and parameters.

