#!/usr/bin/env python3

"""
Basic example of edge_tts usage.
"""

import asyncio
import edge_tts
import os
import argparse
import re
import io
from os import listdir
from os.path import isfile, join
from tempfile import NamedTemporaryFile

async def generate_audio(text: str, voice: str) -> io.BytesIO:
    communicate = edge_tts.Communicate(text, voice)
    output_bytes = io.BytesIO()
    with NamedTemporaryFile(delete=False) as temp_file:
        await communicate.save(temp_file.name)
        temp_file.seek(0)
        output_bytes.write(temp_file.read())
    os.unlink(temp_file.name)
    return output_bytes

async def main():
    audio_script_location = r"F:\Youtube Video Projects\reddit_content_scraper\scripts2"
    output_location = r"F:\Youtube Video Projects\reddit_content_scraper\audio"
    
    parser = argparse.ArgumentParser(description='Edge text to speech code')
    parser.add_argument('-f', '--file', type=str, default='what_is_normalized', dest='file', help='Enter filename of script.')
    parser.add_argument('-v', '--voice', type=str, default='en-US-GuyNeural', metavar='VOICE', dest='voice', help='Selects the voice to use for generation.')
    args = parser.parse_args()
    file_name = args.file
    
    if file_name == 'all':
        onlyfiles = [f for f in listdir(audio_script_location) if isfile(join(audio_script_location, f))]
    else:
        onlyfiles = [file_name]

    for file_name in onlyfiles:
        with open(os.path.join(audio_script_location, file_name), "r", encoding='utf-8') as file:
            content = file.read()

        delimiter_pattern = r'@+'
        split_points = [m.start() for m in re.finditer(delimiter_pattern, content)]
        num_spaces = [len(m.group(0)) for m in re.finditer(delimiter_pattern, content)]
        content = re.sub(delimiter_pattern, '', content)

        chunks = []
        start = 0
        for idx, end in enumerate(split_points):
            chunks.append(content[start:end])
            start = end

        chunks.append(content[start:])
        in_memory_files = []

        for chunk, spaces in zip(chunks[:-1], num_spaces):
            text = chunk.strip()
            voice = args.voice
            output_bytes = await generate_audio(text, voice)
            in_memory_files.append(output_bytes)

            # Add spaces
            in_memory_files.append(io.BytesIO(b' ' * spaces))

        # Add the last chunk
        text = chunks[-1].strip()
        voice = args.voice
        output_bytes = await generate_audio(text, voice)
        in_memory_files.append(output_bytes)

        output_file = os.path.join(output_location, file_name.split('.')[0] + ".mp3")
        with open(output_file, "wb") as f:
            for file in in_memory_files:
                f.write(file.getbuffer())

if __name__ == "__main__":
    asyncio.run(main())


