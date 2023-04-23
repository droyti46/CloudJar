from tkinter import messagebox, filedialog, ttk
import tkinter as tk, random, os, shutil, json, re
import project_menu, classes, code_editor, features

textures = {}
pos_ratio = 1
current_script = None

def start(name, path):
    global root, project_path, project_objects_list, scene_objects_list
    project_path = path
    current_script = None

    global main_directory
    main_directory = os.getcwd()

    try:
        with open(f'{path}/project_objects.json', 'r') as f:
            project_objects_list = json.load(f)
    except:
        project_objects_list = {}
        
    try:
        with open(f'{path}/scene_objects.json', 'r') as f:
            scene_objects_list = json.load(f)
    except:
        scene_objects_list = {}

    try:
        shutil.copy(f'{main_directory}\\engine.py', f'{path}')
    except: pass
    
    try:
        shutil.copy(f'{main_directory}\\features_classes.py', f'{path}')
    except: pass

    
    root = tk.Tk()
    root.state('zoomed')
    root.title(name+' - Cloud Jar')
    root.iconbitmap('pictures/icon.ico')
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.geometry("%dx%d" % (width, height))
    root.minsize(800,600)

    global delete_icon, configure_icon
    delete_icon = tk.PhotoImage(file = 'pictures/delete.png')
    delete_icon = delete_icon.subsample(4, 4)

    configure_icon = tk.PhotoImage(file = 'pictures/configure.png')
    configure_icon = configure_icon.subsample(4, 4)

    main_menu = tk.Menu(bd=0,background='blue',relief='flat')

    panels()
    project_objects_update()

    project_menu = tk.Menu(bg='#1c1c1c',fg='#fff',activebackground='#42aaff',tearoff=0,
                           relief='flat')
    project_menu.add_command(label='Настройки проекта')
    project_menu.add_command(label='Экспортировать проект')
    project_menu.add_command(label='Выйти в меню проектов')

    scenes_menu = tk.Menu(bg='#1c1c1c',fg='#fff',activebackground='#42aaff',tearoff=0)
    scenes_menu.add_command(label='Добавить сцену',command=new_scene)
    
    main_menu.add_cascade(label='Проект',menu=project_menu)
    main_menu.add_cascade(label='Сцены',menu=scenes_menu)
    main_menu.add_cascade(label='Редактор')
    main_menu.add_cascade(label='Справка')

    root.bind('<F5>', run_project)
    
    root.config(bg='#4b4d4b', menu=main_menu)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

    
def on_closing():
    questions = ['Вы точно хотите выйти?']
    if messagebox.askokcancel('Вы уверены?', random.choice(questions)):
        try:
            save_objects()
        except:
            pass
        root.destroy()
        project_menu.start()

def panels(): # (Объекты проекта, объекты сцены, каталог проекта)
    global sprites_icon, scripts_icon, run_icon
    sprites_icon = tk.PhotoImage(file = 'pictures/sprites.png')
    scripts_icon = tk.PhotoImage(file = 'pictures/scripts.png')
    run_icon = tk.PhotoImage(file = 'pictures/run.png').subsample(5, 5)

    # Панель сверху
    top_menu = tk.Frame(bg='#373434')

    tk.Label(top_menu,text='Текущая сцена:',bg='#373434',
             fg='#fff').grid(column=0, row=0)

    global current_scene
    current_scene = ttk.Combobox(top_menu,
                                 values=list(scene_objects_list.keys()))
    current_scene.grid(column=1, row=0)
    current_scene.bind('<<ComboboxSelected>>', scene_objects_update)

    classes.classic_button(top_menu,'Удалить эту сцену',delete_scene).grid(column=2, row=0)

##    run_project_button = tk.Button(top_menu,image=run_icon,
##                           bg='#373434',relief='flat',
##                           cursor='hand2',bd=0,command=run_project,
##                           text='Запустить проект',compound='left',
##                           fg='#fff')
##    run_project_button.grid(column=3, row=0)

    run_scene_button = tk.Button(top_menu,image=run_icon,
                           bg='#373434',relief='flat',
                           cursor='hand2',bd=0,command=run_project,
                           text='Запустить сцену',compound='left',
                           fg='#fff')
    run_scene_button.grid(column=3, row=0)
    
    top_menu.pack(fill='x',side='top')

    
    
    # Объекты проекта
    project_objects_frame = tk.Frame(root,bg='#4b4d4b')
    project_objects_frame.pack(fill='y',side='left')

    tk.Label(project_objects_frame,text='Объекты проекта:',
             bg='#4b4d4b',fg='#fff',width=40).pack()

    create_project_objects_button = classes.classic_button(project_objects_frame,'Новый объект',
                                                           new_object)
    create_project_objects_button.pack(fill='x')
    
    global project_objects
    project_objects = classes.scroll_frame(project_objects_frame,bg="#4b4d4b")

    project_objects.pack(fill='both',expand=1)



    # Объекты сцены
    scene_objects_frame = tk.Frame(root,bg='#4b4d4b')
    scene_objects_frame.pack(fill='y',side='right')

    tk.Label(scene_objects_frame,text='Объекты сцены:',
             bg='#4b4d4b',fg='#fff',width=40).pack()

    create_scene_objects_button = classes.classic_button(scene_objects_frame,'Добавить объект',
                                                         new_scene_object)
    create_scene_objects_button.pack(fill='x')
    
    global scene_objects
    scene_objects = classes.scroll_frame(scene_objects_frame,bg="#4b4d4b")
    scene_objects.pack(fill='both',expand=1)



    # Каталог
    catalog = tk.Frame(root,bg="#373434",height=240,bd=20)

    sprites_button = tk.Button(catalog,image=sprites_icon,bg='#373434',bd=0,
                               fg='#fff',text='Спрайты',compound='top',cursor='hand2',
                               command=open_sprites)
    sprites_button.grid(column=0, row=0)

    scripts_button = tk.Button(catalog,image=scripts_icon,bg='#373434',bd=0,
                               fg='#fff',text='Скрипты',compound='top',cursor='hand2',
                               command=open_scripts)
    scripts_button.grid(column=1, row=0)
    
    catalog.pack(fill='x',side='bottom')



    # Экран с игрой и скриптами
    screen = ttk.Notebook(root)

    global tab_game
    tab_game = tk.Frame(screen,bg='#1c1c1c')
    tab2 = tk.Frame(screen,bg='#1c1c1c')

    tab_game.bind("<MouseWheel>", zoom_scene)

    screen.add(tab_game, text ='Игра')
    screen.add(tab2, text ='Скрипты')
    screen.pack(expand = 1, fill ="both")

    # Игра
    global game_scene
    game_scene = tk.Frame(tab_game,width=400,height=300,
                         bg='#A5A5A5')
    game_scene.pack_propagate(0)
    game_scene.pack()
    
    game_scene.bind("<Button-3>", on_drag_start)
    game_scene.bind("<B3-Motion>", on_drag_motion)
    game_scene.bind("<Motion>", show_cursor_coordinates)
    game_scene.bind("<MouseWheel>", zoom_scene)

    global cursor_coordinates
    cursor_coordinates = tk.Label(tab_game, text='0;0',
                                  bg='#1c1c1c',fg='#fff',
                                  font='Arial 15')
    cursor_coordinates.place(relx=.9, rely=.9)

    # Скрипты
    global scripts_list
    scripts_list = tk.Listbox(tab2,bg='#373434',bd=0,fg='#fff',
                              font='Arial 12',relief='flat',
                              activestyle='none',selectforeground='#42aaff',
                              selectbackground='#373434')
    scripts_list.pack(side='left',fill='y')
    scripts_list.pack_propagate(0)
    scripts_list.bind('<<ListboxSelect>>', code_update)

    y_scripts_scrollbar = tk.Scrollbar(scripts_list) # Скроллбар скриптов y
    y_scripts_scrollbar.pack(side='right',fill='y')
    x_scripts_scrollbar = tk.Scrollbar(scripts_list,
                                       orient='horizontal') # Скроллбар скриптов x
    x_scripts_scrollbar.pack(side='bottom',fill='x')

    scripts_list.config(yscrollcommand=y_scripts_scrollbar.set,
                        xscrollcommand=x_scripts_scrollbar.set)

    y_scripts_scrollbar.config(command=scripts_list.yview)
    x_scripts_scrollbar.config(command=scripts_list.xview)


    code_editor.start(root=tab2, path=project_path)

    screen.pack(fill='both',expand=1)
    

def code_update(event):
    col = '#42aaff'
    try:
        select = scripts_list.curselection()[0]
        for item in range(scripts_list.size()):
            scripts_list.itemconfig(item, {'fg':'#fff'})
            
        scripts_list.itemconfig(select, {'fg':col})
        current_script = scripts_list.get(0,'end')[select]

        code_editor.code_update(select, current_script)
    except:
        pass
    

def show_cursor_coordinates(event):
    cursor_coordinates.config(text=
                              f'{event.x};{event.y}')

def new_object():
    global new
    new = tk.Toplevel(root)
    new.resizable(width=False, height=False)
    new.title('Создать новый объект')
    #new.geometry('300x100+300+250')
    center_window(new, 300, 100)
    new.iconbitmap('pictures/icon.ico')

    global object_name
    object_name = tk.Entry(new, width=40)
    object_name.insert(0, 'Новый объект')
    object_name.focus()
    object_name.pack()

    create_button = classes.classic_button(new,'Создать',create_new_object)
    create_button.pack(fill='x',side='bottom')

    new.transient(root)
    new.configure(bg='#1c1c1c')
    new.mainloop()

def new_scene_object():
    global new_sobj
    new_sobj = tk.Toplevel(root)
    new_sobj.focus()
    new_sobj.resizable(width=False, height=False)
    new_sobj.title('Добавить в сцену новый объект')
    center_window(new_sobj, 300, 100)
    #new_sobj.geometry('300x100+800+250')
    new_sobj.iconbitmap('pictures/icon.ico')

    global scene_obj_choose
    scene_obj_choose = ttk.Combobox(new_sobj, 
                            values=list(project_objects_list.keys()))
    scene_obj_choose.pack()
    
    add_button = classes.classic_button(new_sobj,'Добавить',
                                        create_new__scene_object)
    add_button.pack(fill='x',side='bottom')

    new_sobj.transient(root)
    new_sobj.configure(bg='#1c1c1c')
    new_sobj.mainloop()

def new_scene():
    global new_s
    new_s = tk.Toplevel(root)
    new_s.resizable(width=False, height=False)
    new_s.title('Создать новую сцену')
    center_window(new_s, 300, 100)
    #new_s.geometry('300x100+300+250')
    new_s.iconbitmap('pictures/icon.ico')

    global scene_name
    scene_name = tk.Entry(new_s, width=40)
    scene_name.insert(0, 'Новая сцена')
    scene_name.focus()
    scene_name.pack()

    create_button = classes.classic_button(new_s,'Создать',create_new_scene)
    create_button.pack(fill='x', side='bottom')

    new_s.transient(root)
    new_s.configure(bg='#1c1c1c')
    new_s.mainloop()

def create_new_object():
    global project_path
    name = object_name.get()
    new.destroy()
    if name != '' and name not in project_objects_list:
        project_objects_list[name] = {
            'sprite' : None,
            'script' : None,
            'features' : {},
            }
        os.chdir(f'{project_path}')
        open(f'{name}.py', 'w')
        os.chdir(main_directory)
        
        save_objects()

def create_new__scene_object():
    global project_path
    name = scene_obj_choose.get()
    scene = current_scene.get()
    new_sobj.destroy()
    try:
        if name != '':
            if '(' in name:
                obj_original = name[:obj.find('(')-1]
            else:
                obj_original = name
            keys = []
            for key in scene_objects_list[scene].keys():
                if '(' in key:
                    keys.append(key[:key.find('(')-1])
                else:
                    keys.append(key)
            count = keys.count(obj_original)
            if count != 0:
                name = f'{name} ({count})'
            scene_objects_list[scene][name] = {
                'original' : obj_original,
                'count' : count,
                'pos_x' : 0,
                'pos_y' : 0,
                'scale_x' : 1,
                'scale_y' : 1,
                'angle' : 0,
                }
            save_objects()
            scene_objects_update()
    except:
        pass


def create_new_scene():
    global project_path
    name = scene_name.get()
    new_s.destroy()
    if name != '' and name not in list(scene_objects_list.keys()):
        scene_objects_list[name] = {}

        os.chdir(f'{project_path}')
        open(f'{name}.py', 'w')
        os.chdir(main_directory)
        
        save_objects()
        scenes_update()
    

def project_objects_update():
    for obj in project_objects.interior.winfo_children():
        a = '.!scroll_frame.!canvas.!frame.!label'
        b = '.!scroll_frame.!canvas.!frame.!button'
        if str(obj) != a and str(obj) != b:
            obj.destroy()
        
    for name, obj in project_objects_list.items():
        obj_label = tk.Frame(project_objects.interior,bg='#373434')
        obj_label.bind("<Button-1>", on_drag_obj_label_start)
        obj_label.bind("<B1-Motion>", on_drag_obj_label_motion)
        obj_label.bind("<ButtonRelease>", on_drag_obj_label_finish)
        
        obj_label.bind('<Enter>', obj_label_focus)
        obj_label.bind('<Leave>', obj_label_focus_out)
        
        obj_name = tk.Label(obj_label,text=name,bg='#373434',fg='#fff')
        obj_name.grid(column=1,row=0,rowspan=2)

        configure_button = tk.Button(obj_label,image=configure_icon,bg='#373434',
                                  bd=0,cursor='hand2',text=name)
        configure_button.grid(column=0,row=0)
        configure_button.bind('<Button-1>', configure_object)

        delete_button = tk.Button(obj_label,text=name,image=delete_icon,bg='#373434',
                                  bd=0,cursor='hand2')
        delete_button.bind('<Button-1>', delete_object)
        delete_button.grid(column=0,row=1)

        obj_label.pack(fill='x')
        
def scene_objects_update(event=0):
    screen_update()
    scripts_update()
    for obj in scene_objects.interior.winfo_children():
        a = '.!scroll_frame2.!canvas.!frame.!label'
        b = '.!scroll_frame2.!canvas.!frame.!button'
        if str(obj) != a and str(obj) != b:
            obj.destroy()
        
    for name, obj in scene_objects_list[current_scene.get()].items():
        obj_label = tk.Frame(scene_objects.interior,bg='#373434')
        obj_label.bind("<Button-1>", on_drag_obj_label_start)
        obj_label.bind("<B1-Motion>", on_drag_obj_label_motion)
        obj_label.bind("<ButtonRelease>", on_drag_scene_obj_label_finish)
        
        obj_label.bind('<Enter>', obj_label_focus)
        obj_label.bind('<Leave>', obj_label_focus_out)
        
        obj_name = tk.Label(obj_label,text=name,bg='#373434',fg='#fff')
        obj_name.grid(column=1,row=0,rowspan=2)

        configure_button = tk.Button(obj_label,image=configure_icon,bg='#373434',
                                  bd=0,cursor='hand2',text=name)
        configure_button.grid(column=0,row=0)
        configure_button.bind('<Button-1>', configure_scene_object)

        delete_button = tk.Button(obj_label,text=name,image=delete_icon,bg='#373434',
                                  bd=0,cursor='hand2')
        delete_button.bind('<Button-1>', delete_scene_object)
        delete_button.grid(column=0,row=1)

        obj_label.pack(fill='x')


def open_sprites():
    sprites = tk.Toplevel(root)
    sprites.title('Спрайты')
    #sprites.geometry('900x600+100+100')
    center_window(sprites, 900, 600)
    sprites.iconbitmap('pictures/icon.ico')
    sprites.focus_set()

    up_frame = tk.Frame(sprites,bg='#373434',bd=10)
    up_frame.pack(fill='x')

    add_sprite_button = classes.classic_button(up_frame,text='Добавить спрайт',command=add_sprite)
    add_sprite_button.pack(fill='x',expand=1)

    delete_sprite_button = classes.classic_button(up_frame,'Удалить спрайт',delete_sprite)
    delete_sprite_button.pack(fill='x',expand=1)

    sprites_list = tk.Frame(sprites,bg="#4b4d4b")
    sprites_list.pack(fill='both',expand=1)

    scrollbar = tk.Scrollbar(sprites_list) # Скроллбар спрайтов
    scrollbar.pack(side='right',fill='y')

    global sprites_listbox
    sprites_listbox = tk.Listbox(sprites_list,bg='#4b4d4b',fg='white',yscrollcommand=scrollbar.set,
                                  width=50,selectbackground='#b8b8b8',font='Arial 12', bd=10,
                                 relief='flat')
    sprites_listbox.pack(side='left',fill='both',expand=1)
    scrollbar.config(command=sprites_listbox.yview)

    update_sprites()
    sprites.transient(root)
    sprites.mainloop()

def open_scripts():
    global scripts
    scripts = tk.Toplevel(root)
    scripts.title('Скрипты')
    #scripts.geometry('900x600+100+100')
    center_window(scripts, 900, 600)
    scripts.iconbitmap('pictures/icon.ico')
    scripts.focus_set()

    up_frame = tk.Frame(scripts,bg='#373434',bd=10)
    up_frame.pack(fill='x')

    add_script_button = classes.classic_button(up_frame,'Добавить скрипт',add_script)
    add_script_button.pack(fill='x',expand=1)

    delete_script_button = classes.classic_button(up_frame,'Удалить скрипт',delete_script)
    delete_script_button.pack(fill='x',expand=1)

    scripts_list = tk.Frame(scripts,bg="#4b4d4b")
    scripts_list.pack(fill='both',expand=1)

    scrollbar = tk.Scrollbar(scripts_list) # Скроллбар спрайтов
    scrollbar.pack(side='right',fill='y')

    global scripts_listbox
    scripts_listbox = tk.Listbox(scripts_list,bg='#4b4d4b',fg='white',yscrollcommand=scrollbar.set,
                                  width=50,selectbackground='#b8b8b8',font='Arial 12', bd=10,
                                 relief='flat')
    scripts_listbox.pack(side='left',fill='both',expand=1)
    scrollbar.config(command=scripts_listbox.yview)

    update_scripts()
    scripts.transient(root)
    scripts.mainloop()


def add_sprite():
    sprite_path = filedialog.askopenfilename()
    try:
        shutil.copy(sprite_path, f'{project_path}/sprites')
        update_sprites()
    except:
        pass

def add_script():
    global new_script
    new_script = tk.Toplevel(scripts)
    new_script.resizable(width=False, height=False)
    new_script.title('Создать новый скрипт')
    #new_script.geometry('300x100')
    center_window(new_script, 300, 100)
    new_script.iconbitmap('pictures/icon.ico')

    global script_name
    script_name = tk.Entry(new_script, width=40)
    script_name.insert(0, 'Новый скрипт')
    script_name.focus()
    script_name.pack()

    create_button = classes.classic_button(new_script,'Создать',create_script)
    create_button.pack(fill='x', side='bottom')

    new_script.transient(scripts)
    new_script.configure(bg='#1c1c1c')
    new_script.mainloop()

def create_script():
    name = script_name.get()
    new_script.destroy()
    try:
        os.chdir(f'{project_path}/scripts')
        open(f'{name}.py', 'w')
        update_scripts()
        os.chdir(main_directory)
    except:
        pass

def delete_sprite():
    select = sprites_listbox.curselection()
    sprites = os.listdir(f'{project_path}/sprites')
    try:
        sprites_listbox.delete(select[0])
        os.remove(f'{project_path}/sprites/{sprites[select[0]]}')
    except:
        pass

def delete_script():
    select = scripts_listbox.curselection()
    scripts = os.listdir(f'{project_path}/scripts')
    try:
        scripts_listbox.delete(select[0])
        os.remove(f'{project_path}/scripts/{scripts[select[0]]}')
    except:
        pass

def update_sprites():
    sprites_listbox.delete(0,'end')
    #textures = {}
    for sprite in os.listdir(f'{project_path}/sprites'):
        sprites_listbox.insert('end', sprite)
        #textures[sprite] = tk.PhotoImage(file=f'{project_path}/sprites/{sprite}')

def update_scripts():
    scripts_listbox.delete(0,'end')
    for script in os.listdir(f'{project_path}/scripts'):
        scripts_listbox.insert('end', script)
        
def delete_object(event):
    name = event.widget.cget('text')
    if messagebox.askokcancel('Вы уверены?', f'Вы точно хотите удалить объект {name}?'):
        project_objects_list.pop(name)
        
        os.chdir(f'{project_path}')
        os.remove(f'{name}.py')
        os.chdir(main_directory)
        
        save_objects()

def delete_scene_object(event=None):
    global name
    if event:
        name = event.widget.cget('text')
    if messagebox.askokcancel('Вы уверены?', f'Вы точно хотите удалить объект {name}?'):
        scene = current_scene.get()
        name_original = scene_objects_list[scene][name]['original']
        count = scene_objects_list[scene][name]['count']

        scene_objects_list[current_scene.get()].pop(name)

        for obj in list(scene_objects_list[scene].keys()):
            obj_original = scene_objects_list[scene][obj]['original']
            count_cur = scene_objects_list[scene][obj]['count']
                
            if obj_original == name_original and count_cur > count:
                if count_cur != 1:
                    new_key = f'{obj_original} ({count_cur-1})'
                else:
                    new_key = obj_original
                scene_objects_list[scene][obj]['count'] -= 1
                scene_objects_list[scene][new_key]=scene_objects_list[scene].pop(obj)
        
        save_objects()
        scene_objects_update()

def delete_scene():
    name = current_scene.get()
    if messagebox.askokcancel('Вы уверены?', f'Вы точно хотите удалить сцену {name}?'):
        scene_objects_list.pop(name)

        os.chdir(f'{project_path}')
        os.remove(f'{name}.py')
        os.chdir(main_directory)
        
        save_objects()
        scenes_update()

def configure_object(event=None):
    global name
    if event:
        name = event.widget.cget('text')
    else:
        scene = current_scene.get()
        name = scene_objects_list[scene][name]['original']
    global obj_name
    obj_name = name
    global config
    config = tk.Toplevel()
    center_window(config, 800, 600)
    config.iconbitmap('pictures/icon.ico')
    config.focus_set()
    config.title(f'Редактирование {name}')

    tab_control = ttk.Notebook(config)
  
    tab1 = tk.Frame(tab_control,bg='#373434')
    tab2 = tk.Frame(tab_control,bg='#373434')

    classes.classic_button(tab2,'Добавить свойство',new_feature).pack(fill='x')
    global features_frame
    features_frame = classes.scroll_frame(tab2,'#373434')
    features_frame.pack(fill='both',expand=1)
    update_features()

    tab_control.add(tab1, text ='Параметры')
    tab_control.add(tab2, text ='Свойства')
    tab_control.pack(expand = 1, fill ="both")

    tk.Label(tab1,text='Спрайт:',
             bg='#373434',fg='#fff').grid(column=0,row=0)
    tk.Label(tab1,text='Скрипт:',
             bg='#373434',fg='#fff').grid(column=0,row=1)

    global obj_sprite
    obj_sprite = ttk.Combobox(tab1, 
                            values=os.listdir(f'{project_path}/sprites'))
    sprites = os.listdir(f'{project_path}/sprites')

    global obj_script
    obj_script = ttk.Combobox(tab1, 
                            values=os.listdir(f'{project_path}/scripts'))
    scripts = os.listdir(f'{project_path}/scripts')

    try:
        sprite = sprites.index(project_objects_list[name]['sprite'])
        obj_sprite.current(sprite)

        script = scripts.index(project_objects_list[name]['script'])
        obj_script.current(script)
    except:
        pass
    obj_sprite.grid(column=1, row=0)
    obj_script.grid(column=1, row=1)

    classes.classic_button(config,'Сохранить',save_obj).pack(fill='x',side='bottom')

    config.transient(root)
    config.config(bg='#4b4d4b')
    config.mainloop()

def new_feature():
    features_win = tk.Toplevel()
    center_window(features_win, 800, 600)
    features_win.iconbitmap('pictures/icon.ico')
    features_win.focus_set()
    features_win.title(f'Добавить новое свойство')

    features_frame = classes.scroll_frame(features_win,'#373434')
    features_frame.pack(fill='both',expand=1)
    features.show_all(features_frame.interior, features_win)

    features_win.transient(config)
    features_win.mainloop()
    
def add_feature(feature_lst):
    feature_name = feature_lst[0]
    feature_options = feature_lst[1]
    project_objects_list[obj_name]['features'][feature_name] = feature_options
    update_features()

def update_features():
    global features_dict_save, features_dict_delete
    features_dict_save = {}
    features_dict_delete = {}
    bg = '#373434'
    for feature in features_frame.interior.winfo_children():
        feature.destroy()
    global functions_image, methods_image
    functions_image = tk.PhotoImage(file='pictures/functions.png').subsample(4,4)
    methods_image = tk.PhotoImage(file='pictures/methods.png').subsample(5,5)
    for feature in project_objects_list[obj_name]['features']:
        tk.Label(features_frame.interior,text=f'Свойство {feature}',
                 bg=bg,fg='grey').pack()
        tab_feature = ttk.Notebook(features_frame.interior)
        
        parameters = tk.Frame(tab_feature, bg=bg)
        functions = tk.Frame(tab_feature, bg=bg)
        methods = tk.Frame(tab_feature, bg=bg)

        for parameter in project_objects_list[obj_name]['features'][feature]:
            tk.Label(parameters,text=parameter,
                     bg=bg,fg='#fff').pack(side='left')
            value = tk.Entry(parameters,bg='#524d4d',fg='#fff',
                                       font='Arial 15',insertbackground='gray')
            txt = project_objects_list[obj_name]['features'][feature][parameter]
            value.insert(0,str(txt))
            value.pack(fill='x',side='left',expand=1)

            features_dict_save[value] = [feature, parameter]

        i = 0
        for function in features.features_list[feature]['functions']:
            tk.Button(functions,image=functions_image,bg=bg,bd=0).grid(row=i,column=0)
            tk.Label(functions,text=function,
                     bg=bg,fg='#fff').grid(row=i,column=1,sticky='w')
            i+=1
            
        i = 0
        for method in features.features_list[feature]['methods']:
            tk.Button(methods,image=methods_image,bg=bg,bd=0).grid(row=i,column=0)
            tk.Label(methods,text=method,
                     bg=bg,fg='#fff').grid(row=i,column=1,sticky='w')
            i+=1

        tab_feature.add(parameters, text = 'Параметры')
        tab_feature.add(functions, text = 'Функции')
        tab_feature.add(methods, text = 'Методы')

        tab_feature.pack(fill='x')
        delete = classes.classic_button(features_frame.interior,'Удалить',None)
        delete.bind('<Button-1>', delete_feature)
        delete.pack(fill='x')
        features_dict_delete[delete] = feature

def delete_feature(event):
    widget = event.widget
    project_objects_list[obj_name]['features'].pop(features_dict_delete[widget])
    update_features()

def configure_scene_object(event=None):
    global s_name
    global name
    if event:
        name = event.widget.cget('text')

    config_s = tk.Toplevel()
    center_window(config_s, 800, 600)
    config_s.iconbitmap('pictures/icon.ico')
    config_s.focus_set()
    config_s.title(f'Редактирование {name}')

    classes.classic_button(config_s,'Сохранить',save_obj).pack(fill='x',side='bottom')

    config_s.transient(root)
    config_s.config(bg='#4b4d4b')
    config_s.mainloop()

def save_obj():
    project_objects_list[obj_name]['sprite'] = obj_sprite.get()
    project_objects_list[obj_name]['script'] = obj_script.get()
    save_objects()
    try:
        screen_update()
    except:
        pass
    try:
        scripts_update()
    except:
        pass

    for value in features_dict_save:
        feature = features_dict_save[value][0]
        parameter = features_dict_save[value][1]
        project_objects_list[obj_name]['features'][feature][parameter] = int(value.get())

    config.destroy()

def save_objects(event=0):
    project_objects_update()
    with open(f'{project_path}/project_objects.json', 'w') as f:
        json.dump(project_objects_list, f)
        
    with open(f'{project_path}/scene_objects.json', 'w') as f:
        json.dump(scene_objects_list, f)
        
def scenes_update():
    current_scene.config(values=list(scene_objects_list.keys()))

def screen_update():
        global pos_ratio
        scene = current_scene.get()
        
        # Обновление экрана
        game_scene.place(width=400,height=300)
        pos_ratio = 1

        global textures
        textures = {}
        for obj in game_scene.winfo_children():
            obj.destroy()

    #try:
        for obj in scene_objects_list[scene]:
            if '(' in obj:
                obj_original = obj[:obj.find('(')-1]
            else:
                obj_original = obj
            try:
                image = project_objects_list[obj_original]['sprite']
                image = tk.PhotoImage(file=f'{project_path}/sprites/{image}')
                
                obj_on_screen = tk.Button(game_scene,text=obj,
                                          image=image,relief='flat',
                                          bg='#fff',bd=0,cursor='hand2')

                textures[obj_on_screen] = image
            except:
                obj_on_screen = tk.Label(game_scene,text=obj)
            
            x = scene_objects_list[scene][obj]['pos_x']
            y = scene_objects_list[scene][obj]['pos_y']
            obj_on_screen.place(x=x, y=y, anchor='center')

            obj_on_screen.bind("<Button-1>", on_drag_start)
            obj_on_screen.bind("<B1-Motion>", on_drag_motion)
            obj_on_screen.bind('<ButtonRelease-1>', save_objects)

            obj_on_screen.bind('<Enter>', obj_focus)
            obj_on_screen.bind('<Leave>', obj_focus_out)
            
            obj_on_screen.bind("<MouseWheel>", zoom_scene)
            obj_on_screen.bind("<Button-3>", on_drag_game_start)
            obj_on_screen.bind("<B3-Motion>", on_drag_game_motion)

            obj_on_screen.bind("<ButtonRelease-3>", show_menu1)
    #except:
     #    pass

def show_menu1(event):
    global name
    name = event.widget.cget('text')
    menu = tk.Menu(root,tearoff=0,bg='#131313',fg='#fff')
    menu.add_command(label='Удалить',image=delete_icon,
                     compound='left',command=delete_scene_object)
    menu.add_separator()
    menu.add_command(label='Настроить (как объект проекта)',
                     image=configure_icon,compound='left',
                     command=configure_object)
    menu.add_command(label='Настроить (как объект сцены)',
                     image=configure_icon,compound='left',
                     command=configure_scene_object)
    menu.post(event.x_root, event.y_root)

def obj_focus(event):
    obj = event.widget
    obj.config(bg='#1D1E33')
    global obj_descp
    text = f'{obj.cget("text")}\nx:{obj.winfo_x()} y:{obj.winfo_y()}'
    obj_descp = tk.Label(tab_game,text=text,bg='#131313',
                         fg='#fff')
    obj_descp.place(x=obj.winfo_x()+game_scene.winfo_x(),
                    y=obj.winfo_y()+game_scene.winfo_y()-50)
def obj_focus_out(event):
    obj = event.widget
    obj.config(bg='#fff')
    obj_descp.destroy()

def obj_label_focus(event):
    obj = event.widget
    obj.config(bg='#6b6565')
    for widget in obj.winfo_children():
        widget.config(bg='#6b6565')
def obj_label_focus_out(event):
    obj = event.widget
    obj.config(bg='#373434')
    for widget in obj.winfo_children():
        widget.config(bg='#373434')


def scripts_update():
    scripts_list.delete(0, 'end')
    scene = current_scene.get()
    for name in scene_objects_list[scene]:
        try:
            script = project_objects_list[name]['script']
            scripts_list.insert('end', script)
        except:
            pass


def on_drag_start(event):
    widget = event.widget
    if widget in textures:
        image = textures[widget]
        widget._drag_start_x = event.x - abs(image.width()/2)
        widget._drag_start_y = event.y - abs(image.height()/2)
    else:
        widget._drag_start_x = event.x - abs(widget.cget('width')/2)
        widget._drag_start_y = event.y - abs(widget.cget('height')/2)
        
def on_drag_motion(event):
    widget = event.widget
    x = widget.winfo_x() - widget._drag_start_x + event.x
    y = widget.winfo_y() - widget._drag_start_y + event.y
        
    widget.place(x=x, y=y, anchor='center')

    try:
        name = event.widget.cget('text')
        scene = current_scene.get()
        if name in scene_objects_list[scene]:
            scene_objects_list[scene][name]['pos_x'] = x/pos_ratio
            scene_objects_list[scene][name]['pos_y'] = y/pos_ratio
            obj_descp.place(x=widget.winfo_x()+game_scene.winfo_x(),
                    y=widget.winfo_y()+game_scene.winfo_y()-50)
            text = f'{widget.cget("text")}\nx:{widget.winfo_x()} y:{widget.winfo_y()}'
            obj_descp.config(text=text)
    except:
        pass

def on_drag_game_start(event):
    game_scene._drag_start_x = event.x - abs(game_scene.cget('width')/2)
    game_scene._drag_start_y = event.y - abs(game_scene.cget('height')/2)
def on_drag_game_motion(event):
    widget = game_scene
    x = widget.winfo_x() - widget._drag_start_x + event.x
    y = widget.winfo_y() - widget._drag_start_y + event.y
    widget.place(x=x, y=y, anchor='center')
    
def on_drag_obj_label_start(event):
    widget = event.widget
    widget._drag_start_y = event.y
    widget.lift()
def on_drag_obj_label_motion(event):
    widget = event.widget
    x = widget.winfo_x()
    y = widget.winfo_y() - widget._drag_start_y + event.y
    widget.config(bg='#6b6565')
    for child in widget.winfo_children():
        child.config(bg='#6b6565')
    if y > 0:
        widget.place(x=x, y=y, width=400)
def on_drag_obj_label_finish(event):
    global project_objects_list
    widget = event.widget
    var = widget.winfo_height()
    var = widget.winfo_y() // var
    for obj in widget.winfo_children():
        try:
            name = obj.cget('text')
            break
        except:
            pass
    obj = project_objects_list.pop(name)
    project_objects_list = list(project_objects_list.items())
    project_objects_list.insert(var, (name, obj))
    project_objects_list = dict(project_objects_list)
    save_objects()
def on_drag_scene_obj_label_finish(event):
    global scene_objects_list
    widget = event.widget
    var = widget.winfo_height()
    var = widget.winfo_y() // var
    scene = current_scene.get()
    for obj in widget.winfo_children():
        try:
            name = obj.cget('text')
            break
        except:
            pass
    obj = scene_objects_list[scene].pop(name)
    lst = list(scene_objects_list[scene].items())
    lst.insert(var, (name, obj))
    scene_objects_list[scene] = dict(lst)
    save_objects()
    scene_objects_update()


def zoom_scene(event):
    pass
##    global pos_ratio
##    ratio = 1.2
##    widget = game_scene
##    
##    height = widget.winfo_height()
##    width = widget.winfo_width()
##    
##    if event.delta > 0:
##        pos_ratio *= ratio
##        widget.place(height=height*ratio, width=width*ratio, anchor='center')
##        
##        for obj in widget.winfo_children():
##            height = obj.winfo_height() * ratio
##            width = obj.winfo_width() * ratio
##            x = obj.winfo_x() * ratio
##            y = obj.winfo_y() * ratio
##            obj.place(height=height, width=width)
##    else:
##        pos_ratio /= ratio
##        widget.place(height=height/ratio, width=width/ratio, anchor='center')
##
##        for obj in widget.winfo_children():
##            height = obj.winfo_height() / ratio
##            width = obj.winfo_width() / ratio
##            x = obj.winfo_x() / ratio
##            y = obj.winfo_y() / ratio
##            obj.place(height=height, width=width)



def run_project(event=0):
    os.chdir(project_path)
    scene = current_scene.get()

    main = 'import '
    for s in scene_objects_list:
        main += f'{s}, '
    
    main += f'''engine, tkinter as tk

def main():
    root = tk.Tk()
    root.geometry('400x300')
    root.title("Игра на Cloud Jar")

    global game_canvas
    game_canvas = tk.Canvas(root, bg="#a5a5a5", bd=0)
    engine.canvas = game_canvas
    game_canvas.pack(fill="both",expand=1)

    {scene}.start(game_canvas)

    root.mainloop()

if __name__ == "__main__":
    main()'''
    
    with open(f'{project_path}/main.py','w',encoding='utf-8') as f:
        f.write(main)

    for s in scene_objects_list:
        scene_script = 'import '
        for obj in project_objects_list:
            scene_script += f'{obj}, '
        
        scene_script += '''tkinter as tk

def start(game_canvas):\n\tpass\n'''
        process_objs = []
        for obj in scene_objects_list[s]:
            original = scene_objects_list[s][obj]['original']
            x = scene_objects_list[s][obj]['pos_x']
            y = scene_objects_list[s][obj]['pos_y']
            image = project_objects_list[original]['sprite']
            count = scene_objects_list[s][obj]['count']
            name = original + str(count)
            
            scene_script += f'\t{name} = {original}.obj(game_canvas, {x}, {y})\n'
        

        with open(f'{project_path}/{s}.py','w',encoding='utf-8') as f:
            f.write(scene_script)

    for o in project_objects_list:
        object_script = 'import '
        try:
            module = project_objects_list[o]['script'].split('.')[0]
            sprite = project_objects_list[o]['sprite']
        except: pass
        if module != '':
            object_script += f'scripts.{module} as script, '
        object_script += f'''tkinter as tk, features_classes

textures = []
game = None

class obj:
    def __init__(self, canvas, x, y):
        global sprite
        try:
            self.script = script
        except:
            self.script = None
        self.name = "{o}"
        self.canvas = canvas
        sprite = tk.PhotoImage(file=f"sprites/{sprite}")
        textures.append(sprite)
        self.object = canvas.create_image(x, y, image=sprite)
        
'''
        for feature in project_objects_list[o]['features']:
            object_script += f'        self.{feature} = features_classes.{feature}(self, self.canvas, self.script'
            for parameter in project_objects_list[o]['features'][feature]:
                value = project_objects_list[o]['features'][feature][parameter]
                object_script += f', {parameter}={value}'
            object_script += ')\n'

        
        if module != '':
            object_script += f'        script.self = self\n'
            object_script += f'        script.game = self.canvas\n'
        try:
            script = project_objects_list[o]['script']
            with open(f'scripts/{script}','r',encoding='utf-8') as f:
                if 'def ready()' in f.read():
                    object_script += f'        script.ready()\n'
                    
            with open(f'scripts/{script}','r',encoding='utf-8') as f:
                if 'def process()' in f.read():
                    object_script += f'''        self.process()
    def process(self):
        script.self = self
        script.process()
        self.canvas.after(20, self.process)
'''
        except: pass

        object_script += '''    def delete(self):
        self.canvas.delete(self.object)

    def x(self, x = None):
        if x:
            self.canvas.coords(self.object, x, self.y())
        self.pos_x = self.canvas.coords(self.object)[0]
        return self.pos_x
    def y(self, y = None):
        if y:
            self.canvas.coords(self.object, self.x(), y)
        self.pos_y = self.canvas.coords(self.object)[1]
        return self.pos_y
    def sprite(self, sprite):
        sprite = tk.PhotoImage(file=f"sprites/{sprite}")
        textures.append(sprite)
        self.canvas.itemconfigure(self.object, image=sprite)

        '''
        
        with open(f'{project_path}/{o}.py','w',encoding='utf-8') as f:
            f.write(object_script)

        
    
    os.system(f'start cmd /K "{project_path}/main.py"')
    os.chdir(main_directory)
    #os.startfile(f'{project_path}/main.py'))

    
def center_window(win, w, h):
    sw = win.winfo_screenwidth()
    sh = win.winfo_screenheight()
    x = (sw - w) / 2
    y = (sh - h) / 2
    win.geometry('%dx%d+%d+%d' % (w, h, x, y))
    
if __name__ == '__main__':
    start("Проверка", "C:")
