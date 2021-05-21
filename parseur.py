import utils
import sys

initial_facts = []
queries = []


def unpack_facts_to_list(facts):
    """
        :param facts: string to decompose into a list of chars
        :return: list of chars

        Unpacking a string into a list of chars, used for initial facts
        and queries
    """
    lst_facts = []
    for c in facts:
        if c == '#':
            break
        elif c.isspace() or c == "=" or c == "?":
            continue
        lst_facts.append(c)
    return lst_facts


def update_initial_fact(line):
    pass


def check_initial_facts_cond(fact, initial):
    """
        :param fact: string
        :return: Bool wheter the string fact is inside the global initial or not

        returns True if the fact name is inside initial list or False if it isn't
    """
    return True if fact in initial else False


def add_coord_to_class(instance, new_coord):
    """
        :param instance (class): class instance we want the coordinates to be updated
        :param new_coord (int, int): the coordinates to add the instance coordinates list
                -> new_coord correspond to the x (inside line related) and y(wich line) coordinates
                   of the new element to add to the class
        :return: update coordinates list

        Update Fact and Comment classes coordinates
    """
    instance.coord.append(new_coord)
    return instance.coord


class Parsing:
    def __init__(self, file_path):
        """
            :param file_path(string)                : Path to the input file

            raw_content(list of class instances)    : all the raw file content
            queries(list of chars)                  : all the queries inside the file
            comments(list of Comment() instances)   : all the comments encountered inside the file
            equations(list of Equation() instances) : all the equation encountered inside the file
        """
        self.raw_content = []
        self.queries = []
        self.comments = []
        self.equations = []
        self.read_input_file(file_path)

    def parsing_loop(self):
        """
            Main parsing loop
        """
        global initial_facts
        global queries

        for (y, line) in enumerate(self.raw_content):
            line_type = utils.check_line_type(line)
            if line_type == "Initial Facts":
                initial_facts = unpack_facts_to_list(line)
            elif line_type == "Query":
                queries = unpack_facts_to_list(line)
            elif line_type == "Equation":
                self.handle_equation(line, y)
            elif line_type == "Comment":
                self.handle_comment(line, y)

    def handle_comment(self, line, y):
        self.comments.append(Comment((0, y), line, 0))

    def handle_equation(self, line, y):
        facts_names = []
        reverse_eq = False
        left_facts = []
        right_facts = []
        splitted_line = line.replace(" ", "").split('#')

        # STORE THE COMMENT from splitted_line[1]

        if "<=>" in splitted_line[0]:
            reverse_eq = True
            right, left = splitted_line[0].split('<=>')
            # print(right, "-------", left, 'line operator : ')
        else:
            left, right = splitted_line[0].split('=>')
            # print(left, "#######", right, 'line operator : ')
        prev = None
        for (x, elem) in enumerate(left):
            tmp_negation = False
            if elem not in facts_names:
                if elem.isalpha():
                    left_facts.append(Fact(elem, (x, y)))
                    left_facts[-1].previous = prev
                    prev = elem
                else:
                    continue
                    # working but need to do something about negation operator at the beginning of the line
                    """print(elem)
                    #Handle case were the line begins with an operator
                    if elem == '!' and len(left_facts) == 0:
                        tmp_negation = True
                        continue
                    left_facts[-1].operator = elem"""
        for i in range(len(left_facts)):
            print(left_facts[i].name, left_facts[i].cond, left_facts[i].previous)

    def read_input_file(self, file_path):
        """
            :param file_path(string) : path to the file that we are going to read information from

            Reading input file to store every line into a list
        """
        self.raw_content = []
        with open(file_path, "r+") as fd:
            for line in fd:
                # Skipping empty lines
                if len(line) > 1:
                    self.raw_content.append(line)
        # Don't forget to remove spaces from the lines


class Comment:
    def __init__(self, coord, line, start_pos):
        """
            :param coord(tuple(x, y)) : x, y position of the comment
            :param line(string)       : full line content
            :param start_pos(int)     : x position where we start getting the comment content
        """
        self.coord = []
        self.coord = add_coord_to_class(self, coord)
        self.content = line[start_pos:]


class Query:
    def __init__(self, compact_queries):
        """
            :param compact_queries(string) : queries glued to each other inside a string

            queries (list of chars)        : list of all the queries
        """
        self.queries = []
        self.queries = unpack_facts_to_list(compact_queries)


class Equation:
    def __init__(self):
        """
            neg_bool (tuple(bool, bool))        : if the left/righ part if the equation has a negation operator '!'
            operator (char)                     : operator on the right side of the fact, related to the next fact
            left (list of class instances)      : left side of the equation, list of facts
            right (list of class instances)     : right side of the equation, list of facts
        """
        self.neg_bool = (False, False)
        self.operator = ''
        self.left = []
        self.right = []


class Fact:
    def __init__(self, c, coord):
        """
            cond (bool)                  : If the fact is true or not regarding to the initial_facts
            operator (char)              : Operator (after the fact) associated with a fact
            name (char)                  : name of the fact -> ex: A
            relative_coord (tuple(x, y)) : x, y coordinates -> x = inside line pos and y = line number
            previous (class instance)    : left connected element to the current fact
        """
        global initial_facts

        self.cond = check_initial_facts_cond(c, initial_facts)
        self.operator = ''
        self.name = c
        self.coord = []
        self.coord = add_coord_to_class(self, coord)
        self.previous = [None]
