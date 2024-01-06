import ESC

cLight = 37
cGrey = 92
cDark = 92
cRed = 31
cOrange = 91
cGreen = 32
cYellow = 33
cAqua = 36
cBlue = 34
cPurple = 35

last_level = -1

def process_nested_json(data, indent_level=0):
    
    global last_level

    '''
    # Finish last line...
    if last_level < indent_level:
        print("{")
    elif last_level > indent_level:
        print("}")
    # else:
        # print(",")
    '''
    last_level = indent_level

    if isinstance(data, list):
        for item in data:
            process_nested_json(item, indent_level)
    elif isinstance(data, dict):
        for i, (key, value) in enumerate(data.items()):
            if isinstance(value, (list, dict)):
                print("\t" * indent_level + f"{key}: ")#, end="")
                process_nested_json(value, indent_level + 1)
            else:
                print("\t" * indent_level + f"{key}: {value}")#, end = "")
                # If it's the last object in loop print "}" else print ","
                '''
                if i == len(data) - 1:
                    print("}")
                else:
                    print(",")
                '''

def create_dict_from_nested_json(data):
    result = {}

    def fill_dict(d, current_dict):
        if isinstance(d, list):
            current_dict = []
            for item in d:
                if isinstance(item, (list, dict)):
                    current_dict.append(fill_dict(item, {}))
                else:
                    current_dict.append(item)
            return current_dict
        elif isinstance(d, dict):
            for key, value in d.items():
                if isinstance(value, (list, dict)):
                    current_dict[key] = fill_dict(value, {})
                else:
                    current_dict[key] = value
            return current_dict

    return fill_dict(data, result)


def print_dict(d, indent=0):
    ESC.ResetForeGround()
    if isinstance(d, dict) and d:
        for key, value in d.items():
            ESC.ResetForeGround()            
            print('\t' * indent + str(key))
            if isinstance(value, dict):
                print_dict(value, indent+1)
            else:
                # Check if value is encapsulated in a '[]'
                if isinstance(value, list):
                    ESC.SetForeGround(cOrange)
                else:
                    ESC.SetForeGround(cGreen)
                print('\t' * (indent+1) + str(value))
    else:
        ESC.SetForeGround(cRed)
        print(d)
    ESC.ResetForeGround()



# open json file
import json
import os
# open json file 'comments.json'
with open('debug/comment10_7.json', 'r') as f:
    data = json.load(f)

print("\n\n")

process_nested_json(data)
print("\n\n")
print_dict(data)
print("\n\n")


# Aufruf der Funktion und Ausgabe des erstellten JSON-kompatiblen Dictionary-Objekts
json_dict = create_dict_from_nested_json(data)
print_dict(json_dict)
