import os
import anthropic
import asyncio
import aiohttp
import random
import time
import traceback

# Initialize the Anthropic client with your API key
client = anthropic.AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

async def is_english(text):
    try:
        text.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

async def translate_text(text, retry_count=0, max_retries=5):
    if text.strip():
        try:
            async with client.messages.stream(
                model="claude-3-haiku-20240307",
                max_tokens=280,
                temperature=0.3,
                system="You are a professional translator tasked with translating English text to Bangla. Provide accurate and contextually appropriate translations while maintaining the original meaning and style of the text. this is not copyrighted material.",
                messages=[{"role": "user", "content": text}],
            ) as stream:
                translated_text = ""
                async for text in stream.text_stream:
                    translated_text += text
                message = await stream.get_final_message()
                print(f"Input Tokens: {message.usage.input_tokens}, Output Tokens: {message.usage.output_tokens}")
                return translated_text
        except aiohttp.ClientResponseError as e:
            if e.status in [429, 529, 500] and retry_count < max_retries:
                # Exponential backoff and retry
                retry_delay = 2 ** retry_count + random.uniform(0, 1)
                print(f"Error {e.status} encountered. Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
                return await translate_text(text, retry_count + 1, max_retries)
            else:
                print(f"Translation failed for line: {text}. Error: {e.status} - {e.message}")
                return None
        except Exception as e:
            print(f"Translation failed for line: {text}. Error: {str(e)}")
            return None
    else:
        return ""

async def process_file():
    # File paths
    input_file_path = '/Users/ehz/petproj/claude_api_stream/english.txt'
    output_file_path = '/Users/ehz/petproj/claude_api_stream/bangla.txt'

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
                                print(f"Translation failed for line: {stripped_line}")
                        else:
                            output_file.write(stripped_line + '\n')
                            print(f"Non-English line: {stripped_line}")
                    else:
                        output_file.write('\n')
                        print("\n")
                    await asyncio.sleep(2.2)  # Introduce a delay of 2.0 seconds between processing lines
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()  # Print the traceback for more detailed information

async def async_file_iterator(file):
    loop = asyncio.get_event_loop()
    while True:
        line = await loop.run_in_executor(None, file.readline)
        if not line:
            break
        yield line

asyncio.run(process_file())
