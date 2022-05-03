from PIL import Image
import numpy as np
import os
import random
import json
from typing import List, Dict
import time

def combine_props(props):
    """Props' z-index is equal to their position in the props list."""
    final = props[-1]
    for attr in reversed(props):
        final = np.where(attr[:, :, 3:4] == 0, final, attr)
    return final

def sample_props(props_path):
    props = []
    props_names = []
    for path, dirs, files in os.walk(props_path):
        dirs.sort()
        for d2i in dirs:
            for _, _, files in os.walk(props_path + '/' + d2i):
                if(len(files) > 0):
                    filepaths = list(map(lambda x: d2i + '/' + x, files))
                    filename = random.choice(filepaths)
                    fullpath = os.path.join(path, filename)
                    this_file = np.array(Image.open(fullpath))
                    props_names.append(filename)
                    props.append(this_file)
    return props, props_names

generated: List[int] = []
duplicates = 0
num_images = 10
start = time.time()
while len(generated) < num_images:
    props, props_names = sample_props('./properties')
    new_hash = hash(tuple(props_names))
    if new_hash not in generated:
        generated.append(new_hash)
        properties = list(map(lambda x: x.split('/'), props_names))
        attributes = list(map(lambda x: {'trait_type': x[0].split('_')[1],
                                         'value': x[1].split('.')[0]},
                              properties))
        image = combine_props(props)
        image = Image.fromarray(image)
        image_id = str(len(generated))
        with open('./metadata/' + image_id, 'w') as f:
            f.write(json.dumps(attributes))
        print(image_id)
        image.save('./images/' + image_id + '.png')
    else:
        duplicates += 1
print('duplicates: ' + str(duplicates))
print('time: ' + str(time.time() - start))
