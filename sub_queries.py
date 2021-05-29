import utils
import copy


class Evaluate:
    def __init__(self, exsys):
        self.queries = exsys.queries
        self.initials = exsys.initials
        self.facts = exsys.facts
        self.rpn = exsys.rpn

    def update_query_state(self, query):
        """
            :param query(Fact instance): query to get sub_queries for
            :return: list of sub_queries for one main query
        """
        lst_eq = []
        sub_queries = [query]
        sub_queries, lst_eq = self.get_sub_queries(sub_queries, query, lst_eq, len(sub_queries))
        if len(sub_queries) > 1:
            sub_queries.pop(0)
            new_sub_q = [sub_queries[0]]
            for i in range(len(sub_queries)):
                new_sub_q, lst_eq = self.get_sub_queries(sub_queries, sub_queries[i], lst_eq, len(sub_queries))
            sub_queries = self.update_sub_queries(sub_queries, new_sub_q)
        return sub_queries

    def update_sub_queries(self, sub, tmp):
        """
            :param sub(list of facts): list of sub_queries to be updated
            :param tmp(list of facts): list of facts to append to sub_queries
            :return: updated sub_queries
        """
        for elem in tmp:
            if elem not in sub:
                sub.append(elem)
                sub[-1].coord = utils.locate_query_inside_rpns(elem.name, self.rpn)
        return sub

    def get_sub_queries(self, sub_queries, query, lst_eq, index_q):
        """
            :param sub_queries(list of facts)	: list of sub_queries for one query, incrementing with the recursion
            :param query(Fact instance)			: the query we are basing the recursion on, applied on the dynamic
                                                  sub_queries list aswell
            :param lst_eq(list of equations)	: where to look for the facts, dynamic list
            :param index_q(int)					: index inside the sub_queries list, decreasing as we go on the recursion
            :return								: list of sub_queries ans list of equations
        """
        rpn_idx = utils.locate_query_inside_rpns(query.name, self.rpn)
        if not rpn_idx:
            return sub_queries, lst_eq
        lst_eq.append(self.rpn[rpn_idx[0][0]])
        left_side, operators = utils.unpack_facts_operators(self, lst_eq[-1])
        undetermined_facts = self.check_solvable_side(left_side)
        if not undetermined_facts:
            if utils.check_recursion_coord(rpn_idx, sub_queries):
                lst_eq.pop(-1)
            return sub_queries, lst_eq
        sub_queries = self.update_sub_queries(sub_queries, undetermined_facts)
        if index_q - 1 > 0:
            return self.get_sub_queries(sub_queries, sub_queries[index_q], lst_eq, index_q - 1)
        return sub_queries, lst_eq

    def evaluate_equation(self, query):
        """
            :param query(Fact instance): The query we want sub_queries for
            :return: list of sub_queries for one query
        """
        sub_queries = []
        #obj_query = copy.deepcopy(query)
        obj_query = query
        sub_queries.append(self.update_query_state(obj_query))
        return sub_queries

    def get_fact(self, name):
        """
            :param name(string): name of the fact you want to access
            :return wheter the fact instance or None
        """
        for elem in self.facts:
            if elem.name == name:
                return elem
        return None

    def check_solvable_side(self, side):
        """
            :param side(list): list of facts and operators inside an equation side
            :return: list of facts whose states are undertermined
        """
        lst_undetermined = []
        for elem in side:
            if elem.cond is None:
                lst_undetermined.append(elem)
        return lst_undetermined
