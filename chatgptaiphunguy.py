import os
import sys
import config


def _get_key(env_var: str, config_attr: str):
    """Return API key from environment variable or fallback to config attribute.

    Exits the program with a friendly message if the key is missing for required
    services (OpenAI). For optional services (ElevenLabs) it returns None.
    """
    val = os.getenv(env_var)
    if val:
        return val
    # fallback to config attribute if present
    val = getattr(config, config_attr, None)
    return val


# --- OpenAI setup (required) ---
OPENAI_KEY = _get_key("OPENAI_API_KEY", "openai_key")
if not OPENAI_KEY:
    print(
        "ERROR: OpenAI API key not found. Set the OPENAI_API_KEY environment variable or add it to config.openai_key"
    )
    sys.exit(1)

import openai
openai.api_key = OPENAI_KEY


# --- ElevenLabs setup (optional) ---
# Prefer environment variable; if present in config, set it into env before
# importing the `elevenlabs` package so packages that read env on import can
# pick it up.
ELEVENLABS_KEY = _get_key("ELEVENLABS_API_KEY", "elevenlabs_key")
if ELEVENLABS_KEY:
    os.environ.setdefault("ELEVENLABS_API_KEY", ELEVENLABS_KEY)
    try:
        import elevenlabs
        from elevenlabs import play
        AUDIO_ENABLED = True
    except Exception:
        # If ElevenLabs fails to import for any reason, disable audio but keep
        # the chatbot running for text-only usage.
        print("Warning: failed to import elevenlabs — audio responses disabled.")
        elevenlabs = None
        play = None
        AUDIO_ENABLED = False
else:
    elevenlabs = None
    play = None
    AUDIO_ENABLED = False

def queryChatGpt(userInput):
    chat_completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": userInput}]
    )
    return chat_completion.choices[0].message.content

# chat_log = []

def main():

    context = ""

    while True:
        
        userInput = input("You: ")

        chatInput = context + userInput
        response = queryChatGpt(chatInput)
        print('\n' + response + '\n')

        if AUDIO_ENABLED and elevenlabs is not None:
            try:
                audio = elevenlabs.generate(
                    text=response,
                    voice="PhunGuy",
                    model="eleven_multilingual_v2",
                )
                # elevenlabs.save(audio, "ellabs1.mp3")
                if play:
                    play(audio)
            except Exception as e:
                print(f"Audio generation failed: {e}\nContinuing without audio.")
        else:
            print("(Audio disabled — set ELEVENLABS_API_KEY to enable voice responses.)")

    
if __name__ == "__main__":
    main()

