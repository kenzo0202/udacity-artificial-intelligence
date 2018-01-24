
from utils import *
from collections import Counter


row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units

# TODO: Update the unit list to add the new diagonal units
unitlist = unitlist

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


def naked_twins(values):
    # 指定したboxのpeersを調べる
    # もし同じ組み合わせが存在する時
    # そのボックスが存在するUnitの中から、指定した数字が存在する場合、削除する
    # for box in values.keys():
    #     for peer in peers[box]:
    #         if values[box] == values[peer]:
    #             for target in peers[box]:
    #                 values[target].strip(values[box])

    # unitlistの中でそれぞれのunitを調べる
    # 数あるボックスの中で、同じvalueのものが存在しないか調べる
    for unit in unitlist:
        double_value = Counter([values[box] for box in unit])
        twins_value = []
        for value, cnt in double_value.most_common():
            if cnt > 1 and len(value) == 2:
                twins_value.append(value)

        if not twins_value:
            continue
        else:
            for box in unit:
                if values[box] not in twins_value and len(values[box]) > 1:
                    for val in twins_value:
                        for digit in val:
                            values[box] = values[box].replace(digit, "")
    return values



    """Eliminate values using the naked twins strategy.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers

    Notes
    -----
    Your solution can either process all pairs of naked twins from the input once,
    or it can continue processing pairs of naked twins until there are no such
    pairs remaining -- the project assistant test suite will accept either
    convention. However, it will not accept code that does not process all pairs
    of naked twins from the original input. (For example, if you start processing
    pairs of twins and eliminate another pair of twins before the second pair
    is processed then your code will fail the PA test suite.)

    The first convention is preferred for consistency with the other strategies,
    and because it is simpler (since the reduce_puzzle function already calls this
    strategy repeatedly).
    """


def eliminate(values):
    # 一つの数字のとき
    # row col 3×3 のpeersから数字を除去する
    solved_values = []
    for key, value in values.items():
        if len(value) == 1:
            solved_values.append(key)

    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit, '')

    return values


def only_choice(values):
     for unit in unitlist:
        for num in list("123456789"):
            dplace = [box for box in unit if num in values[box]]
            if len(dplace) == 1:
                values[dplace[0]] = num

     return values


def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        eliminate(values)

        # Your code here: Use the Only Choice Strategy
        only_choice(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):

    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False  ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values  ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt


def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)

    try:
        import PySudoku

        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
