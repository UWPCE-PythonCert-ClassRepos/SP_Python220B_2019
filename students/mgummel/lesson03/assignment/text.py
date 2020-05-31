delete_customer('12345')
delete_customer('123456')
delete_customer('1234s1234564564332486736')

add_customer('12345', 'Max2', 'Tucker2', '40312 22nd ave SW', '2062-519-2405', 'mgummel225@gmail.com', True, 45600)
add_customer('123456', 'Max', 'Tucker', '4031 22nd ave SW', '206-519-2405', 'mgummel225@gmail.com', False, 45600)
add_customer('1234s1234564564332486736', 'Max', 'Tucker', '4031324 22nd ave SW', '206-519-2405', 'mgummel225@gmail.com',
             True, 45600)

print(list_active_customers())
update_customer_credit('1234s1234564564332486736', 24500)