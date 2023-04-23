ms_process = 20

class mouse_events:
    def __init__(self, obj, game, script):
        self.obj = obj
        self.game = game
        self.script = script

        self.game.tag_bind(self.obj.object, '<Button-1>', self.on_click)
        self.game.tag_bind(self.obj.object, '<Enter>', self.mouse_entered)
        self.game.tag_bind(self.obj.object, '<Leave>', self.mouse_exited)

    def on_click(self, event):
        if hasattr(self.script, 'on_click'):
            self.script.self = self.obj
            self.script.on_click()
    def mouse_entered(self, event):
        if hasattr(self.script, 'mouse_entered'):
            self.script.self = self.obj
            self.script.mouse_entered()
    def mouse_exited(self, event):
        if hasattr(self.script, 'mouse_exited'):
            self.script.self = self.obj
            self.script.mouse_exited()

class top_down_move:
    def __init__(self, obj, game, script, speed):
        self.can_move = True
        
        self.vx = 0
        self.vy = 0
        self.speed = speed

        self.a = False
        self.d = False
        self.w = False
        self.s = False

        self.obj = obj
        self.game = game
        self.script = script
        self.process()
        
        self.game.bind_all('<KeyPress>', self.move)
        self.game.bind_all('<KeyRelease>', self.move_finish)

    def process(self):
        if self.can_move:
            self.game.move(self.obj.object, self.vx*0.03*self.speed, self.vy*0.03*self.speed)

            if self.vx != 0 or self.vy != 0:
                if hasattr(self.script, 'in_motion'):
                    self.script.in_motion()
            if self.vx == 0 and self.vy == 0:
                if hasattr(self.script, 'in_idle'):
                    self.script.in_idle()
            if self.vx == -1:
                if hasattr(self.script, 'moving_left'):
                    self.script.moving_left()
            if self.vx == 1:
                if hasattr(self.script, 'moving_right'):
                    self.script.moving_right()
            if self.vy == -1:
                if hasattr(self.script, 'moving_up'):
                    self.script.moving_up()
            if self.vy == 1:
                if hasattr(self.script, 'moving_down'):
                    self.script.moving_down()
            
            self.game.after(ms_process, self.process)

    def move(self, event):
        if event.keycode == 65:
            self.vx = -1
            self.a = True
        if event.keycode == 68:
            self.vx = 1
            self.d = True
        if event.keycode == 87:
            self.vy = -1
            self.w = True
        if event.keycode == 83:
            self.vy = 1
            self.s = True
            
    def move_finish(self, event):
        if event.keycode == 65:
            if self.d:
                self.vx = 1
            else:
                self.vx = 0
            self.a = False
            
        if event.keycode == 68:
            if self.a:
                self.vx = -1
            else:
                self.vx = 0
            self.d = False
            
        if event.keycode == 87:
            if self.s:
                self.vy = 1
            else:
                self.vy = 0
            self.w = False

        if event.keycode == 83:
            if self.w:
                self.vy = -1
            else:
                self.vy = 0
            self.s = False
            
    def stop(self):
        self.can_move = False
    def start(self):
        self.can_move = True
