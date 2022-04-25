import fetch_twitch
import write
import db
import asyncio
import time


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
		if db_process:
			db.write(database, db_process)
			if db_process[1] == 'ON':  # 뱅온일 때만 등록
				[subject, content] = write.create_content(database, db_process)
				write.write(subject, content)
		time.sleep(5)
	print("======== END ========")
	print("")



