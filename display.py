import os


def clear_screen():
    '''
    Clears the terminal.
    '''
    if os.name == 'nt': # For Windows systems
        os.system('cls')
    else: # For macOS / Linux systems
        os.system('echo -e \\\\\033c')

def yesno_question(question: str) -> bool:
    '''
    Asks a yes/no question to the user.
    :returns: The answer of the user. (True for yes, False for no)
    '''
    x = ''
    while (x not in ['y', 'n', 'yes', 'no']):
        x = input(f'{question} [y/n]: ').lower()
    return x.startswith('y')

def ask_position(board: list[list[int]]) -> tuple[int]:
    '''
    Asks the user where they want to place a block.

    :param board: The board being used in the game. This allows the function to check whether the coordinates provided
    by the user are out of bound.
    :returns: The coordinates given by the user.
    '''
    x = y = -1
    while x < 0 or y < 0 or x > len(board[0]) or y > len(board):
        position = input('Where do you want to place it ? ')
        if position.lower() in ['exit', 'quit','stop']:
            return -1, -1
        if len(position) != 2: 
            continue
        # Coordinates must be input like so: <xCoordinate><yCoordinate>
        # The x coordinate being a lowercase letter and the y coordinate an uppercase letter.
        x = ord(position[0]) - 97
        y = ord(position[1]) - 65
    return x, y

def menu(options: list[str]) -> int:
    '''
    Lets the user choose among several options.

    :param options: The options presented to the user.
    :returns: An integer representing the option chosen by the user. **(starts at 1)**
    '''
    LENGTH = 28
    print('╔' + '═'*LENGTH + '╗')
    for i in range(len(options)):
        opt = options[i]
        # The -3 accounts for the length of the prefixing number.
        space_len = (LENGTH - len(opt) - 3)//2
        # In case the length of this line is odd, we make sure to keep the border aligned.
        r = (LENGTH - len(opt) - 3) % 2
        print('║' + ' '*space_len + str(i + 1) +'. ' + opt + ' '*(space_len + r) + '║')
    print('╚' + '═'*LENGTH + '╝')
    choice = -1
    while (choice < 1 or choice > len(options)):
        # The input might not be convertible into an int. Hence, we use a try-except block to avoid any crash.
        try:
            choice = int(input('Choice [1-' + str(len(options)) + ']: '))
        except:
            pass
    return choice

def display_board(board: list[list[int]], test=False) -> None:
    '''
    Displays a board in a readable format, with helpful side marks.

    :param board: The board to display.
    :param name: The name of the board.
    :param name: The name of the board. Only used when `test` is `True`.
    '''
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    top_letters = [alphabet[i].lower() for i in range(len(board[0]))]
    chars = [' ', '□', '■']
    print('  ' + ' '.join(top_letters))
    for i in range(len(board)):
        print(alphabet[i], end=' ')
        row = [ chars[x] for x in board[i] ]
        print(' '.join(row) + (f' {i}' if test else ''))

    if test:
        # We use modulo to avoid double digit numbers which would unalign the indexes.
        bottom_numbers = [str(i % 10) for i in range(len(board[0]))]
        print('  ' + ' '.join(bottom_numbers))

def display_blocks(blocks: list[list[list[int]]]) -> None:
    '''
    Displays a list of blocks on the terminal.

    :param blocks: The set of blocks to showcase.
    '''
    size = (len(blocks[0][0]), len(blocks[0]))
    line = '╦'.join(['═' * (size[0] * 2 + 1) for _ in blocks])
    print('╔' + line + '╗')
    
    for i in range(len(blocks[0])):
            print('║ ', end='')
            for j in range(len(blocks)):
                chars = ['□','■']
                row = [ chars[x] for x in blocks[j][i]]
                print(' '.join(row), end='')
                print(' ║ ', end='')
            print()
    line = '╩'.join(['═' * (size[0] * 2 + 1) for _ in blocks])
    print('╚' + line + '╝')