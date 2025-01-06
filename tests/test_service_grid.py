import services.service_grid as sgrid

def test_is_first_column():
    grid_size_square = (4,4)

    test_coordinates_square = [0, 3, 6, 9, 12, 13, 15]
    expected_square = [True, True, False, False, False, False, False]
    for i in range(len(test_coordinates_square)):
        assert sgrid.is_first_column(cell_idx=test_coordinates_square[i], grid_size=grid_size_square) == expected_square[i], f"Is first column fails for square with index {i}"


def test_is_last_column():
    grid_size_square = (4,4)
    grid_size_more_rows = (5,4)
    grid_size_more_columns = (4,5)

    test_coordinates_square = [0, 3, 6, 9, 12, 13, 15]
    expected_square = [False, False, False, False, True, True, True]
    for i in range(len(test_coordinates_square)):
        assert sgrid.is_last_column(cell_idx=test_coordinates_square[i], grid_size=grid_size_square) == expected_square[i], f"Is last column fails for square with index {i}"

    test_coordinates_more_rows = [0, 8, 14, 15, 17, 19]
    expected_more_rows = [False, False, False, True, True, True]
    for i in range(len(test_coordinates_more_rows)):
        assert sgrid.is_last_column(cell_idx=test_coordinates_more_rows[i], grid_size=grid_size_more_rows) == expected_more_rows[i], f"Is last column fails for more rows with index {i}"

    test_coordinates_more_cols = [0, 5, 8, 15, 16, 18, 19]
    expected_more_cols = [False, False, False, False, True, True, True]
    for i in range(len(test_coordinates_more_cols)):
        assert sgrid.is_last_column(cell_idx=test_coordinates_more_cols[i], grid_size=grid_size_more_columns) == expected_more_cols[i], f"Is last column fails for more rows with index {i}"

def test_is_top_row():
    grid_size_square = (4,4)
    grid_size_more_rows = (5,4)
    grid_size_more_columns = (4,5)

    test_coordinates_square = [0, 3, 6, 9, 12, 13, 15]
    expected_square = [True, False, False, False, True, False, False]
    for i in range(len(test_coordinates_square)):
        assert sgrid.is_top_row(cell_idx=test_coordinates_square[i], grid_size=grid_size_square) == expected_square[i], f"Is top row fails for square with index {i}"

    test_coordinates_more_rows = [0, 8, 14, 15, 17, 19]
    expected_more_rows = [True, False, False, True, False, False]
    for i in range(len(test_coordinates_more_rows)):
        assert sgrid.is_top_row(cell_idx=test_coordinates_more_rows[i], grid_size=grid_size_more_rows) == expected_more_rows[i], f"Is top row fails for more rows with index {i}"

    test_coordinates_more_cols = [0, 5, 8, 15, 16, 18, 19]
    expected_more_cols = [True, False, True, False, True, False, False]
    for i in range(len(test_coordinates_more_cols)):
        assert sgrid.is_top_row(cell_idx=test_coordinates_more_cols[i], grid_size=grid_size_more_columns) == expected_more_cols[i], f"Is top row fails for more rows with index {i}"

def test_is_bottom_row():
    grid_size_square = (4,4)
    grid_size_more_rows = (5,4)
    grid_size_more_columns = (4,5)

    test_coordinates_square = [0, 3, 6, 9, 11, 12, 13, 15]
    expected_square = [False, True, False, False, True, False, False, True]
    for i in range(len(test_coordinates_square)):
        assert sgrid.is_bottom_row(cell_idx=test_coordinates_square[i], grid_size=grid_size_square) == expected_square[i], f"Is bottom row fails for square with index {i}"

    test_coordinates_more_rows = [0, 8, 14, 15, 17, 19]
    expected_more_rows = [False, False, True, False, False, True]
    for i in range(len(test_coordinates_more_rows)):
        assert sgrid.is_bottom_row(cell_idx=test_coordinates_more_rows[i], grid_size=grid_size_more_rows) == expected_more_rows[i], f"Is bottom row fails for more rows with index {i}"

    test_coordinates_more_cols = [0, 3, 5, 7, 15, 16, 18, 19]
    expected_more_cols = [False, True, False, True, True, False, False, True]
    for i in range(len(test_coordinates_more_cols)):
        assert sgrid.is_bottom_row(cell_idx=test_coordinates_more_cols[i], grid_size=grid_size_more_columns) == expected_more_cols[i], f"Is bottom row fails for more rows with index {i}"

def test_get_adjacent_cross_cells_distance_one():
    grid_size_square = (4,4)
    grid_size_more_rows = (5,4)
    grid_size_more_columns = (4,5)

    test_coordinates_square = [0, 1, 3, 6, 9, 11, 12, 13, 15]
    expected_square = [[3, 4, 1, 12], 
                       [0, 5, 2, 13], 
                       [2, 7, 0, 15], 
                       [5, 10, 7, 2],
                       [8, 13, 10, 5],
                       [10, 15, 8, 7],
                       [15, 0, 13, 8],
                       [12, 1, 14, 9],
                       [14, 3, 12, 11]]
    for i in range(len(test_coordinates_square)):
        result = sgrid.get_adjacent_cross_cells_distance_one(cell_idx=test_coordinates_square[i], grid_size=grid_size_square)
        for j in range(4):
            assert result[j] == expected_square[i][j], f"get_adjacent_cross_cells_distance_one() fails for square with index {i} and {j} returning {result[j]} instead of {expected_square[i][j]}"

    test_coordinates_more_rows = [0, 2, 4, 5, 8, 11, 14, 15, 18, 19]
    expected_more_rows = [[4, 5, 1, 15],
                          [1, 7, 3, 17],
                          [3, 9, 0, 19],
                          [9, 10, 6, 0],
                          [7, 13, 9, 3],
                          [10, 16, 12, 6],
                          [13, 19, 10, 9],
                          [19, 0, 16, 10],
                          [17, 3, 19, 13],
                          [18, 4, 15, 14]]
    for i in range(len(test_coordinates_more_rows)):
        result = sgrid.get_adjacent_cross_cells_distance_one(cell_idx=test_coordinates_more_rows[i], grid_size=grid_size_more_rows)
        for j in range(4):
            assert result[j] == expected_more_rows[i][j], f"get_adjacent_cross_cells_distance_one() fails for more rows with index {i} and {j} returning {result[j]} instead of {expected_more_rows[i][j]}"

    test_coordinates_more_cols = [0, 1, 3, 6, 8, 11, 14, 16, 18, 19]
    expected_more_cols = [[3, 4, 1, 16],
                          [0, 5, 2, 17],
                          [2, 7, 0, 19],
                          [5, 10, 7, 2],
                          [11, 12, 9, 4],
                          [10, 15, 8, 7],
                          [13, 18, 15, 10],
                          [19, 0, 17, 12],
                          [17, 2, 19, 14],
                          [18, 3, 16, 15]]
    for i in range(len(test_coordinates_more_cols)):
        result = sgrid.get_adjacent_cross_cells_distance_one(cell_idx=test_coordinates_more_cols[i], grid_size=grid_size_more_columns)
        for j in range(4):
            assert result[j] == expected_more_cols[i][j], f"get_adjacent_cross_cells_distance_one() fails for more columns with index {i} and {j} returning {result[j]} instead of {expected_more_cols[i][j]}"

def test_get_adjacent_square_cells_eight():
    grid_size_square = (4,4)
    grid_size_more_rows = (5,4)
    grid_size_more_columns = (4,5)

    test_coordinates_square = [0, 1, 3, 6, 9, 11, 12, 13, 15]
    expected_square = [[3, 7, 4, 5, 1, 13, 12, 15], 
                       [0, 4, 5, 6, 2, 14, 13, 12], 
                       [2, 6, 7, 4, 0, 12, 15, 14], 
                       [5, 9, 10, 11, 7, 3, 2, 1],
                       [8, 12, 13, 14, 10, 6, 5, 4],
                       [10, 14, 15, 12, 8, 4, 7, 6],
                       [15, 3, 0, 1, 13, 9, 8, 11],
                       [12, 0, 1, 2, 14, 10, 9, 8],
                       [14, 2, 3, 0, 12, 8, 11, 10]]
    for i in range(len(test_coordinates_square)):
        result = sgrid.get_adjacent_square_cells_eight(cell_idx=test_coordinates_square[i], grid_size=grid_size_square)
        for j in range(len(expected_square[i])):
            assert result[j] == expected_square[i][j], f"get_adjacent_square_cells_eight() fails for square with index {i} and {j} returning {result[j]} instead of {expected_square[i][j]}"

    test_coordinates_more_rows = [0, 2, 4, 5, 8, 11, 14, 15, 18, 19]
    expected_more_rows = [[4, 9, 5, 6, 1, 16, 15, 19],
                          [1, 6, 7, 8, 3, 18, 17, 16],
                          [3, 8, 9, 5, 0, 15, 19, 18],
                          [9, 14, 10, 11, 6, 1, 0, 4],
                          [7, 12, 13, 14, 9, 4, 3, 2],
                          [10, 15, 16, 17, 12, 7, 6, 5],
                          [13, 18, 19, 15, 10, 5, 9, 8],
                          [19, 4, 0, 1, 16, 11, 10, 14],
                          [17, 2, 3, 4, 19, 14, 13, 12],
                          [18, 3, 4, 0, 15, 10, 14, 13]]
    for i in range(len(test_coordinates_more_rows)):
        result = sgrid.get_adjacent_square_cells_eight(cell_idx=test_coordinates_more_rows[i], grid_size=grid_size_more_rows)
        for j in range(len(expected_more_rows[i])):
            assert result[j] == expected_more_rows[i][j], f"get_adjacent_square_cells_eight() fails for more rows with index {i} and {j} returning {result[j]} instead of {expected_more_rows[i][j]}"

    test_coordinates_more_cols = [0, 1, 3, 6, 8, 11, 14, 16, 18, 19]
    expected_more_cols = [[3, 7, 4, 5, 1, 17, 16, 19],
                          [0, 4, 5, 6, 2, 18, 17, 16],
                          [2, 6, 7, 4, 0, 16, 19, 18],
                          [5, 9, 10, 11, 7, 3, 2, 1],
                          [11, 15, 12, 13, 9, 5, 4, 7],
                          [10, 14, 15, 12, 8, 4, 7, 6],
                          [13, 17, 18, 19, 15, 11, 10, 9],
                          [19, 3, 0, 1, 17, 13, 12, 15],
                          [17, 1, 2, 3, 19, 15, 14, 13],
                          [18, 2, 3, 0, 16, 12, 15, 14]]
    for i in range(len(test_coordinates_more_cols)):
        result = sgrid.get_adjacent_square_cells_eight(cell_idx=test_coordinates_more_cols[i], grid_size=grid_size_more_columns)
        for j in range(len(expected_more_cols[i])):
            assert result[j] == expected_more_cols[i][j], f"get_adjacent_square_cells_eight() fails for more columns with index {i} and {j} returning {result[j]} instead of {expected_more_cols[i][j]}"              


def run_all():
    test_is_first_column()
    test_is_last_column()
    test_is_top_row()
    test_is_bottom_row()
    test_get_adjacent_cross_cells_distance_one()
    test_get_adjacent_square_cells_eight()
    print("all tests have passed")

"""
0   4   8   12
1   5   9   13
2   6   10  14
3   7   11  15 


0   5   10  15
1   6   11  16
2   7   12  17
3   8   13  18
4   9   14  19

0   4   8   12  16
1   5   9   13  17
2   6   10  14  18
3   7   11  15  19

"""