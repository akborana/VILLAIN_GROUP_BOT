from pyrogram import filters

# Credits AKAY TEAM


def callback_data(data):
    def func(flt, client, callback_query):
        return callback_query.data in flt.data

    data = data if isinstance(data, list) else [data]
    return filters.create(func, "CustomCallbackDataFilter", data=data)
