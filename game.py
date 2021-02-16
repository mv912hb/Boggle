from tkinter import *
from tkinter import messagebox
from logic import *
from textwrap import wrap
import sys

INVALID_ACTION = "You can't choose the same letter more than once"
FONT = "Arial"
LETTER_IN_PATH = "Aquamarine"
REGULAR_COLOR = "lime green"
BUTTON_ACTIVE_COLOR = "burlywood3"
BUTTON_STYLE = {"font": ("Courier", 30),
                "borderwidth": 1,
                "relief": RAISED,
                "bd": 5,
                "bg": REGULAR_COLOR,
                "activebackground": BUTTON_ACTIVE_COLOR}
QUESTION = "You are out of time! Do you want to play one more round?"
AN_QUESTION = "Do you want to exit game?"
RULES = "Welcome to Boggle game! \n" \
        "RULES: \n" \
        "1. You have to guess as much as you can in the 3 minutes!\n" \
        "2. You can only choose the adjacent cells! \n" \
        "3. Try to guess long words! \n" \
        "4. Score is given for each word is equal to squared amount of the letter \n" \
        "5. Do not cheat and use any dictionaries! \n" \
        "GOOD LUCK!"
TIME = 180

class GameGUI:
    _letters = {}

    def __init__(self, words):
        root = Tk()
        root.geometry("700x700")
        root.title("Boggle game")
        root.resizable(False, False)

        self.__start_flag = False
        self.__game_board = GameModule(randomize_board(), words)
        self.__timer = TIME
        self.__path = []
        self.__main_window = root

        self.__frame_top_left = Frame(self.__main_window, bg="LightSkyBlue2")
        self.__frame_top_right = Frame(self.__main_window, bg="LightSkyBlue2")
        self.__guessed_words_txt = Label(self.__frame_top_left,
                                         text="Guessed words:",
                                         bg="floral white",
                                         font=("Times", 15, "bold"))
        self.__guessed_words = Label(self.__frame_top_left, text=RULES,
                                     bg="LightSkyBlue2",
                                     font=("Times", 12),
                                     anchor="nw")
        self.__messages_txt = Label(self.__frame_top_right, text="Status",
                                    bg="floral white",
                                    font=("Times", 15, "bold"))
        self.__messages = Label(self.__frame_top_right,
                                bg="LightSkyBlue2",
                                font=("Times", 12))
        self.__separator = Label(self.__frame_top_right, bg="black")
        self.__left_frame = Frame(self.__main_window, bg="lime green")
        self.__right_frame = Frame(self.__main_window, bg="IndianRed2")
        self.__score_txt = Label(self.__right_frame, text="Your score",
                                 bg="HotPink4", font=(FONT, 15))
        self.__score = Label(self.__right_frame, text="0", bg="HotPink4",
                             font=("Times", 25, "bold"))
        self.__time_txt = Label(self.__right_frame, text="Your time",
                                bg="salmon2", font=(FONT, 15))
        self.__time = Label(self.__right_frame, text="03:00", bg="salmon2",
                            font=("Times", 25, "bold"))
        self.__start = Button(self.__right_frame, text="START!", bg="cyan4",
                              activebackground="gold", font=(FONT, 30),
                              command=self.start_action())
        self.__enter = Button(self.__right_frame, text="ENTER!",
                              bg="firebrick4", activebackground="gold",
                              font=(FONT, 30), command=self.finish_input)

    def make_letter(self, letter, row, col):
        """
        :param letter: letter which would be in the current cell
        """
        button = Button(self.__left_frame, text=letter, **BUTTON_STYLE,
                        command=lambda: self.create_path((row, col)))
        button.grid(row=row, column=col, rowspan=1, columnspan=1, sticky=NSEW)
        self._letters[(row, col)] = button

    def update_score(self):
        self.__score["text"] = self.__game_board.get_score()

    def create_path(self, coordinate):
        """
        :param coordinate: coordinate of current cell
        """
        self._letters[coordinate]["bg"] = LETTER_IN_PATH
        if coordinate not in self.__path:
            self.__path.append(coordinate)
        else:
            self.update_messages(INVALID_ACTION, self.__messages)

    def convert(self):
        """
        converting 180 seconds timer to mm:ss format
        :return:
        """
        mins, secs = divmod(self.__timer, 60)
        time_format = '{:02d}:{:02d}'.format(mins, secs)
        return time_format

    def timer(self):
        self.__time["text"] = self.convert()
        if self.__timer:
            self.__timer -= 1
            self.__main_window.after(1000, self.timer)
        else:
            self.next_round()

    def start_action(self):
        """
        function for action when pressing start button
        """
        def func():
            if not self.__start_flag:
                self.__start_flag = True
                self.create_board()
                self.timer()
        return func

    @staticmethod
    def update_messages(message, label: Label):
        label['text'] = message
        if len(message) > 6:
            char_width = label.winfo_width() / len(message)
            wrapped_text = '\n'.join(wrap(message, int(150 / char_width)))
            label['text'] = wrapped_text

    def finish_input(self):
        """
        function for action after guessing word
        """
        result = self.__game_board.set_path(self.__path)
        self.__path = []
        self.update_messages(result, self.__messages)

        self.set_words()
        self.update_score()
        for button in self._letters.values():
            button["bg"] = REGULAR_COLOR

    def next_round(self):
        """
        function to start the next round if user wants
        """
        answer = messagebox.askquestion("Question", QUESTION)
        if answer == "yes":
            self.__path = []
            self.__guessed_words["text"] = ""
            self.update_score()
            self.__timer = TIME
            self.__start_flag = False
            self.__game_board.new_round()
            self.create_board()
            self.timer()
        else:
            exit = messagebox.askquestion("Question", AN_QUESTION)
            if exit == "yes":
                quit()
            else:
                self.next_round()

    def create_board(self):
        """
        creating the board for current round
        """
        for i in range(4):
            Grid.columnconfigure(self.__left_frame, i, weight=1)

        for i in range(4):
            Grid.rowconfigure(self.__left_frame, i, weight=1)

        for row in range(len(self.__game_board.get_board())):
            for col in range(len(self.__game_board.get_board()[row])):
                self.make_letter(self.__game_board.get_board()[row][col], row, col)

    def pack(self):
        self.__frame_top_left.place(relwidth=0.65, relheight=0.25)
        self.__frame_top_right.place(relx=0.65, rely=0, relwidth=0.35, relheight=0.25)
        self.__separator.place(relwidth=0.01, relheight=1)
        self.__guessed_words_txt.place(relwidth=1, relheight=0.15)
        self.__guessed_words.place(rely=0.15, relwidth=1, relheight=0.85)
        self.__messages_txt.place(relx=0, rely=0, relwidth=1, relheight=0.15)
        self.__messages.place(rely=0.15, relwidth=1, relheight=0.85)
        self.__left_frame.place(relx=0, rely=0.25, relwidth=0.75, relheight=0.75)
        self.__right_frame.place(relx=0.75, rely=0.25, relwidth=0.25, relheight=0.75)
        self.__score_txt.place(relx=0, rely=0, relwidth=1, relheight=0.125)
        self.__score.place(relx=0, rely=0.125, relwidth=1, relheight=0.125)
        self.__time_txt.place(relx=0, rely=0.25, relwidth=1, relheight=0.125)
        self.__time.place(relx=0, rely=0.375, relwidth=1, relheight=0.125)
        self.__start.place(relx=0, rely=0.5, relwidth=1, relheight=0.25)
        self.__enter.place(relx=0, rely=0.75, relwidth=1, relheight=0.25)

    def run(self):
        self.pack()
        self.__main_window.mainloop()

    def set_words(self):
        self.__guessed_words["text"] = \
            "\n".join(["  ".join(option) for option in self.__game_board.get_words()])

if __name__ == "__main__":
        try:
            words = load_words_dict(sys.argv[1])
        except IndexError:
            words = load_words_dict("boggle_dict.txt")
        game = GameGUI(words)
        game.run()