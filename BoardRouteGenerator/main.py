import kivy
kivy.require('2.2.1')

from kivy.app import App
from kivy.uix.image import Image

class BoardGenerator(App):

    def build(self):
        return Image(source='img/stokt_board.jpg')
    
if __name__ == '__main__':
    BoardGenerator().run()
