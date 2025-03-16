import vertexai
from vertexai.language_models import TextGenerationModel
from bs4 import BeautifulSoup as bs
import io
import pypandoc
import panflute
import time



def summ (text):
    project_id = "optimum-task-411411"
    location = "us-west1"
    
    vertexai.init(project=project_id, location=location)
    
    parameters = {
        "temperature": 0.2,
        "max_output_tokens": 2048,
        "top_p": 0.95,
        "top_k": 40,
    }

    model = TextGenerationModel.from_pretrained("text-bison@002")
    
    #j = "Bonsoir, a bientot"
    
    response = model.predict (text, **parameters)
    
    # print (f"Response is: response.text}")
    
    return response

PROMPT = "Answer this viva question of C++ OOP"


data = pypandoc.convert_file ("sample.md", "html")
soup = bs (data, "html.parser")

# print (soup.prettify ())

head = soup.find_all ("ol")
text = soup.find_all ("li")

op = open ("op.md", "w")

for i in head:
    print ("\nEnding sleep;")
    op.write (f"## {i.string}\n")
    # print (i.prettify ())

    # text = head.findChildren ()
    
    for j in i.children:
        print (f"{j.string}")
        op.write (f"### {j.string}\n")
        
        res = summ (PROMPT + j.string)
        op.write (f"{res.text}\n\n")
    print ("\nstarting sleep;")
    time.sleep (2 * 60)
    
op.close ()
