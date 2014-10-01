#-*- encoding: utf-8 -*-
import xml
import codecs
import sys
import json
import hashlib
import random
import urllib
import re
import json
import operator
import random
import string
import os

def encode(s):
    return u' '.join([s, ' ']).encode('utf-8').strip()

def writeGraph(term_list, output):
    if not term_list:
        return

    for term in term_list:
        for child in term['childs']:
            encoded_term = u' '.join([term['term'], ' ']).encode('utf-8').strip()
            encoded_child = u' '.join([child['term'], ' ']).encode('utf-8').strip()
            output.writelines(['\t', encoded_term, ' -- ', encoded_child, '\r'])
            writeGraph(child['childs'], output)

def generateChilds(term, cluster, max, depth, parent_list = []):

    if 0 >= depth:
        return

    candidate_child_list = getChilds(term, cluster['points'], max)

    child_list = []
    for child in candidate_child_list:
        child_list.append({
            'term': child,
            'childs': generateChilds(child, cluster['points'], max, depth - 1, parent_list)
        })

    return child_list

def getChilds(term, points, max):

    childs = {}

    for word in filter(lambda words: True if term in words['point'] else False, points):
        pattern = re.compile('.*=.*\[(.*)\]')
        result = re.match(pattern, word['point'])

        for candidate_child in map(lambda x: x.split(':'), result.group(1).split(', ')):
            name, weight = candidate_child[0], candidate_child[1]

            if 2 > len(name): # skip if name length == 1
                continue
            try:
                childs[name] += weight
            except KeyError:
                childs[name] = weight

    # cut term
    del childs[term]

    return sorted(childs.iterkeys(), key=(lambda key: childs[key]))[:max]

def main(argv):

    input_file_name = 'cute.json'
    output_file_name = 'cute'
#    term_max = argv[1]
#    child_max = argv[2]
#    depth = argv[3]

    term_max = 10
    child_max = 5
    depth = 1

    cluster_list = []
    with open(input_file_name) as f:
        for l in f.readlines():
            try:
                cluster_list.append(json.loads(l))
            except: #TODO: checking exception name
                pass

    output_list = []
    for cluster in cluster_list:

        term_list = []
        for idx, term in enumerate(cluster['top_terms']):
            if idx > term_max:
                break
            if 2 > len(term['term']): # skip if term word length == 1
                continue

            term_list.append({
                'term': term['term'],
                'childs': generateChilds(term['term'], cluster, child_max, depth)
            });

        output_list.append(term_list[0]['term'] + '.dot')

        output_file = open(output_list[-1], 'w')
        output_file.writelines(['graph ' + term_list[0]['term'] + ' {', '\r'])
        output_file.writelines(['ratio = fill; node [style=filled];', '\r'])

        for idx, term in enumerate(term_list):
            output_file.writelines([encode(term['term']), ' [sides=9, distortion="0.936354", orientation=28, skew="-0.126818", color="#FF' + ('%02x%02x' % ((idx * 25), (idx * 16))) + '"];', '\r']) 

        writeGraph(term_list, output_file)

        output_file.writelines(['}'])
        output_file.close()

    pic_list = []
    ext = 'png'
    for output in output_list:
        pic_list.append(os.path.splitext(output)[0] + ext)
        os.system('dot ' + output + ' -T' + ext + ' -Gcharset=latin1 > /usr/share/nginx/html/' + output_file_name + '/' + pic_list[-1])

    html = open('/usr/share/nginx/html/' + output_file_name + '/' + output_file_name + '.html', 'w')

    html.writelines(['<html><head></head><body>', '\r'])
    for pic in pic_list:
        html.writelines(['<img border="5" src="', pic, ' "/>', '\r'])

    html.writelines(['</body></html>'])

    html.close()

if __name__ == "__main__":
    main(sys.argv)
