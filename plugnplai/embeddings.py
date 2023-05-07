from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from langchain.vectorstores import FAISS


class PluginRetriever:
    def __init__(self, manifests: list, returnList: list = None):
        """
        manifests: list of manifest objects
        returnList: list of objects to be returned,
            can be a list of urls or a list of objects
            like LangChain AIPluging object
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

    def retrieve_names(self, query):
        # Get relevant documents based on query
        docs = self.retriever.get_relevant_documents(query)

        # Get toolkits based on relevant documents
        plugin_names = [d.metadata["plugin_name"] for d in docs]

        return plugin_names

    def retrieve_urls(self, query):
        if not self.urls:
            raise Exception("No urls provided in constructor.")

        # Get relevant documents based on query
        docs = self.retriever.get_relevant_documents(query)

        # Get toolkits based on relevant documents
        plugin_urls = [d.metadata["plugin_object"] for d in docs]

        return plugin_urls
