import xml
import codecs
import sys
import json
import hashlib
import random
import urllib

def main(argv):
    argv.append('chatlog.txt')
    chat_list = open(argv[1]).readlines()
    doc_list = ['<add>\n']


    i = 0

    for line in chat_list:
        sentence = line.split(':')
        striped_str = map(str.strip, sentence)
        if 1 < len(striped_str):
            doc_list.append('<doc>\n')
            doc_list.append('<field name="id">%s</field>\n' % i)
            doc_list.append('<field name="name">%s</field>\n' % striped_str[0])
            doc_list.append('<field name="manu">%s</field>\n' % urllib.quote(striped_str[1]))
            doc_list.append('</doc>\n')


        i += 1

    doc_list.append('</add>\n')
    with open('chat.xml', 'w') as f:
        f.writelines(doc_list)
'''

    for line in chat_list:
        sentence = line.split(':')
        striped_str = map(str.strip, sentence)
        if 1 < len(striped_str):
            print '<id>%s</id>' % striped_str[0]
            print '<content>%s</content>' % striped_str[1]
            doc = {}
            doc['id'] = striped_str[0]
            doc['content'] = striped_str[1]

            print json.dumps(doc)
            doc_list.append(doc)
            
    with open('chat.json', 'w') as f:
        f.writelines(json.dumps(doc_list))
'''

if __name__ == "__main__":
    main(sys.argv)
