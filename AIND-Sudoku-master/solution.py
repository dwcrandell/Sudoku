assignments = []
rows = 'ABCDEFGHI'
columns = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

#Assign grid labels to boxes
boxes = cross(rows, columns)
#Group boxes into rows
row_units = [cross(r, columns) for r in rows]
#Group boxes into columns
column_units = [cross(rows, c) for c in columns]
#Generate 3x3 square units
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
#Generate diagonal units
diag_1 = [[r + str(i+1) for i, r in enumerate(rows)]]
diag_2 = [[r + str(i+1) for i, r in enumerate(rows[::-1])]]
unit_list = row_units + column_units + square_units + diag_1 + diag_2

#Get peers for each box
units = dict((s, [u for u in unit_list if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    #Examine each unit
    for unit in unit_list:
        for box in unit:
            #Identify possible naked twins candidate
            if len(values[box]) == 2:
                for b in unit:
                    #Find another box in unit that has same values
                    if values[b] == values[box] and b!= box:
                        nt = values[box]
                        #Remove values from other peers
                        for p in unit:
                            if values[p] != nt:
                                assign_value(values, p, values[p].replace(nt[0], ""))
                                assign_value(values, p, values[p].replace(nt[1], ""))
    return values

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    assert len(boxes) == len(grid)
    return {box: (value if value is not '.' else '123456789') for (box, value) in zip(boxes,grid)}

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in columns))
        if r in 'CF': print(line)
    print

def eliminate(values):
	'''If a box has a value, remove this value from the possible values for all of the boxes peers'''
	for box in values:
		if len(values[box]) == 1:
			known_value = values[box]
			for cell in peers[box]:
				if known_value in values[cell]:
					assign_value(values, cell, values[cell].replace(known_value, ""))
	return values

def only_choice(values):
	'''Assign value to box if there is only one possible choice for that box'''
	for unit in unit_list:
		for digit in '123456789':
			dplaces = [box for box in unit if digit in values[box]]
			if len(dplaces) == 1:
				assign_value(values, dplaces[0], digit)
	return values

def reduce_puzzle(values):
	'''Try to eliminate possible values
	   Use naked twins strategy to remove additional values
	   Assign values using only choice. If a box has no possbible values, return False. There is no solution'''
	solved_values = [box for box in values.keys() if len(values[box]) == 1]
	stalled = False
	while not stalled:
		solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
		values = eliminate(values)
		values = naked_twins(values)
		values = only_choice(values)
		solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
		stalled = solved_values_before == solved_values_after
		if len([box for box in values.keys() if len(values[box]) == 0]):
			return False
	return values

def search(values):
	#Depth first search of all possible solutions
    values = reduce_puzzle(values)
    if values is False:
        return False #Failed
    else:
        if all(len(values[box]) == 1 for box in boxes):
            return values #Solved
    _, box = min((len(values[box]), box) for box in boxes if len(values[box]) > 1)
    #Recursively solve each one of the resulting sudokus
    for value in values[box]:
        new_sudoku = values.copy()
        new_sudoku[box] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid))

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
