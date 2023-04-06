from pymongo import MongoClient
from datetime import datetime
import json
from config import HOST, POST, DB_NAME, COL_NAME,BOT_TOKEN
from aiogram import Bot, Dispatcher, executor, types

client = MongoClient(HOST, POST)
db = client[DB_NAME]
collection = db[COL_NAME]
API_TOKEN = BOT_TOKEN

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

def get_report(dt_from, dt_upto, group_type):
    group_mode = {}

    dt_from = datetime.strptime(dt_from, "%Y-%m-%dT%H:%M:%S")
    dt_upto = datetime.strptime(dt_upto, "%Y-%m-%dT%H:%M:%S")

    if group_type == "hour":
        group_mode = {
            'year': {'$year': '$dt'},
            'month': {'$month': '$dt'},
            'day': {'$dayOfMonth': '$dt'},
            'hour': {'$hour': '$dt'},
        }
    elif group_type == "day":
        group_mode = {
            'year': {'$year': '$dt'},
            'month': {'$month': '$dt'},
            'day': {'$dayOfMonth': '$dt'},
        }
    elif group_type == "week":
        group_mode = {
            'year': {'$year': '$dt'},
            'month': {'$month': '$dt'},
            'week': {'$week': '$dt'},
        }
    elif group_type == "month":
        group_mode = {
            'year': {'$year': '$dt'},
            'month': {'$month': '$dt'},
        }

    pipeline = [
        {
            '$match': {
                'dt': {
                    '$gte': dt_from,
                    '$lte': dt_upto
                }
            }
        },
        {
            "$group":
                {
                    '_id': group_mode,
                    "total": {"$sum": "$value"},
                    "date": {"$first": '$dt'}
                }
        }
    ]
    result = collection.aggregate(pipeline)
    result_dict = {
        'dataset': [],
        'labels': []
    }
    for item in result:
        result_dict['dataset'].append(item['total'])
        result_dict['labels'].append(item['date'].isoformat(sep='T',timespec='auto'))
    return result_dict

@dp.message_handler()
async def echo(message: types.Message):
    query = json.loads(message.text)
    result = get_report(query['dt_from'], query['dt_upto'], query['group_type'])
    await message.answer(str(result))

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
