initial_facts = []


def check_initial_facts_cond(fact):
    """
        :param fact: string
        :return: Bool wheter the string fact is inside the global initial_facts or not

        returns True if the fact name is inside initial_facts list or False if it isn't
    """
    global initial_facts
    return True if fact.name in initial_facts else False


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
        self.parse_content = []
        self.read_input_file(file_path)
        # self.content = [Comment, Comment, Comment, Fact, Fact,..., InitialFacts, Comment, Comment, Comment, Query]

    def read_input_file(self, file_path):
        """
            :param file_path(string) : path to the file that we are going to read information from

            Reading input file to store every line into a list
        """
        self.parse_content = []
        with open(file_path, "r+") as fd:
            for line in fd:
                # Skipping empty lines
                if line:
                    self.parse_content.append(line)
        # Don't forget to remove spaces from the lines


class Comment:
    def __init__(self, coord, line, start_pos):
        self.coord = add_coord_to_class(self, coord)
        self.content = line[start_pos:]


class Query:
    def __init__(self, compact_queries):
        self.queries = []
        self.unpack_queries(compact_queries)

    def unpack_queries(self, compact_queries):
        """
        :param compact_queries: a string where every char is glued to another one

        Where just unpacking the string to a list of chars
        """
        self.queries = []
        for c in compact_queries:
            self.queries.append(Fact(c, (-1, -1)))
            # self.queries.append(c)


class Equation:
    def __init__(self):
        self.left = []
        self.right = []


class Fact:
    def __init__(self, c, coord):
        self.cond = check_initial_facts_cond(c)
        self.name = c
        self.coord = add_coord_to_class(self, coord)