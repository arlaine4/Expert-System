initial_facts = []


def check_initial_facts_cond(fact):
    global initial_facts
    return True if fact in initial_facts else False


def add_coord_to_class(instance, new_coord):
    instance.coord.append(new_coord)
    return instance.coord


class Parsing:
    def __init__(self, file_path):
        self.parse_content = []
        self.read_input_file(file_path)
        # self.content = [Comment, Comment, Comment, Fact, Fact,..., InitialFacts, Comment, Comment, Comment, Query]

    def read_input_file(self, file_path):
        self.parse_content = []
        with open(file_path, "r+") as fd:
            for line in fd:
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