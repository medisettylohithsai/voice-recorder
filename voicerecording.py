import sounddevice as sd
import soundfile as sf
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import threading

class AudioRecorder:
    def __init__(self):
        self.frames = []
        self.recording = False

    def start_recording(self):
        self.frames = []
        self.recording = True
        self.stream = sd.InputStream(callback=self.callback)
        self.stream.start()

    def stop_recording(self):
        self.recording = False
        self.stream.stop()

    def save_recording(self, filename):
        if len(self.frames) == 0:
            messagebox.showwarning("Warning", "No recording to save.")
            return
        sf.write(filename, self.frames, samplerate=44100)
        messagebox.showinfo("Success", f"Recording saved as {filename}")

    def callback(self, indata, frames, time, status):
        if self.recording:
            self.frames.extend(indata.copy())

class GUI:
    def __init__(self, master):
        self.master = master
        self.audio_recorder = AudioRecorder()
        self.create_widgets()

    def create_widgets(self):
        self.start_button = tk.Button(self.master, text="Start Recording", command=self.start_recording)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(self.master, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack(pady=5)

        self.save_button = tk.Button(self.master, text="Save Recording", command=self.save_recording, state=tk.DISABLED)
        self.save_button.pack(pady=5)

    def start_recording(self):
        self.audio_thread = threading.Thread(target=self.audio_recorder.start_recording)
        self.audio_thread.start()
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.save_button.config(state=tk.DISABLED)

    def stop_recording(self):
        self.audio_recorder.stop_recording()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.save_button.config(state=tk.NORMAL)

    def save_recording(self):
        filename = tk.filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("Wave files", "*.wav")])
        if filename:
            self.audio_recorder.save_recording(filename)

def main():
    root = tk.Tk()
    root.title("Audio Recorder")
    gui = GUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
