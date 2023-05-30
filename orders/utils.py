import datetime



def generate_order_number(pk):
    now = datetime.datetime.now()
    return 'ORD-' + str(now.year) + str(now.month) + str(now.day) + str(now.hour) + str(now.minute) + str(now.second) + str(pk)