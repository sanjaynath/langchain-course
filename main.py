from tabnanny import verbose
from dotenv import load_dotenv
import os
load_dotenv()

from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage

from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from tavily import TavilyClient
from langchain_tavily import TavilySearch

tavily  = TavilyClient()

'''
@tool
def search_sanjay(query: str) -> str:
    """
    Tools to fetch job postings for a given role in a given area 
    Args:
        query: The query to search for
    Returns:
        The search results
    """
    print(f"Searching for {query}")
    return tavily.search(query=query)
'''
@tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together"""
    print(f"Adding {a} and {b}")
    return a + b


def main():
    print("Hello from langchain-course!")

    groq_model = "openai/gpt-oss-120b" #"llama-3.1-8b-instant" #"llama-3.3-70b-versatile" 
    llm = ChatGroq(api_key=os.getenv("GROQ_API_KEY"),model=groq_model,temperature=0.0)

    
    llm_gpt = ChatOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-4o-mini",   # or "gpt-4.1-mini", "gpt-4o"
        temperature=0.0)
    
    llm_gem = ChatGoogleGenerativeAI(
        model= "gemini-2.5-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0
    )    

    #tools = [search_sanjay]
    tools = [TavilySearch()]
    print("Tool names:")
    for t in tools:
        print(t.name)

    #print("Model:", llm_gem)
    agent = create_agent(model=llm, tools=tools)
    #result = agent.invoke({"messages": [HumanMessage(content="Use the sclearearch_sanjay tool to find the weather in Tokyo. You must use the tool. And call it only once")]})
    result = agent.invoke({"messages": [HumanMessage(content="Give me links to 2 open job postings for Data Engineer role in Amazon in Hyderabad area")]})
    
    print(result)
    print(result["messages"][-1].content)




if __name__ == "__main__":
    main()
