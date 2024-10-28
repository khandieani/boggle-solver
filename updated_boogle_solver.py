import re

class BoggleSolver:
    def __init__(self, board, word_list):
        # Initialize board, dictionary, and prefix set
        self.board = board
        self.word_list = set(word.lower() for word in word_list)
        self.prefix_set = self.create_prefix_set(word_list)
        self.rows = len(board)
        self.cols = len(board[0]) if board else 0
        self.found_words = set()

    def create_prefix_set(self, word_list):
        """Create a set of all possible prefixes from the word list."""
        prefixes = set()
        for word in word_list:
            for i in range(1, len(word) + 1):
                prefixes.add(word[:i].lower())
        return prefixes

    def is_valid_board(self, board):
        """Check if the board is square and contains only valid characters."""
        if not board or any(len(row) != len(board) for row in board):
            return False

        valid_pattern = r'^(st|qu|[a-prt-z])$'
        for row in board:
            for cell in row:
                if not re.match(valid_pattern, cell.lower()):
                    return False
        return True

    def set_board(self, board):
        """Set a new board and update dimensions."""
        self.board = board
        self.rows = len(board)
        self.cols = len(board[0]) if board else 0

    def set_word_list(self, word_list):
        """Update the dictionary and regenerate the prefix set."""
        self.word_list = set(word.lower() for word in word_list)
        self.prefix_set = self.create_prefix_set(word_list)

    def depth_first_search(self, row, col, current_path, visited):
        """Use DFS to find all valid words from a given cell."""
        if row < 0 or col < 0 or row >= self.rows or col >= self.cols or visited[row][col]:
            return

        current_path += self.board[row][col].lower()

        if current_path not in self.prefix_set:
            return

        if len(current_path) >= 3 and current_path in self.word_list:
            self.found_words.add(current_path)

        visited[row][col] = True

        # Define all possible moves in 8 directions
        for delta_row, delta_col in [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),         (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]:
            self.depth_first_search(row + delta_row, col + delta_col, current_path, visited)

        visited[row][col] = False

    def discover_words(self):
        """Identify all valid words in the board using DFS."""
        self.found_words.clear()
        visited = [[False] * self.cols for _ in range(self.rows)]

        for row in range(self.rows):
            for col in range(self.cols):
                self.depth_first_search(row, col, "", visited)

        return list(self.found_words)

    def get_words(self):
        """Get all valid words found on the board."""
        if not self.is_valid_board(self.board):
            return []
        solutions = self.discover_words()
        return sorted(word.upper() for word in solutions)

