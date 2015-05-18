__author__ = 'Tanmay'

import sys

def find_P(no_symptoms, p_disease, p_sym_d, p_sym_not_d, tests):
    p_disease_sym = p_disease
    for i in range(0, no_symptoms):
        if tests[i] == 'T':
            p_disease_sym *= p_sym_d[i]
        elif tests[i] == 'F':
            p_disease_sym *= (1-p_sym_d[i])

    p_not_disease_sym = 1-p_disease
    for i in range(0, no_symptoms):
        if tests[i] == 'T':
            p_not_disease_sym *= p_sym_not_d[i]
        elif tests[i] == 'F':
            p_not_disease_sym *= (1-p_sym_not_d[i])

    # Normalise
    sum = p_disease_sym + p_not_disease_sym
    p_disease_sym /= sum
    p_not_disease_sym /= sum

    #print p_disease_sym
    #print p_not_disease_sym

    return p_disease_sym


def find_range(no_symptoms, p_disease, p_sym_d, p_sym_not_d, tests):

    for i in range(0, no_symptoms):

        if tests[i] == 'U':

            tests_try = tests[:]

            tests_try[i] = 'T'
            range_t = find_range(no_symptoms, p_disease, p_sym_d, p_sym_not_d, tests_try)

            tests_try[i] = 'F'
            range_f = find_range(no_symptoms, p_disease, p_sym_d, p_sym_not_d, tests_try)

            min_range = min(range_t[0], range_f[0])
            max_range = max(range_t[1], range_f[1])

            final_range = [min_range, max_range]

            return final_range

    P = find_P(no_symptoms, p_disease, p_sym_d, p_sym_not_d, tests)

    return [P, P]

def num2str(num):
    round_num = round(num, 4)
    string = '%.4f'%round_num
    return string

# --------------------------  MAIN -----------------------------
def main():

    diseases_list = list()
    no_symptoms_list = list()
    P_disease_list = list()

    all_symptoms_list = list()
    all_P_sym_d_list = list()
    all_P_sym_not_d_list = list()

    f_input = open(sys.argv[2], 'r')
    split_slash = sys.argv[2].split('/')
    [fname, fext] = split_slash[-1].split('.')
    write_name = (fname+'_inference.'+fext)
    f_output = open(write_name, 'w+')

    # FIRST LINE LIST

    line_list = (f_input.readline()).split()
    no_diseases = int(line_list[0])
    no_patients = int(line_list[1])

    # DISEASES LIST

    for i in range(0, no_diseases):
        line_list = (f_input.readline()).split()

        diseases_list.append(line_list[0])
        no_symptoms_list.append(int(line_list[1]))
        P_disease_list.append(float(line_list[2]))

        line_eval = eval(f_input.readline())
        all_symptoms_list.append(line_eval)

        line_eval = eval(f_input.readline())
        all_P_sym_d_list.append(line_eval)

        line_eval = eval(f_input.readline())
        all_P_sym_not_d_list.append(line_eval)

    # PATIENTS TESTS LIST
    all_patients_diseases_tests_list = list()

    for i in range(0, no_patients):
        all_diseases_tests_list = list()

        for j in range(0, no_diseases):
            line_eval = eval(f_input.readline())
            all_diseases_tests_list.append(line_eval)

        all_patients_diseases_tests_list.append(all_diseases_tests_list)



    for i in range(0, no_patients):

        P_disease_sym_dict = dict()
        q3_P_disease_sym_dict = dict()
        min_max_P_disease_sym_dict = dict()

        for j in range(0, no_diseases):

            disease = diseases_list[j]
            no_symptoms = no_symptoms_list[j]
            P_disease = P_disease_list[j]

            symptoms = all_symptoms_list[j]

            P_sym_d = all_P_sym_d_list[j]
            P_sym_not_d = all_P_sym_not_d_list[j]

            tests = all_patients_diseases_tests_list[i][j]

            #disease = 'diabetes'
            #no_symptoms = 3
            #P_disease = 0.13

            #symptoms = ['thirst', 'weightloss', 'blurredvision']

            #P_sym_d = [0.6, 0.7, 0.9]
            #P_sym_not_d = [0.2, 0.3, 0.015]

            #tests = ['T', 'F', 'U']

            # -------------------------   QUESTION  1 ---------------------------------------------------------

            P_disease_sym = find_P(no_symptoms, P_disease, P_sym_d, P_sym_not_d, tests)
            P_disease_sym_dict[disease] = (num2str(P_disease_sym))

            # -------------------------   QUESTION  2 ---------------------------------------------------------

            [min, max] = find_range(no_symptoms, P_disease, P_sym_d, P_sym_not_d, tests)
            [min_str, max_str] = [num2str(min), num2str(max)]
            min_max_P_disease_sym_dict[disease] = [min_str, max_str]

            # -------------------------   QUESTION  3 ---------------------------------------------------------
            min_P_disease_sym = P_disease_sym
            max_P_disease_sym = P_disease_sym

            largest_inc_test_name = 'None'
            largest_inc_test_value = 'N'

            largest_dec_test_name = 'None'
            largest_dec_test_value = 'N'

            for k in range(0, no_symptoms):
                if tests[k] == 'U':
                    tests_try = tests[:]

                    tests_try[k] = 'T'
                    P_disease_sym_try_t = find_P(no_symptoms, P_disease, P_sym_d, P_sym_not_d, tests_try)

                    tests_try[k] = 'F'
                    P_disease_sym_try_f = find_P(no_symptoms, P_disease, P_sym_d, P_sym_not_d, tests_try)


                    #  LARGEST DEC
                    if P_disease_sym_try_t <= min_P_disease_sym:
                        if P_disease_sym_try_t < min_P_disease_sym or sorted([largest_dec_test_name, symptoms[k]], key=str.lower)[0] == symptoms[k]:
                            largest_dec_test_name = symptoms[k]
                            largest_dec_test_value = 'T'
                            min_P_disease_sym = P_disease_sym_try_t

                    if P_disease_sym_try_f <= min_P_disease_sym:
                        if P_disease_sym_try_f < min_P_disease_sym or sorted([largest_dec_test_name, symptoms[k]], key=str.lower)[0] == symptoms[k]:
                            largest_dec_test_name = symptoms[k]
                            largest_dec_test_value = 'F'
                            min_P_disease_sym = P_disease_sym_try_f

                    # LARGEST INC
                    if P_disease_sym_try_t >= max_P_disease_sym:
                        if P_disease_sym_try_t > max_P_disease_sym or sorted([largest_inc_test_name, symptoms[k]], key=str.lower)[0] == symptoms[k]:
                            largest_inc_test_name = symptoms[k]
                            largest_inc_test_value = 'T'
                            max_P_disease_sym = P_disease_sym_try_t

                    if P_disease_sym_try_f >= max_P_disease_sym:
                        if P_disease_sym_try_f > max_P_disease_sym or sorted([largest_inc_test_name, symptoms[k]], key=str.lower)[0] == symptoms[k]:
                            largest_inc_test_name = symptoms[k]
                            largest_inc_test_value = 'F'
                            max_P_disease_sym = P_disease_sym_try_f

            q3_P_disease_sym_dict[disease] = [largest_inc_test_name, largest_inc_test_value, largest_dec_test_name, largest_dec_test_value]

        print("Patient-"+ str(i+1) + ":")
        print P_disease_sym_dict
        print min_max_P_disease_sym_dict
        print q3_P_disease_sym_dict

        f_output.write("Patient-"+ str(i+1) + ":\n")
        f_output.write(str(P_disease_sym_dict) + '\n')
        f_output.write(str(min_max_P_disease_sym_dict) + '\n')
        f_output.write(str(q3_P_disease_sym_dict) + '\n')
main()