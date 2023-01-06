import os


def actual_size(block: list[list[int]]) -> tuple[int, int]:
    """
    Returns the actual size of a given block rather than the size of the matrix it's stored in.
    For example, a 2x1 block stored in a 3x3 matrix (e.g. Triangle's Horizontal Small I).
    
    :param block: The block to get the size of.
    :returns: The actual size of the specified block.
	"""
    width = 0
    # Since a block starts from the bottom, 
    # we deduce the actual height from the first row in which there's a square (so technically, the value 1) 
    start = -1
    for i in range(len(block)):
        row = block[i]
        # This represents the actual width in the current row
        w = 0
        for j in range(len(row)):
            val = row[j]
            if val == 1:
                # If we find a 1 at index j, then the currently presumed width is j + 1, since array indexes start at 0. 
                 w = j + 1
                 if start == -1: 
                      # If this is the first 1 we find, the current row is the top row of the actual block.
                      start = i
            # If the actual width of the current row is the biggest we have found so far,
            # it becomes the presumed width of the block 
            if w > width:
                 width = w
    height = len(block) - start
    return (width, height)

def truncate_block(block: list[list[int]]) -> list[list[int]]:
    """
    Returns the 2d matrix of a block in its actual size rather than the size it's stored in.
    :param block: The block to truncate.
    :returns: The truncated block.
    """
    (x,y) = actual_size(block)
    start = len(block) - y
    truncated = []
    for i in range(start, len(block)):
        truncated.append([])
        row = block[i]
        for j in range(x):
            truncated[-1].append(row[j])
    return truncated

def block_value(block: list[list[int]]) -> int:
    val = 0
    for line in block:
        for i in line: 
            if i == 1:
                val+=2
    return val

def valid_position(grid: list[list[int]], block: list[list[int]], i: int, j: int) -> bool: 
    """
    Checks whether the block `block` can be placed on the slot of coordinates (i,j) on the grid `grid`.
    
    :param grid: The grid in use.
    :param block: The block which is being attempted to place.
    :param i: The x coordinate of the block on the grid.
    :param j: The y coordinate of the block on the grid (from the bottom of the block).
    :returns: Whether the block can be placed on the grid at (i,j).
    """
    truncated = truncate_block(block)
    # (x size, y size)
    block_size = (len(truncated[0]), len(truncated))
    # First of all we check if the block can be contained in the grid at this position,
    # only depending on the size of the whole grid and the block.
    if (i + block_size[0] > len(grid[0])
        or j > len(grid)
        or i  < 0
        or j - block_size[1] + 1 < 0):
        return False

    for k in range(block_size[1]):
        # j references the bottom of the block, while y is going from top to bottom.
        # Hence we must substrct the size of the block to compare squares at the correct y position.
        y = j - block_size[1] + 1 + k
        for l in range(block_size[0]):
            x = i + l
            # If the grid square is not a placeable square (0) or an already used square (1),
            # and the block has a square to place in the same position, we deduce that we can't
            # place this block on the grid at the given position. Therefore, we return False.
            if grid[y][x] in [0, 2] and truncated[k][l]:
                return False
    # If we didn't return False earlier, the block can be placed. 
    return True

def place_block(grid: list[list[int]], block: list[list[int]], i: int, j: int) -> bool: 
    """
    Places a block in the grid. (Modifies the given matrix in-place)

    :param grid: The grid in which the place is placed.
    :param block: The block to place.
    :param i: The x coordinate of the block on the grid.
    :param j: The y coordinate of the block on the grid (from the bottom of the block).
    :returns: Whether the block was successfully placed.
    """
    if not valid_position(grid, block, i, j):
        return False
    truncated = truncate_block(block)
    block_size = (len(truncated[0]), len(truncated))
    # Here We use the same loop strategy as in `valid_position`.
    for k in range(block_size[1]):
        y = j - block_size[1] + 1 + k
        for l in range(block_size[0]):
            x = i + l
            if truncated[k][l] == 1:
                grid[y][x] = 2
    return True

def row_state(grid: list[list[int]], i: int) -> bool:
    """
    Verifies if the row `i` in the grid `grid` is full.

    :param grid: The grid to use.
    :param i: The index of the row to verify.
    :returns: Whether the row is full.
    """
    return 1 not in grid[i]

def col_state(grid: list[list[int]], i: int) -> bool:
    """
    Verifies if the column `i` in the grid `grid` is full.
    
    :param grid: The grid to use.
    :param i: The index of the column to verify.
    :returns: Whether the column is full.
    """
    for row in grid:
        if row[i] == 1:
            return False
    return True

def clear_col(grid: list[list[int]], i: int) -> int:
    """
    Clears the `i` column in the `grid`. Modifies the provided grid **in-place**.
    
    :param grid: The grid to use.
    :param i: The index of the column to clear.
    :returns: How many cells were cleared.
    """
    cleared = 0
    for j in range(len(grid)):
       if grid[j][i] == 2:
            cleared+=1
            grid[j][i] = 1
    return cleared

def clear_row(grid: list[list[int]], i: int) -> int:
    """
    Clears the `i` row in the `grid` and makes the remaining rows fall down. Modifies the provided grid **in-place**.
    :param grid: The grid to use.
    :param i: The index of the row to clear.
    :returns: How many cells were cleared.
    """
    # We first count how many cells are to be cleared.    
    cleared = 0
    for j in range(len(grid[i])):
        if grid[i][j] == 2:
            cleared += 1
    # This loop goes from the row to clear to the top of the grid and replaces each row with the one above it.
    # We don't need to explicitly clear the `i` row because it will be overwritten by the row above it.
    for j in range(i, 0, -1):
        for k in range(len(grid[j])):
            if grid[j][k] in [1, 2]:
                # When moving a row down, we make sure not to overwrite a non-playable square (0) with a playable square (1).
                # In the same way, we don't overwrite a playable square (1) with a non-playable square (0).
                if grid[j-1][k] == 0 and grid[j][k] != 0:
                    grid[j][k] = 1
                else:
                    grid[j][k] = grid[j-1][k]
    # Finally, we clear the top row, respecting the shape of the board.
    for j in range(len(grid[0])):
        if grid[0][j] != 0:
            grid[0][j] = 1
    return cleared

def fetch_save() -> tuple[int, int, str, list[list[int]]] | bool:
    '''
    Fetches data from the save file, if it exists.
    :returns: A tutple containing the following saved data:
        - int: The score of the game.
        - int: The difficulty of the game.
        - str: The type of board.
        - list[list[int]]: The state of the board.
        Or a boolean: False if the file just doesn't exist, True if it was corrupted.
    '''
    if not os.path.exists('~SAVE'):
        return False
    with open('~SAVE', 'r') as f:
        # The first two lines contain the score and the difficulty.
        for i in range(2):
            try:
                if i == 0:
                    score = int(f.readline())
                else:
                    difficulty = int(f.readline())
            except:
                # If this fails, somehow the save file has been corrupted and we have no choice but to delete it.
                os.remove('~SAVE')
                return True
        board_type = f.readline().strip()
        if board_type not in ['CIRCLE','DIAMOND', 'TRIANGLE']:
            os.remove('~SAVE')
            return True
        board = []
        previous_len = None
        for line in f.readlines():
            # All the lines must have the same length, or something went wrong in the save file.
            if previous_len != None and previous_len != len(line):
                os.remove('~SAVE')
                return True
            previous_len = len(line)
            board.append([])
            for c in line.strip():
                # Every character must be 0, 1 or 2. 
                # If we can't convert it into an integer, or if its value is not between 0 and 2, something went wrong.
                try:
                    i = int(c)
                except:
                    i = -1
                if not 0 <= i <= 2:
                    os.remove('~SAVE')
                    return True
                board[-1].append(i)
    return (score, difficulty, board_type, board)


def save_game(score:int , difficulty: int, board_type: str, board: list[list[int]]) -> None:
    '''
    Saves the game in the `~SAVE` file.
    :param score: The score of the game.
    :param difficulty: The difficulty of the game.
    :param board_type: The type of board used.
    :param board: The state of the board.
    '''
    with open('~SAVE', 'w') as f:
        f.write(f'{score}\n')
        f.write(f'{difficulty}\n')
        f.write(f'{board_type}\n')
        for line in board:
            converted = [str(i) for i in line]
            f.write(''.join(converted) + '\n')