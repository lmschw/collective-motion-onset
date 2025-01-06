import math

def is_first_column(cell_idx, grid_size):
    return cell_idx < grid_size[0]

def is_last_column(cell_idx, grid_size):
    return cell_idx >= (grid_size[0] * (grid_size[1]-1))

def is_top_row(cell_idx, grid_size):
    return cell_idx % grid_size[0] == 0

def is_bottom_row(cell_idx, grid_size):
    return cell_idx % grid_size[0] == (grid_size[0]-1)


def get_adjacent_cross_cells_distance_one(cell_idx, grid_size):
    # top is one less unless the cell is in the top row. Otherwise, it is the bottom of the same column 
    if is_top_row(cell_idx=cell_idx, grid_size=grid_size):
        top = cell_idx + grid_size[0] - 1
    else:
        top = cell_idx - 1

    # bottom is one more than the current cell unless the cell is in the bottom row. In that case, it is the top of the same column
    if is_bottom_row(cell_idx=cell_idx, grid_size=grid_size):
        bottom = cell_idx % grid_size[0] - grid_size[0] + 1 + (math.floor(cell_idx / grid_size[0]) * grid_size[0])
    else:
        bottom = cell_idx + 1

    # left is one whole column less than the current index except when we are in the first column. Then it is the equivalent in the last column
    if is_first_column(cell_idx=cell_idx, grid_size=grid_size):
        left = cell_idx + (grid_size[0] * (grid_size[1]-1))
    else:
        left = cell_idx - grid_size[0]
    
    # right is one whole colum more than the current index except when we are in the last column. THen it is the equivalent in the first column
    if is_last_column(cell_idx=cell_idx, grid_size=grid_size):
        right = cell_idx % grid_size[0]
    else:
        right = cell_idx + grid_size[0]

    return [top, right, bottom, left]

def get_adjacent_square_cells_eight(cell_idx, grid_size):
    top, right, bottom, left = get_adjacent_cross_cells_distance_one(cell_idx=cell_idx, grid_size=grid_size)
    is_top = is_top_row(cell_idx=cell_idx, grid_size=grid_size)
    is_bottom = is_bottom_row(cell_idx=cell_idx, grid_size=grid_size)
    is_first = is_first_column(cell_idx=cell_idx, grid_size=grid_size)
    is_last = is_last_column(cell_idx=cell_idx, grid_size=grid_size)
    # top right for the top right corner is the bottom left corner
    if is_top and is_last:
        top_right = grid_size[0] - 1
    # top right for the top row is the last cell on the next column
    elif is_top:
        top_right = cell_idx + (2 * grid_size[0]) - 1
    # top right for the last column is the first cell in the row above
    elif is_last:
        top_right = cell_idx % grid_size[0] - 1
    # for all others
    else:
        top_right = cell_idx + grid_size[0] - 1

    # bottom right for the bottom right corner is the top left cell
    if is_bottom and is_last:
        bottom_right = 0
    # bottom right for the bottom row is the top cell in the next column, so the next cell
    elif is_bottom:
        bottom_right = cell_idx + 1
    # bottom right for the last column is the corresponding cell in the first column + 1
    elif is_last:
        bottom_right = (cell_idx % grid_size[0]) + 1
    else:
        bottom_right = cell_idx + grid_size[0] + 1

    # bottom left for the bottom left corner is the top right cell
    if is_bottom and is_first:
        bottom_left = grid_size[0] * (grid_size[1]-1)
    # bottom left for the bottom row is the first cell in the previous column
    elif is_bottom:
        bottom_left = cell_idx - 2*grid_size[0] + 1
    # bottom left or the first column is the cell on the next row in the last column
    elif is_first:
        bottom_left = grid_size[0] * (grid_size[1]-1) + (cell_idx % grid_size[0]) + 1
    else:
        bottom_left = cell_idx - grid_size[0] + 1

    # top left for the top left corner is the very last cell in the grid
    if is_top and is_first:
        top_left = (grid_size[0] * grid_size[1]) - 1
    # top left for the top row is the last cell in the previous column, i.e. the previous cell
    elif is_top:
        top_left = cell_idx - 1
    # top left for the first column is the cell in the previous row in the last column
    elif is_first:
        top_left = (grid_size[0] * (grid_size[1]-1)) + (cell_idx % grid_size[0]) - 1
    else:
        top_left = cell_idx - grid_size[0] -1

    return [top, top_right, right, bottom_right, bottom, bottom_left, left, top_left]