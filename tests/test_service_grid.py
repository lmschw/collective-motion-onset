import services.service_grid as sgrid

import unittest

class TestServiceGrid(unittest.TestCase):
    
    def test_is_first_column(self):
        grid_size_square = (4,4)

        test_coordinates_square = [0, 3, 6, 9, 12, 13, 15]
        expected_square = [True, True, False, False, False, False, False]
        for i in range(len(test_coordinates_square)):
            assert sgrid.is_first_column(cell_idx=test_coordinates_square[i], grid_size=grid_size_square) == expected_square[i], f"Is first column fails for square with index {i}"

    def test_is_last_column(self):
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

    def test_is_top_row(self):
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

    def test_is_bottom_row(self):
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

    def test_get_adjacent_cross_cells_distance_one(self):
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

    def test_get_adjacent_cross_cells_distance_two(self):
        grid_size_square = (5,5)
        grid_size_more_rows = (5,4)
        grid_size_more_columns = (4,5)

        """
        0   5   10  15  20
        1   6   11  16  21
        2   7   12  17  22
        3   8   13  18  23
        4   9   14  19  24
        """
        test_coordinates_square = [0, 1, 4, 6, 9, 10, 12, 19, 20, 22, 24]
        expected_square = [[4, 5, 1, 20, 3, 10, 2, 15], 
                        [0, 6, 2, 21, 4, 11, 3, 16], 
                        [3, 9, 0, 24, 2, 14, 1, 19], 
                        [5, 11, 7, 1, 9, 16, 8, 21],
                        [8, 14, 5, 4, 7, 19, 6, 24],
                        [14, 15, 11, 5, 13, 20, 12, 0],
                        [11, 17, 13, 7, 10, 22, 14, 2],
                        [18, 24, 15, 14, 17, 4, 16, 9],
                        [24, 0, 21, 15, 5, 23, 5, 22, 10],
                        [21, 2, 23, 17, 20, 7, 24, 12],
                        [23, 4, 20, 19, 22, 9, 21, 14]]
        for i in range(len(test_coordinates_square)):
            result = sgrid.get_adjacent_cross_cells_distance_two(cell_idx=test_coordinates_square[i], grid_size=grid_size_square)
            for j in range(4):
                assert result[j] == expected_square[i][j], f"get_adjacent_cross_cells_distance_one() fails for square with index {i} and {j} returning {result[j]} instead of {expected_square[i][j]}"

        """
            0   5   10  15
            1   6   11  16
            2   7   12  17
            3   8   13  18
            4   9   14  19
        """
        test_coordinates_more_rows = [0, 2, 4, 5, 8, 11, 14, 15, 18, 19]
        expected_more_rows = [[4, 5, 1, 15, 3, 10, 2, 10],
                            [1, 7, 3, 17, 0, 12, 4, 12],
                            [3, 9, 0, 19, 2, 14, 1, 14],
                            [9, 10, 6, 0, 8, 15, 7, 15],
                            [7, 13, 9, 3, 6, 18, 5, 18],
                            [10, 16, 12, 6, 14, 1, 13, 1],
                            [13, 19, 10, 9, 12, 4, 11, 4],
                            [19, 0, 16, 10, 18, 5, 17, 5],
                            [17, 3, 19, 13, 16, 8, 15, 8],
                            [18, 4, 15, 14, 17, 9, 16, 9]]
        for i in range(len(test_coordinates_more_rows)):
            result = sgrid.get_adjacent_cross_cells_distance_two(cell_idx=test_coordinates_more_rows[i], grid_size=grid_size_more_rows)
            for j in range(4):
                assert result[j] == expected_more_rows[i][j], f"get_adjacent_cross_cells_distance_one() fails for more rows with index {i} and {j} returning {result[j]} instead of {expected_more_rows[i][j]}"

        """
            0   4   8   12  16
            1   5   9   13  17
            2   6   10  14  18
            3   7   11  15  19
        """
        test_coordinates_more_cols = [0, 1, 3, 6, 8, 11, 14, 16, 18, 19]
        expected_more_cols = [[3, 4, 1, 16, 2, 8, 2, 12],
                            [0, 5, 2, 17, 3, 9, 3, 13],
                            [2, 7, 0, 19, 1, 11, 1, 15],
                            [5, 10, 7, 2, 4, 14, 4, 18],
                            [11, 12, 9, 4, 10, 16, 10, 0],
                            [10, 15, 8, 7, 9, 19, 9, 3],
                            [13, 18, 15, 10, 12, 2, 12, 6],
                            [19, 0, 17, 12, 18, 4, 18, 8],
                            [17, 2, 19, 14, 16, 6, 16, 10],
                            [18, 3, 16, 15, 17, 7, 17, 11]]
        for i in range(len(test_coordinates_more_cols)):
            result = sgrid.get_adjacent_cross_cells_distance_two(cell_idx=test_coordinates_more_cols[i], grid_size=grid_size_more_columns)
            for j in range(4):
                assert result[j] == expected_more_cols[i][j], f"get_adjacent_cross_cells_distance_one() fails for more columns with index {i} and {j} returning {result[j]} instead of {expected_more_cols[i][j]}"

    def test_get_adjacent_square_cells_twenty_four(self):
        grid_size_square = (6,6)
        grid_size_more_rows = (6,5)
        grid_size_more_columns = (5,6)

        """
        0   6   12  18  24  30
        1   7   13  19  25  31
        2   8   14  20  26  32
        3   9   15  21  27  33
        4   10  16  22  28  34
        5   11  17  23  29  35

        28  34  4   10  16  22  28  34  4   10
        29  35  5   11  17  23  29  35  5   11
        24  30  0   6   12  18  24  30  0   6
        25  31  1   7   13  19  25  31  1   7
        26  32  2   8   14  20  26  32  2   8
        27  33  3   9   15  21  27  33  3   9
        28  34  4   10  16  22  28  34  4   10
        29  35  5   11  17  23  29  35  5   11
        24  30  0   6   12  18  24  30  0   6
        25  31  1   7   13  19  25  31  1   7

        """
        test_coordinates_square = [0, 2, 5, 10, 12, 23, 30, 32, 35]
        expected_square = [[5, 11, 6, 7, 1, 31, 30, 35, 28, 34, 4, 10, 16, 17, 12, 13, 14, 8, 2, 32, 26, 25, 24, 29],
                           [1, 7, 8, 9, 3, 33, 32, 31, 24, 30, 0, 6, 12, 13, 14, 15, 16, 10, 4, 34, 28, 27, 26, 25],
                           [4, 10, 11, 6, 0, 30, 35, 34, 27, 33, 3, 9, 15, 16, 17, 12, 13, 7, 1, 31, 25, 24, 29, 28],
                           [9, 15, 16, 17, 11, 5, 4, 3, 32, 2, 8, 14, 20, 21, 22, 23, 18, 12, 6, 0, 30, 35, 34, 33],
                           [17, 23, 18, 19, 13, 7, 6, 11, 4, 10, 16, 22, 28, 29, 24, 25, 26, 20, 14, 8, 2, 1, 0, 5],
                           [22, 28, 29, 24, 18, 12, 17, 16, 9, 15, 21, 27, 33, 34, 35, 30, 31, 25, 19, 13, 7, 6, 11, 10],
                           [35, 5, 0, 1, 31, 25, 24, 29, 22, 28, 34, 4, 10, 11, 6, 7,8, 2, 32, 26, 20, 19, 18, 23],
                           [31, 1, 2, 3, 33, 27, 26, 25, 18, 24, 30, 0, 6, 7, 8, 9, 10, 4, 34, 28, 22, 21, 20, 19],
                           [34, 4, 5, 0, 30, 24, 29, 28, 21, 27, 33, 3, 9, 10, 11, 6, 7, 1, 31, 25, 19, 18, 23, 22]]
        for i in range(len(test_coordinates_square)):
            result = sgrid.get_adjacent_square_cells_twenty_four(cell_idx=test_coordinates_square[i], grid_size=grid_size_square)
            for j in range(len(expected_square[i])):
                assert result[j] == expected_square[i][j], f"get_adjacent_square_cells_eight() fails for square with index {i} and {j} returning {result[j]} instead of {expected_square[i][j]}"


    def test_get_adjacent_square_cells_eight(self):
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

    def test_get_grid_cell_idx(self):
        """
        0   6   12  18  24
        1   7   13  19  25
        2   8   14  20  26
        3   9   15  21  27
        4   10  16  22  28
        5   11  17  23  29
        """
        grid_size = (6, 5)
        xs = [0, 3, 5]
        ys = [0, 2, 4]
        expected_cell_idx = [[0, 12, 24], [3, 15, 27], [5, 17, 29]]
        for i in range(len(xs)):
            for j in range(len(ys)):
                assert expected_cell_idx[i][j] == sgrid.get_grid_cell_idx(x=xs[i], y=ys[j], grid_size=grid_size)

    def test_get_x_y_for_cell_idx(self):
        grid_size = (6, 5)
        cell_indices = [0, 3, 5, 12, 15, 17, 24, 27, 29]
        coordinates = [[0, 0], [3, 0], [5, 0], [0, 2], [3, 2], [5, 2], [0, 4], [3, 4], [5, 4]]
        for i in range(len(cell_indices)):
            coords = sgrid.get_x_y_for_cell_idx(cell_idx=cell_indices[i], grid_size=grid_size)
            assert coordinates[i][0] == coords[0]
            assert coordinates[i][1] == coords[1]

    def run_all(self):
        unittest.main(exit=False)

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