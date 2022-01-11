##################################################################################################
## Working with the Files

import glob

def get_text(file):

    with open(file, encoding="utf8") as f:
        lines = f.readlines()
    return lines

txt_files = glob.glob('newsstream/*.txt')

## Put all the files together

with open("data/compile.txt", 'w') as nf:
    for i in txt_files:
        with open(i, encoding='utf8') as f:
            lines = f.readlines()
            nf.writelines(lines)
            nf.write("\n")