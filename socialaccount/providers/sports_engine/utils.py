import os
import json
import pprint

SAVE_DIR = os.environ.get('SAVE_DIR', False)
if SAVE_DIR:
    print('Saving data enabled to', SAVE_DIR)

def debug_save_data(data, filename):
    if not SAVE_DIR:
        return
    os.makedirs(SAVE_DIR, exist_ok = True)
    save_dir = os.path.join(SAVE_DIR, filename)
    with open(save_dir, 'a') as fp:
        try:
            json.dump(data, fp, indent = 4)
            print(file = fp)
        except:
            pprint.pprint(data, fp, indent = 4, width = 120)
            print(file = fp)
    print('Saved data into', save_dir)

