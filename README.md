# Amazon Bedrock AgentCore with Strands Agent

A simple weather assistant demonstrating Strands Agents with Amazon Bedrock integration.

## Features

- **Weather Forecasting**: Fetches 7-day weather forecasts using National Weather Service API
- **Word Counting**: Custom tool to count words in responses
- **Bedrock Integration**: Uses Claude-3-Haiku via Amazon Bedrock
- **Tool Orchestration**: LLM autonomously decides when and how to use tools

## Quick Start

```bash
# Setup virtual environment
python3.13 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure AWS credentials (via environment variables)
export aws_access_key_id="your-key"
export aws_secret_access_key="your-secret"
export aws_region="us-east-1"

# Run the weather assistant
python weather_word_count.py
```

## How It Works

1. **Tool #1**: `http_request` - Gets Washington D.C. coordinates from weather.gov
2. **Tool #2**: `http_request` - Retrieves detailed weather forecast
3. **Tool #3**: `word_count` - Counts words in the final response

The LLM (Claude-3-Haiku) autonomously orchestrates these tools based on the user query.