import utils

initial_facts = []
queries = []


def unpack_facts_to_list(facts):
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
    return True if fact.name in initial else False


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
        self.raw_content = []
        self.queries = []
        self.comments = []
        self.equations = []
        self.read_input_file(file_path)

    def parsing_loop(self):
        global initial_facts
        global queries
        for line in self.raw_content:
            line_type = utils.check_line_type(line)
            if line_type == "Initial Facts":
                initial_facts = unpack_facts_to_list(line)
            elif line_type == "Query":
                queries = unpack_facts_to_list(line)
            elif line_type == "Equation":
                self.handle_equation(line)
            elif line_type == "Comment":
                self.handle_comment(line)
        print("initial facts = {}".format(initial_facts))
        print("queries       = {}".format(queries))

    def handle_comment(self, line):
        pass

    def handle_equation(self, line):
        pass


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
        self.coord = add_coord_to_class(self, coord)
        self.content = line[start_pos:]


class Query:
    def __init__(self, compact_queries):
        self.queries = []
        self.queries = unpack_facts_to_list(compact_queries)


class Equation:
    def __init__(self):
        self.neg_bool = False
        self.operator = ''
        self.left = []
        self.right = []


class Fact:
    def __init__(self, c, coord):
        self.cond = check_initial_facts_cond(c)
        self.operator = ''
        self.name = c
        self.relative_coord = []
        self.relative_coord = add_coord_to_class(self, coord)
        self.previous = None
