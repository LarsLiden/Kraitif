# https://dev.azure.com/msresearch/TRAPI/_wiki/wikis/TRAPI.wiki/16858/Getting-Started-Guide

# Required packages
import base64
from openai import AzureOpenAI
from azure.identity import (
    ChainedTokenCredential,
    AzureCliCredential,
    ManagedIdentityCredential,
    get_bearer_token_provider,
)

# Global client instance
_client = None


def get_ai_client():
    """Get or create the AzureOpenAI client instance."""
    global _client
    if _client is None:
        # Authenticate by trying az login first, then a managed identity, if one exists on the system)
        scope = "api://trapi/.default"
        credential = get_bearer_token_provider(
            ChainedTokenCredential(
                AzureCliCredential(),
                ManagedIdentityCredential(),
            ),
            scope,
        )

        api_version = "2024-10-21"  # Ensure this is a valid API version see: https://learn.microsoft.com/en-us/azure/ai-services/openai/api-version-deprecation#latest-ga-api-release
        instance = "gcr/shared"  # See https://aka.ms/trapi/models for the instance name
        endpoint = f"https://trapi.research.microsoft.com/{instance}"

        # Create an AzureOpenAI Client
        _client = AzureOpenAI(
            azure_endpoint=endpoint,
            azure_ad_token_provider=credential,
            api_version=api_version,
        )
    return _client


def get_ai_response(prompt, chat_history=None, context_data=None, selected_context=None):
    """
    Get AI response with optional structured data extraction.

    Args:
        prompt (str): The user's message
        chat_history (list): Optional list of previous messages
        context_data (dict): Optional context data (can be all available topics or specific context)
        selected_context (dict): Optional selected context from user selections

    Returns:
        tuple: (ai_response_text, structured_data, prompt_info)
               - ai_response_text: Clean text response for display in chat
               - structured_data: Extracted JSON structure or None
               - prompt_info: Dict with info about the prompt sent to AI
    """

    try:
        client = get_ai_client()
        deployment_name = "gpt-4o_2024-08-06"

        # Build messages array
        messages = []
        if chat_history:
            messages.extend(chat_history)

        # Add the current user message
        messages.append(
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                ],
            }
        )

        # Do a chat completion and capture the response
        response = client.chat.completions.create(
            model=deployment_name,
            messages=messages,
        )

        # Parse out the message
        response = response.choices[0].message.content

        print("===============PROMPT=================")
        print(prompt)
        print("===============RESPONSE=================")
        print(response)

        return response

    except Exception as e:
        # Return error message instead of raising
        return f"Error: {str(e)}"

