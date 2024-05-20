import openai
import config
import elevenlabs
from elevenlabs import play

openai.api_key = config.openai_key
elevenlabs.set_api_key(config.elevenlabs_key)



def queuryChatGpt(userInput):
    chat_completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": userInput}]
    )
    return (chat_completion.choices[0].message.content)

# chat_log = []

def main():

    context = ""

    while True:
        
        userInput = input("You: ")

        chatInput = context + userInput
        response = queuryChatGpt(chatInput)
        print('\n' + response + '\n')

        audio = elevenlabs.generate(
        text = response,
        voice = "PhunGuy",
        model = "eleven_multilingual_v2"
        )

        # elevenlabs.save(audio, "ellabs1.mp3")  
        play(audio)

    
if __name__ == "__main__":
    main()

