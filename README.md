# 🎸 Plug and PlAI

Plug and PlAI is an open source library that allows you to manage AI plugins. It provides utility functions to load available plugins, get plugin manifests, and extract OpenAPI specifications.

## Installation

You can install Plug and PlAI using pip:

`pip install git+https://github.com/edreisMD/plugnplai`

## Usage

### Utility Functions

The following utility functions are available in the library:

- `get_plugins(get_plugins_endpoint)`: Get a list of available plugins from a [plugins repository](https://www.plugplai.com/_functions/getUrls).
- `get_plugin_manifest(url)`: Get the AI plugin manifest from the specified plugin URL.
- `get_openapi_url(url, manifest)`: Get the OpenAPI URL from the plugin manifest.
- `get_openapi_spec(openapi_url)`: Get the OpenAPI specification from the specified OpenAPI URL.
- `spec_from_url(url)`: Get the OpenAPI specification from the specified plugin URL.

### Example

Here is an example of how to use the utility functions:

```python
import plugnplai

# Get a list of available plugins
plugins = plugnplai.get_plugins()

# Get the manifest for the first plugin
manifest = plugnplai.get_plugin_manifest(plugins[0])

# Get the OpenAPI URL from the manifest
openapi_url = plugnplai.get_openapi_url(plugins[0], manifest)

# Get the OpenAPI specification
openapi_spec = plugnplai.get_openapi_spec(openapi_url)

# Extract all parameters from the OpenAPI specification
all_parameters = plugnplai.extract_all_parameters(openapi_spec)

# Print the extracted parameters
print(all_parameters)
```

## Contributing

We welcome contributions to Plug and PlAI! If you're interested in contributing, please follow these steps:

1. Fork the repository on GitHub.
2. Create a branch for your changes.
3. Make your changes and commit them to your branch.
4. Submit a pull request to the main repository.

Before submitting your pull request, please ensure that your code adheres to the coding standards of the project and that any new features or changes are accompanied by appropriate documentation and tests.

## License

Plug and PlAI is released under the MIT License. By contributing to Plug and PlAI, you agree that your contributions will be licensed under the same license. For more details, see the [LICENSE](LICENSE) file in the repository.

## Links

- GitHub Repository: [https://github.com/edreisMD/plugnplai](https://github.com/edreisMD/plugnplai)
- Plugins database: [https://plugplai.com/](https://plugplai.com/)
- Database API: [https://plugnplai.github.io/](https://plugnplai.github.io/)
