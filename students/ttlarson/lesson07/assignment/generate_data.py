import random, csv
import pandas as pd

END = 10000

if __name__ == '__main__':
    df_customer = pd.DataFrame(columns=['user_id', 'name', 'address', 'phone_number', 'email'])
    df_product = pd.DataFrame(columns=['product_id', 'description', 'product_type', 'quantity_available'])
    df_rental = pd.DataFrame(columns=['rental_id', 'product_id', 'user_id', 'dt_start', 'dt_end', 'quantity'])

    list_random = random.sample(range(0, END), END)
    i = 0
    for num in list_random:
        num_0f_0 = (len(str(END))-len(str(num)))
        user_id = 'U{}{}'.format(num_0f_0*'0', num)
        product_id = 'P{}{}'.format(num_0f_0*'0', num)
        rental_id = 'R{}{}'.format(num_0f_0*'0', num)
        print('{}: {}, {}, {}'.format(i, user_id, product_id, rental_id))

        df_customer.loc[i] = [user_id, 'firstname, lastname', '1 Nowhere Dr, Middleland, NO', '999-999-9999', 'me@here.com']
        df_product.loc[i] = [product_id, 'Some Product', 'Some Product Type', num]
        df_rental.loc[i] = [rental_id, product_id, user_id, '0000-00-00', '9999-99-99', num]

        i = i + 1

    df_customer.to_csv('customers.csv', index=False, quoting=csv.QUOTE_NONNUMERIC)
    df_product.to_csv('products.csv', index=False, quoting=csv.QUOTE_NONNUMERIC)
    df_rental.to_csv('rentals.csv', index=False, quoting=csv.QUOTE_NONNUMERIC)