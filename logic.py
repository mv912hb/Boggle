import random

RIGHT_MESSAGE = "RIGHT!"
WRONG_MASSAGE = "Word doesn't exist or you used the wrong path!"
OPEN_WORD_MESSAGE = "You have already guessed this word!"
BOARD_SIZE = 4
LETTERS = [
    ['A', 'E', 'A', 'N', 'E', 'G'],
    ['A', 'H', 'S', 'P', 'C', 'O'],
    ['A', 'S', 'P', 'F', 'F', 'K'],
    ['O', 'B', 'J', 'O', 'A', 'B'],
    ['I', 'O', 'T', 'M', 'U', 'C'],
    ['R', 'Y', 'V', 'D', 'E', 'L'],
    ['L', 'R', 'E', 'I', 'X', 'D'],
    ['E', 'I', 'U', 'N', 'E', 'S'],
    ['W', 'N', 'G', 'E', 'E', 'H'],
    ['L', 'N', 'H', 'N', 'R', 'Z'],
    ['T', 'S', 'T', 'I', 'Y', 'D'],
    ['O', 'W', 'T', 'O', 'A', 'T'],
    ['E', 'R', 'T', 'T', 'Y', 'L'],
    ['T', 'O', 'E', 'S', 'S', 'I'],
    ['T', 'E', 'R', 'W', 'H', 'V'],
    ['N', 'U', 'I', 'H', 'M', 'QU']
]


class GameModule:
    def __init__(self, board, words):
        self.__board = board
        self.__guessed_words = [[]]
        self.__score = 0
        self.__all_words = words

    def add_score(self, word):
        """
        :param word: guessed word
        """
        self.__score += len(word)**2

    def set_path(self, path):
        """
        :param path: path of current word
        :return: message to user
        """
        word = is_valid_path(self.__board, path, self.__all_words)
        if word:
            if not any(word in sublist for sublist in self.__guessed_words):
                self.set_words(word)
                self.add_score(word)
                return RIGHT_MESSAGE
            else:
                return OPEN_WORD_MESSAGE
        else:
            return WRONG_MASSAGE

    def new_round(self):
        self.__board = randomize_board()
        self.__guessed_words = []
        self.__score = 0

    def set_words(self, word):
        """
        :param word: current guessed word
        """
        for lst in self.__guessed_words:
            if len(lst) < 8:
                lst.append(word)
                return
        self.__guessed_words.append([word])

    def get_score(self):
        return self.__score

    def get_board(self):
        return self.__board

    def get_words(self):
        return self.__guessed_words

    def update_board(self, new_board):
        self.__board = new_board


def load_words_dict(file_path="boggle_dict.txt"):
    """
    :param file_path: path to the file contains all words
    :return: dictionary with all the words as a key
    """
    dictionary = {}
    with open(file_path, "r") as file:
        for line in file:
                key = line.rstrip("\n")
                if key and key not in dictionary:
                    dictionary[key] = True
    return dictionary

def is_valid_path(board, path, words):
    """
    :return: word if path is correct
    """
    if not path:
        return
    if len(path) != len(set(path)):
        return
    if not 0 <= path[0][0] < BOARD_SIZE or not 0 <= path[0][1] < BOARD_SIZE:
        return
    word = board[path[0][0]][path[0][1]]
    for ind in range(1, len(path)):
        for i in range(2):
            if not 0 <= path[ind][i] < BOARD_SIZE:
                return
            if not -1 <= path[ind][i] - path[ind - 1][i] <= 1:
                return
            if ind != len(path) - 1:
                if not -1 <= path[ind][i] - path[ind + 1][i] <= 1:
                    return
        word += board[path[ind][0]][path[ind][1]]
    if word in words:
        return word

def find_length_n_words(n, board, words):
    """
    :param n: length
    :param board: current board
    :return: all words with length n located on current board
    """
    results = []
    for word in words:
        if len(word) == n:
            _find_length_n_words_helper(board, results, word, [], 0)
    return results

def _find_length_n_words_helper(board, results, word, path, ind):
    if ind == len(word):
        results.append((word, path[:]))
        return
    first_letters = []
    for row in range(len(board)):
        for col in range(len(board[row])):
            if len(board[row][col]) == 2:
                if ind != len(word) - 1:
                    if board[row][col] == word[ind] + word[ind + 1]:
                        first_letters.append((board[row][col], (row, col)))
                        continue
            if board[row][col] == word[ind]:
                first_letters.append((board[row][col], (row, col)))
    if len(first_letters) == 0:
        return
    for letter in first_letters:
        if len(path) != 0:
            if letter[1] != path[-1]:
                flag = True
                for i in range(2):
                    if not -1 <= letter[1][i] - path[-1][i] <= 1:
                        flag = False
                if flag:
                    if len(letter[0]) == 2:
                        if letter[1] not in path:
                            path.append(letter[1])
                            _find_length_n_words_helper(board, results, word, path, ind + 2)
                            path.pop()
                    else:
                        if letter[1] not in path:
                            path.append(letter[1])
                            _find_length_n_words_helper(board, results, word, path, ind + 1)
                            path.pop()
        else:
            if len(letter[0]) == 2:
                if letter[1] not in path:
                    path.append(letter[1])
                    _find_length_n_words_helper(board, results, word, path, ind + 2)
                    path.pop()
            else:
                if letter[1] not in path:
                    path.append(letter[1])
                    _find_length_n_words_helper(board, results, word, path, ind + 1)
                    path.pop()

def randomize_board(dice_list=LETTERS):
    dice_indices = list(range(len(dice_list)))
    random.shuffle(dice_indices)
    board = []
    for i in range(BOARD_SIZE):
        row = []
        for j in range(BOARD_SIZE):
            die = dice_list[dice_indices[i * 4 + j]]
            letter = random.choice(die)
            row.append(letter)
        board.append(row)
    return board






















