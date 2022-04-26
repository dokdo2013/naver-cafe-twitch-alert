import os
import dotenv
from pytz import timezone
import datetime
from sqlalchemy import create_engine


def init():
	dotenv.load_dotenv()
	DB_HOSTNAME = os.getenv('DB_HOSTNAME')
	DB_USERNAME = os.getenv('DB_USERNAME')
	DB_PASSWORD = os.getenv('DB_PASSWORD')
	DB_DATABASE = os.getenv('DB_DATABASE')
	DB_PORT = os.getenv('DB_PORT')

	dbinfo = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/{DB_DATABASE}"
	db = create_engine(dbinfo)
	return db


def db_process(db, data):
	# 뱅온/뱅종 상태가 서로 다를 경우 -> 등록 및 이벤트 발행
	streamer_name = data[0]
	current_status = data[1]
	success_rate = data[2]
	if current_status:
		current_status_msg = 'ON'
		decision_rate = success_rate
	else:
		current_status_msg = 'OFF'
		decision_rate = 100 - success_rate
	streamer_idx = get_idx(db, streamer_name)
	db_status = get_db_status(db, streamer_idx)
	current_time_now = datetime.datetime.now(timezone('Asia/Seoul'))
	current_time = current_time_now.strftime("%Y-%m-%d %H:%M:%S")
	
	if db_status != current_status_msg:
		init_data = [streamer_idx, current_status_msg, decision_rate, current_time]
	else:
		init_data = False
	return init_data


def write(db, data):
	if data[1] == 'ON':
		sql1 = f"UPDATE leaven SET broadcast_status = 'ON', on_broadcast_datetime = '{data[3]}', update_datetime = '{data[3]}' WHERE idx = {data[0]}"
	else:
		sql1 = f"UPDATE leaven SET broadcast_status = 'OFF', off_broadcast_datetime = '{data[3]}', update_datetime = '{data[3]}' WHERE idx = {data[0]}"
	sql2 = f"INSERT INTO leaven_history(leaven_idx, action_type, decision_rate) VALUES({data[0]}, '{data[1]}', {data[2]})"
	db.execute(sql1)
	db.execute(sql2)


def get_idx(db, streamer_name):
	sql = f"SELECT idx FROM leaven WHERE streamer_name = '{streamer_name}'"
	res = db.execute(sql)
	return res.fetchone()['idx']


def get_db_status(db, streamer_idx):
	sql = f"SELECT broadcast_status FROM leaven WHERE idx = {streamer_idx}"
	res = db.execute(sql)
	return res.fetchone()['broadcast_status']


def get_info(db, streamer_idx):
	sql = f"SELECT * FROM leaven WHERE idx = {streamer_idx}"
	res = db.execute(sql)
	return res.fetchone()
