# Health and Wellness Agent

An AI agent that provides personalized health and wellness recommendations using AgentOps for observability.

## Installation

### Using uv (Recommended - Faster)
1. Install uv if you haven't already:
```bash
pip install uv
```

2. Create and activate virtual environment:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
uv pip install -r requirements.txt
```

### Using pip (Alternative)
1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Environment Setup
Create a `.env` file in the project root:
```bash
OPENAI_API_KEY=your_openai_api_key
AGENTOPS_API_KEY=your_agentops_api_key
```

## Usage

Run the agent:
```bash
python health_agent.py
```

## Monitoring
View your agent's performance in the [AgentOps Dashboard](https://app.agentops.ai). 