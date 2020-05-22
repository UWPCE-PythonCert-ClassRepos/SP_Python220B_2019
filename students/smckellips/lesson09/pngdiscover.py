'''HP Norton PNG Discovery Module'''
import os
from pprint import pprint as pp

PNGS = {}

def discover_png(path):
    '''Recursive function to discover all png.'''
    # Recurse for any directories in path.
    with os.scandir(path) as contents:
        for content in contents:
            if content.is_dir():
                # print(content.path)
                discover_png(content.path)
            elif content.name.endswith('.png'):
                branch = content.path.rsplit('/', 1)[0]
                png = PNGS.get(branch, [])
                png.append(content.name)
                PNGS[branch] = png

def main(path):
    '''main function to get output and translate dict to requested list.'''
    discover_png(path)
    output_list = []
    for key in PNGS:
        output_list.append((key, PNGS[key]))
    return output_list


if __name__ == "__main__":
    RESULTS = main('./data')
    pp(RESULTS)
