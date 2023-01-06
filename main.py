import os
import random
import shutil
from copy import deepcopy

from constants.blocks import *
from constants.boards import *
from display import *
from game import *

print('\n')
(width, height) = shutil.get_terminal_size()
if (width < 100 or height < 30):
    try:
        if os.name == 'nt':
            os.system('mode con: cols=100 lines=40')
        else:
            os.system('printf \'\\e[8;40;100t\'')
    except:
        print('It is recommended to play Efreitris in a 100x40 (at least) terminal for the best experience.')

allow_clear = yesno_question('Do you allow efreitris to clear your terminal for a better playing experience?')

def tutorial():
    '''
    Displays a short tutorial of the game.
    '''
    if allow_clear:
        clear_screen()
    print('╔══════════════════════════════════════════════════════════════════╗')
    print('║   Efreitris is a Tetris-like game. Your job is to fill a board   ║')
    print('║  with blocks to clear lines and columns and earn the most points ║')
    print('║   that you can! But place your blocks wisely.. If you fill the   ║')
    print('║      board so much that you cannot place anymore, you lose.      ║')
    print('╚══════════════════════════════════════════════════════════════════╝')
    input('-- Press ENTER to continue --')
    print('╔══════════════════════════════════════════════════════════════════╗')
    print('║   For each game, you can choose between three different boards:  ║')
    print('║     Circle, Diamond and Triangle. They all come in 3 sizes!      ║')
    print('║  They all have their own blocks, in addition to the common ones. ║')
    print('║                       Let\'s look at them!                        ║')
    print('╚══════════════════════════════════════════════════════════════════╝')
    input('-- Press ENTER to continue --')
    print('Here is the CIRCLE board:\n')
    display_board(SMALL_CIRCLE_BOARD)
    input('\n-- Press ENTER to continue --')
    print('Now, the DIAMOND board:\n')
    display_board(SMALL_DIAMOND_BOARD)
    input('\n-- Press ENTER to continue --')
    print('And finally, the TRIANGLE board:\n')
    display_board(SMALL_TRIANGLE_BOARD)
    input('\n-- Press ENTER to continue --')
    print('╔══════════════════════════════════════════════════════════════════╗')
    print('║        At every turn, you will choose between three blocks       ║')
    print('║               (or five if you play in easy mode.)                ║')
    print('║      Then, you will have to carefully place the chosen one.      ║')
    print('║                     Let\'s see how to do this!                    ║')
    print('╚══════════════════════════════════════════════════════════════════╝')
    input('-- Press ENTER to continue --\n')
    example_board = deepcopy(SMALL_DIAMOND_BOARD)
    display_board(example_board)
    display_blocks(COMMON_BLOCKS[:1])
    print('╔══════════════════════════════════════════════════════════════════╗')
    print('║     For example here, I\'m playing on the Small Diamond Board     ║')
    print('║                and want to place this small block.               ║')
    print('║    When placing a block, you are asked the COORDINATES of where  ║')
    print('║  you want to place it. These coordinates are represented like so ║')
    print('║            "xY" (e.g. gG for the center of this board)           ║')
    print('║   One important thing to remember is that a block\'s origin is    ║')
    print('║     its BOTTOM LEFT corner. So, if I want to place my block      ║')
    print('║      at top of the board, I should enter the gc coordinates      ║')
    print('║                       Here is the result:                        ║')
    print('╚══════════════════════════════════════════════════════════════════╝')
    input('-- Press ENTER to continue --\n')
    place_block(example_board, COMMON_BLOCKS[0], 6, 2)
    display_board(example_board)
    input('-- Press ENTER to continue --')
    print('╔══════════════════════════════════════════════════════════════════╗')
    print('║                                                                  ║')
    print('║              Well, you know everything you need now.             ║')
    print('║                     Good luck and have fun!                      ║')
    print('║                                                                  ║')
    print('╚══════════════════════════════════════════════════════════════════╝')
    input('-- Press ENTER to play! --')

def play(saved: tuple[int, int, list[list[int]]] = None):
    '''
    Handles all the logic of one game:
        1. Options selection
        2. Game loop
        3. End of game screen
    :param saved: The content of the save, if there was one.
    '''
    if allow_clear:
        clear_screen()
    if saved:
        difficulty = saved[1]
        board_type = saved[2]
        board = saved[3]
    else:
        # 1. Options selection
        print('On what board do you want to play?')
        i = menu(['Circle', 'Diamond', 'Triangle'])
        board_type = ['CIRCLE','DIAMOND', 'TRIANGLE'][i - 1]
        print('What size of board do you want to use?')
        i = menu(['Small', 'Medium', 'Large'])
        size_choice = ['SMALL', 'MEDIUM', 'LARGE'][i - 1]
        board = deepcopy(globals()[f'{size_choice}_{board_type}_BOARD'])
        print('What difficulty do you want to play?')
        difficulty = menu(['Easy', 'Normal'])

    # 2. Game loop
    blocks = COMMON_BLOCKS
    if difficulty == 1:
        blocks += globals()[f'{board_type}_BLOCKS']
    playing = True
    lost = False
    score = saved[0] if saved else 0
    while playing:
        if allow_clear:
            clear_screen()
        score_str = f' Score: {score} '
        print('-'*len(score_str))
        print(score_str)
        print('-'*len(score_str))

        display_board(board)

        available_blocks = [random.choice(blocks) for _ in range(10 if difficulty == 1 else 5)]
        for i in range(0, len(available_blocks), 5):
            display_blocks(available_blocks[i:i+5])
        i = -1
        while playing and (i < 0 or i >= len(available_blocks)):
            try:
                val = input(f'What block do you want to place? [1-{len(available_blocks)}]: ').lower()
                if val in ['exit', 'quit', 'stop']:
                    playing = False
                else:
                    i = int(val) - 1
            except:
                i = -1
        if playing:
            block = available_blocks[i]
            x,y = ask_position(board)
            if x == -1:
                playing = False
        attempts = 2
        while playing and not valid_position(board, block, x, y) and attempts > 0:
            print(f'You can\'t place this block here! ({attempts} attempt{"s" if attempts > 1 else ""} remaning)')
            x,y = ask_position(board)
            attempts -= 1
        if attempts == 0:
            playing = False
            lost = True
        elif playing:
            place_block(board, block, x, y)
            score += block_value(block)
            col_score = 0
            cleared_cols_count = 0
            row_score = 0
            cleared_rows_count = 0
            for i in range(len(board)):
                if row_state(board, i):
                    row_score += clear_row(board, i) * 3
                    cleared_rows_count += 1
            for j in range(len(board[0])):
                if col_state(board, j):
                    col_score += clear_col(board, j) * 3
                    cleared_cols_count += 1
            total = col_score * cleared_cols_count + row_score + cleared_rows_count
            if cleared_cols_count != 0 and cleared_rows_count != 0:
                total*= min(cleared_cols_count, cleared_rows_count) * 2
            score += total
    # 3. End of game screen (either loss or exit)
    if lost:
        if allow_clear:
            clear_screen()
            display_board(board)
        print(f'\nYou lost! Well played though, you earned {score} points!')
        input('--Press ENTER to go back to the main menu--')
    elif yesno_question('Do you want to save the game?'):
            save_game(score, difficulty, board_type, board)
main_menu_choice = 0
while main_menu_choice != 3:
    saved = fetch_save()
    if allow_clear:
        clear_screen()
    print('███████╗███████╗██████╗ ███████╗██╗████████╗██████╗ ██╗███████╗')
    print('██╔════╝██╔════╝██╔══██╗██╔════╝██║╚══██╔══╝██╔══██╗██║██╔════╝')
    print('█████╗  █████╗  ██████╔╝█████╗  ██║   ██║   ██████╔╝██║███████╗')
    print('██╔══╝  ██╔══╝  ██╔══██╗██╔══╝  ██║   ██║   ██╔══██╗██║╚════██║')
    print('███████╗██║     ██║  ██║███████╗██║   ██║   ██║  ██║██║███████║')
    print('╚══════╝╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚══════╝')
    if saved == True:
        print('We\'re sorry, your save file was corrupted and the progress of your previous game has been lost.')
        saved = None
    main_menu_choice = menu(['Play', 'Tutorial', 'Quit'])
    match main_menu_choice:
        case 1:
            if saved and yesno_question('Do you want to resume the saved game? If not, the save will be erased!'):
                play(saved)
            else:
                if os.path.exists('~SAVE'): os.remove('~SAVE')
                play()
        case 2:
            tutorial()

if allow_clear:
    clear_screen()