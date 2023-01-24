import sys
import json
import simpleaudio as sa
import numpy as np
from ui_window import Ui_MainWindow
from PyQt6.QtWidgets import QApplication, QMainWindow

# Define the frequency and duration of the beep
frequency = 500  # Hz
duration = 50  # ms

# Generate a numpy array with the beep sound
sample_rate = 44100  # samples per second
sample_short = np.concatenate([np.ones(int(sample_rate * duration / 2000)), np.zeros(int(sample_rate * duration / 2000))])

sample_long = np.concatenate([np.ones(int(sample_rate * duration * 3 / 2000)), np.zeros(int(sample_rate * duration * 3 / 2000))])

sample_zero = np.zeros(int(sample_rate * duration * 7))

with open("morse.json") as morse_json:
    morse = json.load(morse_json)


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.morse_text.textChanged.connect(self.to_morse)
        self.ui.play_button.clicked.connect(self.play_sound)
        self.ui.pause_button.clicked.connect(self.pause_sound)
        self.beep = None
        self.play = False
        self.show()

    def to_morse(self):
        text_input = (self.ui.morse_text.toPlainText()).lower()
        text_to_morse = [morse[f"{char}"] for char in text_input]
        label_text = "".join([str(char) for char in text_to_morse])
        self.ui.text_label.setText(label_text)

    def play_sound(self):
        samples = []
        for char in self.ui.text_label.text():

            for dot in char:

                if dot == ".":
                    samples.append(sample_short)

                elif dot == "-":
                    samples.append(sample_long)

                else:
                    samples.append(sample_zero)

        combined_samples = np.concatenate(samples)
        beep = sa.WaveObject(combined_samples, 2, 1, sample_rate)
        try:
            if not self.play:
                self.beep.resume()
                self.play = True
        except AttributeError:
            pass

        try:
            if not self.beep.is_playing():
                self.play = True
                self.beep = beep.play()
        except AttributeError:
            self.play = True
            self.beep = beep.play()

    def pause_sound(self):

        if self.play:
            self.beep.pause()
            self.play = False
            print(self.beep.is_playing())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = Window()
    sys.exit(app.exec())
