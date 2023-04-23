import tkinter as tk
import classes, main_engine

textures = []
feature_dict = {}

features_list = {
    'mouse_events' : {
            'name' : 'Взаимодействие с мышью',
            'description' : 'Добавляет события, позволяющие взаимодействовать с мышью. Например, клик по объекту или наведение в его область.',
            'options' : {},
            'functions' : ['on_click()','mouse_entered()','mouse_exited()'],
            'methods' : []
        },
    
    'top_down_move' : {
            'name' : 'Управление с видом сверху',
            'description' : 'Добавляет объекту управление вверх, вниз, влево и вправо.',
            'options' : {'speed' : 100},
            'functions' : ['in_motion()','in_idle()','moving_left()','moving_right()',
                           'moving_up()','moving_down()'],
            'methods' : ['.start()', '.stop()']
        }
}

def show_all(frame, root):
    global win
    win = root
    textures.clear()
    feature_dict.clear()
    bg = '#373434'
    for feature in features_list:
        feature_frame = tk.Frame(frame, bg=bg)
        name = features_list[feature]['name']
        desc = features_list[feature]['description']
        options = features_list[feature]['options']
        feature_frame.pack(fill='x')

        image = tk.PhotoImage(file=f'pictures/{feature}.png').subsample(2,2)
        textures.append(image)

        tk.Button(feature_frame,image=image,bd=0,bg=bg).pack(side='left')
        tk.Label(feature_frame,text=f'{name} ({feature})',fg='#fff',bg=bg).pack()
        tk.Label(feature_frame,text=desc,fg='#fff',bg=bg).pack()
        add = classes.classic_button(feature_frame,'Добавить',None)
        add.bind('<Button-1>', choose)
        add.pack(fill='x',side='bottom')
        feature_dict[add] = [feature, options.copy()]
        
def choose(event):
    global win
    widget = event.widget
    main_engine.add_feature(feature_dict[widget])
    win.destroy()
