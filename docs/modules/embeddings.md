# PluginRetriever

This module provides a `PluginRetriever` class that retrieves plugin information based on queries using embeddings and vector stores.

## Classes

### PluginRetriever

`PluginRetriever` retrieves plugin information based on queries using embeddings and vector stores.

#### Parameters

- `manifests` (list): List of manifest objects.
- `returnList` (list, optional): List of objects to be returned. Can be a list of URLs or a list of objects like `LangChain` `AIPlugin` object. Defaults to `None`.

#### Methods

- `__init__(manifests, returnList=None)`: Initializes the `PluginRetriever`.
- `from_urls(urls)`: Creates a `PluginRetriever` object from a list of URLs.
- `from_directory(provider='plugnplai')`: Creates a `PluginRetriever` object from a directory.
- `retrieve_names(query)`: Retrieves plugin names based on a query.
- `retrieve_urls(query)`: Retrieves plugin URLs based on a query.
