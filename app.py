# app.py
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from scipy.io import wavfile
import pygame
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import os
import librosa
from PIL import Image, ImageTk

class AnnotationApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Training App")
        self.master.geometry("600x800")

        self.file_paths = []
        self.current_index = -1

        # Initialize data and sound
        self.responses = []
        self.current_position = 0  # Current position in audio playback
        self.canvas = None  # To hold the spectrogram canvas

        pygame.mixer.init()  # Initialize the mixer for audio playback

        # UI Components
        self.qs_label = ttk.Label(self.master, anchor="center", wraplength=500, padding=5, font=("Arial", 16))
        self.qs_label.grid(row=0, columnspan=5, pady=10)

        self.spectrogram_frame = ttk.Frame(self.master)
        self.spectrogram_frame.grid(row=1, columnspan=5, pady=3)
        
        self.slider = tk.Scale(self.master, from_=0, to=10, orient=tk.HORIZONTAL, length=300, showvalue=1, resolution=0.25)
        self.slider.grid(row=2, columnspan=5, pady=10)

        self.play_button = ttk.Button(self.master, text="Play Sound", command=self.play, state="disabled")
        self.play_button.grid(row=3, column=3, pady=10)

        self.selected_answer = tk.StringVar()
        self.choices = ["Yes", "Maybe", "No"]
        for i, choice in enumerate(self.choices):
            radio_btn = ttk.Radiobutton(self.master, text=choice, variable=self.selected_answer, value=choice, command=self.record_response)
            radio_btn.grid(row=4, column=i + 2, padx=5, pady=10)

        self.notes_label = ttk.Label(self.master, text="Notes")
        self.notes_label.grid(row=5, column=2, pady=5)

        self.notes_entry = tk.Text(self.master, height=3, width=40)
        self.notes_entry.grid(row=6, columnspan=5, padx=10, pady=5)

        self.prev_btn = ttk.Button(self.master, text="Previous", command=self.previous_question)
        self.prev_btn.grid(row=7, column=2, padx=5, pady=10)

        self.next_btn = ttk.Button(self.master, text="Next", command=self.next_question, state="disabled")
        self.next_btn.grid(row=7, column=4, padx=5, pady=10)

        self.question_number_label = ttk.Label(self.master, text="", font=("Arial", 12))
        self.question_number_label.grid(row=8, column=3)

        self.select_files_button = ttk.Button(self.master, text="Select Files", command = self.select_files)
        self.select_files_button.grid(row=8, column=4, padx=5, pady=10)

        # self.show_question()

        # Bind hotkeys
        self.set_hotkeys()  

    def select_files(self):
        file_names = filedialog.askopenfilenames(
            title = 'Select Files', filetypes=[('Audio Files', '*.wav')]
        )
        self.file_paths = file_names
        self.current_index = 0
        self.show_spectrogram(self.file_paths[0])
        self.play_button.config(state="normal")

    def play(self):
        """Play the current audio file."""
        self.record_response()
        audio = self.file_paths[self.current_index]
        pygame.mixer.music.load(audio)
        pygame.mixer.music.play(loops=0)

        # Set the maximum length of the slider based on the audio length
        self.set_slider_max_length(audio)
        self.update_slider()  # Start updating the slider

    def set_slider_max_length(self, audio_file):
        """Set the maximum value of the slider based on audio file length."""
        sample_rate, data_wav = wavfile.read(audio_file)
        audio_length = len(data_wav) / sample_rate  # Length in seconds
        self.slider.config(to=audio_length)  # Update the maximum value of the slider

    def show_spectrogram(self, audio_file):
        """Display the spectrogram of the current audio file."""

        y, sr = librosa.load(audio_file)
    
        s = librosa.feature.melspectrogram(y=y, sr=sr)
        s_db = librosa.power_to_db(s, ref=np.max)

        plt.figure(figsize=(5, 3))
        librosa.display.specshow(s_db, cmap='gray_r', sr=sr, x_axis='time', y_axis='mel')
        plt.colorbar(format='%+2.0f dB')
        plt.title('Mel-frequency spectrogram')

        plt.savefig('spectrogram.png')
        plt.close()

        img = Image.open('spectrogram.png')
        img = ImageTk.PhotoImage(img)

        label = tk.Label(self.spectrogram_frame, image=img)
        label.grid(row=3, column=0, pady=10)

        label.image = img

    def update_slider(self):
        """Update the slider based on the current position in audio playback."""
        if pygame.mixer.music.get_busy():
            # Get the current position of the audio in seconds
            self.current_position = pygame.mixer.music.get_pos() / 1000.0  # Convert ms to seconds
            self.slider.set(self.current_position)  # Update the slider position
            self.master.after(100, self.update_slider)  # Update every 100 ms

    def show_question(self):
        """Display the current question and its associated audio."""
        question = self.file_paths[self.current_index]

        # Show the spectrogram for the current audio
        self.show_spectrogram(question)

        # Reset the slider position
        self.slider.set(0)
        
        # Load previous answer and notes if they exist
        if self.current_index < len(self.responses):
            self.selected_answer.set(self.responses[self.current_index].get('user_answer', ''))
            self.notes_entry.delete(1.0, tk.END)  # Clear the text box
            self.notes_entry.insert(tk.END, self.responses[self.current_index].get('notes', ''))  # Load previous notes
        else:
            self.selected_answer.set("")  # Reset answer
            self.notes_entry.delete(1.0, tk.END)  # Clear notes box

        # Enable the next button if any choice is selected
        if self.selected_answer.get():
            self.next_btn.config(state="normal")
        else:
            self.next_btn.config(state="disabled")

        # Update the question number label
        self.question_number_label.config(text=f"Sound file {self.current_index + 1} / {len(self.file_paths)}")

        # Change the button text based on whether it’s the last question
        if self.current_index == len(self.file_paths) - 1:
            self.next_btn.config(text="Submit")
        else:
            self.next_btn.config(text="Next")

    def record_response(self, choice=None):
        """Record the user's response to the current question."""
        # If a choice is passed via the hotkey, use that. Otherwise, get the selected choice.
        if choice:
            self.selected_answer.set(choice)

        selected_choice = self.selected_answer.get()
        notes = self.notes_entry.get(1.0, tk.END).strip()

        # Store the response with sound file path and user's answer
        if self.current_index < len(self.responses):
            self.responses[self.current_index]['user_answer'] = selected_choice  # Update existing response
            self.responses[self.current_index]['notes'] = notes  # Update existing notes
        else:
            parts = self.file_paths[self.current_index].split("t-", 1)

            if len(parts) > 1:
                file_name = "t-" + parts[1]

            self.responses.append({
                "sound": file_name,  # File path of the audio
                "user_answer": selected_choice,  # User's selected answer
                "notes": notes  # Notes entered by the user
            })

        # Enable the next button if any choice is selected
        if selected_choice:  # Check if an answer is selected
            self.next_btn.config(state="normal")

    def next_question(self):
        """Move to the next question."""
        # Record response and stop the sound before moving to the next question
        self.record_response()
        pygame.mixer.music.stop()

        if self.current_index < len(self.file_paths) - 1:
            self.current_index += 1
            self.show_question()
        else:
            self.submit_answers()

    def set_hotkeys(self):
        """Bind hotkeys to buttons."""
        self.master.bind('<space>', lambda event: self.play())
        # Bind keyboard hotkeys for selecting answers
        self.master.bind('<KeyPress-a>', lambda event: self.record_response("Yes"))  #  "Yes"
        self.master.bind('<KeyPress-s>', lambda event: self.record_response("Maybe"))  #  "Maybe"
        self.master.bind('<KeyPress-d>', lambda event: self.record_response("No"))   # "No"

        # Bind 'Enter' or another key to trigger next question
        self.master.bind('<Right>', lambda event: self.next_question())
        self.master.bind('<Left>', lambda event: self.previous_question())

    def previous_question(self):
        """Move to the previous question."""
        self.record_response()
        pygame.mixer.music.stop()  # Stop the audio when going back
        if self.current_index > 0:
            self.current_index -= 1
            self.show_question()

    def submit_answers(self):
        """Handle submission of answers and show a message box."""
        
        # Check if there are any incomplete responses
        incomplete_responses = any(response['user_answer'] == '' for response in self.responses)
        
        if incomplete_responses:
            messagebox.showwarning("Incomplete Response", "Please review your submission. At least one of your annotations is incomplete!")
            return  # Don't submit if there are incomplete answers
        
        # Proceed with submission if all responses are complete
        date_submitted = datetime.now().strftime("%Y%m%d")
        filename = f"responses_{date_submitted}.csv"
        filepath = os.path.join('results', filename)
        
        df = pd.DataFrame(self.responses)
        df.to_csv(filepath, index=False)

        messagebox.showinfo("Submission", "Your responses have been submitted!")
        self.master.quit()  # Close the application after submission

