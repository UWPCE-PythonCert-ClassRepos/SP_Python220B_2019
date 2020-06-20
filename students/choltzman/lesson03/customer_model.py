import peewee as pw

DB = pw.SqliteDatabase('customers.db')


class BaseModel(pw.Model):
    class Meta:
        database = DB


class Customer(BaseModel):
    customer_id = pw.IntegerField(primary_key=True)
    full_name = pw.CharField(max_length=100)
    last_name = pw.CharField(max_length=40)
    home_address = pw.CharField(max_length=200)
    phone_number = pw.CharField(max_length=10)
    email_address = pw.CharField(max_length=50)
    is_active = pw.BooleanField(default=False)
    credit_limit = pw.IntegerField()


def create_tables():
    with DB:
        DB.create_tables([Customer])
