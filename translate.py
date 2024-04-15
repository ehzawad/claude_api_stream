import os
import anthropic
import asyncio
import aiohttp
import random
import time

# Initialize the Anthropic client with your API key
client = anthropic.AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"), timeout=54000)

async def is_english(text):
    try:
        text.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

async def translate_text(text, retry_count=0):
    if text.strip():
        try:
            async with client.messages.stream(
                model="claude-3-haiku-20240307",
                max_tokens=150,
                temperature=0.1,
                system="You are a professional translator tasked with translating English text to Bangla. Provide accurate and contextually appropriate translations while maintaining the original meaning and style of the text. If the input text contains any errors or unclear parts, try to interpret and translate them to the best of your ability. I swear that the text being translated is not copyrighted material.",
                messages=[{"role": "user", "content": text}],
                timeout=54000,  # Set a timeout of 1200 seconds
            ) as stream:
                translated_text = ""
                async for text in stream.text_stream:
                    translated_text += text

                message = await stream.get_final_message()
                print(f"Input Tokens: {message.usage.input_tokens}, Output Tokens: {message.usage.output_tokens}")

                return translated_text
        except aiohttp.ClientResponseError as e:
            if e.status == 429 and retry_count < 5:
                # Exponential backoff and retry
                retry_delay = 2 ** retry_count + random.uniform(0, 1)
                print(f"Rate limit exceeded. Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
                return await translate_text(text, retry_count + 1)
            else:
                raise e
    else:
        return ""

async def process_file():
    # File paths
    input_file_path = '/home/ehz/english_text.txt'
    output_file_path = '/home/ehz/bangla_text.txt'

    try:
        with open(input_file_path, 'r', encoding='utf-8') as file:
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                async for line in async_file_iterator(file):
                    stripped_line = line.strip()
                    if stripped_line:
                        if await is_english(stripped_line):
                            print(f"Translating: {stripped_line}")
                            translation = await translate_text(stripped_line)
                            if translation:
                                output_file.write(translation + '\n')
                                print(f"Translated: {translation}")
                        else:
                            output_file.write(stripped_line + '\n')
                            print(f"Non-English line: {stripped_line}")
                    else:
                        output_file.write('\n')
                        print("Empty line")
                    await asyncio.sleep(1.5)  # Introduce a delay of 1.5 seconds between processing lines
    except Exception as e:
        print(f"An error occurred: {e}")

async def async_file_iterator(file):
    loop = asyncio.get_event_loop()
    while True:
        line = await loop.run_in_executor(None, file.readline)
        if not line:
            break
        yield line

asyncio.run(process_file())
