import argparse
import os
import sys
import requests
import json
from credentials import SMMRY_URL, SMMRY_API_KEY


def summarizeText(text):
    url=SMMRY_URL+'&SM_API_KEY='+SMMRY_API_KEY
    headers={
    'Expect':''
    }
    response=requests.post(url, data={'sm_api_input':text}, headers=headers)
    summary=json.loads(response.content.decode('utf-8'))
    return summary

def summarizeFile(file):
    print("Input file is: {}".format(args.ifile.name))
    fileText=args.ifile.read()
    return summarizeText(fileText)

def summarizeURL(url, lines=None):
    # print("URL to summarize is: {}".format(url))
    url=SMMRY_URL+'&SM_API_KEY='+SMMRY_API_KEY+'&SM_URL='+url
    if lines:
        url += '&SM_LENGTH=' + str(lines)
    response=requests.get(url)
    summary=json.loads(response.content.decode('utf-8'))
    return summary

def summarizeStdin():
    inp=input("Using standard input for summary. Type the text you want to summarize:")
    return summarizeText(inp)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group=parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--ifile', type=argparse.FileType('r'), help='Input file to summarize')
    group.add_argument('-u', '--url', help='URL of page to summarize')
    parser.add_argument('-o', '--ofile', type=argparse.FileType('w', encoding='UTF-8'), help='Output file')

    args = parser.parse_args()
    if args.ifile:
        summary=summarizeFile(args.ifile)
    elif args.url:
        summary=summarizeURL(args.url)
    else:
        summary=summarizeStdin()
    if args.ofile:
        print("Summary was written to: {}".format(args.ofile.name))
        args.ofile.write(summary)
    else:
        print("The summarized text is:\n{}".format(summary))