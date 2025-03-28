import asyncio
import pytz
from datetime import datetime

# Add these lines at the top of the file to make the agent importable
__all__ = ['restaurant_agent', 'Runner']

from agents import Agent, Runner, WebSearchTool
import os
from dotenv import load_dotenv
import agentops

# Load environment variables and initialize
load_dotenv()
AGENTOPS_API_KEY = os.getenv("AGENTOPS_API_KEY")
agentops.init(AGENTOPS_API_KEY)

# Initialize the OpenAI client
web_search = WebSearchTool()

# Create specialized agents for different aspects of restaurant search
restaurant_search_agent = Agent(
    name="restaurant_search_agent",
    instructions="""You are a restaurant search specialist.
    
    CRITICAL: When searching for restaurants, you MUST:
    1. Check the current day and time provided in each query
    2. Verify the restaurant is CURRENTLY OPEN before recommending
    3. Include the closing time for each recommended restaurant
    4. Only recommend restaurants that are confirmed to be open
    5. NEVER recommend permanently closed restaurants
    6. Verify the restaurant's current operational status through recent reviews or their website
    
    VERIFICATION STEPS FOR EACH RESTAURANT:
    1. Check if the business is permanently closed
    2. Verify recent activity (reviews, social media, website updates)
    3. Confirm current operating status through official sources
    4. Double-check current day's operating hours
    5. Only proceed with recommendation if all verifications pass
    
    When asked about restaurants, use the web_search tool to find current open restaurants 
    that match the user's dietary restrictions and allergies.
    Return the information in a clear, structured format.
    
    Always include:
    - Restaurant name
    - CURRENT OPERATING STATUS (Must be open now)
    - Today's closing time
    - Last verified date/source (e.g., "Verified open via website 2024-03-XX")
    - Address
    - Type of cuisine
    - Price range
    - Menu highlights that match dietary restrictions
    - URL to the restaurant's website or menu
    - Current rating/reviews with recent dates
    
    Pay special attention to:
    - Recent reviews or social media posts confirming operation
    - Special holiday hours or temporary closures
    - Allergy information and cross-contamination policies
    - Dietary accommodation options (vegan, gluten-free, etc.)
    - Kitchen closing times (if different from restaurant hours)
    
    If you're unsure about a restaurant's current operational status, DO NOT recommend it.
    
    After providing verified open restaurant options, ask ONE specific follow-up question about their 
    dining preferences or restrictions to provide better recommendations.
    """,
    tools=[web_search],
)

dietary_agent = Agent(
    name="dietary_agent",
    instructions="""You are a dietary requirements specialist.
    
    Help users identify restaurants that can safely accommodate their:
    - Food allergies
    - Dietary restrictions (vegan, vegetarian, kosher, halal, etc.)
    - Special dietary needs
    
    Use web_search to find:
    - Restaurant allergy policies
    - Cross-contamination prevention practices
    - Special menu options
    - Kitchen practices for dietary accommodations
    
    After providing information, ask ONE specific follow-up question about their 
    dietary needs to ensure all restrictions are properly addressed.
    """,
    tools=[web_search]
)

location_agent = Agent(
    name="location_agent",
    instructions="""You are a location and accessibility specialist.
    
    When asked about restaurant locations, use web_search to find:
    - Current traffic conditions
    - Parking availability
    - Public transportation options
    - Accessibility features
    - Nearby landmarks or points of reference
    
    Always verify:
    - Current operating status
    - Special hours or closures
    - Delivery/takeout options
    
    After providing location information, ask ONE follow-up question about their 
    transportation preferences or accessibility needs.
    """,
    tools=[web_search]
)

# Main restaurant recommendation agent
restaurant_agent = Agent(
    name="restaurant_agent",
    instructions="""You are a comprehensive restaurant recommendation assistant that helps users 
    find suitable dining options considering their allergies, dietary restrictions, and location.
    
    IMPORTANT: Only use web search or hand off to specialized agents when specific current information is needed:
    1. For specific restaurant searches and current openings -> hand off to restaurant_search_agent
    2. For detailed dietary and allergy accommodation info -> hand off to dietary_agent
    3. For location-specific details and accessibility -> hand off to location_agent
    
    For general dining questions or follow-up questions about previous responses,
    use your existing knowledge to respond without web searches.
    
    Always maintain a focus on food safety for users with allergies and dietary restrictions.
    After answering a query, ask ONE specific follow-up question to better understand their needs.
    
    Be transparent about when you're using current data vs general knowledge.
    """,
    tools=[web_search],
    handoffs=[restaurant_search_agent, dietary_agent, location_agent]
)

async def main():
    print("Welcome to the Restaurant Recommendation Assistant!")
    print("I can help you find restaurants that accommodate your dietary needs and allergies.")
    print("Type 'exit' at any time to end the conversation.\n")
    
    # Get user's timezone
    timezone = input("What's your timezone (e.g., US/Pacific, US/Eastern)?: ")
    try:
        tz = pytz.timezone(timezone)
    except pytz.exceptions.UnknownTimeZoneError:
        print("Invalid timezone. Defaulting to UTC.")
        tz = pytz.UTC
    
    conversation_inputs = [{
        "role": "system",
        "content": """You are a restaurant recommendation assistant. Help users find safe dining options 
        that accommodate their allergies and dietary restrictions. Use web search for current restaurant 
        information and operating hours. Only recommend restaurants that are currently open."""
    }]
    
    # Gather essential information
    print("\nTo help you better, I need to know a few things:")
    allergies = input("Please list any food allergies you have: ")
    dietary_restrictions = input("Any dietary restrictions (vegetarian, vegan, etc.)?: ")
    location = input("What's your location (city/neighborhood)?: ")
    
    query = input("\nWhat kind of restaurant are you looking for? ")
    
    while query.lower() != 'exit':
        try:
            # Get current time in user's timezone
            current_time = datetime.now(tz)
            current_day = current_time.strftime('%A')
            current_time_str = current_time.strftime('%I:%M %p')
            
            # Create user profile
            user_profile = f"""
            Current Time: {current_time_str}
            Current Day: {current_day}
            Location: {location}
            Timezone: {timezone}
            Allergies: {allergies}
            Dietary Restrictions: {dietary_restrictions}
            """
            
            enhanced_query = f"""User Profile:\n{user_profile}\n\nQuery: {query}"""
            
            new_input = conversation_inputs + [{"role": "user", "content": enhanced_query}]
            result = await Runner.run(restaurant_agent, new_input)
            
            conversation_inputs = result.to_input_list()
            print(f"\nRestaurant Assistant: {result.final_output}\n")
            
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}\n")
        
        query = input("You: ")

if __name__ == "__main__":
    asyncio.run(main()) 