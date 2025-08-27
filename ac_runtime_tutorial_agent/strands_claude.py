from strands import Agent, tool
from strands_tools import calculator # Import the calculator tool
import argparse
import json
from strands.models import BedrockModel

# for Bedrock AgentCore deployment from local runtime
from bedrock_agentcore.runtime import BedrockAgentCoreApp

# initialize the Bedrock AgentCore App
app = BedrockAgentCoreApp()

# Create a custom tool 
@tool
def weather():
    """ Get weather """ # Dummy implementation
    return "sunny"


model_id = "anthropic.claude-3-haiku-20240307-v1:0"
model = BedrockModel(
    model_id=model_id,
)
agent = Agent(
    model=model,
    tools=[calculator, weather],
    system_prompt="You're a helpful assistant. You can do simple math calculation, and tell the weather."
)

@app.entrypoint
def strands_agent_bedrock(payload):
    """
    Invoke the agent with a payload

    Call example from command line:
    - python strands_claude.py '{"prompt": "What is 2 + 6?"}'
    - python strands_claude.py '{"prompt": "What is the weather in Tokyo?"}'
    """
    try:
        print(f"Received payload: {payload}")
        
        # Handle different payload formats
        if isinstance(payload, str):
            import json
            payload = json.loads(payload)
        
        user_input = payload.get("prompt")
        if not user_input:
            return {"error": "No 'prompt' field found in payload"}
        
        print(f"Processing user input: {user_input}")
        response = agent(user_input)
        
        print(f"Agent response type: {type(response)}")
        print(f"Agent response message: {response.message}")
        
        # Extract text from response
        if hasattr(response, 'message') and 'content' in response.message:
            content = response.message['content']
            if content and len(content) > 0 and 'text' in content[0]:
                result_text = content[0]['text'].strip()
                print(f"Returning result: {result_text}")
                return {"result": result_text}
            else:
                return {"error": "No text content found in response"}
        else:
            return {"error": "Invalid response structure"}
            
    except Exception as e:
        print(f"Error in strands_agent_bedrock: {e}")
        import traceback
        traceback.print_exc()
        return {"error": str(e)}

if __name__ == "__main__":
    # When running from command line
    # parser = argparse.ArgumentParser()
    # parser.add_argument("payload", type=str)
    # args = parser.parse_args()
    # response = strands_agent_bedrock(json.loads(args.payload))
    # print(response)

    # When running after local server
    # python strands_claude.py
    # curl -X POST http://127.0.0.1:8080/invocations -H "Content-Type: application/json" -d '{"prompt": "What is 2 + 6?"}'
    app.run()