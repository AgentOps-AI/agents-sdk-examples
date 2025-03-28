# Restaurant Finder Assistant

An AI-powered restaurant recommendation system that considers dietary restrictions, allergies, and current operating hours.

## Features
- Real-time restaurant availability checking
- Dietary restrictions and allergy considerations
- Location-aware recommendations

## Installation

### Basic Installation (CLI only)
```bash
# Clone the repository
git clone <repository-url>
cd menu

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install basic requirements
pip install -r requirements.txt
```

### Full Installation (including Web Interface)
```bash
# Follow basic installation steps, then:
pip install -r requirements-web.txt
```

## Configuration

1. Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your_openai_api_key
AGENTOPS_API_KEY=your_agentops_api_key
```

2. Make sure your environment variables are set:
```bash
# On Unix/macOS
export OPENAI_API_KEY="your_openai_api_key"
export AGENTOPS_API_KEY="your_agentops_api_key"

# On Windows (PowerShell)
$env:OPENAI_API_KEY="your_openai_api_key"
$env:AGENTOPS_API_KEY="your_agentops_api_key"
```

## Usage

### CLI Interface
Run the assistant in your terminal:
```bash
python main.py
```

You'll be prompted to:
1. Enter your timezone
2. List any food allergies
3. Specify dietary restrictions
4. Provide your location
5. Enter your restaurant preferences

### Web Interface (Optional)
Run the Streamlit web app:
```bash
streamlit run streamlit_app.py
```

The web interface provides:
- User-friendly form inputs
- Real-time updates
- Interactive search
- Recommendation history
- Visual presentation of results
