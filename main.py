from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.label import Label
from random import randint

class GameWidget(Widget):
    score = NumericProperty(0)
    time_left = NumericProperty(10)
    player = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        Clock.schedule_interval(self.update, 1.0/60.0)
        Clock.schedule_interval(self.countdown, 1.0)
        
    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None
        
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'escape':
            App.get_running_app().stop()
            
    def update(self, dt):
        # Gerakkan kotak target
        self.player.center_y += randint(-5, 5)
        self.player.center_x += randint(-5, 5)
        
        # Batasi gerakan di layar
        if self.player.top > self.height:
            self.player.top = self.height
        if self.player.y < 0:
            self.player.y = 0
        if self.player.right > self.width:
            self.player.right = self.width
        if self.player.x < 0:
            self.player.x = 0
            
    def countdown(self, dt):
        self.time_left -= 1
        if self.time_left <= 0:
            self.game_over()
            
    def on_touch_down(self, touch):
        if self.player.collide_point(*touch.pos):
            self.score += 1
            self.player.center = (randint(50, Window.width-50), 
                                 randint(50, Window.height-50))
        return super().on_touch_down(touch)
            
    def game_over(self):
        Clock.unschedule(self.update)
        Clock.unschedule(self.countdown)
        self.add_widget(Label(
            text=f'Game Over!\nScore: {self.score}',
            font_size='40sp',
            center_x=self.width/2,
            center_y=self.height/2,
            color=(1,0,0,1)
        ))

class GameApp(App):
    def build(self):
        return GameWidget()

if __name__ == '__main__':
    GameApp().run()