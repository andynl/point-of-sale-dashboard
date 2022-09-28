from datetime import datetime
import random
import uuid
from typing import Any, List, Tuple
from faker import Faker

def _get_orders(cust_ids: List[int], num_orders: int):
    # order_id, customer_id, item_id, item_name, size, ordered_on
    fake = Faker(["id_ID"])
    items = [
        "Caffe Latte",
        "Cappuccino",
        "Flat White",
        "Americano",
        "Caffe Mocha",
        "Chocolate Cappuccino",
    ]

    sizes = [
        "Large",
        "Medium",
        "Small"
    ]

    data = ""
    for _ in range(num_orders):
        data += f'{uuid.uuid4()},{random.choice(cust_ids)},'
        data += f'{uuid.uuid4()},{random.choice(items)},'
        data += f'{random.choice(sizes)},'
        data += f'{fake.date_time_between(start_date="-7d", end_date="now")}'
        data += f"\n"

    return data

def _get_products():
    items = [
        [1, "Caffe Latte"],
        [2, "Cappuccino",]
        # "Flat White",
        # "Americano",
        # "Caffe Mocha",
        # "Chocolate Cappuccino",
    ]

    data = ""
    data = [row[1] for row in items]
            #  data += f'{items[i],items[j]}'

    return data

if __name__ == "__main__":
    # print("Run")
    # cust_ids = [random.randint(1, 10000) for _ in range(1000)]
    # _get_orders(cust_ids, 100)
    print(_get_products())