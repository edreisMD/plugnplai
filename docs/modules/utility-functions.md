# Utility Functions

### Utility Functions

The following utility functions are available in the library:

* `get_plugins(endpoint)`: Get a list of available plugins from a [plugins repository](https://www.plugplai.com/). 
Gets a list of plugin URLs from the specified plugins repository (default is plugnplai.com).

* `get_plugin_manifest(url)`: Get the AI plugin manifest from the specified plugin URL.
Gets the AI plugin manifest from the specified plugin URL.

* `get_openapi_url(url, manifest)`: Get the OpenAPI URL from the plugin manifest.
Gets the OpenAPI URL from the AI plugin manifest.

* `get_openapi_spec(openapi_url)`: Get the OpenAPI specification from the specified OpenAPI URL. 
Gets the OpenAPI specification from the specified OpenAPI URL.

* `spec_from_url(url)`: Returns the Manifest and OpenAPI specification from the plugin URL.
Returns the AI plugin manifest and OpenAPI specification from the specified plugin URL.

