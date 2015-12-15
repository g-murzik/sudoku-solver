import sys
import os.path


VERBOSE = False


def print_sudoku():
    for i in range(9):
        global output
        output = []
        for field in sudoku:
            if field // 9 == i:
                if len(sudoku[field]) == 1:
                    output.append(str(sudoku[field][0]))
                else:
                    output.append('*')
        print(' '.join(output))


def print_canidates():
    if '*' in output:
        for row in rows:
            s = []
            for position in row:
                s.append(str(sudoku[position]))
            s = ' '.join(s)
            print(s)


def reduce_canidates():
    improvements = 0
    global sudoku, fields
    for field in sudoku:
        if len(sudoku[field]) > 1:
            for compare_field in fields[field]:
                if (len(sudoku[compare_field]) == 1 and
                        sudoku[compare_field][0] in sudoku[field]):
                    sudoku[field].remove(sudoku[compare_field][0])
                    improvements += 1
    return improvements


def block_test():
    numbers_found = 0
    for block in blocks:
        one = [1]
        two = [2]
        three = [3]
        four = [4]
        five = [5]
        six = [6]
        seven = [7]
        eight = [8]
        nine = [9]
        numbers = [one, two, three, four, five, six, seven, eight, nine]

        for position in block:
            for i, number in enumerate(numbers):
                if number[0] in sudoku[position]:
                    numbers[i].append(position)
        for number in numbers:
            if len(number) == 2 and len(sudoku[number[1]]) > 1:
                sudoku[number[1]] = [number[0]]
                numbers_found += 1
    return numbers_found


def remove_pairs(x):
    improvements = 0
    for y in x:
        pair_dict = dict()
        pairs = []
        for position in y:
            pair_dict[position] = sudoku[position]
        for i in pair_dict:
            for j in pair_dict:
                if i != j and pair_dict[i] == pair_dict[j] and len(pair_dict[i]) == 2:
                    if VERBOSE:
                        print('%i and %i are a pair!' % (i, j))
                    if (i, j) not in pairs:
                        pairs.append((i, j, sudoku[i][0], sudoku[i][1]))
        if pairs:
            for position in y:
                for i, j, m, n in pairs:
                    if position != i and position != j:
                        if m in sudoku[position] and len(sudoku[position]) > 1:
                            sudoku[position].remove(m)
                            improvements += 1
                        if n in sudoku[position] and len(sudoku[position]) > 1:
                            sudoku[position].remove(n)
                            improvements += 1
    return improvements


def pair_test():
    improvements = 0
    test = [rows, columns, blocks]
    for group in test:
        improvements += remove_pairs(group)
    return improvements


def solve_sudoku():
    print('The following sudoku was given:')
    print_sudoku()
    print()
    while True:
        improvements = reduce_canidates()
        numbers_found = block_test()
        improvements += pair_test()
        if improvements == 0 and numbers_found == 0:
            break
        else:
            if VERBOSE:
                print((
                    'canidates reduced: %i, numbers found: %i' % (
                        improvements, numbers_found)))
    print('The sudoku was solved this far:')
    print_sudoku()
    if VERBOSE:
        print_canidates()


if len(sys.argv) == 2 and os.path.exists(sys.argv[1]):
    # create sudoku
    sudoku = dict()
    for i in range(81):
        sudoku[i] = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    # assume, that the provided file meets the guidelines (README.md)
    with open(sys.argv[1]) as fin:
        given_numbers = 0
        row = 0
        for line in fin:
            for column, s in enumerate(line):
                if s in '0123456789':
                    sudoku[9 * row + column] = [int(s)]
                    given_numbers += 1
            row += 1

    # get row and column positions
    rows = []
    columns = []
    for i in range(9):
        rows.append([])
        columns.append([])
        divisionsrest = i % 9
        for j in range(81):
            if j % 9 == divisionsrest:
                columns[i].append(j)
            if j // 9 == i:
                rows[i].append(j)

    # get block positions
    blocks = []
    k = 0
    for i in range(9):
        blocks.append([])
        j = 0
        for m in range(3):
            for n in range(3):
                blocks[i].append(n + j + k)
            j += 9
        k += 3
        if i in [2, 5]:
            k += 18

    # get fields (rows, columns, block) to compare for each field
    fields = dict()
    for field in sudoku:
        temp_fields = []
        for row in rows:
            if field in row:
                for position in row:
                    if position not in temp_fields:
                        temp_fields.append(position)
                break
        for column in columns:
            if field in column:
                for position in column:
                    if position not in temp_fields:
                        temp_fields.append(position)
                break
        for block in blocks:
            if field in block:
                for position in block:
                    if position not in temp_fields:
                        temp_fields.append(position)
                break
        temp_fields.remove(field)
        temp_fields.sort()
        fields[field] = temp_fields

    solve_sudoku()

else:
    print("Please specify (only) one sudoku file.")
    sys.exit(1)
