#!/usr/bin/env python3.7
# Artifact repository for PP0 - for more information see
# https://github.com/yossioren/pp0
# WS server that sends nano timestamps whenever it gets prompted

import asyncio
import websockets
import time
import json
import argparse

WEBSOCKET_PROBE_DATA = "."

async def nanotimer(websocket, path):
    last_time = 0
    probe_list = []
    while True:
        try:
            # wait for some input
            ws_input = await websocket.recv()

            if ws_input[0] == WEBSOCKET_PROBE_DATA:
                if last_time == 0:
                    last_time = time.time_ns()
                else:
                    new_time = time.time_ns()
                    probe_list.append((new_time - last_time) * 1.0 / 1000) # nanoseconds to milliseconds
                    last_time = new_time

            # If this is anything else, send the trace back home
            else:
                print(probe_list)
                await websocket.send(json.dumps(probe_list))

                # the client will hang up now
        except:
            # websock failed, quit the while loop
            break

parser = argparse.ArgumentParser(description='Start a WebSockets server with nanosecond resolution implemented in Python.')
parser.add_argument('--port', default=8080, type=int, help='The port to listen on.')
args = parser.parse_args()

print("Listening on port ", args.port)
start_server = websockets.serve(nanotimer, '', args.port)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
