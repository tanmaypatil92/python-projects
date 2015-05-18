# TANMAY PATIL
# CS 561 : ASSIGNMENT 2 : DPLL
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


def is_or_of_literals(curr_list):
    if operator(curr_list) == 'or':
        for arg in arguments(curr_list):
            if not(is_literal(arg)):
                return False
        return True

    else:
        print_error('get_args_redistribution() : Expected argument to be literal')


def is_clause_true(clause, model):

    if is_literal(clause):
        literal_list = list()
        literal_list.append(clause)
    else:
        is_or_of_literals(clause)
        literal_list = arguments(clause)

    not_sure = False
    for literal in literal_list:
        if is_symbol(literal):
            var = literal
            if var in model:
                if model[var]:
                    return True
            else:
                not_sure = True
        else:
            # ELSE IT IS A NOT OF A SYMBOL
            var = literal[1]
            if var in model:
                if not model[var]:
                    return True
            else:
                not_sure = True
    if not_sure:
        return 'not_sure'
    else:
        return False

def or_args_of(curr_list):
    if is_literal(curr_list):
        return [curr_list]
    elif operator(curr_list) == 'and':
        return [curr_list]
    elif operator(curr_list) == 'or':
        return arguments(curr_list)
    print_error("or_args_of: Unknown operator")


def sign_of_literal(literal):

    if not is_literal(literal):
            print_error("literal expected")

    if is_symbol(literal):
        return True
    else:
        return False

def symbol_of_literal(literal):

    if not is_literal(literal):
            print_error("literal expected")

    if is_symbol(literal):
        return literal
    else:
        return literal[1]

def find_pure_symbol(symbols, clauses):

    for sym in symbols:
        positive = False
        negative = False

        for clause in clauses:

            if sym in or_args_of(clause):
                positive = True

            not_sym = ['not', sym]
            if not_sym in or_args_of(clause):
                negative = True

        if positive == True and negative == False:
            return [sym, True]
        elif positive == False and negative == True:
            return [sym, False]

    return ['null','null']

def find_unit_clause(clauses, model):

    for clause in clauses:

        if is_literal(clause):
            if is_symbol(clause):
                return [clause, True]
            elif operator(clause) == 'not':
                return [symbol_of_literal(clause), False]

        elif operator(clause) == 'or':
            arg_list = arguments(clause)
            total_arg_length = len(arg_list)
            found_length = 0
            not_found_literal = 'null'

            for literal in arg_list:

                sym = symbol_of_literal(literal)

                # CHECK IF SYMBOL PRESENT IN MODEL
                if sym in model:
                    found_length = found_length + 1
                else:
                    not_found_literal = literal

            if (found_length + 1) == total_arg_length:
                return [symbol_of_literal(literal), sign_of_literal(not_found_literal)]

        else:
            print_error("Unexpected argument")

    return ['null', 'null']



def dpll(clauses, symbols, model):

    all_clauses_true = True
    unknown_clauses = list()
    for clause in clauses:
        clause_truth_value = is_clause_true(clause, model)
        if clause_truth_value == False:
            return False
        elif clause_truth_value == 'not_sure':
            all_clauses_true = False
            unknown_clauses.append(clause)

    if all_clauses_true:
        return model

    # Finding pure symbols
    pure_symbol = find_pure_symbol(symbols, unknown_clauses)
    if not pure_symbol[0] == 'null':
        model_pure_symbol = model
        model_pure_symbol[pure_symbol[0]] = pure_symbol[1]

        symbols.remove(pure_symbol[0])
        return dpll(clauses, symbols, model_pure_symbol)

    # Finding unit clauses
    unit_clause_symbol = find_unit_clause(unknown_clauses, model)
    if not unit_clause_symbol[0] == 'null':
        model_unit_clause_symbol = model
        model_unit_clause_symbol[unit_clause_symbol[0]] = unit_clause_symbol[1]

        symbols.remove(unit_clause_symbol[0])
        return dpll(clauses, symbols, model_unit_clause_symbol)

    if len(symbols) == 0:
        print_error('NOT SURE OF SOME SYMBOLS: POSSIBLE SYMBOL MISMATCH')
    next_symbol = symbols.pop()

    # IF SYMBOL IS MADE TRUE
    model_symbol_true = model
    model_symbol_true[next_symbol] = True

    symbol_true = dpll(clauses, symbols, model_symbol_true)
    if symbol_true:
        return symbol_true

    # IF SYMBOL IS MADE FALSE
    model_symbol_false = model
    model_symbol_false[next_symbol] = False

    symbol_false = dpll(clauses, symbols, model_symbol_false)
    if symbol_false:
        return symbol_false

    # IF BOTH OF THEM RETURNED FALSE => RETURN FALSE
    return False


def remove_duplicate_symbols(curr_list):
    for i in range(0, len(curr_list)):
        for j in range((i+1), len(curr_list)):
            if curr_list[i] == curr_list[j]:
                del curr_list[j]
    return curr_list



def add_literal_to_symbols(literal, symbols_list):
    if is_symbol(literal):
        symbols_list.extend(literal)
    else:
        symbols_list.extend(literal[1])


# Finds symbols from the cnf
def get_symbols(input_cnf):

    symbols_list = list()

    if is_literal(input_cnf):
        add_literal_to_symbols(input_cnf, symbols_list)

    else:
        for and_arg in arguments(input_cnf):
            if is_literal(and_arg):
                add_literal_to_symbols(and_arg, symbols_list)
            else:
                for or_arg in arguments(and_arg):
                    if is_literal(or_arg):
                        add_literal_to_symbols(or_arg, symbols_list)

    # REMOVING DUPLICATES
    no_dup_symbol_list = list(set(symbols_list))

    return no_dup_symbol_list

# Solves the input cnf passed
def solve_sat(input_cnf):

    clauses = list()
    if is_literal(input_cnf):
        clauses.append(input_cnf)
    elif operator(input_cnf) == 'or':
        clauses.append(input_cnf)
    elif operator(input_cnf) == 'and':
        clauses.extend(arguments(input_cnf))

    symbols = get_symbols(input_cnf)

    model = dict()

    return dpll(clauses, symbols, model)


def convert_to_str(model):
    list_str = list()
    if model == False:
        list_str.append("false")
    else:

        list_str.append("true")

        for key in model:
            key_str = str(key)

            if model[key] == True:
                key_str = key_str + "=true"
                list_str.append(key_str)
            else:
                key_str = key_str + "=false"
                list_str.append(key_str)

    return str(list_str)

# -------------------  Start of code -------------------------
# Check for arguments  count
if len(sys.argv) != 3:
    print('error')
    exit()


f_input = open(sys.argv[2], 'r')
f_output = open('CNF_satisfiability.txt', 'w')


line_count = f_input.readline()
line_count = eval(line_count)
for i in range(0, line_count):
    input_cnf_text = f_input.readline()
    output_sat = solve_sat(eval(input_cnf_text))
    output_sat_text = convert_to_str(output_sat)
    f_output.write(output_sat_text + '\n')
    print(output_sat_text)
