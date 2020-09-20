from pathlib import Path
import json
import io
#import simplejson as json

def read_jls_and_txts_into_json():
    file_path = Path("data/paper_2020-07-15T17-28-50.jl")
    papers = []
    with io.open(file_path, 'r', encoding='utf8') as f:
        j = 0
        for line in f:
            if j > 3:
                break
            j_content = json.loads(line)
            body = "Leipzig"#j_content['body']
            if 'mainFile' in j_content:
                fileName = j_content['mainFile']['fileName'][:-4]
                with open('data/txts/{}.txt'.format(fileName), 'r') as file:
                    content = file.read()
            else:
                content = "<empty>"
            name = j_content['name']
            resolution = None #j_content['resolution']
            originator = j_content['leipzig:originator']
            paper_type = j_content['paperType']
            published_at = j_content['created']
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
