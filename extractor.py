import xml
import codecs
import sys
import json
import hashlib
import random
import urllib
import re

def main(argv):

    chat_log = None
#'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}Z - info: \[app.js\] msg=.*, color=#.{6}'

    with open('0918.log') as f:
        chat_log = f.read()

    pattern = re.compile('(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}Z) - info: \[.*\] Message in \[(.*)\]\n\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}Z - info: \[app.js\] msg=(.*), color=#(.{6})', re.MULTILINE)
    result = re.findall(pattern, chat_log)

    doc_list = []
    doc_list.append('<add>\n')

    record_number = 0
    for i in result:
        doc_list.append('<doc>\n')
        doc_list.append('\t<field name="id">%s</field>\n' % record_number)
        doc_list.append('\t<field name="date">%s</field>\n' % i[0])
        doc_list.append('\t<field name="room">%s</field>\n' % i[1])
        doc_list.append('\t<field name="msg">%s</field>\n' % i[2])
        doc_list.append('\t<field name="color">%s</field>\n' % i[3])
        doc_list.append('</doc>\n')

        record_number += 1

    doc_list.append('</add>\n')

    with open('chat_log.xml', 'w') as f:
        f.writelines(doc_list)

if __name__ == "__main__":
    main(sys.argv)
