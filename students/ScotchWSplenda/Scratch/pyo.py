'''
Video:
https://www.youtube.com/watch?v=eDXX5evRgQw&list=PLzhOLoKfPrGTn8kVN1hMfoktJp0giW60X&index=8
Article:
https://datatofish.com/how-to-connect-python-to-sql-server-using-pyodbc/
'''

import pyodbc


# for d in pyodbc.drivers():
#     print(d)

server = 'MATSQLPROD02\MATAPPS'
db = 'TRN_MGT'

cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; \
                      SERVER=' + server + '; \
                      DATABASE=' + db + '; \
                      Trusted_Connection=yes;')

cursor = cnxn.cursor()
cursor.execute('select * from vPIDATA_All_Open')
for row in cursor:
    print(row)

# close the cursor and connection
cursor.close()
cnxn.close()
