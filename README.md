# 🎸 Plug and Plai

Plug and Plai is an open source library aiming to simplify the integration of AI plugins into open-source language models (LLMs). 

It provides utility functions to get a list of active plugins from [plugnplai.com](https://plugnplai.com/) directory, get plugin manifests, and extract OpenAPI specifications and load plugins.

## Installation

You can install Plug and PlAI using pip:

```python
pip install plugnplai
```

## Usage

### Utility Functions

The following utility functions are available in the library:

- `get_plugins(endpoint)`: Get a list of available plugins from a [plugins repository](https://www.plugplai.com/).
- `get_plugin_manifest(url)`: Get the AI plugin manifest from the specified plugin URL.
- `get_openapi_url(url, manifest)`: Get the OpenAPI URL from the plugin manifest.
- `get_openapi_spec(openapi_url)`: Get the OpenAPI specification from the specified OpenAPI URL.
- `spec_from_url(url)`: Returns the Manifest and OpenAPI specification from the plugin URL.

### Example

Here is an example of how to use the utility functions:

```python
import plugnplai

# Get all plugins from plugnplai.com
urls = plugnplai.get_plugins()

#  Get ChatGPT plugins - only ChatGPT verified plugins
urls = plugnplai.get_plugins(filter = 'ChatGPT')

#  Get working plugins - only tested plugins (in progress)
urls = plugnplai.get_plugins(filter = 'working')


# Get the Manifest and the OpenAPI specification from the plugin URL 
manifest, openapi_spec = spec_from_url(plugins[0])
```

## Contributing

Plug and Plai is an open source library, and we welcome contributions from the entire community. If you're interested in contributing to the project, please feel free to fork, submit pull requests, report issues, or suggest new features.

## Links

- Plugins directory: [https://plugplai.com/](https://plugplai.com/)
- API reference: [https://plugnplai.github.io/](https://plugnplai.github.io/)
