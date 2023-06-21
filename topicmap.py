#https://towardsdatascience.com/topic-modelling-in-python-with-nltk-and-gensim-4ef03213cd21
import spacy
from pathlib import Path
import os
import argparse

#nlp = de_core_news_sm.load()
nlp = spacy.load("de_core_news_sm", disable=["tok2vec", "tagger", "parser", "attribute_ruler", "lemmatizer"])

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

#        if token.orth_.isspace():
#            continue
#        elif token.like_url:
#            lda_tokens.append('URL')
#        elif token.orth_.startswith('

def tokenize(text):
    lda_tokens = []
    text2 = "tests2"
    doc = nlp(text2)
    print([(w.text, w.pos_) for w in doc])
#    tokens = parser(text)
#    for token in tokens:
#        if token.orth_.isspace():
#            continue
#        elif token.like_url:
#            lda_tokens.append('URL')
#        elif token.orth_.startswith('@'):
#            lda_tokens.append('SCREEN_NAME')
#        else:
#            lda_tokens.append(token.lower_)
    return lda_tokens


file_name = args.file
try:
    with open("data/txts/{}".format(file_name), 'r') as file:
        content = file.read()
        summary = tokenize(content)
        Path("data/tokenized").mkdir(parents=True, exist_ok=True)
        path_to_txt = "data/tokenized/" + file_name
        with open(path_to_txt, "w") as txt_file:
            txt_file.write(summary)
except:
    content = '{}.txt not found>'.format(file_name)    



