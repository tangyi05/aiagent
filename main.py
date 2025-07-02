import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
    load_dotenv()

    #API Key 
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables!")
        sys.exit(1)
    client = genai.Client(api_key=api_key)
    
    argv = [args for args in sys.argv[1:] if (len(sys.argv) > 1 and not args.startswith("--"))]
    if not argv:
        print("Usage: python main.py [--verbose] <prompt>")
        sys.exit(1)
    
    # Join the arguments to form the user prompt
    user_prompt = " ".join(argv)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    verbose = "--verbose" in sys.argv
    print("Hello from aiagent!")

    if verbose:
        print(f"User prompt: {user_prompt}")
    generate_response(client, messages, verbose)


def generate_response(client, messages, verbose): 
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=messages
    )
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    if verbose:
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")
    print("Response:")
    print(response.text)

if __name__ == "__main__":
    main()




