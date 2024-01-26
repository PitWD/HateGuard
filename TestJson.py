import sys
import json
sys.path.append('..')
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

def print_dict(d, indent=0, color = cGreen):
    ESC.ResetForeGround()
    if isinstance(d, dict) and d:
        for key, value in d.items():
            ESC.ResetForeGround()            
            print('\t' * indent + str(key))
            if isinstance(value, dict):
                print_dict(value, indent+1, color)
            else:
                # Check if value is encapsulated in a '[]'
                if isinstance(value, list):
                    #ESC.SetForeGround(cOrange)
                    for val in value:
                        print_dict(val, indent+1, cAqua)
                else:
                    ESC.SetForeGround(color)
                    print('\t' * (indent+1) + str(value))
    else:
        ESC.SetForeGround(cRed)
        print(d)
    ESC.ResetForeGround()


# open json file 'comments.json'
with open('LinkedIn/debug/post_1.json', 'r') as f:
    data = json.load(f)

print("\n\n")
print_dict(data)
print("\n\n")


