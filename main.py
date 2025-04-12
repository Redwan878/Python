from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
import math


class PomodoroTimer(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 50
        self.spacing = 20

        # Constants
        self.WORK_MIN = 25
        self.SHORT_BREAK_MIN = 5
        self.LONG_BREAK_MIN = 20
        self.reps = 0
        self.timer = None

        # Load sound
        self.sound = SoundLoader.load('beep.wav')

        # Title
        self.title_label = Label(
            text='Study Break Timer',
            font_size='40sp',
            color=(0.91, 0.19, 0.36, 1),  # RED
            size_hint=(1, 0.2)
        )
        self.add_widget(self.title_label)

        # Tomato Image
        self.tomato = Image(
            source='tomato.png',
            size_hint=(1, 0.4)
        )
        self.add_widget(self.tomato)

        # Timer display
        self.timer_label = Label(
            text='00:00',
            font_size='60sp',
            color=(0, 0, 0, 1),  # Black color for better visibility
            size_hint=(1, 0.2)
        )
        self.add_widget(self.timer_label)

        # Buttons
        button_layout = BoxLayout(
            size_hint=(1, 0.1),
            spacing=20,
            padding=[20, 0]
        )

        self.start_button = Button(
            text='Start',
            on_press=self.start,
            background_color=(0.61, 0.87, 0.67, 1),
            background_normal='',
            size_hint=(0.4, 1)
        )
        self.reset_button = Button(
            text='Reset',
            on_press=self.reset,
            background_color=(0.89, 0.59, 0.61, 1),
            background_normal='',
            size_hint=(0.4, 1)
        )

        button_layout.add_widget(self.start_button)
        button_layout.add_widget(self.reset_button)
        self.add_widget(button_layout)

        # Checkmarks
        self.check_label = Label(
            text='',
            font_size='30sp',
            color=(0.61, 0.87, 0.67, 1),
            size_hint=(1, 0.1)
        )
        self.add_widget(self.check_label)

    def start(self, instance):
        self.reps += 1
        work_sec = self.WORK_MIN * 60
        short_break = self.SHORT_BREAK_MIN * 60
        long_break = self.LONG_BREAK_MIN * 60

        if self.reps % 8 == 0:
            self.count_down(long_break)
            self.title_label.text = "Long Break"
            if self.sound:
                self.sound.play()
        elif self.reps % 2 == 0:
            self.count_down(short_break)
            self.title_label.text = "Short Break"
            if self.sound:
                self.sound.play()
        else:
            self.count_down(work_sec)
            self.title_label.text = "Study Time"

    def reset(self, instance):
        if self.timer:
            self.timer.cancel()
        self.timer_label.text = "00:00"
        self.title_label.text = "Study Break Timer"
        self.check_label.text = ""
        self.reps = 0

    def count_down(self, count):
        minutes = math.floor(count / 60)
        seconds = count % 60

        time_str = f"{minutes:02d}:{seconds:02d}"
        self.timer_label.text = time_str

        if count > 0:
            self.timer = Clock.schedule_once(
                lambda dt: self.count_down(count - 1), 1)
        else:
            self.start(None)
            work_sessions = math.floor(self.reps / 2)
            self.check_label.text = "✔" * work_sessions


class PomodoroApp(App):
    def build(self):
        Window.clearcolor = (0.97, 0.96, 0.87, 1)  # YELLOW
        return PomodoroTimer()


if __name__ == '__main__':
    PomodoroApp().run()