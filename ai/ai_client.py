# https://dev.azure.com/msresearch/TRAPI/_wiki/wikis/TRAPI.wiki/16858/Getting-Started-Guide

# Required packages
import base64
import os
import time
from datetime import datetime
from openai import AzureOpenAI
from azure.identity import (
    ChainedTokenCredential,
    AzureCliCredential,
    ManagedIdentityCredential,
    get_bearer_token_provider,
)
from prompt_types import PromptType
from ai.ai_cache import get_cache

# Global client instance
_client = None

# Enable/disable caching (set to False to bypass cache)
USE_CACHE = True

# Delay for cached responses (in seconds) to simulate AI processing
CACHE_DELAY_SECONDS = 3


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


def get_ai_response(prompt, prompt_type, chat_history=None, context_data=None, selected_context=None):
    """
    Get AI response with optional structured data extraction and debugging.

    Args:
        prompt (str): The user's message
        prompt_type (PromptType): The type of prompt for debugging categorization
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
        # Check cache first (if enabled and no chat history)
        if USE_CACHE and not chat_history:
            cache = get_cache()
            cached_response = cache.get(prompt)
            if cached_response:
                # Add delay to simulate AI processing for better UX
                time.sleep(CACHE_DELAY_SECONDS)

                print(f"[CACHE HIT] Using cached response for {prompt_type.value}")
                print("===============PROMPT (CACHED)=================")
                print(prompt)
                print("===============RESPONSE (CACHED)==============")
                print(cached_response)
                return cached_response

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

        # Save to cache (if enabled and no chat history)
        if USE_CACHE and not chat_history:
            cache = get_cache()
            cache.set(prompt, response)
            print(f"[CACHE SAVE] Saved response for {prompt_type.value}")

        # Save prompt and response to debug files
        _save_debug_files(prompt, response, prompt_type)

        return response

    except Exception as e:
        # Return error message instead of raising
        error_msg = f"Error: {str(e)}"
        # Still save debug files for errors
        try:
            _save_debug_files(prompt, error_msg, prompt_type)
        except:
            pass  # Don't let debug file saving errors break the main flow
        return error_msg


def _save_debug_files(prompt, response, prompt_type):
    """
    Save prompt and response to debug files for debugging purposes.

    Args:
        prompt (str): The prompt text sent to AI
        response (str): The response received from AI
        prompt_type (PromptType): The type of prompt for file naming
    """
    try:
        # Create debug directory if it doesn't exist
        debug_dir = "debug"
        if not os.path.exists(debug_dir):
            os.makedirs(debug_dir)

        # Use prompt type value for filename
        filename = f"{prompt_type.value}.txt"
        filepath = os.path.join(debug_dir, filename)

        # Create content with timestamp, prompt, and response
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        content = f"""Timestamp: {timestamp}
Prompt Type: {prompt_type.value}

===============PROMPT=================
{prompt}

===============RESPONSE=================
{response}
"""

        # Write to file (overwrite existing)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    except Exception as e:
        # Don't let debug file saving errors break the main flow
        print(f"Warning: Could not save debug files: {e}")
        pass
