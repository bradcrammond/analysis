import glob

txt_files = glob.glob('newsstream/*.txt')

for i in txt_files:
    with open(i, encoding='utf8') as f:
        lines = f.readlines()
        strings = ''.join(lines)
        title = re.findall("Title:(.*)", strings)
        date = re.findall("Publication date:(.*)", strings)
        x = len(date)
        y = len(title)
        if x != y:
            print('Shit! It is file', i)

