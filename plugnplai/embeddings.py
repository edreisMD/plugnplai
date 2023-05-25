"""
Embeddings for LangChain.

This module provides a PluginRetriever class that retrieves plugin information based on queries using embeddings and vector stores.

Classes:
    PluginRetriever

"""
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from langchain.vectorstores import FAISS
from plugnplai.utils import get_plugin_manifest, get_plugins

class PluginRetriever:
    """
    PluginRetriever retrieves plugin information based on queries using embeddings and vector stores.

    Methods:
        __init__(manifests: list, returnList: list = None)
        from_urls(urls: list)
        from_directory(provider: str = "plugnplai")
        retrieve_names(query)
        retrieve_urls(query)
    """
    def __init__(self, manifests: list, returnList: list = None):
        """
        Initialize the PluginRetriever.

        Args:
            manifests (list): List of manifest objects.
            returnList (list, optional): List of objects to be returned. Can be a list of URLs or a list of objects like LangChain AIPluging object. Defaults to None.
        """
        self.returnList = returnList
        if self.returnList:
            # add urls to manifests
            for i in range(len(manifests)):
                manifests[i]["plugin_object"] = self.returnList[i]

        self.docs = [
            Document(
                page_content=manifest["description_for_model"],
                metadata={
                    "plugin_name": manifest["name_for_model"],
                    "plugin_object": manifest.get("plugin_object", None),
                },
            )
            for manifest in manifests
        ]

        # Initialize embeddings
        self.embeddings = OpenAIEmbeddings()

        # Create vector store from documents
        self.vector_store = FAISS.from_documents(self.docs, self.embeddings)

        # Create a retriever
        self.retriever = self.vector_store.as_retriever()

    @classmethod
    def from_urls(self, urls: list):
        """
        Create a PluginRetriever object from a list of URLs.

        Args:
            urls (list): List of URLs.

        Returns:
            PluginRetriever: Initialized PluginRetriever object.
        """
        manifests = [get_plugin_manifest(url) for url in urls]
        return self(manifests, urls)

    @classmethod
    def from_directory(self, provider: str = "plugnplai"):
        """
        Create a PluginRetriever object from a directory.

        Args:
            provider (str, optional): Provider name. Defaults to "plugnplai".

        Returns:
            PluginRetriever: Initialized PluginRetriever object.
        """
        
        urls = get_plugins(filter = "working", provider = provider)
        manifests = [get_plugin_manifest(url) for url in urls]
        return self(manifests)
        
    def retrieve_names(self, query):
        """
        Retrieve plugin names based on a query.

        Args:
            query: Query string.

        Returns:
            list: List of plugin names.
        """
        # Get relevant documents based on query
        docs = self.retriever.get_relevant_documents(query)

        # Get toolkits based on relevant documents
        plugin_names = [d.metadata["plugin_name"] for d in docs]

        return plugin_names

    def retrieve_urls(self, query):
        """
        Retrieve plugin URLs based on a query.

        Args:
            query: Query string.

        Returns:
            list: List of plugin URLs.
        """
        if not self.urls:
            raise Exception("No urls provided in constructor.")

        # Get relevant documents based on query
        docs = self.retriever.get_relevant_documents(query)

        # Get toolkits based on relevant documents
        plugin_urls = [d.metadata["plugin_object"] for d in docs]

        return plugin_urls
