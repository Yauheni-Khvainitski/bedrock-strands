import os

from boto3 import session
from dotenv import load_dotenv
from mcp import StdioServerParameters, stdio_client
from strands import Agent
from strands.models import BedrockModel
from strands.tools.mcp import MCPClient

load_dotenv("config_files/.env")

aws_docs_client = MCPClient(
    lambda: stdio_client(
        StdioServerParameters(
            command="uvx", args=["awslabs.aws-documentation-mcp-server@latest"]
        )
    )
)

aws_diag_client = MCPClient(
    lambda: stdio_client(
        StdioServerParameters(
            command="uvx", args=["awslabs.aws-diagram-mcp-server@latest"]
        )
    )
)

bedrock_model = BedrockModel(
    model_id="anthropic.claude-3-haiku-20240307-v1:0",
    boto_session=session.Session(
        aws_access_key_id=os.getenv("aws_access_key_id", ""),
        aws_secret_access_key=os.getenv("aws_secret_access_key", ""),
        aws_session_token=os.getenv("aws_session_token", ""),
        region_name=os.getenv("aws_region", ""),
    ),
    temperature=0.7,
)

agent = Agent(
    model=bedrock_model,
    tools=[aws_docs_client, aws_diag_client],
)

response = agent(
    "Get the documentation for AWS Lambda then create a diagram of a website that uses AWS Lambda for a static website hosted on S3"
)
print(response)