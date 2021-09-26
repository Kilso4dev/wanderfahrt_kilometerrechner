from .window import create_window
from .mosel_km import main
from .rowing_data import RowingData, rowing_data_from_dict


app = create_window()
app.mainloop() 


data = RowingData()
data.add_person('Paul Seydel')

sec1 = data.append_section(3)
data.insert_day(47.23, section_index=sec1)
data.insert_day(23.1)
sec1 = data.append_section(1)


with open('./out.json', 'w') as f:
    import json
    f.write(json.dumps(data.to_dict()))
 
with open('./out.json', 'r') as f:
    import json
    data = rowing_data_from_dict(json.loads(f.read()))
    print('Data: ', data)


#mosel_km.main()
    
