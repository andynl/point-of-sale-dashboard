from datetime import date, datetime, timedelta
import random
import uuid
from typing import Any, List, Tuple
from faker import Faker
import time

def _get_orders(cust_ids: List[int], num_orders: int):
    # order_id, customer_id, item_id, item_name, size, ordered_on, payment_at
    fake = Faker(["id_ID"])

    sizes = [
        "Large",
        "Medium",
        "Small"
    ]
    data = ""
    for _ in range(num_orders):
        data += f'{uuid.uuid4()},{random.choice(cust_ids)},'
        data += f'{_get_products()},'
        data += f'{random.choice(sizes)},'
        data += f'{random_time_between()},'
        data += f'{random_time_between(random.randint(1,60))}'
        data += f"\n"

    # random_time()
    # add_hour(start)
 

    return data

def _get_products():
    items = [
        [1, "Caffe Latte"],
        [2, "Cappuccino"],
        [3, "Flat White"],
        [4, "Americano"],
        [5, "Caffe Mocha"],
        [6, "Chocolate Cappuccino"]
    ]
    
    item = random.choice(items)
    data = ""
    data += f'{item[0]},'
    data += f'{item[1]}'

    return data

def str_time_prop(start, end, time_format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formatted in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(time_format, time.localtime(ptime))

def covert_datetime(start, end, prop):
    return str_time_prop(start, end, '%Y-%m-%d %H:%M:%S', prop)

def random_time_between(pa = 0):
    today = date.today()
    start_time = datetime.strptime(f'{today} 9:00:00', '%Y-%m-%d %H:%M:%S')
    end_time = datetime.strptime(f'{today} 17:00:00', '%Y-%m-%d %H:%M:%S')
    return covert_datetime(datetime.strftime(start_time, "%Y-%m-%d %H:%M:%S"), datetime.strftime(end_time, "%Y-%m-%d %H:%M:%S"), random.random()) + timedelta(minutes=pa)
    
def random_payment_at(d):  
    dt = datetime.strptime(d, "%Y-%m-%d %H:%M:%S")
    return dt + timedelta(minutes=random.randint(1,60))

if __name__ == "__main__":
    cust_ids = [random.randint(1, 10000) for _ in range(1000)]
    print(_get_orders(cust_ids, 100))
    # print(_get_products())