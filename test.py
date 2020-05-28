# # import pymongo
# # from pymongo import MongoClient
# # import ssl
from datetime import datetime, timedelta


# db_data = {
#             '_id' : 124,
#             'data_count' : 2,
#             'data' : [
#                 {
#                     'list_id' : 1,
#                     'date' : '2020/06/30 1400',
#                     'todo': 'clear homework'
#                 },
#                 {
#                     'list_id' : 2,
#                     'date' : '2020/05/29 1100',
#                     'todo': 'clear dishes'
#                 }
#             ]
#         }
# # cluster = pymongo.MongoClient("mongodb+srv://tedmund123:tedmund123@tedcluster-aalbx.mongodb.net/test?retryWrites=true&w=majority", ssl=True, ssl_cert_reqs=ssl.CERT_NONE)
# # db = cluster.reminderbot
# # collection = db.jobs
# # for chat in collection.find({}):
# #     print(chat)

# import db_methods

# def update_list_id(newlist):
#     i = 1
#     for reminder in newlist:
#         reminder['list_id']  = i
#         i += 1

# db = db_methods.get_db()
# # db.delete_many({})
# chat = db.find_one({'_id':-425798228})
# # print(chat['data'])
# # find = db.find_one({'_id': -425798228, 'data': {'list_id' : 3 , '$exists': True }})
# # print(find)
# # db.update_one({'_id': -425798228}, {'$pull' : {'data' : {'list_id' : 2}}})

# # print(any(d['list_id'] == 1 for d in chat['data']))

# # print('You do not have any Reminders set' == True)
# print(datetime.strptime('2020-05-15 11:00:00', "%Y-%m-%d %H:%M:%S") < datetime.now())

# print(datetime.now().hour == datetime.now().hour

# from methods import db_methods
# db = db_methods.get_db()
# date_to_check = datetime.now()
# print(db.find_one(
#         {'_id': -425798228} ))

# reminder = {
#     'date' : datetime.now()
# }


# reminder_keywords = {
#     'weekly' : reminder['date'].replace(day=reminder['date'].day+7),
#     'daily': reminder['date'].replace(day=reminder['date'].day+1),
#     'monthly': reminder['date'].replace(month=reminder['date'].month+1)
# }

# print(reminder)
# reminder = reminder_keywords['weekly']
# print(reminder)

test = '1hr'
print(test.upper())