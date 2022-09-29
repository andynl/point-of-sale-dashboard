from datetime import date, datetime, timedelta
import random
from time import time
import uuid
from typing import Any, List, Tuple
from faker import Faker
import psycopg2
import boto3

def _get_orders(cust_ids: List[int], num_orders: int) -> str:
    # order_id, customer_id, item_id, item_name, price, size, ordered_at, payment_at
    sizes = [
        "Large",
        "Medium",
        "Small"
    ]
    dt = datetime.now().strftime("%y-%m-%d %H:%M:%S")
    data = ""
    for _ in range(num_orders):
        data += f'{uuid.uuid4()},{random.choice(cust_ids)},'
        data += f'{_get_products()},'
        data += f'{random.choice(sizes)},'
        data += f'{dt},{datetime.strptime(dt, "%y-%m-%d %H:%M:%S") + timedelta(hours=random.randint(1, 5))}'
        data += f"\n"

    return data

def _get_products() -> str:
    items = [
        [1, "Caffe Latte", 10],
        [2, "Cappuccino", 20],
        [3, "Flat White", 5],
        [4, "Americano", 10],
        [5, "Caffe Mocha", 17],
        [6, "Chocolate Cappuccino", 20]
    ]
    
    item = random.choice(items)
    data = ""
    data += f'{item[0]},{item[1]},{item[2]}'

    return data

def _get_customers(cust_ids: List[int]) -> List[Tuple[int, Any, Any, str, str, str]]:
    fake = Faker('id_ID')
    status = [
        "NEW",
        "RETURNING"
    ]

    return [
        (
            cust_id,
            fake.first_name(),
            fake.last_name(),
            random.choice(status),
            datetime.now().strftime("%y-%m-%d %H:%M:%S"),
            datetime.now().strftime("%y-%m-%d %H:%M:%S")
        )
        for cust_id in cust_ids
    ]

def _customer_data_insert_query() -> str:
    return """
        INSERT INTO customers (
            customer_id,
            first_name,
            last_name,
            status,
            datetime_created,
            datetime_updated
        )
        VALUES (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
        )
        on conflict(customer_id)
        do update set
            (first_name, last_name, status, datetime_updated) =
            (EXCLUDED.first_name, EXCLUDED.last_name,
            EXCLUDED.state_code, EXCLUDED.datetime_updated);
    """

def generate_data(iteration: int, orders_bucket = "app-orders") -> None:
    cust_ids = [random.randint(1, 10000) for _ in range(1000)]
    orders_data = _get_orders(cust_ids, 10000)
    customers_data = _get_customers(cust_ids)

    # send orders data to s3
    s3 = boto3.resource(
        "s3",
        endpoint_url="http://cloud-store:9000",
        aws_access_key_id="",
        aws_secret_access_key="",
        region_name=""
    )
    # create bucket if not exists
    if not s3.Bucket(orders_bucket) in s3.buckets.all():
        s3.create_bucket(Bucket=orders_bucket)
    s3.Object(orders_bucket, f"data_{str(iteration)}.csv").put(
        Body=orders_data
    )

    # send customers data to customer_db
    with DatabaseConnection().managed_cursor() as curr:
        insert_query = _customer_data_insert_query()
    for cd in customers_data:
        curr.execute(
            insert_query,
            (
                cd[1],
                cd[2],
                cd[3],
                cd[4],
                cd[5],
            )
        )


class DatabaseConnection:
    def __init__(self):
        self.conn_url = (
            "postgresql://customer_ms:password@customer_db:5432/customer"
        )

    def managed_cursor(self, cursor_factory=None):
        self.conn = psycopg2.connect(self.conn_url)
        self.conn.autocommit = True
        self.curr = self.conn.cursor(cursor_factory=cursor_factory)
        try:
            yield self.curr
        finally:
            self.curr.close()
            self.conn.close()

if __name__ == "__main__":
    itr = 1
    while True:
        generate_data(itr)
        time.sleep(30)
        itr + 1