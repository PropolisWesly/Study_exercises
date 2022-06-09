import argparse
import tempfile
import os
import json

def add_value(key_name, value):
    storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')
    if os.path.exists(storage_path) != True:
        f = open(storage_path, 'w')
        f.write(json.dumps({}))
        f.close()

    with open(storage_path, 'r') as f:
        dict = json.loads(f.read())

    if key_name in dict:
        dict[key_name].append(value)
    else:
        dict[key_name] = [value]

    with open(storage_path, 'w') as f:
        f.write(json.dumps(dict))

def search_value(key_name, value):
    storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')
    if os.path.exists(storage_path) != True:
        return print()

    with open(storage_path, 'r') as f:
        dict = json.loads(f.read())

    if key_name in dict:
        return print(', '.join(dict[key_name]))
    else:
        return print()

parser = argparse.ArgumentParser()
parser.add_argument("--key", help="key for dictionary")
parser.add_argument("--val", help="value for dictionary")
args = parser.parse_args()

if args.val == None:
    search_value(args.key, args.val)
else:
    add_value(args.key, args.val)