import tkinter as tk

canvas = None

class cursor:
    def change(cursor):
        canvas.config(cursor=cursor)
    def hide():
        canvas.config(cursor='none')
    def show():
        canvas.config(cursor='arrow')

def change_scene(scene):
    for obj in canvas.find_all():
        canvas.delete(obj)
    code = f'''import {scene}
{scene}.start(canvas)'''
    exec(code)

def add_object(obj, x=0, y=0):
    code = f'''import {obj}
global new_object
new_object = {obj}.obj(canvas, {x}, {y})'''
    exec(code)
    return new_object
