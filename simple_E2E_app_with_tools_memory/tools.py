# this file contains all the web search related tool functionality
import requests
from bs4 import BeautifulSoup
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
import os
from dotenv import load_dotenv
from langchain.tools import Tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities.google_serper import GoogleSerperAPIWrapper
import requests
from langchain_community.utilities.semanticscholar import SemanticScholarAPIWrapper
from langchain_community.utilities import ArxivAPIWrapper


load_dotenv()


def ddg_search(query: str, max_results: int = 5):
    try:
        search = DuckDuckGoSearchAPIWrapper()
        results = search.run(query)
        if isinstance(results, str) and len(results) > 0:
            return results
        else:
            return f"No results found for query: {query}"
    except Exception as e:
        return f"Error searching DuckDuckGo: {str(e)}"


def google_serper_search(query: str, max_results: int = 5):
    try:
        serper_api_key = os.getenv("GOOGLE_SERPER_API_KEY")
        if not serper_api_key:
            return "Google Serper API key not configured"
        search = GoogleSerperAPIWrapper(serper_api_key=serper_api_key)
        results = search.run(query)
        if isinstance(results, str) and len(results) > 0:
            return results
        else:
            return f"No results found for query: {query}"
    except Exception as e:
        return f"Error searching Google: {str(e)}"


# Make sure your API key is in environment variables
# export TAVILY_API_KEY="your_api_key_here"

def tavily_search(query: str, num_results: int = 5):
    """
    Perform a Tavily search query and return structured results.
    """
    try:
        tavily_api_key = os.getenv("TAVILY_API_KEY")
        if not tavily_api_key:
            return "Tavily API key not configured"
        tavily = TavilySearchResults(max_results=num_results, tavily_api_key=tavily_api_key)
        results = tavily.run(query)
        if results and len(results) > 0:
            # Format the results better
            formatted_results = []
            for result in results:
                if isinstance(result, dict):
                    formatted_results.append(f"Title: {result.get('title', 'N/A')}\nContent: {result.get('content', 'N/A')}\nURL: {result.get('url', 'N/A')}\n")
            return "\n".join(formatted_results) if formatted_results else str(results)
        return f"No results found for query: {query}"
    except Exception as e:
        return f"Error searching Tavily: {str(e)}"




    # Initialize the wrapper with desired parameters
    # top_k_results: Number of top-scored documents to consider
    # load_max_docs: A limit to the number of loaded documents
def ss_seach_academic_papers(query: str, limit: int = 5):
    ss_wrapper = SemanticScholarAPIWrapper(
        top_k_results=3,
        load_max_docs=3
    )
    results = ss_wrapper.run(query)
    return results[:limit]

def arxiv_search_academic_papers(query: str, limit: int = 5):
    arxiv = ArxivAPIWrapper()
    results = arxiv.run(query)
    return results[:limit]

#----------------------------------------------
# Wrap as LangChain Tool
#---------------------------------------------

TavilySearchTool = Tool(
    name="Tavily Web Search",
    func=tavily_search,
    description="Search the web using Tavily API and return structured results. Useful for general web queries, news, or factual lookups."
)

GoogleSearchTool = Tool(
    name="Google Search tool",
    func=google_serper_search,
    description="Search Google for Relevant information"
)

DdgSearchTool = Tool(
    name="DDG Search tool",
    func=ddg_search,
    description="Search DuckDuckGo for Relevant information"
)


AcademicSearchTool = Tool(
    name="arxiv paper search tool",
    func=arxiv_search_academic_papers,
    description="Search academic papers and scholarly papers for technical information and latest research"
)

ss_SearchTool = Tool(
    name="ss search tool",
    func=ss_seach_academic_papers,
    description="Search scholarly papers for technical information and latest research"
)

