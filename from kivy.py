from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout


class myapp(App):
    def build(self):
       layout_utama=BoxLayout(orientation="vertical")
       label1=Label(text="Aplikasiku",font_size=30)
       entry1=TextInput(hint_text="Percobaan",font_size=30)
       button1=Button(text="Tombol",font_size=30)

       layout_utama.add_widget(label1)
       layout_utama.add_widget(entry1)
       layout_utama.add_widget(button1)

       return layout_utama

myapp().run()