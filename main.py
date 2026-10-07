"""Count scalar JSON value types recursively."""
import argparse,csv,io,json,math,re
from collections import Counter
from datetime import date,datetime
from pathlib import Path

import base64,ipaddress,uuid
from urllib.parse import parse_qsl,urlsplit
from http.cookies import SimpleCookie

def analyze(data):
    counts=Counter()
    def visit(value):
        if isinstance(value,dict):
            for child in value.values():visit(child)
        elif isinstance(value,list):
            for child in value:visit(child)
        else:
            kind='null' if value is None else 'boolean' if isinstance(value,bool) else 'integer' if isinstance(value,int) else 'number' if isinstance(value,float) else 'string'
            counts[kind]+=1
    visit(data['document']);return dict(sorted(counts.items()))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',type=Path,help='UTF-8 JSON input file')
    parser.add_argument('--explain',action='store_true',help='Send the local report to the configured chat gateway')
    args=parser.parse_args()
    report=analyze(json.loads(args.input.read_text(encoding='utf-8')))
    if args.explain:
        from gateway_client import explain
        print(explain(report))
    else:print(json.dumps(report,ensure_ascii=False,indent=2))
