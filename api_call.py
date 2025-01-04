#!/usr/bin/python3
#
# - Python module update the patchengine database
# - To Insert data use: python api_call.py insert <token>  <patchid>i <serverid> <changeid> <ownemail> <appemail> <status> <date>
# - To Update table use: python api_call.py update <token> <patchid> <status> <date>
# - To Delete dara use: python api_call.py delete <token> <patchid> <serverid>
# - Ensure the pip modules installed: requests
# - Author: Sunil Kamba Vasu(sunil.hclkv@gmail.com)
#

import requests
import sys

name_of_script = sys.argv[0]
action = sys.argv[1]
baseurl = <URL>

def update_post():
    url = baseurl + "/" + action + "/" + token + "/" + patchid + "/" + status + "/" + date
    try:
        response = requests.get(url)
        print('Response code:', response.status_code)
        print(response.content)
        return None
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None
def insert_post():
    url = baseurl + "/" + action + "/" + token + "/" + patchid + "/" + serverid + "/" + changeid + "/" + own + "/" + app + "/" + status + "/" + date
    try:
        response = requests.get(url)
        print('Response code:', response.status_code)
        print(response.content)
        return None
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None
def delete_post():
    url = baseurl + "/" + action + "/" + token + "/" + patchid + "/" + serverid
    try:
        response = requests.get(url)
        print('Response code:', response.status_code)
        print(response.content)
        return None
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None

if action == 'update':
    token = sys.argv[2]
    patchid = sys.argv[3]
    status = sys.argv[4]
    date = sys.argv[5]
    update_post()
if action == 'insert':
    token = sys.argv[2]
    patchid = sys.argv[3]
    changeid = sys.argv[4]
    serverid = sys.argv[5]
    own = sys.argv[6]
    app = sys.argv[7]
    status = sys.argv[8]
    date = sys.argv[9]
    insert_post()
if action == 'delete':
    token = sys.argv[2]
    patchid = sys.argv[3]
    serverid = sys.argv[4]
    delete_post()
