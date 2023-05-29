# 🎸 Plug and Plai  

Plug and Plai is an open source library aiming to simplify the integration of AI plugins into open-source language models (LLMs).

It provides utility functions to get a list of active plugins from [plugnplai.com](https://plugnplai.com/) directory, get plugin manifests, and extract OpenAPI specifications and load plugins.  

## Installation  

You can install Plug and PlAI using pip:  

```python
pip install plugnplai
```  

## Quick Start Example  

**Apply Plugins in Three Steps:** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/edreisMD/plugnplai/blob/main/examples/apply_plugins_three_steps.ipynb)  


## More Examples  

**Load and Call Step by Step:** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/edreisMD/plugnplai/blob/main/examples/plugins_step_by_step.ipynb)  

**Generate Prompt with Plugins Description:** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/edreisMD/plugnplai/blob/main/examples/create_prompt_plugins.ipynb)  

**Plugins Retrieval:** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/edreisMD/plugnplai/blob/main/examples/plugin_retriever_with_langchain_agent.ipynb)  


## Usage  

### Get a list of plugins  

- `urls = get_plugins()`: Get a list of available plugins from a [plugins repository](https://www.plugplai.com/).  

- `urls = get_plugins(filter = 'ChatGPT', category='dev')`: Use 'filter' or 'category' variables to query specific plugins  

The available filters are:

- "working": Returns only tested plugins (in progress)  
- "ChatGPT": Returns only ChatGPT verified plugins  
- "langchain": Returns only plugins verified for LangChain
- "plugnplai": Returns only plugins verified for Plug and Plai

Example:  

```python
import plugnplai  

# Get all plugins from plugnplai.com  
urls = plugnplai.get_plugins()  

#  Get ChatGPT plugins - only ChatGPT verified plugins  
urls = plugnplai.get_plugins(filter = 'ChatGPT')  

#  Get working plugins - only tested plugins (in progress)  
urls = plugnplai.get_plugins(filter = 'working')  

#  Get plugins verified for LangChain
urls = plugnplai.get_plugins(filter = 'langchain')

#  Get plugins verified for Plug and Plai 
urls = plugnplai.get_plugins(filter = 'plugnplai')

#  Get the names list of categories  
urls = plugnplai.get_category_names()  
```  

### Utility Functions  

Help to load the plugins manifest and OpenAPI specification  

- `manifest = get_plugin_manifest(url)`: Get the AI plugin manifest from the specified plugin URL.  
- `specUrl = get_openapi_url(url, manifest)`: Get the OpenAPI URL from the plugin manifest.  
- `spec = get_openapi_spec(openapi_url)`: Get the OpenAPI specification from the specified OpenAPI URL.  
- `manifest, spec = spec_from_url(url)`: Returns the Manifest and OpenAPI specification from the plugin URL.  

Example:  

```python
import plugnplai  

# Get the Manifest and the OpenAPI specification from the plugin URL  
manifest, openapi_spec = plugnplai.spec_from_url(urls[0])  
```  


### Load Plugins  
**Example:** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/edreisMD/plugnplai/blob/main/examples/plugins_step_by_step.ipynb)  

```python
from plugnplai import Plugins  

###### ACTIVATE A MAX OF 3 PLUGINS ######  
# Context length limits the number of plugins you can activate,  
# you need to make sure the prompt fits in your context lenght,  
# still leaving space for the user message  

# Initialize 'Plugins' by passing a list of urls, this function will  
# load the plugins and build a default description to be used as prefix prompt  
plugins = Plugins.install_and_activate(urls)  

#  Print the deafult prompt for the activated plugins  
print(plugins.prompt)  

#  Print the number of tokens of the prefix prompt  
print(plugins.tokens)  
```  

Example on installing (loading) all plugins, and activating a few later:  

```python
from plugnplai import Plugins  

# If you just want to load the plugins, but activate only  
# some of them later use Plugins(urls) instead  
plugins = Plugins(urls)  

# Print the names of installed plugins  
print(plugins.list_installed)  

# Activate the plugins you want  
plugins.activate(name1)  
plugins.activate(name2)  
plugins.activate(name3)  

# Deactivate the last plugin  
plugins.deactivate(name3)  
```  

### Prompt and Tokens Counting  

The `plugins.prompt` attribute contains a prompt with descriptions of the active plugins.  
The `plugins.tokens` attribute contains the number of tokens in the prompt.  

For example:  
```python
plugins = Plugins.install_and_activate(urls)  
print(plugins.prompt)  
print(plugins.tokens)  
```
This will print the prompt with plugin descriptions and the number of tokens.  


### Parse LLM Response for API Tag  

The `parse_llm_response()` function parses an LLM response searching for API calls. It looks for the `<API>` pattern defined in the `plugins.prompt` and extracts the plugin name, operation ID, and parameters.  


### Call API  

The `call_api()` function calls an operation in an active plugin. It takes the plugin name, operation ID, and parameters extracted by `parse_llm_response()` and makes a request to the plugin API.  


### Apply Plugins  

The `@plugins.apply_plugins` decorator can be used to easily apply active plugins to an LLM function. To use it:  

1. Import the Plugins class and decorator:  

```python
from plugnplai import Plugins, plugins.apply_plugins  
```  

2. Define your LLM function, that necessarily takes a string (the user input) as the first argument and returns a string (the response):  

```python
@plugins.apply_plugins  
def call_llm(user_input):  
  ...  
  return response  
```  

3. The decorator will handle the following:  

- Prepending the prompt (with plugin descriptions) to the user input   
- Checking the LLM response for API calls (the <API>...</API> pattern)  
- Calling the specified plugins   
- Summarizing the API calls in the LLM response  
- Calling the LLM function again with the summary to get a final response  

4. If no API calls are detected, the original LLM response is returned.  

To more details on the implementation of these steps, see example "Step by Step": [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/edreisMD/plugnplai/blob/main/examples/plugins_step_by_step.ipynb)  

### Plugins Retrieval  
**Example:** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/edreisMD/plugnplai/blob/main/examples/plugin_retriever_with_langchain_agent.ipynb)  


```python
from plugnplai import PluginRetriever  

# Initialize the plugins retriever vector database and index the plugins descriptions.  
# Loading the plugins from plugnplai.com directory  
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
- [x] [CallAPI] Add example for calling API     
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
