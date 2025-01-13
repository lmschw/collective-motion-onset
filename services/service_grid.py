import math
import numpy as np

def is_first_column(cell_idx, grid_size):
    return cell_idx < grid_size[0]

def is_last_column(cell_idx, grid_size):
    return cell_idx >= (grid_size[0] * (grid_size[1]-1))

def is_top_row(cell_idx, grid_size):
    return cell_idx % grid_size[0] == 0

def is_bottom_row(cell_idx, grid_size):
    return cell_idx % grid_size[0] == (grid_size[0]-1)

def get_adjacent_cross_cells_distance_one(cell_idx, grid_size):
    x, y = get_x_y_for_cell_idx(cell_idx=cell_idx, grid_size=grid_size)
    top_x = (x-1) % grid_size[0]
    bottom_x = (x+1) % grid_size[0]
    left_y = (y-1) % grid_size[1]
    right_y = (y+1) % grid_size[1]

    top = get_grid_cell_idx(x=top_x, y=y, grid_size=grid_size)
    right = get_grid_cell_idx(x=x, y=right_y, grid_size=grid_size)
    bottom = get_grid_cell_idx(x=bottom_x, y=y, grid_size=grid_size)
    left = get_grid_cell_idx(x=x, y=left_y, grid_size=grid_size)

    return [top, right, bottom, left]

def get_adjacent_cross_cells_distance_two(cell_idx, grid_size):
    top, right, bottom, left = get_adjacent_cross_cells_distance_one(cell_idx=cell_idx, grid_size=grid_size)

    x, y = get_x_y_for_cell_idx(cell_idx=cell_idx, grid_size=grid_size)
    top_two_x = (x-2) % grid_size[0]
    bottom_two_x = (x+2) % grid_size[0]
    left_two_y = (y-2) % grid_size[1]
    right_two_y = (y+2) % grid_size[1]

    top_two = get_grid_cell_idx(x=top_two_x, y=y, grid_size=grid_size)
    right_two = get_grid_cell_idx(x=x, y=right_two_y, grid_size=grid_size)
    bottom_two = get_grid_cell_idx(x=bottom_two_x, y=y, grid_size=grid_size)
    left_two = get_grid_cell_idx(x=x, y=left_two_y, grid_size=grid_size)

    return top, right, bottom, left, top_two, right_two, bottom_two, left_two

def get_adjacent_square_cells_eight(cell_idx, grid_size):
    top, right, bottom, left = get_adjacent_cross_cells_distance_one(cell_idx=cell_idx, grid_size=grid_size)
    x, y = get_x_y_for_cell_idx(cell_idx=cell_idx, grid_size=grid_size)
    top_x = (x-1) % grid_size[0]
    bottom_x = (x+1) % grid_size[0]
    left_y = (y-1) % grid_size[1]
    right_y = (y+1) % grid_size[1]

    top_right = get_grid_cell_idx(x=top_x, y=right_y, grid_size=grid_size)
    bottom_right = get_grid_cell_idx(x=bottom_x, y=right_y, grid_size=grid_size)
    bottom_left = get_grid_cell_idx(x=bottom_x, y=left_y, grid_size=grid_size)
    top_left = get_grid_cell_idx(x=top_x, y=left_y, grid_size=grid_size)

    return [top, top_right, right, bottom_right, bottom, bottom_left, left, top_left]

def get_adjacent_square_cells_twenty_four(cell_idx, grid_size):
    """
    t1          t2          t3          t4              t5
    l1          top_left    top         top_right       r1
    l2          left        cell_idx    right           r2
    l3          bottom_left bottom      bottom_right    r3
    b1          b2          b3          b4              b5        
    """
    top, top_right, right, bottom_right, bottom, bottom_left, left, top_left = get_adjacent_square_cells_eight(cell_idx=cell_idx, grid_size=grid_size)
    
    x, y = get_x_y_for_cell_idx(cell_idx=cell_idx, grid_size=grid_size)
    top_two_x = (x-2) % grid_size[0]
    top_one_x = (x-1) % grid_size[0]
    bottom_one_x = (x+1) % grid_size[0]
    bottom_two_x = (x+2) % grid_size[0]
    left_two_y = (y-2) % grid_size[1]
    left_one_y = (y-1) % grid_size[1]
    right_one_y = (y+1) % grid_size[1]
    right_two_y = (y+2) % grid_size[1]

    t1 = get_grid_cell_idx(x=top_two_x, y=left_two_y, grid_size=grid_size)
    t2 = get_grid_cell_idx(x=top_two_x, y=left_one_y, grid_size=grid_size)
    t3 = get_grid_cell_idx(x=top_two_x, y=y, grid_size=grid_size)
    t4 = get_grid_cell_idx(x=top_two_x, y=right_one_y, grid_size=grid_size)
    t5 = get_grid_cell_idx(x=top_two_x, y=right_two_y, grid_size=grid_size)
    r1 = get_grid_cell_idx(x=top_one_x, y=right_two_y, grid_size=grid_size)
    r2 = get_grid_cell_idx(x=x, y=right_two_y, grid_size=grid_size)
    r3 = get_grid_cell_idx(x=bottom_one_x, y=right_two_y, grid_size=grid_size)
    b1 = get_grid_cell_idx(x=bottom_two_x, y=left_two_y, grid_size=grid_size)
    b2 = get_grid_cell_idx(x=bottom_two_x, y=left_one_y, grid_size=grid_size)
    b3 = get_grid_cell_idx(x=bottom_two_x, y=y, grid_size=grid_size)
    b4 = get_grid_cell_idx(x=bottom_two_x, y=right_one_y, grid_size=grid_size)
    b5 = get_grid_cell_idx(x=bottom_two_x, y=right_two_y, grid_size=grid_size)
    l1 = get_grid_cell_idx(x=top_one_x, y=left_two_y, grid_size=grid_size)
    l2 = get_grid_cell_idx(x=x, y=left_two_y, grid_size=grid_size)
    l3 = get_grid_cell_idx(x=bottom_one_x, y=left_two_y, grid_size=grid_size)

    return [top, top_right, right, bottom_right, bottom, bottom_left, left, top_left, t1, t2, t3, t4, t5, r1, r2, r3, b5, b4, b3, b2, b1, l3, l2, l1]

def get_grid_cell_idx(x, y, grid_size):
    return y * grid_size[0] + x

def get_x_y_for_cell_idx(cell_idx, grid_size):
    return cell_idx % grid_size[0], int(cell_idx / grid_size[0])

def get_grid_string(grid, grid_size, num_predators):
    output = "".join([f"\t{i}" for i in range(grid_size[1])])
    print(line)
    for x in range(grid_size[0]):
        line = f"{x}"
        for y in range(grid_size[1]):
            cell_idx = get_grid_cell_idx(x=x, y=y, grid_size=grid_size)
            cell = np.array(grid[cell_idx])
            preys = cell[cell >= num_predators]

            cell_idx = get_grid_cell_idx(x=x, y=y, grid_size=grid_size)
            cell = np.array(grid[cell_idx])
            predators = cell[cell < num_predators]
            
            prey_string = "".join([f"P{i}" for i in preys])
            predator_string = "".join([f"H{i}" for i in predators])
            line += f"\t{predator_string}{prey_string}"
        output += f"\n{line}"
    return output