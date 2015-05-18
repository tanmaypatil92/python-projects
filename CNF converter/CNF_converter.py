# TANMAY PATIL
# CS 561 : ASSIGNMENT 2a : CNF Converter
# USC ID : 1802228863
__author__ = 'Tanmay'

import sys

# For debugging
def print_error(msg):
    return # not debugging
    print 'ERROR :' + msg
    exit()

# Symbol check
def is_symbol(element):
    if not (type(element) is list):
        if type(element) is str:
            if element[0].isupper():
                return True
    return False

# Literal check
def is_literal(element):
    if is_symbol(element):
        return True
    elif (type(element) is list) and len(element) == 2:
        if element[0] == 'not':
            if is_symbol(element[1]):
                return True
    return False


def check_valid_operator(element):
    if type(element) is str:
        if element == 'or' or element == 'and' or element == 'not' or element == 'implies' or element == 'iff':
            return True
    return False


def operator(element):
    if type(element) is list:
        check_valid_operator(element[0])
        return element[0]
    else:
        print_error('operator() : called on non list element')


def arguments(element):
    if type(element) is list:
        if len(element) >= 2:
            check_valid_operator(element[0])
            return element[1:]
        else:
            print_error('function arguments(): called on list with no arguments')
    elif is_symbol(element):
        return element


def check_literal_op_get_args(element, op):
    if not is_literal(element):
        args = element[1:]
        if not element[0] == op:
            print_error('error in expected operation')
    else:
        args = element[0]
    return args


def remove_duplicates(curr_list):
    for i in range(1, len(curr_list)):
        for j in range((i+1), len(curr_list)):
            if (type(curr_list[i]) is list) and (type(curr_list[j]) is list):
                if operator(curr_list[i]) == operator(curr_list[j]):
                    i_sorted = sorted(arguments(curr_list[i]), key=lambda lst: lst[0])
                    j_sorted = sorted(arguments(curr_list[j]), key=lambda lst: lst[0])
                    if i_sorted == j_sorted:
                        del curr_list[j]
            elif curr_list[i] == curr_list[j]:
                del curr_list[j]
    return curr_list


def promote_list(curr_list):
    promoted_op_list = list()

    if is_literal(curr_list):
        print_error('literal passed to promote_op_list')
    else:
        op = operator(curr_list)
        promoted_op_list.append(op)
        arg_list = arguments(curr_list)
        for arg in arg_list:
            if is_literal(arg):
                promoted_op_list.append(arg)
            elif operator(arg) == op:
                promoted_op_list.extend(arguments(arg))
            else:
                promoted_op_list.append(arg)
    return remove_duplicates(promoted_op_list)


def promote_op(arg_list, op):
    promoted_op_list = list()
    for arg in arg_list:
        if is_literal(arg):
            promoted_op_list.extend(arg)
        elif arg[0] == op:
            promoted_op_list.extend(arguments(arg))
        else:
            promoted_op_list.append(arg)
    return promoted_op_list


def remove_implications(curr_list):

    if is_literal(curr_list):
        return curr_list

    arg_list = arguments(curr_list)

    removed_implication_list = list()
    removed_implication_list.append(operator(curr_list))

    for arg in arg_list:
        removed_implication_list.append(remove_implications(arg))

    if operator(curr_list) == 'implies':
        p = arguments(removed_implication_list)[0]
        q = arguments(removed_implication_list)[1]
        converted_expression = ['or', ['not', p], q]
        return converted_expression

    elif operator(curr_list) == 'iff':
        p = arguments(removed_implication_list)[0]
        q = arguments(removed_implication_list)[1]
        converted_expression = ['and', ['or', ['not', p], q], ['or', p, ['not', q]]]
        return converted_expression

    else:
        return removed_implication_list


def shift_not_inside(curr_list):

    if is_literal(curr_list):
        return curr_list

    if operator(curr_list) == 'not':

        p = arguments(curr_list)[0]
        converted_expression = list()
        if operator(p) == 'or':
            converted_expression.append('and')
            for p_arg in arguments(p):
                converted_expression.append(['not', p_arg])
            converted_expression = shift_not_inside(converted_expression)
            converted_expression = promote_list(converted_expression)
            return converted_expression
        elif operator(p) == 'and':
            converted_expression.append('or')
            for p_arg in arguments(p):
                converted_expression.append(['not', p_arg])
            converted_expression = shift_not_inside(converted_expression)
            converted_expression = promote_list(converted_expression)
            return converted_expression
        elif operator(p) == 'not':
            arg = arguments(p)[0]
            converted_expression = shift_not_inside(arg)
        return converted_expression
    else:
        # FOR EACH ARGUMENT CALL SHIFT_NOT_INSIDE
        shifted_not_list = list()
        shifted_not_list.append(operator(curr_list))

        for arg in arguments(curr_list):
            shifted_not_list.append(shift_not_inside(arg))

        return shifted_not_list


def is_or_of_literals(curr_list):
    if operator(curr_list) == 'or':
        for arg in arguments(curr_list):
            if not(is_literal(arg)):
                return False
        return True

    else:
        print_error('get_args_redistribution() : Expected argument to be literal')


def get_args_redistribution(curr_list):
    if is_literal(curr_list):
        return curr_list
    if operator(curr_list) == 'or':
        if not is_or_of_literals(curr_list):print_error('get_args_redistribution() : Expected argument to be literal')
        or_list = list()
        or_list.append(curr_list)
        return or_list
    elif operator(curr_list) == 'and':
        for arg in arguments(curr_list):
            if not (is_literal(arg) or is_or_of_literals(arg)):
                print_error('get_args_redistribution() : Expected argument to be literal or disjunction of literals')
        return arguments(curr_list)
    else:
        print_error('get_args_redistribution() : Unexpected operator')


def to_cnf(curr_list):

    if is_literal(curr_list):
        return curr_list

    if operator(curr_list) == 'and':

        arg_list = arguments(curr_list)

        cnf_list = list()
        cnf_list.append('and')

        for arg in arg_list:
            if not is_literal(arg):
                arg = to_cnf(arg)
            cnf_list.append(arg)

        return promote_list(cnf_list)

    elif operator(curr_list) == 'or':

        promoted_curr_list = promote_list(curr_list)
        arg_list = arguments(promoted_curr_list)

        if len(arg_list) > 2:
            p = to_cnf(arg_list[0])

            q_list = list()
            q_list.append('or')
            for arg in arg_list[1:]:
                q_list.append(arg)
            q = to_cnf(q_list)

        elif len(arg_list) == 2:
            p = to_cnf(arg_list[0])
            q = to_cnf(arg_list[1])
        else:
            print_error('error in number of args of or')

        # PROMOTING THE OR OPERATOR IN LIST FORMED BY P or Q AND CHECKING IF ALL LITERALS
        pq_list = list()
        pq_list.append('or')
        pq_list.append(p)
        pq_list.append(q)
        promoted_pq_list = promote_list(pq_list)

        all_literals = True
        for arg in arguments(promoted_pq_list):
            if not is_literal(arg):
                all_literals = False

        if all_literals:
            return promoted_pq_list

        # REDISTRIBUTING - SINCE SOME ARGUMENTS ARE and

        cnf_list = list()
        cnf_list.append('and')

        p_args = get_args_redistribution(p)
        q_args = get_args_redistribution(q)

        for pi in p_args:
            for qi in q_args:

                pi_qi_list = list()
                pi_qi_list.append('or')
                pi_qi_list.append(pi)
                pi_qi_list.append(qi)
                pi_qi_promoted_list = (promote_list(pi_qi_list))
                cnf_list.append(pi_qi_promoted_list)

        return promote_list(cnf_list)
    else:
        print_error('to_cnf(): passed list has operator excluding and, or')


def main_cnf(input_list):
    implications_removed_list = remove_implications(input_list)
    # print implications_removed_list
    shifted_not_list = shift_not_inside(implications_removed_list)
    # print shifted_not_list
    return to_cnf(shifted_not_list)

if len(sys.argv) != 3:
    print_error('error in number of arguments')

f_input = open(sys.argv[2], 'r')
f_output = open('sentences_CNF.txt', 'w')

line_count = f_input.readline()
line_count = eval(line_count)
for i in range(0, line_count):
    input_sentences_text = f_input.readline()
    input_sentences_list = eval(input_sentences_text)

    output_cnf = main_cnf(input_sentences_list)
    output_cnf_text = str(output_cnf)

    f_output.write(output_cnf_text + '\n')
    print(output_cnf_text)
