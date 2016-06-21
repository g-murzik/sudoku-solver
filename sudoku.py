import sys
from os import path


class Sudoku(object):
    def __init__(self, file):
        self.VERBOSE = True
        self.sudoku = self.create(file)
        self.fields = self.compute_fields() # also creates rows, columns, blocks


    def create(self, file: str) -> dict:
        """Poullutes a dictionary with the given file where the keys represent
        the positions."""
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
        return sudoku


    def compute_fields(self) -> dict:
        """This functions serves two purposes: Firstly it creates the lists 
        'rows', 'columns' and 'blocks' -- which include positions and secondly
        computes all relevant positions for each field of the sudoku."""
        # create row and column positions
        self.rows = []
        self.columns = []
        rows = self.rows
        columns = self.columns
        for i in range(9):
            rows.append([])
            columns.append([])
            modus = i % 9
            for j in range(81):
                if j % 9 == modus:
                    columns[i].append(j)
                if j // 9 == i:
                    rows[i].append(j)

        # create block positions
        self.blocks = []
        blocks = self.blocks
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

        # compute fields (rows, columns, blocks) to compare for each field
        fields = dict()
        for field in self.sudoku:
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
        return fields


    def reduce_canidates(self) -> int:
        improvements = 0
        for field in self.sudoku:
            if len(self.sudoku[field]) > 1:
                for compare_field in self.fields[field]:
                    if (len(self.sudoku[compare_field]) == 1 and
                            self.sudoku[compare_field][0] in self.sudoku[field]):
                        self.sudoku[field].remove(self.sudoku[compare_field][0])
                        improvements += 1
        return improvements


    def block_test(self) -> int:
        """Checks all blocks and returns the numbers found."""
        numbers_found = 0
        for array in [self.rows, self.columns, self.blocks]:
            for element in array:
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

                for position in element:
                    for i, number in enumerate(numbers):
                        if number[0] in self.sudoku[position]:
                            numbers[i].append(position)
                for number in numbers:
                    if len(number) == 2 and len(self.sudoku[number[1]]) > 1:
                        self.sudoku[number[1]] = [number[0]]
                        numbers_found += 1
        return numbers_found


    def remove_pairs(self, x: list) -> int:
        """Checks a list containing lists"""
        improvements = 0
        for y in x:
            pair_dict = dict()
            pairs = []
            for position in y:
                pair_dict[position] = self.sudoku[position]
            for i in pair_dict:
                for j in pair_dict:
                    if i != j and pair_dict[i] == pair_dict[j] and len(pair_dict[i]) == 2:
                        if self.VERBOSE:
                            print('%i and %i are a pair!' % (i, j))
                        if (i, j) not in pairs:
                            pairs.append((i, j, self.sudoku[i][0], self.sudoku[i][1]))
            if pairs:
                for position in y:
                    for i, j, m, n in pairs:
                        if position != i and position != j:
                            if m in self.sudoku[position] and len(self.sudoku[position]) > 1:
                                self.sudoku[position].remove(m)
                                improvements += 1
                            if n in self.sudoku[position] and len(self.sudoku[position]) > 1:
                                self.sudoku[position].remove(n)
                                improvements += 1
        return improvements


    def pair_test(self) -> int:
        """Calls remove pairs for rows, columns and blocks and returns the 
        number of improvements."""
        improvements = 0
        arrays = [self.rows, self.columns, self.blocks]
        for array in arrays:
            improvements += self.remove_pairs(array)
        return improvements


    def create_output(self) -> list:
        output = []
        for i in range(9):
            temp = []
            for field in self.sudoku:
                if field // 9 == i:
                    if len(self.sudoku[field]) == 1:
                        temp.append(str(self.sudoku[field][0]))
                    else:
                        temp.append('*')
            output.append(temp)
        return output


    def print_sudoku(self):
        output = self.create_output()
        for row in output:
            print(' '.join(row))
        print()


    def print_canidates(self):
        print()
        for row in self.rows:
            s = []
            for position in row:
                s.append(str(self.sudoku[position]))
            s = ' '.join(s)
            print(s)
        print()


    def solve(self):
        print('The following sudoku was given:')
        self.print_sudoku()
        while True:
            improvements = self.reduce_canidates()
            numbers_found = self.block_test()
            improvements += self.pair_test()
            if improvements == 0 and numbers_found == 0:
                break
            else:
                if self.VERBOSE:
                    print('canidates reduced: {}, numbers found: {}'.format(
                        improvements, numbers_found))
        print('The sudoku was solved this far:')
        self.print_sudoku()
        if self.VERBOSE:
            self.print_canidates()


if __name__ == "__main__":
    if len(sys.argv) == 2 and path.exists(sys.argv[1]):
        sudoku = Sudoku(sys.argv[1])
        sudoku.solve()
