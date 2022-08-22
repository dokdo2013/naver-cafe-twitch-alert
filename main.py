import fetch_twitch
import write
import db
import asyncio
import time
import slack
import tmi


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

	database = db.init()
	print("======= START =======")
	for streamer in streamer_list:
		init_list = asyncio.run(fetch_twitch.fetch(streamer))
		db_process = db.db_process(database, init_list)
		if db_process[0]:  # 이전 상태와 다를 때 게시글 중복 등록 방어를 위해 추가 요청
			time.sleep(6)
			init_list2 = asyncio.run(fetch_twitch.fetch(streamer))
			db_process2 = db.db_process(database, init_list2)
			if db_process[1] != db_process2[1]:
				continue
			db.write(database, db_process)
			if db_process[1] == 'ON':  # 뱅온일 때만 등록
				[subject, content] = write.create_content(database, db_process)
				write.write(subject, content)
				slack.send(f"[뱅온 알림] https://twitch.tv/{streamer}")
				tmi.send(streamer)
			else:
				slack.send(f"[뱅종 알림] https://twitch.tv/{streamer}")
		time.sleep(5)
	print("======== END ========")
	print("")



