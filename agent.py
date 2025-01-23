from typing import Dict, List, Tuple, Any
from langgraph.graph import Graph
from langchain.prompts import PromptTemplate
from langchain.llms import HuggingFacePipeline
from transformers import pipeline
import os

# Initialize the LLM
def init_llm():
    model = pipeline(
        "text-generation",
        model="meta-llama/Llama-2-7b-chat-hf",
        token=os.getenv("HF_TOKEN"),
        max_length=512,
        temperature=0.7
    )
    return HuggingFacePipeline(pipeline=model)

# Define node functions
def query_classifier(state):
    """Classify the user query to determine the type of information needed."""
    llm = init_llm()
    
    template = """Classify the following user query into one of these categories:
    - PRODUCT_SEARCH
    - SUPPLIER_INFO
    - PRODUCT_DETAILS
    - UNKNOWN

    Query: {query}
    
    Category:"""
    
    prompt = PromptTemplate(template=template, input_variables=["query"])
    chain = prompt | llm
    
    result = chain.invoke({"query": state["query"]})
    state["query_type"] = result.strip()
    return state

def database_query_generator(state):
    """Generate appropriate database query based on classification."""
    llm = init_llm()
    
    template = """Given the following query type and user query, generate an SQL-like description of what needs to be queried:
    Query Type: {query_type}
    User Query: {query}
    
    SQL Description:"""
    
    prompt = PromptTemplate(template=template, input_variables=["query_type", "query"])
    chain = prompt | llm
    
    result = chain.invoke({"query_type": state["query_type"], "query": state["query"]})
    state["db_query_desc"] = result.strip()
    return state

def response_generator(state):
    """Generate natural language response based on database results."""
    llm = init_llm()
    
    template = """Given the following information, generate a natural, helpful response:
    User Query: {query}
    Database Results: {db_results}
    
    Response:"""
    
    prompt = PromptTemplate(template=template, input_variables=["query", "db_results"])
    chain = prompt | llm
    
    result = chain.invoke({
        "query": state["query"],
        "db_results": state.get("db_results", "No results found")
    })
    state["response"] = result.strip()
    return state

# Create the graph
def create_chat_graph() -> Graph:
    workflow = Graph()
    
    # Add nodes
    workflow.add_node("classify_query", query_classifier)
    workflow.add_node("generate_db_query", database_query_generator)
    workflow.add_node("generate_response", response_generator)
    
    # Add edges
    workflow.add_edge("classify_query", "generate_db_query")
    workflow.add_edge("generate_db_query", "generate_response")
    
    # Set entry point
    workflow.set_entry_point("classify_query")
    
    return workflow.compile()

# Main chat function
async def process_chat_message(message: str, db_results: str = None) -> Dict[str, Any]:
    """Process a chat message through the LangGraph workflow."""
    graph = create_chat_graph()
    
    # Initial state
    state = {
        "query": message,
        "db_results": db_results
    }
    
    # Run the graph
    result = graph.invoke(state)
    return result 