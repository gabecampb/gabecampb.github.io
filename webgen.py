# webgen.py | Gabriel Campbell 2023 (github.com/gabecampb) | Public domain

# requires 'markdown' module to be installed:
#       pip install markdown

import markdown
import sys

if(len(sys.argv) != 2):
    print(sys.argv[0], "-> missing name of input .md file")
    exit(1)

content = ""
with open("docs/" + sys.argv[1], "r") as file:
    content = file.read()
content = markdown.markdown(content)

html = ""
with open("template.html", "r") as file:
    html = file.read()

metadata_start = html.index("PAGE_METADATA")
metadata_end = metadata_start + html[metadata_start:].index('\n')

content_start = html.index("PAGE_CONTENT")
content_end = content_start + html[content_start:].index('\n')

metadata = "<title>ASSEMBLER.MOV</title>"

html = html[:metadata_start-1] + metadata + html[metadata_end:content_start-1] + content + html[content_end:]

with open("index.html", "w") as file:
    file.write(html)
