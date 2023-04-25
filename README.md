# 🎸 Plug and PLAI

Plug and PlAI is an open source library that allows you to manage AI plugins. It provides utility functions to load available plugins, get plugin manifests, and extract OpenAPI specifications.

## Installation

You can install Plug and PlAI using pip:

`pip install plugnplai`

## Usage

### Utility Functions

The following utility functions are available in the library:

- `get_plugins(endpoint)`: Get a list of available plugins from a [plugins repository](https://www.plugplai.com/).
- `get_plugin_manifest(url)`: Get the AI plugin manifest from the specified plugin URL.
- `get_openapi_url(url, manifest)`: Get the OpenAPI URL from the plugin manifest.
- `get_openapi_spec(openapi_url)`: Get the OpenAPI specification from the specified OpenAPI URL.
- `from_url(url)`: Returns the Manifest and OpenAPI specification from the plugin URL.

### Example

Here is an example of how to use the utility functions:

```python
import plugnplai

# Get a list of available plugins
plugins = plugnplai.get_plugins()

# Get the Manifest and the OpenAPI specification from the plugin URL 
manifest, openapi_spec = spec_from_url(plugins[0])
```

## Links

- GitHub Repository: [https://github.com/edreisMD/plugnplai](https://github.com/edreisMD/plugnplai)
- Plugins database: [https://plugplai.com/](https://plugplai.com/)
- Database API: [https://plugnplai.github.io/](https://plugnplai.github.io/)
