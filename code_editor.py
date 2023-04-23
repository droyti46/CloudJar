from tkinter import *
import re

project_path = None
current_script = None
previous_text = ''

normal = '#fff'
def_function = '#4ecab4'
keywords = '#6A5ACD'
comments = '#546270'
string = '#aee237'
function = '#05DBF2'
number = '#FF8800'

repl = [
    ['def \w*', def_function],
    ['(^|\s)(False|None|True|and|as|assert|async|await|break|class|continue|def|del|elif|else|except|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield)($| |:)', keywords],
    ['(^|\(|\s)(abs|aiter|all|any|anext|ascii|bin|bool|breakpoint|bytearray|bytes|callable|chr|classmethod|compile|complex|delattr|dict|dir|divmod|enumerate|eval|exec|filter|float|format|frozenset|getattr|globals|hasattr|hash|help|hex|id|input|int|isinstance|issubclass|iter|len|list|locals|map|max|memoryview|min|next|object|oct|open|ord|pow|print|property|range|repr|reversed|round|set|setattr|slice|sorted|staticmethod|str|sum|super|tuple|type|vars|zip|__import__)', function],
    ['".*?"', string],
    ['\'.*?\'', string],
    ['\d*', number],
    ['#.*?$', comments],
]

def start(root, path):
    global project_path, current_script
    current_script = None
    
    project_path = path
    code_scrollbar = Scrollbar(root) # Скроллбар кода
    code_scrollbar.pack(side='right',fill='y')

    global code
    code = Text(root,bg='#1c1c1c',fg='#fff',font='Consolas 14',
                insertbackground="#42aaff",undo=1,
                yscrollcommand=code_scrollbar.set,
                selectbackground='grey')
    code.pack(fill='both',expand=1)
    code_scrollbar.config(command=code.yview)
    code.bind('<KeyRelease>', changes)

    code.bind('<Control-z>', code_undo)
    code.bind('<Control-x>', code_redo)

    changes()

    

def changes(event=None):
    global previous_text

    if code.get('1.0', END) == previous_text:
        return
    

    double_characters = {'(' : ')', '{' : '}',
                         '[' : ']', '"' : '"', "'" : "'"}
    try:
        if event.char in double_characters:
            code.insert('insert', double_characters[event.char])
            i = list(map(int,code.index(INSERT).split('.')))
            line = i[0]
            column = i[1]
            code.mark_set('insert', '%d.%d' % (line, column-1))
    except:
        pass
    
    if current_script:
        with open(f'{project_path}/scripts/{current_script}','w') as f:
            text = code.get(1.0, 'end') # Считываем код
            # Сохраняем его, при этом уадаляя последнюю строчку
            f.write("\n".join(text.split("\n")[:-1]))

    previous_text = code.get('1.0', END)
    
    for tag in code.tag_names():
        code.tag_remove(tag, '1.0', 'end')

    i = 0
    for pattern, color in repl:
        for start, end in search_re(pattern, code.get('1.0', END)):
            #print(f'{pattern} | {start} | {end}')
            code.tag_add(f'{i}', start, end)
            code.tag_config(f'{i}', foreground=color)

            i += 1


def code_update(select, script):
    global current_script
    if script != current_script:
        current_script = script
    #try:
        code.delete(0.0, 'end')
        with open(f'{project_path}/scripts/{current_script}','r') as f:
                code.insert(0.0, f.read())
        changes()
    #except:
     #   pass


def search_re(pattern, text):
    matches = []
    text = text.splitlines()

    for i, line in enumerate(text):
        for match in re.finditer(pattern, line):
            if match.group():
                matches.append(
                    (f"{i + 1}.{match.start()}", f"{i + 1}.{match.end()}")
                )

    return matches

def code_undo(event):
    try:
        code.edit_undo()
        changes()
    except:
        pass

def code_redo(event):
    try:
        code.edit_redo()
        changes()
    except:
        pass
