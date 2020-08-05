import json2table
import json

# infoFromJson = json.loads('app2.json')
with open("app2.json", "w") as write_file:
    json.dump(data, write_file)
build_direction = "LEFT_TO_RIGHT"
table_attributes = {"style": "width:100%"}
print(json2table.convert(data,
                         build_direction=build_direction,
                         table_attributes=table_attributes))
