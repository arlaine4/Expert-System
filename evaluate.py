import utils
import parseur
import copy


class Evaluate:
    def __init__(self, queries, initials, facts, rpn):
        self.queries = queries
        self.initials = initials
        self.facts = facts
        self.rpn = rpn

        # Filled queries will contain the queries that we know the answer from,
        # the goal with this is to continue the evaluation of equations until the len
        # of filled_queries equals to len of queries
        self.filled_queries = []

    def get_fact(self, name):
        for elem in self.facts:
            if elem.name == name:
                return elem
        return None

    def check_solvable_side(self, side):
        lst_undetermined = []
        for elem in side:
            if elem.cond is None:
                lst_undetermined.append(elem)
        return lst_undetermined

    def update_sub_queries(self, sub, tmp):
        for elem in tmp:
            sub.append(elem)
            sub[-1].coord = utils.locate_query_inside_rpns(elem.name, self.rpn)
        return sub

    def update_query_state(self, query):
        sub_queries = [query]
        lst_eq = []
        cond = self.solve_query(query, sub_queries, lst_eq)
        return cond

    def evaluate_equation(self):
        print(self.queries)
        print(self.initials)
        print(self.facts)
        print(self.rpn)
        i = 0
        #while len(self.filled_queries) != len(self.queries):
        for i in range(len(self.queries)):
            obj_query = copy.deepcopy(self.queries[i])
            obj_query.cond = self.update_query_state(obj_query)
            print("Answer for {} is : {}".format(obj_query.name, obj_query.cond))

    def solve_query(self, query, sub_queries, lst_eq, eq=None):
        rpn_idx = utils.locate_query_inside_rpns(query.name, self.rpn)
        if not eq:
            if rpn_idx:
                lst_eq.append(self.rpn[rpn_idx[0][0]])
            else:
                print(sub_queries)
                # TODO
                return None
        left_side, operators = utils.unpack_facts_operators(self, lst_eq[-1])
        sub_tmp = self.check_solvable_side(left_side)
        print("sub_tmp for \033[34m{}\033[0m is : {}".format(lst_eq[-1], sub_tmp))
        if sub_tmp:
            if sub_tmp not in sub_queries: #THIS SHOULD BE sub_tmp in sub_queries
                # TODO
                return None
            else:
                sub_queries = self.update_sub_queries(sub_queries, sub_tmp)
                rpn_idx = utils.locate_query_inside_rpns(sub_queries[-1].name, self.rpn)
                lst_eq.append(self.rpn[rpn_idx[0][0]]) if rpn_idx else lst_eq
                return self.solve_query(query, sub_queries, lst_eq, lst_eq[-1])
        print("list of equation we need to solve : ", lst_eq)
        print("done with sub queries recursion")


    def solvee_query(self, obj_query, eq=None):
        # rpn_idx stands for rpn_indexes
        sub_queries = [obj_query]
        rpn_idx = utils.locate_query_inside_rpns(obj_query.name, self.rpn)
        sub_idx = [rpn_idx]
        solvable_rpn = False
        if not eq:
            if rpn_idx:
                eq = self.rpn[rpn_idx[0][0]]
            else:
                return -1
        print("Current equation being evaluated :\033[33m", eq, " \033[0m")
        left_side, operators = utils.unpack_facts_operators(self, eq)
        while not solvable_rpn:
            sub_tmp = self.check_solvable_side(left_side)
            if sub_tmp:
                sub_queries, sub_idx = self.update_sub_queries(sub_queries, sub_tmp)

                return self.solve_query()
                print("Unsolvable left side")
            else:
                solvable_rpn = True
                print("Left side solvable")
            break
            # if self.check_solvable_side(left_side, operators):
            #    print("Left side solvable")
            # else:
            #    print("Unsolvable left side")
        print("yaaay")