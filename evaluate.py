import utils
import copy


class Evaluate:
    def __init__(self, queries, initials, facts, rpn):
        self.queries = queries
        self.filled_queries = []
        self.initials_filled_q = []
        self.initials = initials
        self.facts = facts
        self.rpn = rpn

        # Filled queries will contain the queries that we know the answer from,
        # the goal with this is to continue the evaluation of equations until the len
        # of filled_queries equals to len of queries
        self.filled_queries = []

    def update_query_state(self, query):
        lst_eq = []
        sub_queries = [query]
        print("before sub queries for {} are : {} ".format(query, sub_queries))
        sub_queries, lst_eq = self.get_sub_queries(sub_queries, query, lst_eq)
        if len(sub_queries) > 1:
            sub_queries.pop(0)
            new_sub_q = [sub_queries[0]]
            for i in range(len(sub_queries)):
                new_sub_q, lst_eq = self.get_sub_queries(sub_queries, sub_queries[i], lst_eq)
            sub_queries = self.update_sub_queries(sub_queries, new_sub_q)
        print("Sub queries for {} are : {}".format(query, sub_queries))
        if sub_queries:
            cond_query = self.solve_query(query, lst_eq)
        else:
            cond_query = None
        return cond_query

    def update_sub_queries(self, sub, tmp):
        for elem in tmp:
            if elem not in sub:
                sub.append(elem)
                sub[-1].coord = utils.locate_query_inside_rpns(elem.name, self.rpn)
        return sub

    def get_sub_queries(self, sub_queries, query, lst_eq):
        rpn_idx = utils.locate_query_inside_rpns(query.name, self.rpn)
        if not rpn_idx or utils.check_recursion_coord(rpn_idx, sub_queries):
            if rpn_idx:
                lst_eq.append(self.rpn[rpn_idx[0][0]])
                left_side, operators = utils.unpack_facts_operators(self, lst_eq[-1])
                undetermined_facts = self.check_solvable_side(left_side)
                if not undetermined_facts:
                    lst_eq.pop(-1)
                    return sub_queries, lst_eq
                else:
                    sub_queries = self.update_sub_queries(sub_queries, undetermined_facts)
                    return self.get_sub_queries(sub_queries, sub_queries[-1], lst_eq)
            else:
                return sub_queries, lst_eq
        else:
            lst_eq.append(self.rpn[rpn_idx[0][0]])
            left_side, operators = utils.unpack_facts_operators(self, lst_eq[-1])
            undetermined_facts = self.check_solvable_side(left_side)
            if not undetermined_facts:
                return sub_queries, lst_eq
            sub_queries = self.update_sub_queries(sub_queries, undetermined_facts)
            return self.get_sub_queries(sub_queries, sub_queries[-1], lst_eq)
        return sub_queries, lst_eq

    def evaluate_equation(self):
        print('\n\n')
        for i in range(len(self.queries)):
            obj_query = copy.deepcopy(self.queries[i])
            if obj_query.cond is not True:
                obj_query.cond = self.update_query_state(obj_query)
            print("current obj_query is : ", obj_query)
            print("Answer for {} is : {}".format(obj_query.name, obj_query.cond))

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

    def solve_query(self, query, lst_eq):
        return None

    """def solve_query(self, query, sub_queries, lst_eq, eq=None):
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
        print("done with sub queries recursion")"""


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