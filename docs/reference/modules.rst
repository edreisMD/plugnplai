.. _Embeddings:  

Embeddings
==============================  

.. automodule:: plugnplai.embeddings
   :members:
   :inherited-members:
   :undoc-members:
   :show-inheritance:  

This module provides embeddings functionality for the PluginRetriever.  

Utility Functions
=================  

.. _get_plugins:   

get_plugins
-----------  

.. autofunction:: plugnplai.utils.get_plugins
   :noindex:  

Get a list of plugins from the PlugnPlai directory.  

This function fetches a list of plugins from the PlugnPlai directory at https://plugnplai.com.  
You can filter the plugins by:  

- ChatGPT: Only ChatGPT verified plugins  
- working: Only tested plugins (in progress)  

Parameters
----------  
filter : str, optional
    Filter to apply. Can be "ChatGPT" or "working". Defaults to None.  
provider : str, optional
    Provider name. Defaults to "plugnplai".  

Returns
-------  
list
    List of plugin URLs.  

.. _get_plugin_manifest:  

get_plugin_manifest
-------------------  

.. autofunction:: plugnplai.utils.get_plugin_manifest
   :noindex:   

Get the manifest of a plugin from its URL.  

This function fetches the manifest (ai-plugin.json) of a plugin from its URL.  

Parameters
----------  
url : str
    URL of the plugin.  

Returns   
-------  
dict
    The manifest of the plugin.

PluginObject
==============================

.. autoclass:: plugnplai.plugins.PluginObject
   :members:
   :inherited-members:
   :undoc-members:
   :show-inheritance:

This class represents an AI plugin object.

Attributes
----------
openapi : dict
    The OpenAPI specification for the plugin.
info : dict
    The info object from the OpenAPI spec.
paths : dict
    The paths object from the OpenAPI spec.
servers : list
    The servers list from the OpenAPI spec.
manifest : dict
    The plugin manifest.
url : str
    URL of the plugin.

Returns 
-------
dict
    The manifest of the plugin.
