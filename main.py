import fetch_twitch
import write
import asyncio


if __name__ == '__main__':
	streamer_list = [
		'gamjagabee',
		'gunaguna00',
		'beadyo97',
		'vnek1234',
		'kbs9981',
		'adricham',
		'yudarlinn',
		'gofl2237',
		'jeeya0402',
		'kimc6h12o6',
	]

	for streamer in streamer_list:
		[streamer, success_rate, cts] = asyncio.run(fetch_twitch.fetch(streamer))
		

	# write.write('[TEST] 자동등록 Test 중입니다', '<p>자동등록 테스트 중입니다. 곧 삭제 에정입니다. - 여의도연구원</p>')




