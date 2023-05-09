#!/usr/bin/env python3

"""
Basic example of edge_tts usage.
"""

import asyncio
import edge_tts
import os
import argparse
from os import listdir
from os.path import isfile, join

async def _main() -> None:
    communicate = edge_tts.Communicate(TEXT, VOICE)
    await communicate.save(OUTPUT_FILE)

audio_script_location = r"F:\Youtube Video Projects\reddit_content_scraper\scripts2"
output_location = r"F:\Youtube Video Projects\reddit_content_scraper\audio"

parser = argparse.ArgumentParser(
    description='Edge text to speech code')
    
parser.add_argument(
    '-f, --file', type=str, default='what_is_normalized', dest='file',
    help='Enter filename of script.')

parser.add_argument(
    '-v, --voice', type=str, default='en-US-GuyNeural', metavar='VOICE', dest='voice',
    help='Selects the voice to use for generation.')

args = parser.parse_args()

file_name = args.file

if file_name == 'all':
    onlyfiles = [f for f in listdir(audio_script_location) if isfile(join(audio_script_location, f))]
else:
    onlyfiles = [file_name]

for file_name in onlyfiles:
    with open(os.path.join(audio_script_location, file_name), "r", encoding='utf-8') as file:
        content = file.read()

    TEXT = content
    VOICE = args.voice
    OUTPUT_FILE = os.path.join(output_location, file_name.split('.')[0] + ".mp3")

    asyncio.get_event_loop().run_until_complete(_main())

    
