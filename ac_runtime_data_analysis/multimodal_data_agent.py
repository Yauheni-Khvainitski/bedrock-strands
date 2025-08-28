from strands import Agent, tool
from strands.models import BedrockModel
import pandas as pd
import base64
import io
import json
from bedrock_agentcore.runtime import BedrockAgentCoreApp

app = BedrockAgentCoreApp()

# Initialize the model and agent
model_id = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
model = BedrockModel(
    model_id=model_id,
    max_tokens=16000
)

agent = Agent(
    model=model,
    system_prompt="""
    You are a data analysis assistant that can process large Excel files and images.
    When given multi-modal data, analyze both the structured data and visual content,
    then provide comprehensive insights combining both data sources.
    """
)

@app.entrypoint
def multimodal_data_processor(payload, context):
    """
    Process large multi-modal payloads containing Excel data and images.

    Args:
        payload: Contains prompt, excel_data (base64), image_data (base64)
        context: Runtime context information

    Returns:
        str: Analysis results from both data sources
    """
    prompt = payload.get("prompt", "Analyze the provided data.")
    excel_data = payload.get("excel_data", "")
    image_data = payload.get("image_data", "")

    print(f"=== Large Payload Processing ===")
    print(f"Session ID: {context.session_id}")

    if excel_data:
        print(f"Excel data size: {len(excel_data) / 1024 / 1024:.2f} MB")
    if image_data:
        print(f"Image data size: {len(image_data) / 1024 / 1024:.2f} MB")
    print(f"Excel data {excel_data}")
    print(f"Image data {image_data}")
    print(f"=== Processing Started ===")
    # Decode base64 to bytes
    excel_bytes = base64.b64decode(excel_data)
    # Decode base64 to bytes
    image_bytes = base64.b64decode(image_data)

    # Enhanced prompt with data context
    enhanced_prompt = f"""{prompt}
    Please analyze both data sources and provide insights.
    """

    response = agent(
        [{
            "document": {
                "format": "xlsx",
                "name": "excel_data",
                "source": {
                    "bytes": excel_bytes
                }
            }
        },
        {
            "image": {
                "format": "png",
                "source": {
                    "bytes": image_bytes
                }
            }
        },
        {
            "text": enhanced_prompt
        }]
    )
    return response.message['content'][0]['text']

if __name__ == "__main__":
    app.run()
