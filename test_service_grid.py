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


test_is_first_column()
test_is_last_column()
test_is_top_row()
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