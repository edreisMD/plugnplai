Welcome to plugnplai
=====================================

Overview
^^^^^^^^

Plug and Plai is an open source library aiming to simplify the integration of AI plugins into open-source language models (LLMs).

It provides utility functions to get a list of active plugins from https://plugnplai.com/ directory, get plugin manifests, and extract OpenAPI specifications and load plugins.

## Installation

You can install Plug and PlAI using pip:

```python
pip install plugnplai
```

## Quick Start Example

**Apply Plugins in Three Steps:** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/edreisMD/plugnplai/blob/main/examples/apply_plugins_three_steps.ipynb)


.. toctree::
   :maxdepth: 1
   :caption: Getting Started
   :hidden:

   get-started/quickstart.md

  


.. toctree::
   :caption: Examples
   :hidden:

   examples/get-list-of-plugins.md
   examples/plugin_retriever_with_langchain_agent_clean_version.ipynb
   examples/plugin_retriever_with_langchain_agent.ipynb
   examples/apply_plugins_three_steps.ipynb
   examples/create_prompt_plugins.ipynb
   examples/plugins_step_by_step.ipynb


.. toctree::
   :maxdepth: 2
   :caption: Modules
   :hidden:

   modules/utility-functions.md


.. toctree::
   :maxdepth: 2
   :caption: Reference
   :hidden:

   
   reference/modules.rst
