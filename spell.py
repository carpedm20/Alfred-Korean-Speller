import sys
import unicodedata
from ast import literal_eval

import requests
from bs4 import BeautifulSoup
import bs4


def find_parens(s):
    toret = {}
    pstack = []
    for i, c in enumerate(s):
        if c == '[':
            pstack.append(i)
        elif c == ']':
            if len(pstack) == 0:
                raise IndexError("No matching closing parens at: " + str(i))
            toret[pstack.pop()] = i
    if len(pstack) > 0:
        raise IndexError("No matching opening parens at: " + str(pstack.pop()))
    return toret

full_url = "http://speller.cs.pusan.ac.kr/results"

query = sys.argv[1]
#q = query.decode('utf-8')
q = query
q = unicodedata.normalize("NFC", q)
#q = q.encode('utf-8')

r = requests.post(full_url, data={'text1': " ".join(q.split())})

soup = BeautifulSoup(r.content)
# javascript portion
s = soup.find_all('script')[-1].text
paren_start = 39
paren_dict = find_parens(s)

if paren_dict:
    paren_end = paren_dict[paren_start]
    answers = []
    for x, y in [(k['orgStr'], k['candWord']) for k in literal_eval(s[paren_start:paren_end+1])[0]['errInfo']]:
        answers.append(" ".join(y.split()))
        # print("{}\n\t->".format(x.contents[0].encode('utf-8'))),
        print("{} -> {}\n".format(x, " ".join(y.split())))
        # print("{}\n\t->".format(x)),
        # #print("{}".format('\n\t-> '.join([x for x in y.contents if type(x) != bs4.element.Tag]).encode('utf-8')))
        # print("{}".format('\n\t-> '.join([x for x in yif type(x) != bs4.element.Tag])))
    # candidates = " ".join(answers).split("|")
    # if len(candidates) > 1:
    #     for idx, answer in enumerate(candidates):
    #         print(f"{idx}. {answer}")
    # else:
    #     print(" ".join(answers))
else:
    print("Done.")
