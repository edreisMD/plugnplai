# 🎸 Plug and Plai

Plug and Plai is an open source library aiming to simplify the integration of AI plugins into open-source language models (LLMs). 

It provides utility functions to get a list of active plugins from [plugnplai.com](https://plugnplai.com/) directory, get plugin manifests, and extract OpenAPI specifications and load plugins.

## Installation

You can install Plug and PlAI using pip:

```python
pip install plugnplai
```

## Usage

### Get a list of plugins

- `urls = get_plugins()`: Get a list of available plugins from a [plugins repository](https://www.plugplai.com/).

- `urls = get_plugins(filter = 'ChatGPT', category='dev')`: Use 'filter' or 'category' variables to query specific plugins 

#### Example
```python
import plugnplai

# Get all plugins from plugnplai.com
urls = plugnplai.get_plugins()

#  Get ChatGPT plugins - only ChatGPT verified plugins
urls = plugnplai.get_plugins(filter = 'ChatGPT')

#  Get working plugins - only tested plugins (in progress)
urls = plugnplai.get_plugins(filter = 'working')

#  Get plugins by category - only tested plugins (in progress)
urls = plugnplai.get_plugins(category = 'travel')

#  Get the names list of categories
urls = plugnplai.get_category_names()
```

### Utility Functions

Help to load the plugins manifest and OpenAPI specification

- `manifest = get_plugin_manifest(url)`: Get the AI plugin manifest from the specified plugin URL.
- `specUrl = get_openapi_url(url, manifest)`: Get the OpenAPI URL from the plugin manifest.
- `spec = get_openapi_spec(openapi_url)`: Get the OpenAPI specification from the specified OpenAPI URL.
- `manifest, spec = spec_from_url(url)`: Returns the Manifest and OpenAPI specification from the plugin URL.

#### Example

Here is an example of how to use the utility functions:

```python
import plugnplai

# Get the Manifest and the OpenAPI specification from the plugin URL 
manifest, openapi_spec = plugnplai.spec_from_url(urls[0])
```

### Create Prompt with Plugins Description

#### Example notebook
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/edreisMD/plugnplai/blob/main/examples/plugin_retriever_with_langchain_agent.ipynb)

```python
from plugnplai import Plugins

# Initialize 'Plugins' by passing a list of urls, this function will load the plugins and build a default description to be used as prefix prompt
plugins = Plugins.install_and_activate(urls)

#  Print the deafult prompt for the activated plugins
print(plugins.prompt)

#  Print the number of tokens of the prefix prompt
print(plugins.tokens)

###### ACTIVATE A MAX OF 3 PLUGINS ######
# Context length might limiti the number of plugins you can activate, you need to make sure the prompt fits in your context lenght, leaving space for the user message
```

Install all, and activate a few later:

```python
from plugnplai import Plugins

#If you just want to load the plugins, but activate only some of them later use Plugins(urls) instead
plugins = Plugins(urls)

# Print the names of installed plugins
print(plugins.list_installed)

# Activate the plugins you want
plugins.activate(name1)
plugins.activate(name2)
plugins.activate(name3)

# Deactivate the last plugin
plugins.deactivate(name3)

# Print the names of the active plugins
print(plugins.list_active)

# Look at the current prompt
print(plugins.prompt)
print(plugins.tokens)
```

#### Plugins Retrieval

Example notebook with LangChain agent:
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/edreisMD/plugnplai/blob/main/examples/plugin_retriever_with_langchain_agent.ipynb)

```python
from plugnplai import PluginRetriever

# Initialize the plugins retriever vector database and index the plugins descriptions. Loading the plugins from plugnplai.com directory
plugin_retriever = PluginRetriever.from_directory()

#  Retrieve the names of the plugins given a user's message
plugin_retriever.retrieve_names("what shirts can i buy?")
```

## Contributing

Plug and Plai is an open source library, and we welcome contributions from the entire community. If you're interested in contributing to the project, please feel free to fork, submit pull requests, report issues, or suggest new features.

#### To dos
- [x] [Load] Define a default object to read plugins - use LangChain standard? (for now using only manifest and specs jsons)
- [ ] [Load] Fix breaking on reading certain plugins specs
- [x] [Load] Accept different specs methods and versions (param, query, body)
- [x] [Prompt] Build a utility function to return a default prompts for a plugin
- [x] [Prompt] Fix prompt building for body (e.g. "Speak") 
- [x] [Prompt] Build a utility function to return a default prompts for a set of plugins
- [x] [Prompt] Build a utility function to count tokens of the plugins prompt
- [ ] [Prompt] Use the prompt tokens number to short or expand a plugin prompt, use LLM to summarize the prefix prompt
- [x] [CallAPI] Build a function to call API given a dictionary of parameters
- [ ] [CallAPI] Add example for calling API
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