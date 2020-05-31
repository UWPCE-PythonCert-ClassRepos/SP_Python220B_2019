from customer_model import *
import logging
from assignment import create_db

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
create_db.main()


def add_customer(customer_id, name, lastname, home_address, phone_number, email_address, active, credit_limit):
    try:
        with database.transaction():
            contact_id = Identity.create(
                customer_id=customer_id,
                name=name,
                last_name=lastname,
                credit_limit = credit_limit,
                active=active
            )
            contact_id.save()
        LOGGER.info(f"Succesfully added record to Identity {contact_id.customer_id}: {contact_id.last_name}")

    except Exception as e:
        LOGGER.info(f'Error creating = {customer_id}: {name} {lastname}')
        LOGGER.info(e)


    try:
        with database.transaction():
            contact_info = Contact.create(
                home_address=home_address,
                email_address=email_address,
                phone_number=phone_number,
                customer_id=customer_id
            )
            contact_info.save()

            LOGGER.info(f"Contact updated successfully with {contact_info.customer_id}: {contact_info.home_address}")

    except Exception as e:
        LOGGER.info(f'Error creating = {customer_id}: {home_address}')
        LOGGER.info(e)


def search_customer(customer_id):
    customer_info = dict()
    try:
        with database.transaction():
            customer = Identity \
                .select(Identity, Contact) \
                .join(Contact, JOIN.INNER) \
                .where(Contact.customer_id==customer_id)\
                .get()


        customer_info['name'] = customer.name
        customer_info['lastname'] = customer.last_name
        customer_info['email_address'] = customer.contact.email_address
        customer_info['phone_number'] = customer.contact.phone_number

    except Identity.DoesNotExist:
        LOGGER.warning(f"The customer ID {customer_id} does not exist in the database")

    return customer_info


def delete_customer(customer_id):
    try:
        with database.transaction():
            customer = Identity \
                .select(Identity.customer_id) \
                .where(Identity.customer_id == customer_id) \
                .get()

            customer.delete_instance(recursive=True)
        LOGGER.info(f"Successfully deleted user from database.")

    except Identity.DoesNotExist:
        LOGGER.warning(f"The customer ID {customer_id} does not exist in the database")

def update_customer_credit(customer_id, credit_limit):

    try:
        with database.transaction():
            customer = (Identity
                        .select()
                        .where(Identity.customer_id==customer_id)
                        .get())

            LOGGER.info(f"Updating {customer.name} {customer.last_name} with credit limit {credit_limit}")
            customer.credit_limit = credit_limit
            customer.save()
            LOGGER.info(f"Updated {customer.name} {customer.last_name} credit limit to: {customer.credit_limit}")

    except Identity.DoesNotExist:
        LOGGER.warning(f"The customer ID {customer_id} does not exist in the database")

def list_active_customers():

    try:
        with database.transaction():
            customer = (Identity
                        .select()
                        .where(Identity.active== 1)
                        .count())
            print(customer)

            #LOGGER.info(f"Updating {customer.name} {customer.last_name} with credit limit {credit_limit}")
    except Exception as e:
        print (e)
    #except Identity.DoesNotExist:
    #   a;woeifja;oeiwfj;aoweifj;aowiefj;aoweifja;oweifja;woeifja;woeifja;woeifja;woeifjaw;eofija;woeifja;oweifja;woeifja;woeijfia;oweiifj;woaeifjia;oweifj;aoiwef;aw    LOGGER.warning(f"The customer ID {customer_id} does not exist in the database")


if __name__ == '__main__':
    add_customer('12345', 'Max2', 'Tucker2', '40312 22nd ave SW', '2062-519-2405', 'mgummel225@gmail.com', True, 45600)
    add_customer('123456', 'Max', 'Tucker', '4031 22nd ave SW', '206-519-2405', 'mgummel225@gmail.com', True, 45600)
    add_customer('1234s1234564564332486736', 'Max', 'Tucker', '4031324 22nd ave SW', '206-519-2405', 'mgummel225@gmail.com', True, 45600)
    delete_customer('12345')
    delete_customer('123456')
    delete_customer('1234s1234564564332486736')
    print("this is active:")
    list_active_customers()
    update_customer_credit('1234s1234564564332486736', 24500)

