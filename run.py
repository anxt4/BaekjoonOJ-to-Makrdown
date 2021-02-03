#-*- coding:utf-8 -*-
#!/usr/local/bin/python3

# test
import html2markdown as md
from bs4 import BeautifulSoup
import request, sys
from itertools import zip_longest

if len(sys.argv) == 2:
   URL = sys.argv[1]
else: exit()
PREFIX_URL = 'https://www.acmicpc.net'
html = request.get(URL).text
soup = BeautifulSoup(html, 'html.parser')

""" set html title """
def title(soup):
    title = soup.h1.text.strip()
    title = title[:title.find('\n')]
    title = ['# ' + title]
    title.append('   \n')
    return title

""" set html body """
def body(soup):
    problem_body = soup.find('div', {'id': 'problem-body'})
    problem = problem_body.find_all('div', {'class': 'col-md-12'})

    md_text = []
    for div in problem:
        heads = div.find_all('h2') # h2
        paragraphs = div.find_all('p') # paragraph
        samples = div.find_all('pre', {'class':"sampledata"}) #sample data

        for head, paragraph, sample in zip_longest(heads, paragraphs, samples):
            if head and not paragraph and not sample:
                continue
            if head: #말머리
                try:
                    head_text = head.text.replace('복사', '').strip()
                except:
                    head_text = head.text
                md_text.append('## ' + head_text )
                md_text.append('   \n')
            if paragraph: #본문
                md_text.append(md.convert(str(paragraph)))
                md_text.append('   \n')
                md_text.append('   \n')
                if paragraph.img: #이미지
                    if str(paragraph.img).find('https') > 0:
                        md_text.append(str(paragraph.img))
                    else:
                        md_text.append(str(paragraph.img).replace('src="', 'src="'+ PREFIX_URL ))
                    md_text.append('   \n')
                    md_text.append('   \n')
            if sample: #예제 입력
                md_text.append('```')
                md_text.append('   \n')
                md_text.append(sample.text.strip())
                md_text.append('   \n')
                md_text.append('```')
                md_text.append('   \n')

    return md_text

""" set html reference """
def reference(URL):
    line = ["\n"]
    line.append("### 출처\n")
    line.append(str(URL))
    return line


with open('README.md', 'w') as file:
    file.writelines(title(soup))
    file.writelines(body(soup))
    file.writelines(reference(URL))
