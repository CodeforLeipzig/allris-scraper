import openai_summarize
from pathlib import Path
import os
import argparse

# create API key: https://platform.openai.com/account/api-keys
openai_summarizer = openai_summarize.OpenAISummarize(os.environ["OPEN_API_KEY"])

parser = argparse.ArgumentParser(description='Zusammenfassung erstellen')

params = [
    {
        "command_arg": "file",
        "default": "2015-09-09 VI-DS-01825 Bau- und Finanzierun SAO.txt",
        "help": "file to summarize"
    }
]

for entry in params:
    parser.add_argument('--' + entry['command_arg'], 
                        dest=entry['command_arg'], 
                        action='store',
                        default=entry['default'],
                        help=entry['help'])

args = parser.parse_args()

file_name = args.file
try:
    with open("data/txts/{}".format(file_name), 'r') as file:
        content = file.read()
        summary = openai_summarizer.summarize_text(content)
        Path("data/summaries").mkdir(parents=True, exist_ok=True)
        path_to_txt = "data/summaries/" + file_name + ".txt"
        with open(path_to_txt, "w") as txt_file:
            txt_file.write()
        print(summary)
except:
    content = '{}.txt not found>'.format(file_name)    
