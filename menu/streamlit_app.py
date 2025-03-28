import streamlit as st
from datetime import datetime
import pytz
from menu import restaurant_agent, Runner
import asyncio
import uuid

st.set_page_config(
    page_title="Restaurant Finder",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'conversation_inputs' not in st.session_state:
    st.session_state.conversation_inputs = [{
        "role": "system",
        "content": """You are a restaurant recommendation assistant. Help users find safe dining options 
        that accommodate their allergies and dietary restrictions. Use web search for current restaurant 
        information and operating hours. Only recommend restaurants that are currently open."""
    }]

if 'thread_id' not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

# Sidebar for user profile
st.sidebar.title("Your Profile")

# Timezone selection
timezone = st.sidebar.selectbox(
    "Select your timezone",
    options=pytz.common_timezones,
    index=pytz.common_timezones.index('US/Pacific')
)

# User information
location = st.sidebar.text_input("Your location (city/neighborhood)")
allergies = st.sidebar.text_area("Food allergies (if any)")
dietary_restrictions = st.sidebar.text_area("Dietary restrictions (e.g., vegetarian, vegan)")

# Main content
st.title("🍽️ Smart Restaurant Finder")
st.markdown("""
Find restaurants that match your dietary needs and are open right now!
""")

# Current time display
try:
    tz = pytz.timezone(timezone)
    current_time = datetime.now(tz)
    current_day = current_time.strftime('%A')
    current_time_str = current_time.strftime('%I:%M %p')
    st.info(f"Current time in {timezone}: {current_time_str} on {current_day}")
except Exception as e:
    st.error(f"Error with timezone: {str(e)}")
    tz = pytz.UTC

# Query input
query = st.text_input("What kind of restaurant are you looking for?")

# Search button
if st.button("Search Restaurants", type="primary"):
    if not location:
        st.warning("⚠️ Please enter your location in the sidebar first!")
    else:
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

            with st.spinner('🔍 Searching for the perfect restaurants...'):
                async def search_restaurants():
                    new_input = st.session_state.conversation_inputs + [{"role": "user", "content": enhanced_query}]
                    result = await Runner.run(restaurant_agent, new_input)
                    st.session_state.conversation_inputs = result.to_input_list()
                    return result

                # Run the async function
                result = asyncio.run(search_restaurants())
                
                st.markdown('''
                    <div class="restaurant-card">
                        <h3><i class="fas fa-check-circle"></i> Restaurant Recommendations</h3>
                    </div>
                    ''', unsafe_allow_html=True)
                st.markdown(result.final_output)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
💡 **Tips:**
- Be specific about your cuisine preferences
- Include any dietary restrictions in the sidebar
- Make sure your location is accurate
""")