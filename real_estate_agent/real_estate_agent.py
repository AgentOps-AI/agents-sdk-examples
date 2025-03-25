from agents import Agent, Runner, function_tool
from agents import WebSearchTool
import asyncio
from typing import List, Dict, Optional
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv
import agentops
from openai import OpenAI

# Set the OPENAI_API_KEY environment variable on your terminal
# export OPENAI_API_KEY="..."

# Load AGENTOPS_API_KEY environment variable from .env file
load_dotenv()

# Get AGENTOPS_API key from environment variables
AGENTOPS_API_KEY = os.getenv("AGENTOPS_API_KEY")

# Initialize AgentOps - this is all you need for automatic instrumentation
agentops.init(AGENTOPS_API_KEY)

# Initialize the OpenAI client
client = OpenAI()
web_search = WebSearchTool()

# Create specialized agents
property_search_agent = Agent(
    name="property_search_agent",
    instructions="""You are a real estate property search specialist.
    
    When asked about properties or homes for sale, use the web_search tool to find current listings.
    Return the information in a clear, structured format.
    
    Always include if available:
    - Property address
    - Listing price
    - Number of bedrooms and bathrooms
    - Square footage
    - Property type
    - URL to the actual listing (must be real URLs from your web search, never use example.com or placeholder URLs)
    - URL to the actual listing, not the example URL
    
    After providing property listings, ask ONE specific follow-up question to learn more about the user's 
    preferences, budget constraints, or must-have features. This will help you provide more targeted property recommendations.
    """,
    tools=[web_search],
)

mortgage_agent = Agent(
    name="mortgage_agent",
    instructions="""You are a mortgage specialist.
    
    When asked about mortgages, financing, or home loans, use the web_search tool to find current rates and information.
    Consider the user's budget, down payment capabilities, and financial goals.
    
    Always include when possible:
    - Loan amount options
    - Current interest rates
    - Estimated monthly payments
    - Recommended down payment
    
    After providing mortgage information, ask ONE specific follow-up question to learn more about the 
    user's financial situation, credit score range, or long-term housing plans. This will help you provide more accurate mortgage advice.
    """,
    tools=[web_search]
)

neighborhood_agent = Agent(
    name="neighborhood_agent",
    instructions="""You are a neighborhood information specialist.
    
    When asked about neighborhoods or locations, use the web_search tool to find relevant information.
    Provide details about schools, amenities, safety, and transportation options.
    
    Always include when possible:
    - School ratings and districts
    - Local amenities (parks, shopping, restaurants)
    - Crime statistics and safety information
    - Public transportation options and walkability
    
    After providing neighborhood information, ask ONE specific follow-up question to understand if the user 
    has specific concerns about the area or particular amenities they're looking for. This will help you provide more relevant information.
    """,
    tools=[web_search]
)

# Create the main real estate agent that coordinates the specialized agents using handoffs
real_estate_agent = Agent(
    name="real_estate_agent",
    instructions="""You are a comprehensive real estate assistant that helps users find properties, 
    understand mortgage options, and learn about neighborhoods.
    
    Based on the user's query:
    1. If they're asking about specific properties or home listings, hand off to the property_search_agent
    2. If they're asking about mortgages, financing, or affordability, hand off to the mortgage_agent
    3. If they're asking about neighborhoods, schools, or local amenities, hand off to the neighborhood_agent
    
    For general real estate questions, use web_search to find relevant information.
    
    Provide helpful, accurate information and maintain a professional, friendly tone.
    If the user's request spans multiple categories, prioritize addressing their primary concern first,
    then offer to help with related aspects.
    
    IMPORTANT: Always personalize your advice. After answering a user's question, ask ONE specific follow-up 
    question to learn more about their personal situation, preferences, or requirements. This will help you 
    provide more tailored recommendations in future interactions.
    
    Examples of good follow-up questions:
    - "What's your budget range for a new home?"
    - "Are there specific neighborhoods you're interested in?"
    - "How many bedrooms and bathrooms are you looking for?"
    - "Are you planning to buy with a conventional mortgage or exploring other options?"
    
    Always be transparent about the information sources and any limitations in the data provided.
    """,
    tools=[web_search],
    handoffs=[property_search_agent, mortgage_agent, neighborhood_agent]
)

async def main():
    print("Welcome to the Real Estate Assistant!")
    print("I can help you find properties, understand mortgage options, and learn about neighborhoods.")
    print("Type 'exit' at any time to end the conversation.\n")
    
    query = input("What real estate information are you looking for? ")
    
    while query.lower() != 'exit':
        try:
            # Run the agent - AgentOps will automatically track this
            result = await Runner.run(real_estate_agent, query)
            
            # Print the response to the user
            print(f"\nReal Estate Assistant: {result.final_output}\n")
            
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}\n")
        
        # Get the next query
        query = input("You: ")

if __name__ == "__main__":
    asyncio.run(main())