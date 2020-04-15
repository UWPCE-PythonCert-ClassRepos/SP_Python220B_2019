'''
png discover tool
'''
import os

def search_png(directory):
    ''' searches directory for files ending .png or calls function again '''
    items_in_directory = os.listdir(directory)
    pngs_found = [f'{directory}']

    for item in items_in_directory:
        if '.png' in item:
            pngs_found.append(f'{item}')
        if os.path.isdir(f'{directory}/{item}'):
            pngs_found.append(search_png(f'{directory}/{item}'))

    return pngs_found

if __name__ == "__main__":
    cwd = os.getcwd()
    pngs = search_png(f'{cwd}/images')
    print(pngs)
