from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from restart_progress import restart_progress
from test_word import Tester
from create_word import Creator
import json
import csv

class VocabInterface:
    def __init__(self):
        self.root = Tk()
        self.root.title("Vocabulary Trainer")
        self.tester = Tester()
        self.creator = Creator()
        
        with open("words_created.json", "r") as file2:
            self.words_created = json.load(file2) 

        with open("mastery.json", "r") as file3:
            self.mastery = json.load(file3)

        with open ("words_list_exp.csv", "r") as file1:
            self.words_list = list(csv.reader(file1))
        
        self.current_word, self.mastery, self.words_created = self.tester.get_initial_word(self.mastery, self.words_list, self.words_created)
        self.current_word = str(self.current_word)
        self.current_word_mastery_level = 0
        self.answer = StringVar()
        self.setup_ui() 
        self.setup_menu()
        self.root.mainloop()

    def setup_ui(self):
        words_created = self.words_created

        self.frm = ttk.Frame(self.root, padding=50)
        self.frm.grid()

        word_data = words_created[self.current_word]
        self.word_label = ttk.Label(self.frm, text=word_data['word'])
        self.word_label.grid(column=1, row=1)
        self.result_label = ttk.Label(self.frm, text="")
        self.result_label.grid(column=1, row=3)

        ttk.Label(self.frm, text="").grid(column=1, row=4)

        self.total_words_label = ttk.Label(self.frm, text=f"Total words: {len(self.words_created)}")
        self.total_words_label.grid(column=1, row=5)   
        self.level_0_words_label = ttk.Label(self.frm, text=f"Level 0: {len(self.mastery['mastery_0'])}")
        self.level_0_words_label.grid(column=1, row=6)
        self.level_1_words_label = ttk.Label(self.frm, text=f"Level 1: {len(self.mastery['mastery_1'])}")
        self.level_1_words_label.grid(column=1, row=7)
        self.level_2_words_label = ttk.Label(self.frm, text=f"Level 2: {len(self.mastery['mastery_2'])}")
        self.level_2_words_label.grid(column=1, row=8)
        self.level_3_words_label = ttk.Label(self.frm, text=f"Level 3: {len(self.mastery['mastery_3'])}")
        self.level_3_words_label.grid(column=1, row=9)
        self.level_4_words_label = ttk.Label(self.frm, text=f"Level 4: {len(self.mastery['mastery_4'])}")
        self.level_4_words_label.grid(column=1, row=10)
        self.level_5_words_label = ttk.Label(self.frm, text=f"Level 5: {len(self.mastery['mastery_5'])}")
        self.level_5_words_label.grid(column=1, row=11)

        ttk.Label(self.frm, text="Translate this word:").grid(column=0, row=1)
        ttk.Label(self.frm, text="Translation: ").grid(column=0, row=2)

        self.entry = ttk.Entry(self.frm, width=50, textvariable=self.answer)
        self.entry.grid(column=1, row=2)
        self.entry.bind("<Return>", lambda event: self.handle_submit())

        ttk.Button(self.frm, text="Submit", command=self.handle_submit).grid(column=2, row=2)

    def setup_menu(self):
        menu = Menu(self.root)
        self.root.config(menu=menu)
        filemenu = Menu(menu)
        menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Reset progress", command=self.restart)
        filemenu.add_separator()
        filemenu.add_command(label="Quit", command=self.root.destroy)    
    
    def update_word(self, new_word):
        words_created = self.words_created

        self.current_word = str(new_word)
        self.word_label.config(text=words_created[self.current_word]['word'])
        self.answer.set("")

        self.total_words_label.config(text=f"Total words: {len(self.words_created)}")
        self.level_0_words_label.config(text=f"Level 0: {len(self.mastery['mastery_0'])}")
        self.level_1_words_label.config(text=f"Level 1: {len(self.mastery['mastery_1'])}")
        self.level_2_words_label.config(text=f"Level 2: {len(self.mastery['mastery_2'])}")
        self.level_3_words_label.config(text=f"Level 3: {len(self.mastery['mastery_3'])}")
        self.level_4_words_label.config(text=f"Level 4: {len(self.mastery['mastery_4'])}")
        self.level_5_words_label.config(text=f"Level 5: {len(self.mastery['mastery_5'])}")

    def handle_submit(self):
        user_answer = self.answer.get()
        answer, self.mastery = self.tester.check_answer(user_answer, self.mastery, self.words_created, self.current_word, self.current_word_mastery_level)
        # self.mastery = mastery  
        if answer == True:
            self.result_label.config(text=f"{user_answer} was: Correct!")
            self.get_next_word()
        else:
            self.result_label.config(text=f"{user_answer} was: Incorrect, try again! (hint: {self.words_created[self.current_word]['translation']}, {self.current_word})")
            if self.current_word_mastery_level > 0:
                self.current_word_mastery_level -= 1
            else:
                self.current_word_mastery_level = 0

    def get_next_word(self):
        next_word, mastery_level, self.mastery, self.words_created = self.tester.get_word(self.mastery, self.words_list, self.words_created)
        self.current_word_mastery_level = mastery_level
        self.update_word(next_word)

    def restart(self):
        restart_progress()
        with open("mastery.json", "r") as file3:
            self.mastery = json.load(file3)
        with open("words_created.json", "r") as file2:
            self.words_created = json.load(file2)
        self.current_word, self.mastery, self.words_created = self.tester.get_initial_word(self.mastery, self.words_list, self.words_created)
        self.current_word = str(self.current_word)
        self.current_word_mastery_level = 0
        print("restart successful")
        self.result_label.config(text="Vocabulary training restarted")
        self.update_word(self.current_word)




    