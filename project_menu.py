from tkinter import filedialog, messagebox
import tkinter as tk, json, main_engine, os, classes

version = 'alpha v1.0'
user_path = os.path.expanduser('~')

# {name : path, name2 : path2}
projects = {}
projects_search = {}

class EntryWithPlaceholder(tk.Entry):
    def __init__(self,master=None,placeholder=None,width=None,textvariable=None):
        super().__init__(master,width=width,textvariable=textvariable)
        if placeholder is not None:
            self.placeholder = placeholder
            self.placeholder_color = 'grey'
            self.default_fg_color = self['fg']

            self.bind("<FocusIn>", self.focus_in)
            self.bind("<FocusOut>", self.focus_out)

            self.put_placeholder()
    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color
    def focus_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color
    def focus_out(self, *args):
        if not self.get():
            self.put_placeholder()

def start():
    global project_directory
    project_directory = os.getcwd()
    
    global projects
    try:
        with open(user_path + r'\AppData\Roaming\CloudJar\projects.json', 'r') as f:
            projects = json.load(f)
    except FileNotFoundError:
        os.chdir(user_path + r'\AppData\Roaming')
        if not os.path.isdir('CloudJar'):
            os.mkdir('CloudJar')
        open(user_path + r'\AppData\Roaming\CloudJar\projects.json', 'w')
        os.chdir(project_directory)
        
        
    # Создание окна меню проектов
    global root
    root = tk.Tk()
    root.resizable(width=False, height=False)
    root.title('Cloud Jar - библиотека проектов')
    root.iconbitmap('pictures/icon.ico')
    root.geometry('800x500')
    
    scrollbar = tk.Scrollbar(root) # Скроллбар проектов
    scrollbar.pack(side='right',fill='y')

    version_text = tk.Label(root,text=version,fg='grey',bg='#1c1c1c')
    version_text.pack()
    
    sv = tk.StringVar()
    search_project = EntryWithPlaceholder(root,'Поиск проектов',300,textvariable=sv)
    sv.trace("w", lambda name, index, mode, sv=sv: search_projects(sv,search_project))
    search_project.pack()

    global projects_listbox
    projects_listbox = tk.Listbox(root,bg='#4b4d4b',fg='white',yscrollcommand=scrollbar.set,
                                  width=50,selectbackground='#b8b8b8',font='Arial 12', bd=0)

    for project in projects.keys():
        projects_listbox.insert('end', project+' ('+projects[project]+')')
    projects_listbox.pack(side='left',fill='both')

    scrollbar.config(command=projects_listbox.yview)

    open_button = classes.classic_button(root,'Редактировать',open_project)
    open_button.pack(fill='x')

    delete_button = classes.classic_button(root,'Удалить проект',delete)
    delete_button.pack(fill='x')

    add_button = classes.classic_button(root,'Создать проект',new_project)
    add_button.pack(fill='x')
    
    root.configure(bg='#1c1c1c')
    root.mainloop()

    

def delete(): # Удаление проекта
    select = projects_listbox.curselection()
    if messagebox.askokcancel('Вы уверены?', f'Вы точно хотите удалить проект {select[0]}?'):
        try:
            projects_listbox.delete(select[0])
            projects.pop(list(projects)[select[0]])
            with open(user_path + r'\AppData\Roaming\CloudJar\projects.json', 'w') as f:
                json.dump(projects, f)
        except:
            pass

def new_project():
    global new
    new = tk.Toplevel(root)
    new.grab_set()
    new.focus()
    new.resizable(width=False, height=False)
    new.title('Создать новый проект')
    new.geometry('300x200+300+250')
    new.iconbitmap('pictures/icon.ico')

    global name
    name = tk.Entry(new, width=40)
    name.insert(0, 'Новый проект')
    name.pack()

    global path
    path = tk.Label(new,text='Путь не выбран',bg='#1c1c1c',
                    fg='#fff')
    path.pack()

    global path_button
    path_button = classes.classic_button(new,'Выбрать путь',command=choose_path)
    path_button.pack()


    create_button = classes.classic_button(new,'Создать',create_new_project)
    create_button.pack(fill='x',side='bottom')

    new.transient(root)
    new.configure(bg='#1c1c1c')
    new.mainloop()

def choose_path():
    global folder_selected
    folder_selected = filedialog.askdirectory()
    path.config(text=folder_selected)

def create_new_project():
    try:
        global folder_selected
        if name.get() != '' and folder_selected:
            projects_listbox.insert('end',f'{name.get()} ({folder_selected})')
            projects[name.get()] = folder_selected
            
            # Меняем текущую директорию на директориюию проекта
            os.chdir(folder_selected)
            # Создаём нужные папки и скрипт main
            os.mkdir('sprites')
            os.mkdir('scripts')
            project_objects = open('project_objects.json', 'w')
            scene_objects = open('scene_objects.json', 'w')
            open(f'main.py', 'w')
            
            new.destroy()

            # Меняем директори обратно
            os.chdir(project_directory)
            with open(user_path + r'\AppData\Roaming\CloudJar\projects.json', 'w') as f:
                json.dump(projects, f)
    except:
        pass

def search_projects(sv, search_project):
    projects_search.clear()
    projects_listbox.delete(0,'end')
        
    if search_project.get() != 'Поиск проектов':
        for i,p in enumerate(projects.keys()):
            if search_project.get().lower()in p.lower() and p not in projects_search:
                projects_search[p] = projects[p]
        for p in projects_search:
            projects_listbox.insert('end', p+' ('+projects_search[p]+')')
    else:
        projects_listbox.delete(0,'end')
        for project in projects.keys():
            projects_listbox.insert('end', project+' ('+projects[project]+')')
            
    
def open_project():
    try:
        select = projects_listbox.curselection()
        name = list(projects)[select[0]]
        path = projects[name]

        root.destroy()

        main_engine.start(name, path)
    except:
        pass

if __name__ == '__main__':
    start()
