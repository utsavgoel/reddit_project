# Example POST request for automated_testing

import requests

files = {'upload_file': open('file.txt','rb')}
r = requests.post("https://afternoon-falls-83076.herokuapp.com/automated_testing", files=files)

# returns a JSON object
print(r.content)