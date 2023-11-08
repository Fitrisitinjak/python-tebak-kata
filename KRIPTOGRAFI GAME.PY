from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.colorpicker import ColorPicker
from kivy.graphics import Color, Rectangle
from kivy.core.text import LabelBase
import random  # Impor modul random

# Kamus penggantian simbol matematika
simbol_matematika = {
    'A': '∆',
    'B': 'Σ',
    'C': 'Ω',
    'D': 'φ',
    'E': 'ε',
    'F': '∫',
    'G': '∂',
    'H': 'μ',
    'I': '!',
    'J': '∏',
    'K': '∝',
    'L': '⊥',
    'M': 'ω',
    'N': 'Π',
    'O': 'θ',
    'P': '∂',
    'Q': 'δ',
    'R': '∠',
    'S': '§',
    'T': 'τ',
    'U': '√',
    'V': '∀',
    'W': 'Φ',
    'X': '*',
    'Y': 'λ',
    'Z': 'ζ',
}

# Fungsi untuk mengenkripsi teks dengan Caesar Cipher dan simbol matematika
def caesar_cipher_encrypt(text, shift):
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            is_upper = char.isupper()
            char = char.upper()
            char_code = ord(char) - ord('A')
            encrypted_char = chr(((char_code + shift) % 26) + ord('A'))
            if not is_upper:
                encrypted_char = encrypted_char.lower()
        else:
            encrypted_char = char
        if encrypted_char in simbol_matematika:
            encrypted_char = simbol_matematika[encrypted_char]
        encrypted_text += encrypted_char
    return encrypted_text

class TebakKataApp(App):
    def build(self):
        self.kata_asli = ["PENA","BUKU","PENCIL","PENGGARIS","SPIDOL","KUNCI","GEMBOK","DOMPET","CINCIN","GELANG"]
        self.kata_enkripsi = [caesar_cipher_encrypt(word, 3) for word in self.kata_asli]

        # Membuat list indeks pertanyaan dan mengacaknya
        self.random_question_indices = list(range(len(self.kata_asli)))
        random.shuffle(self.random_question_indices)

        layout = BoxLayout(orientation="vertical", spacing=10, padding=10)
        layout.canvas.before.add(Color(0.5, 0.5, 0.5, 1))  # Warna latar belakang

        # Menggambar gambar latar belakang
        with layout.canvas.before:
            background = Rectangle(source="bluee.jpg", pos=layout.pos, size=(1500, 1000), )

        # Menambahkan gambar di bawah judul
        image_layout = BoxLayout(orientation="horizontal")
        border_image = Image(source="simbol.png", size_hint=(1, 1.4), size=(150,150), allow_stretch=True)
        image_layout.add_widget(border_image)
        layout.add_widget(image_layout)

        # Membuat judul game
        judul_font_path = "MyFont.ttf"  # Ganti dengan path ke file font Anda
        LabelBase.register(name="MyFont", fn_regular=judul_font_path)
        judul = Label(
            text="Game Caesar Cipher", 
            font_size=30, 
            color=(1, 1, 1, 1),
           
            )  # Warna teks merah
        layout.add_widget(judul)

        # Membuat ScrollView untuk daftar pertanyaan
        scroll_view = ScrollView()
        scroll_layout = GridLayout(cols=1, spacing=10)
        scroll_view.add_widget(scroll_layout)

        self.current_question = 0
        self.pertanyaan_label = Label(text=f"{self.current_question + 1}. Ayo Tebak Nama Benda Apakah ini? ({self.kata_enkripsi[self.random_question_indices[self.current_question]]} )", font_size=20, color=(1, 1, 1, 1))  # Warna teks biru
        scroll_layout.add_widget(self.pertanyaan_label)

        self.jawaban_input = TextInput(hint_text="Jawaban", font_size=18, background_color=(1, 1, 1, 1))  # Warna latar belakang putih
        scroll_layout.add_widget(self.jawaban_input)

        self.periksa_tombol = Button(text="Periksa", on_release=self.periksa_jawaban, background_color=(0, 0.5, 1, 1))  # Warna latar belakang hijau
        scroll_layout.add_widget(self.periksa_tombol)

        scroll_layout.size_hint = (1, None)
        scroll_layout.height = 300
        layout.add_widget(scroll_view)

        # Membuat tombol back dan lanjut
        tombol_layout = BoxLayout(orientation="horizontal", spacing=10, padding=10)
        back_tombol = Button(text="Back", on_release=self.back_question, background_color=(1, 0, 0, 1))  # Warna latar belakang merah
        lanjut_tombol = Button(text="Lanjut", on_release=self.next_question, background_color=(0, 0, 1, 1))  # Warna latar belakang biru
        tombol_layout.add_widget(back_tombol)
        tombol_layout.add_widget(lanjut_tombol)
        layout.add_widget(tombol_layout)

        self.popup = None

        return layout

    def periksa_jawaban(self, instance):
        jawaban = self.jawaban_input.text
        kata_asli = self.kata_asli[self.random_question_indices[self.current_question]]  # Mendapatkan kata asli
        if jawaban == kata_asli:
            self.show_popup(f"Jawaban benar! Plain Text: {kata_asli}")
        else:
            self.show_popup(f"Jawaban salah. Plain Text: {kata_asli}")

    def show_popup(self, message):
        content = BoxLayout(orientation="vertical")
        content.add_widget(Label(text=message, font_size=18))
        popup = Popup(title="Info 3x Pergeseran Huruf", content=content, size_hint=(None, None), size=(300, 150))
        popup.open()

    def back_question(self, instance):
        if self.current_question > 0:
            self.current_question -= 1
            self.update_question()

    def next_question(self, instance):
        if self.current_question < len(self.kata_asli) - 1:
            self.current_question += 1
            self.update_question()
        else:
            self.show_popup("Permainan selesai. Terima kasih!")

    def update_question(self):
        self.pertanyaan_label.text = f"{self.current_question + 1}. Ayo Tebak Nama Benda Apakah ini? ({self.kata_enkripsi[self.random_question_indices[self.current_question]]}"
        self.jawaban_input.text = ""

if __name__ == "__main__":
    TebakKataApp().run()
