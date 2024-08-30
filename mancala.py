import math
import random

class Mancala:
    def __init__(self, random_mode=False, total_stones_per_side=24):
        if random_mode:
            self.board = self.random_board(total_stones_per_side)
        else:
            # Default board initialization: 4 stones per pit
            self.board = [4] * 6 + [0] + [4] * 6 + [0]  # Player 1 [0-5], Store 1 [6], Player 2 [7-12], Store 2 [13]

    def random_board(self, total_stones):
        # Ensure each pit has at least one stone
        pits = [1] * 6
        remaining_stones = total_stones - 6  # Subtract 1 stone from each pit

        # Randomly distribute the remaining stones
        for i in range(6):
            if i == 5:
                pits[i] += remaining_stones
            else:
                max_additional_stones = remaining_stones - (5 - i)  # Ensure at least 1 stone remains for each remaining pit
                add_stones = random.randint(0, max_additional_stones)
                pits[i] += add_stones
                remaining_stones -= add_stones

        random.shuffle(pits)
        return pits + [0] + pits.copy() + [0]  # Mirror the distribution for the other side


    def display_board_part(self):
        print("\nBoard View:")
        print("Player 2 (Top)")
        print("---------------------------------")
        print("|            Store 2            |")
        print(f"|             ({self.board[13]:2} )             |")
        for i in range(6):
            print(f"| Pit {i + 1:2} | {self.board[i]:2} |   | {self.board[12 - i]:2} | Pit {12 - i + 1:2} | ")
        print(f"|             ({self.board[6]:2} )             |")
        print("|            Store 1            |")
        print("---------------------------------")
        print("Player 1 (Bottom)")
        print("\n")
    
    def display_board(self):
        space_between = " " * 10  # Define the white space between the two views
        print("\n")
        print(f"Board View For Player 1:          {space_between} Board View For Player 2:")
        print(f"Player 2 (Top)                    {space_between} Player 1 (Top)")
        print(f"--------------------------------- {space_between} ---------------------------------")
        print(f"|            Store 2            | {space_between} |            Store 1            |")
        print(f"|             ({self.board[13]:2} )             | {space_between} |             ({self.board[6]:2} )             |")
        for i in range(6):
            print(f"| Pit {i + 1:2} | {self.board[i]:2} |   | {self.board[12 - i]:2} | Pit {12 - i + 1:2} | {space_between} | Pit {12 + i - 4:2} | {self.board[12 + i - 5]:2} |   | {self.board[ 6 - i - 1]:2} | Pit {6 - i:2} | ")
        print(f"|             ({self.board[6]:2} )             | {space_between} |             ({self.board[13]:2} )             |")
        print(f"|            Store 1            | {space_between} |            Store 2            |")
        print(f"--------------------------------- {space_between} --------------------------------- ")
        print(f"Player 1 (Bottom)                 {space_between} Player 2 (Bottom)")
        print("\n")
 
    def make_move(self, pit):
        stones = self.board[pit]
        self.board[pit] = 0
        position = pit
        
        while stones > 0:
            position = (position + 1) % 14
            if position == 6 and pit > 5:  # Skip Player 1's store if Player 2 is moving
                continue
            elif position == 13 and pit < 6:  # Skip Player 2's store if Player 1 is moving
                continue
            self.board[position] += 1
            stones -= 1

        # Check for capture
        if 0 <= position < 6 and self.board[position] == 1 and pit < 6:  # Player 1 captures
            opposite_pit = 12 - position
            captured = self.board[opposite_pit]
            if captured > 0:
                self.board[6] += captured + 1
                self.board[position] = 0
                self.board[opposite_pit] = 0
        elif 7 <= position < 13 and self.board[position] == 1 and pit > 5:  # Player 2 captures
            opposite_pit = 12 - position
            captured = self.board[opposite_pit]
            if captured > 0:
                self.board[13] += captured + 1
                self.board[position] = 0
                self.board[opposite_pit] = 0

        # Return whether the player gets an extra turn
        return (position == 6 and pit < 6) or (position == 13 and pit > 5)

    def is_game_over(self):
        return sum(self.board[0:6]) == 0 or sum(self.board[7:13]) == 0

    def collect_remaining_stones(self):
        # Player 1 collects all remaining stones on their side
        self.board[6] += sum(self.board[0:6])
        for i in range(6):
            self.board[i] = 0

        # Player 2 collects all remaining stones on their side
        self.board[13] += sum(self.board[7:13])
        for i in range(7, 13):
            self.board[i] = 0

    def determine_winner(self):
        if self.board[6] > self.board[13]:
            return ">>> Player 1 wins!"
        elif self.board[13] > self.board[6]:
            return ">>> Player 2 wins!"
        else:
            return ">>> It's a tie!"

    def evaluate(self):
        return self.board[6] - self.board[13]  # Player 1 store - Player 2 store

    def minimax(self, depth, alpha, beta, maximizingPlayer):
        if depth == 0 or self.is_game_over():
            return self.evaluate(), -1  # Return evaluation and invalid pit

        if maximizingPlayer:
            maxEval = -math.inf
            best_move = -1
            for pit in range(6):  # Player 1 pits
                if self.board[pit] == 0:
                    continue
                new_board = Mancala()
                new_board.board = self.board.copy()
                extra_turn = new_board.make_move(pit)
                if extra_turn:
                    eval, _ = new_board.minimax(depth, alpha, beta, True)
                else:
                    eval, _ = new_board.minimax(depth - 1, alpha, beta, False)
                if eval > maxEval:
                    maxEval = eval
                    best_move = pit
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return maxEval, best_move
        else:
            minEval = math.inf
            best_move = -1
            for pit in range(7, 13):  # Player 2 pits
                if self.board[pit] == 0:
                    continue
                new_board = Mancala()
                new_board.board = self.board.copy()
                extra_turn = new_board.make_move(pit)
                if extra_turn:
                    eval, _ = new_board.minimax(depth, alpha, beta, False)
                else:
                    eval, _ = new_board.minimax(depth - 1, alpha, beta, True)
                if eval < minEval:
                    minEval = eval
                    best_move = pit
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return minEval, best_move

    def best_move(self, depth, maximizingPlayer=True):
        _, move = self.minimax(depth, -math.inf, math.inf, maximizingPlayer)
        return move

def choose_mode_and_level():
    print("*** Choose game mode ***")
    print("1. Player 1 vs Computer")
    print("2. Computer vs Player 2")
    print("3. Computer vs Computer")
    print("4. Player vs Player")
    mode = int(input(">>> Enter the mode (1-4): "))

    print("\n*** Choose Level ***")
    print("1. Beginner")
    print("2. Intermediate")
    print("3. Advanced")
    print("4. Master")
    level = int(input(">>> Enter the level (1-4): "))

    print("\n*** Board Initialization ***")
    print("1. Standard Board (4 stones per pit)")
    print("2. Random Board (Equal stones per side, random distribution)")
    board_choice = int(input(">>> Choose board initialization (1-2): "))

    random_mode = board_choice == 2
    print("\n")
    return mode, level, random_mode

def play_game(mode, level, random_mode):
    game = Mancala(random_mode=random_mode)
    print("********************************* Game Start *********************************")
    print(">>> Initial Board")
    game.display_board()

    if level == 1:
        depth = 2
    elif level == 2:
        depth = 3
    elif level == 3:
        depth = 5
    else:
        depth = 10

    while not game.is_game_over():
        if mode == 1:  # Player 1 vs Computer (Player 2)
            print(">>> Player 1's Turn")
            player_1_move = int(input("Enter your move (1-6): ")) - 1
            extra_turn = game.make_move(player_1_move)
            game.display_board()

            while extra_turn and not game.is_game_over():
                print(">>> Player 1's Extra Turn")
                player_1_move = int(input("Enter your move (1-6): ")) - 1
                extra_turn = game.make_move(player_1_move)
                game.display_board()

            if game.is_game_over():
                break

            print(">>> Computer's Turn (Player 2)")
            player_2_move = game.best_move(depth, maximizingPlayer=False)
            print(f"Computer (Perfect Move): Pit {player_2_move + 1}")
            extra_turn = game.make_move(player_2_move)
            game.display_board()

            while extra_turn and not game.is_game_over():
                print(">>> Computer's Extra Turn")
                player_2_move = game.best_move(depth, maximizingPlayer=False)
                print(f"Computer (Extra Turn): Pit {player_2_move + 1}")
                extra_turn = game.make_move(player_2_move)
                game.display_board()

        elif mode == 2:  # Computer (Player 1) vs Player 2
            print(">>> Computer's Turn (Player 1)")
            player_1_move = game.best_move(depth, maximizingPlayer=True)
            print(f"Computer (Perfect Move): Pit {player_1_move + 1}")
            extra_turn = game.make_move(player_1_move)
            game.display_board()

            while extra_turn and not game.is_game_over():
                print(">>> Computer's Extra Turn")
                player_1_move = game.best_move(depth, maximizingPlayer=True)
                print(f"Computer (Extra Turn): Pit {player_1_move + 1}")
                extra_turn = game.make_move(player_1_move)
                game.display_board()

            if game.is_game_over():
                break

            print(">>> Player 2's Turn")
            player_2_move = int(input("Enter your move (1-6): ")) - 1
            extra_turn = game.make_move(player_2_move)
            game.display_board()

            while extra_turn and not game.is_game_over():
                print(">>> Player 2's Extra Turn")
                player_2_move = int(input("Enter your move (1-6): ")) - 1
                extra_turn = game.make_move(player_2_move)
                game.display_board()

        elif mode == 3:  # Computer vs Computer
            print(">>> Computer 1's Turn")
            player_1_move = game.best_move(depth, maximizingPlayer=True)
            print(f"Computer 1 (Perfect Move): Pit {player_1_move + 1}")
            extra_turn = game.make_move(player_1_move)
            game.display_board()

            while extra_turn and not game.is_game_over():
                print(">>> Computer 1's Extra Turn")
                player_1_move = game.best_move(depth, maximizingPlayer=True)
                print(f"Computer 1 (Extra Turn): Pit {player_1_move + 1}")
                extra_turn = game.make_move(player_1_move)
                game.display_board()

            if game.is_game_over():
                break

            print(">>> Computer 2's Turn")
            player_2_move = game.best_move(depth, maximizingPlayer=False)
            print(f"Computer 2 (Perfect Move): Pit {player_2_move + 1}")
            extra_turn = game.make_move(player_2_move)
            game.display_board()

            while extra_turn and not game.is_game_over():
                print(">>> Computer 2's Extra Turn")
                player_2_move = game.best_move(depth, maximizingPlayer=False)
                print(f"Computer 2 (Extra Turn): Pit {player_2_move + 1}")
                extra_turn = game.make_move(player_2_move)
                game.display_board()

        elif mode == 4:  # Player vs Player
            print(">>> Player 1's Turn")
            player_1_move = int(input("Player 1, enter your move (1-6): ")) - 1
            extra_turn = game.make_move(player_1_move)
            game.display_board()

            while extra_turn and not game.is_game_over():
                print(">>> Player 1's Extra Turn")
                player_1_move = int(input("Player 1, enter your move (1-6): ")) - 1
                extra_turn = game.make_move(player_1_move)
                game.display_board()

            if game.is_game_over():
                break

            print(">>> Player 2's Turn")
            player_2_move = int(input("Player 2, enter your move (1-6): ")) - 1
            extra_turn = game.make_move(player_2_move)
            game.display_board()

            while extra_turn and not game.is_game_over():
                print(">>> Player 2's Extra Turn")
                player_2_move = int(input("Player 2, enter your move (1-6): ")) - 1
                extra_turn = game.make_move(player_2_move)
                game.display_board()

    # Game over: collect remaining stones and determine winner
    game.collect_remaining_stones()
    game.display_board()
    print("********************************* Game  End  *********************************")
    print(game.determine_winner())

def main():
    mode, level, random_mode = choose_mode_and_level()
    play_game(mode, level, random_mode)
