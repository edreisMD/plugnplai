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

### Examples

#### Utility functions

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
manifest, openapi_spec = plugnplai.spec_from_url(urls[0])
```

#### Plugins Retrieval
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/edreisMD/plugnplai/blob/main/docs/examples/plugin_retriever_with_langchain_agent.ipynb)


## Contributing

Plug and Plai is an open source library, and we welcome contributions from the entire community. If you're interested in contributing to the project, please feel free to fork, submit pull requests, report issues, or suggest new features.

#### To dos
- [ ] Define a default object to read plugins - use LangChain standard? (for now using only manifest and specs jsons)
- [ ] [Load] Fix breaking on reading certain plugins specs
- [ ] [Load] Accept different specs methods and versions (param, query, body)
- [ ] [Prompt] Build a utility function to return a default prompts for a plugin
- [ ] [Prompt] Fix prompt building for body (e.g. "Speak") 
- [ ] [Prompt] Build a utility function to return a default prompts for a set of plugins
- [ ] [Prompt] Build a utility function to count tokens of the plugins prompt
- [ ] [Prompt] Use the prompt tokens number to short or expand a plugin prompt
- [ ] [Embeddings] Add filter option (e.g. "working", "ChatGPT") to "PluginRetriever.from_directory()"
- [ ] [Docs] Add Sphynx docs
- [ ] [Verification] Build automated tests to verify new plugins
- [ ] [Verification] Build automated monitoring for working plugins
- [ ] [Website] Build an open-source website

#### Project Roadmap
1. Build auxiliary functions that helps everyone to use plugins as defined by [OpenAI](https://platform.openai.com/docs/plugins/introduction)
2. Build in compatibility with different open-source formats (e.g. LangChain, BabyAGI, etc)
3. Find a best prompt format for plugins, optimizing for token number and description completness
4. Build a dataset to finetune open-source models to call plugins
5. Finetune an open-source model to call plugins
6. Help with authentication
7. Etc.

## Links

- Plugins directory: [https://plugnplai.com/](https://plugnplai.com/)
- API reference: [https://plugnplai.github.io/](https://plugnplai.github.io/)