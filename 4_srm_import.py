from pathlib import Path
import json
import io
#import simplejson as json

def read_jls_and_txts_into_json():
    papers = []
    pathlist = Path("data/").glob("**/*.jl")
    for file_path in pathlist:
        with io.open(file_path, 'r', encoding='utf8') as f:
            j = 0
            for line in f:
                if j > 3:
                    break
                j_content = json.loads(line)
                body = "Leipzig"#j_content['body']
                if 'mainFile' in j_content:
                    fileName = j_content['mainFile']['fileName'][:-4]
                    try:
                        with open('data/txts/{}.txt'.format(fileName), 'r') as file:
                            content = file.read()
                    except:
                        content = '<data/txts/{}.txt not found>'.format(fileName)    
                else:
                    content = "<empty>"
                name = j_content['name']
                resolution = None #j_content['resolution']
                if 'leipzig:originator' in j_content:
                    originator = j_content['leipzig:originator']
                else:
                    originator = 'Unbekannt'
                paper_type = j_content['paperType']
                published_at = j_content['date']
                reference = j_content['reference']
                url = j_content['web']

                #print("body ", body)
                #print("content ", content)
                #print("name ", name)
                #print("resolution ", resolution)
                #print("originator ", originator)
                #print("paper_type ", paper_type)
                #print("published_at ", published_at)
                #print("reference ", reference)
                print("url ", url)

                paperdict = {}
                paperdict["body"] = body
                paperdict["content"] = content
                paperdict["name"] = name
                paperdict["resolution"] = resolution
                paperdict["originator"] = originator
                paperdict["paper_type"] = paper_type
                paperdict["published_at"] = published_at
                paperdict["reference"] = reference
                paperdict["url"] = url
                papers.append(paperdict)
    return papers

def write_to_json():
    with io.open('input.json', 'w', encoding='utf8') as json_file:
        json.dump(read_jls_and_txts_into_json(), json_file)

write_to_json()
