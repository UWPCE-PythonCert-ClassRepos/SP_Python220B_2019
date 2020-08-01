import pyodbc
import json
import collections
import json2table

server = 'MATSQLPROD02\MATAPPS'
db = 'TRN_MGT'

cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; \
                      SERVER=' + server + '; \
                      DATABASE=' + db + '; \
                      Trusted_Connection=yes;')

cursor = cnxn.cursor()
cursor.execute(
"""
SELECT [Type]
      ,[Country]
      ,[City]
      ,[PI Project ID] as [PIID]
      ,[Principal Legal Entity] [Principal_Legal_Etity]
      ,[Vendor Legal Entity] [VendorLegalEntity]
      ,[Fee Paid By] [FeePaidBy]


      ,[Approved]
      ,[SQFT (if range take avg)] [SQFT]
      ,[LOE Type] [LOEType]

      ,[Status]
      ,[Needs PO] [NeedsPO]

  FROM [TRN_MGT].[dbo].[LOEs]
            """)
rows = cursor.fetchall()

warray_list = []
for rorow in rows:
    t = (rorow.Type, rorow.Country, rorow.City, rorow.PIID,
         rorow.Principal_Legal_Etity, rorow.VendorLegalEntity, rorow.FeePaidBy,
         # rorow.GrossAnticipatedMarketFeeUSD, rorow.LessInitialRebat,
         # rorow.NetAnticipated,
         #  ,rorow.rebate %,
         # rorow.Effective, rorow.Completion, rorow.Received, rorow.Submitted,
         # rorow.Approved,
         rorow.SQFT, rorow.LOEType,
         #  ,rorow.LOE Name_(replace LOE w ES for ES, CPA for CPA),
         rorow.Status, rorow.NeedsPO)
          #rorow.Uploaded)
    warray_list.append(t)

# for x in warray_list:
#     print(x)


# j = json.dumps(warray_list)
# rowarrays_file = 'student_rowarrays.js'
# f = open(rowarrays_file, 'w')
# # print >> f, j
#
# with open('student_rowarrays.js', 'w') as fw:
#     json.dump()

with open('app.json', 'w', encoding='utf-8') as f:
    json.dump(warray_list, f, ensure_ascii=False, indent=4)

objects_list = []
for row in rows: #line 35 object from cursor
    d = collections.OrderedDict()
    d['Type'] = row.Type
    d['Country'] = row.Country
    d['City'] = row.City
    d['asPIID'] = row.PIID
    d['Principal_Legal_Etity'] = row.Principal_Legal_Etity
    d['VendorLegalEntity'] = row.VendorLegalEntity
    d['FeePaidBy'] = row.FeePaidBy
    # d['GrossAnticipatedMarketFeeUSD'] = row.GrossAnticipatedMarketFeeUSD
    # d['LessInitialRebat'] = row.LessInitialRebat
    # d['NetAnticipated'] = row.NetAnticipated
    # d['Effective'] = row.Effective
    # d['Completion'] = row.Completion
    # d['Received'] = row.Received
    # d['Submitted'] = row.Submitted
    # d['Approved'] = row.Approved
    d['SQFT'] = row.SQFT
    d['LOEType'] = row.LOEType
    d['Status'] = row.Status
    d['NeedsPO'] = row.NeedsPO
    # d['Uploaded'] = row.Uploaded
    objects_list.append(d)


with open('app2.json', 'w', encoding='utf-8') as f:
    json.dump(objects_list, f, ensure_ascii=False, indent=4)
#
# j = json.dumps(objects_list)
# objects_file = 'student_objects.js'
# f = open(objects_file, 'w')
#

infoFromJson = json.dumps(objects_list)
build_direction = "LEFT_TO_RIGHT"
table_attributes = {"style": "width:100%"}
print(json2table.convert(infoFromJson,
                         build_direction=build_direction,
                         table_attributes=table_attributes))
cnxn.close()
