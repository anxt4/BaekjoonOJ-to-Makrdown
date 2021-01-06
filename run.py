#-*- coding:utf-8 -*-
#!/usr/local/bin/python3


import html2markdown as md
from bs4 import BeautifulSoup
import request, sys

if len(sys.argv) == 2:
   URL = sys.argv[1]
else: exit()

html = request.get(URL).text
soup = BeautifulSoup(html, 'html.parser')


def title(soup):
    title = soup.h1.text.strip()
    title = title[:title.find('\n')]
    return "# " + title +'\n'


def body(soup):
    problem_body = soup.find('div', {'id': 'problem-body'})
    problem = problem_body.find_all('div', {'class': 'col-md-12'})

    md_text = []
    for div in problem:
        h2 = div.find_all('h2')

        if len(h2) >= 2:
            simple_data = div.find_all('pre', {'class':"sampledata"})
            for h, data in zip(h2, simple_data):
                title = h.text[:h.text.find('\n')]
                data = data.text.strip()
                md_text.append("## " + title + "\n" )
                md_text.append("```\n" + data + "\n```" + "\n" )
        else:
            title = md.convert(str(div.h2)) + "\n"
        try:
            content = div.p.get_text().replace('\xa0', ' ')  + "\n"
        except :
            continue
        md_text.append(title)
        md_text.append(content)
    return md_text

def reference(URL):
    line = ["\n"]
    line.append("### 출처\n")
    line.append(str(URL))
    return line



with open('README.md', 'w') as file:
    file.writelines(title(soup))
    file.writelines(body(soup))
    file.writelines(reference(URL))
