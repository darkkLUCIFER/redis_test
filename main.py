import random
import redis

try:
    r = redis.StrictRedis(host='localhost', port=6379, db=1, password='', decode_responses=True)
    # r.set('key', 'value')
    # print(r.get('key'))

except Exception as e:
    print(f'[-] i can not connect to redis! {e}')


class Shop():

    def __init__(self):
        self.old_value = None
        self.product_price = None
        self.product_type = None
        self.product_date = None
        self.product_name = None
        self.product_key = None

        print('welcome to shop')
        r.set('admin', 'mahdi')
        r.set('shop_name', 'redis_shop')
        r.set('version', '1.0.0')

    def add_to_shop(self):
        counter = int(input('enter number of products:'))
        for i in range(0, counter):
            self.product_key = random.randint(1000, 10000)
            print(self.product_key)
            r.rpush('product_key', self.product_key)

            self.product_name = input('enter name of product')
            r.rpush('product_name', self.product_name)

            self.product_date = input('enter date')
            r.rpush('product_date', self.product_date)

            self.product_type = input('enter type of product')
            r.rpush('product_type', self.product_type)

            self.product_price = int(input('enter price'))
            r.rpush('product_price', self.product_price)

            r.hmset(self.product_key, {'product_name': self.product_name, 'product_date': self.product_date,
                                       'product_type': self.product_type, 'product_price': self.product_price})

    def display(self, key=None):
        if key == 'all':
            for i in r.lrange('product_key', 0, -1):
                for j in r.hgetall(i):
                    print(f'{i}:{j}, {r.hget(i, j)}')
        elif key == 'name':
            print(f'{r.lrange("product_name", 0, -1)}')

        elif key == 'price':
            print(f'{r.lrange("product_price", 0, -1)}')

    def update(self, key=None, field=None, value=None):
        self.old_value = r.hget(key, field)

        r.hset(key, value, field)
        if field == 'name':
            for i in range(r.llen('product_name')):
                if self.old_value == r.lindex('product_name', i):
                    r.lset('product_name', i, value)

        elif field == 'price':
            for i in range(r.llen('product_price')):
                if self.old_value == r.lindex('product_price', i):
                    r.lset('product_price', i, value)

    def sort(self, field=None):
        if field == 'product_price':
            print(r.sort(field))
        else:
            print(r.sort(field, alpha=True))

    def rev_sort(self, field=None):
        if field == 'product_price':
            print(r.sort(field), reversed)
        else:
            print(r.sort(field, alpha=True), reversed)

    def delete(self, key=None):
        r.delete(key)


if __name__ == '__main__':
    test_shop = Shop()
    test_shop.add_to_shop()
    test_shop.display()
    test_shop.update()
    test_shop.sort('product_price')
    test_shop.rev_sort('product_price')
    test_shop.delete()
