from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
# from langchain.agents.agent_toolkits import NLAToolkit


class PluginRetriever:
    def __init__(self, AI_PLUGINS):
        # Initialize embeddings
        self.embeddings = OpenAIEmbeddings()
        
        # Create documents based on AI_PLUGINS
        self.docs = [
            Document(page_content=plugin.description_for_model, 
                     metadata={"plugin_name": plugin.name_for_model})
            for plugin in AI_PLUGINS
        ]
        
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