"""Basic CRUD operations for a SQL based backend."""

import logging
import peewee as pw

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

DATABASE = pw.SqliteDatabase(None)


class BaseModel(pw.Model): # pylint: disable=too-few-public-methods
    """Peewee module convention is to inherit from a base model like this."""
    class Meta: # pylint: disable=too-few-public-methods
        """Required Meta class for Peewee model."""
        database = DATABASE


class Customer(BaseModel):
    """The customer class in RDBMS format."""
    customer_id = pw.IntegerField(primary_key=True)
    first_name = pw.CharField(max_length=30, null=True)
    last_name = pw.CharField(max_length=30, null=True)
    address = pw.CharField(max_length=100, null=True)
    phone = pw.IntegerField(null=True)
    email = pw.CharField(max_length=50, null=True)
    is_active = pw.BooleanField(null=True)
    credit_limit = pw.DecimalField(max_digits=11, decimal_places=2, null=True)


def add_customer(*, customer_id, name=None, lastname=None, home_address=None,
                 phone_number=None, email_address=None, status=None,
                 credit_limit=None):
    """Add a customer to the database."""
    with DATABASE.transaction():
        try:
            new_customer = Customer.create(
                customer_id=customer_id,
                first_name=name,
                last_name=lastname,
                address=home_address,
                phone=phone_number,
                email=email_address,
                is_active=status,
                credit_limit=credit_limit
            )
            new_customer.save()
            LOGGER.info('Database add successful: (%s, %s)', lastname, name)
            return new_customer
        except pw.IntegrityError:
            LOGGER.warning('Database add error: (%s, %s)', lastname, name)


def add_all_customers(customers):
    """Return a list containing all the added customers."""
    return [add_customer(**customer) for customer in customers]


def search_customer(customer_id):
    """Try to retrieve a customer from the database by ID."""
    try:
        return Customer.get(Customer.customer_id == customer_id)
    except pw.DoesNotExist:
        LOGGER.warning('Could not find customer with id %s', customer_id)


def search_all_customers(customer_ids):
    """Retrieve all customers from the database that correspond to the supplied
    customer IDs. Generator will supply None for any customer not found."""
    return (search_customer(cid) for cid in customer_ids)


def delete_customer(customer_id):
    """Try to delete a customer from the database by ID."""
    found = search_customer(customer_id)
    if found is None:
        LOGGER.warning('Could not find customer for delete with id %d.',
                       customer_id)
    else:
        found.delete_instance()


def update_customer_credit(customer_id, credit_limit):
    """Try to find customer in database by ID and update credit limit."""
    customer = search_customer(customer_id)
    if customer is None:
        raise ValueError(f'Could not find customer for update with id '
                         f'{customer_id}.')
    customer.credit_limit = credit_limit
    customer.save()


def list_active_customers():
    """Return count of customers in database that are active customers."""
    return Customer.select().where(Customer.is_active).count()


def setup_logging():
    """Directs logging to both console and file."""
    formatter = logging.Formatter(LOG_FORMAT)
    level = logging.INFO

    file_handler = logging.FileHandler('db.log')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)

    logger = logging.getLogger()
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.setLevel(level)


if __name__ == "__main__":
    setup_logging()
    DATABASE.init('customers.db')
    DATABASE.create_tables([Customer])
