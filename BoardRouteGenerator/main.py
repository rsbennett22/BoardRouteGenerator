import kivy
kivy.require('2.2.1')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.label import Label

board = Image(source='img/stokt_board.jpg')

Window.size = (board.width * 10, board.height * 10)

class BoardGenerator(Widget):
    pass

class BoardGeneratorApp(App):
    def build(self):
        self.label = Label()
        Window.bind(mouse_pos=lambda w, p: setattr(self.label, 'text', str(p)))
        return self.label, BoardGenerator()
    
if __name__ == '__main__':
    BoardGeneratorApp().run()
