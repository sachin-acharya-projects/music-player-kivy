from kivy.lang import Builder
from kivy.app import App
# from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.config import Config
from MusicPlayer import MusicPlayer
from MusicPlayer import generateMusicDirectory
Window.size = (700, 450)
# My Layout Class
Builder.load_file('builder.kv')
data = MusicPlayer()
class MyLayout(Widget):
    def update(self, screen, name):
        screen.text = data.status(name)
    def play(self):
        play = self.ids.play
        screen = self.ids.screen
        if play.text == 'Play':
            item = data.play()
            play.text = 'Pause'
            self.update(screen, item)
        else:
            item = data.pause()
            play.text = 'Play'
            self.update(screen, item)
    def next(self):
        screen = self.ids.screen
        item = data.next()
        self.update(screen, item)
    def prev(self):
        screen = self.ids.screen
        item = data.prev()
        self.update(screen, item)
    def stop(self):
        screen = self.ids.screen
        play = self.ids.play
        item = data.stop()
        self.update(screen, item)
        play.text = 'Play'
    def exit(self):
        exit()
    def generate(self):
        generateMusicDirectory()
        self.ids.screen.text = "MusicList Successfully Generated"
class Player(App):
    def build(self):
        Window.clearcolor = (0, 0, 0, 1)
        self.title = 'Music Player'
        return MyLayout()
if __name__ == '__main__':
    Player().run()
