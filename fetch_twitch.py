"""
Fetch Twitch RULE
[참고] https://github.com/LeftBased/StreamLiveChecker
"""
from time import time
import requests
from lxml import html
import os
import asyncio

async def fetch(streamer):
	cts = None
	try:
		loop = asyncio.get_event_loop()
		url = "https://twitch.tv/" + streamer

		send1 = loop.run_in_executor(None, requests.get, url)
		send2 = loop.run_in_executor(None, requests.get, url)
		send3 = loop.run_in_executor(None, requests.get, url)
		send4 = loop.run_in_executor(None, requests.get, url)
		send5 = loop.run_in_executor(None, requests.get, url)
		
		res1 = await send1
		res2 = await send2
		res3 = await send3
		res4 = await send4
		res5 = await send5

		body1 = res1.text
		body2 = res2.text
		body3 = res3.text
		body4 = res4.text
		body5 = res5.text

		success_rate = 0

		if "isLiveBroadcast" in body1:
			cts = True
			success_rate += 20
		if "isLiveBroadcast" in body2:
			cts = True
			success_rate += 20
		if "isLiveBroadcast" in body3:
			cts = True
			success_rate += 20
		if "isLiveBroadcast" in body4:
			cts = True
			success_rate += 20
		if "isLiveBroadcast" in body5:
			cts = True
			success_rate += 20
		else:
			cts = False
		print(streamer, success_rate, cts)
	except Exception as e:
		print(e)
	finally:
		return [streamer, cts, success_rate]

