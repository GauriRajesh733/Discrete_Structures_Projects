import random

# play_random_move: computer removes random number of squares from random row (XOR sum already 0)
def play_random_move(piles):
    print("playing random move!")
    valid_move = False
    while not valid_move:
        row = random.randint(0, (len(piles) - 1))
        if piles[row] > 0:
            num_squares = random.randint(1, piles[row])
            valid_move = True
    
    print(f"computer is removing {num_squares} from row {row}")
    piles[row] = piles[row] - num_squares
    draw_game(piles)
    return piles

# calculate_xor_sum: performs XOR-sum of each binary digit across remaining number of squares in each pile 
def calculate_xor_sum(piles):
    xor_sum = 0
    for pile in piles:
        xor_sum ^= pile
    return xor_sum

# draw_game: draws square game given remaining number of squares in each pile
def draw_game(piles):
    largest_pile = len(bin(max(piles))[2:])
    for pile in piles:
        bin_squares_in_row = bin(pile)[2:]
        whitespace = largest_pile - len(bin_squares_in_row) + 3
        print(bin_squares_in_row, end = " " * whitespace)
        for i in range(pile):
            print("▢", end = " ")
        print()

# user_turn: prompts user to input row and number of squares they would like to remove (first row is represented by 0)
def user_turn(piles):
    draw_game(piles)
    print("------------------------------")
    valid_move = False
    while not valid_move:
        print("Select a row: ")
        row = int(input())
        if row < 0 or row > len(piles) - 1:
            print("Please enter a valid row!")
        else:
            print("Enter how many squares you would like to remove: ")
            num_squares = int(input())
            if num_squares <= 0 or num_squares > piles[row]:
                print("Please enter a valid number of squares to remove: ")
            else:
                valid_move = True
                piles[row] = piles[row] - num_squares
    
    print(f"player is removing {num_squares} from row {row}")
    draw_game(piles)
    print("------------------------------")
    return piles

# computer_turn: if xor_sum is not 0, then computer plays optimally; otherwise, removes random number of squares from random row
def computer_turn(piles):
    xor_sum = calculate_xor_sum(piles)
    row = 0
    num_squares = 0
    if xor_sum == 0:
        return play_random_move(piles)
    for i in range(len(piles)):
        target = piles[i] ^ xor_sum
        if target <= piles[i]:
            print(f"computer is removing {piles[i] - target} from row {i}")
            piles[i] = target
            return piles
    return play_random_move(piles)
        
# game_over: if all piles are empty, returns True because game is over
def game_over(piles):
    return all(pile == 0 for pile in piles)

# play_game: creates square game with number of rows given by user and 1-10 squares per row
def play_game():
    '''
    print("Enter number of rows: ")
    num_rows = int(input())
    print("Enter maximum number of squares per row: ")
    max_squares = int(input())
    piles = []
    
    for i in range (num_rows):
        piles.append(random.randint(1, max_squares))
    '''
    piles = [5,5,2,5,5]
    print("Would you like to play first or last?  Enter 1 to play first or 2 to play second.")
    user_play_order = int(input())
    while not game_over(piles):
        if (user_play_order == 1):
            piles = user_turn(piles)
            if game_over(piles):
                print("GAME OVER!  USER WON!")
                break
            piles = computer_turn(piles)
            if game_over(piles):
                print("GAME OVER!  COMPUTER WON!")
                break
        else:
            current_player = "Computer"
            piles = computer_turn(piles)
            if game_over(piles):
                print("GAME OVER!  COMPUTER WON!")
                break
            current_player = "User"
            piles = user_turn(piles)
            if game_over(piles):
                print("GAME OVER!  USER WON!")
                break

# run play_game          
play_game()