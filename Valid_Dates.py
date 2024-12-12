# PROJECT 3: VALID DATES -------------------------------

# PART A: BRUTE FORCE -------------------------------

# HELPER FUNCTIONS ------------------------------- 

# factorial: computes n!
def factorial (n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial (n - 1)

# combination: computes n choose r using combinatorics formula
def combination (n, r):
    return int(factorial (n) / (factorial (n - r) * factorial (r)))

# get_sibling: returns sibling of given brother or sister
def get_sibling(person):
    if "x" in person:
        return "y_" + person[-1]
    if "y" in person:
        return "x_" + person[-1]
    if "a" in person:
        return "b_" + person[-1]
    if "b" in person:
        return "a_" + person[-1]

# insert_elem_into_list: generates all possible ways in which element can be inserted into list
def insert_elem_into_list(n, l):
    combinations = []
    for i in range(len(l) + 1):
        sublist = l.copy()
        sublist.insert(i,n)
        combinations.append(sublist)
    return combinations

# insert_elem_into_sublists: generates all possible ways in which element can be inserted into sublists
def insert_elem_into_sublists(n,l):
    combinations = []
    for sublist in l:
        new_combinations = insert_elem_into_list(n,sublist)
        for i in range(len(new_combinations)):
            combinations.append(new_combinations[i])
    return combinations

# permute_sisters: generates all possible permutations of sisters
def permute_sisters(n):
    perms = [[]]
    for i in range (1, n + 1):
        perms = insert_elem_into_sublists(("a_" + str(i)), perms)
        perms = insert_elem_into_sublists(("b_" + str(i)), perms)
    return perms

# valid_date: determines if given date is valid (True) based on current date assignemtns
def valid_date(brother, sister, dates):
    brother_sibling = get_sibling(brother)
    sibling_date = None
    for i in range(len(dates)):
        if dates[i][0] == brother_sibling:
            sibling_date = dates[i][1]
    return sibling_date is None or not (get_sibling(sister) == sibling_date)
    
# --------------------------------------------------

# generate_dates: generates all valid dates (brute force algorithm)
def generate_dates(n):
    # base cases: n = 0 or n = 1
    if n == 0:
        print("Base Case: 1 arrangements!")
        return
    if n == 1:
        print("Base Case: 0 arrangements!")
        return
    brothers = []
    sister_perms = permute_sisters(n)
    for i in range (1, n + 1):
        brothers.append("x_" + str(i))
        brothers.append("y_" + str(i))
    all_perms = []
    for perm in sister_perms:
        contradictions = False
        single_perm = []
        for i in range(len(perm)):
            curr_brother = brothers[i]
            curr_sister = perm[i]
            if not valid_date(curr_brother, curr_sister, single_perm):
                contradictions = True
                break
            else:
                single_perm.append([brothers[i], perm[i]])
        if contradictions:
            continue
        else:
            all_perms.append(single_perm)
    # print all possible combinations
    for perm in all_perms:
        print(perm)
    print(f"Valid Arrangements (Brute Force): {len(all_perms)}")

#generate_dates(2)
#generate_dates(3)
#generate_dates(4)

# PART B: RECURRENT CALCULATION O(N) -------------------------------

# recurrence_r: calculates valid dating arrangements R(n) that form cycle (recurrence formula)
def recurrence_r (n):
    # base cases: n = 0, 1, 2
    r_array = [0, 0, 16]
    for i in range (3, n + 1):
        r_array.append(2 * i * 2 * (i - 1) * r_array[i - 1])
    return r_array

#print("Valid Cycle Arrangements (Recurrence):", recurrence_r(2))
#print("Valid Cycle Arrangements (Recurrence):", recurrence_r(3))
#print("Valid Cycle Arrangements (Recurrence):", recurrence_r(4))
#print("Valid Cycle Arrangements (Recurrence):", recurrence_r(5))

# close_form_r: calculates valid dating arrangements R(n) that form cycle (close form formula)
def close_form_r(n):
    # base cases
    if n == 0:
        return 1
    if n == 1:
        return 0
    return (2 ** (2 * n - 1)) * factorial(n) * factorial(n - 1)

#print("Valid Cycle Arrangements (Close Form):", close_form_r(2))
#print("Valid Cycle Arrangements (Close Form):", close_form_r(3))
#print("Valid Cycle Arrangements (Close Form):", close_form_r(4))

def recurrence_t_with_r(n):
    # base cases: n = 0, 1
    t_array = [1, 0]

    for i in range(2, n + 1):
        total = 0
        for k in range (2, i + 1):
            total = total + combination(i, k) * combination(i - 1, k - 1) * close_form_r(k) * t_array[i - k]
        t_array.append(total)
    return t_array

#print("Valid Arrangements (Recurrence with T(n - k) and R(n)):", recurrence_t_with_r(3))
#print("Valid Arrangements (Recurrence with T(n - k) and R(n)):", recurrence_t_with_r(4))
#print("Valid Arrangements (Recurrence with T(n - k) and R(n)):", recurrence_t_with_r(5))

# PART C: RECURRENT CALCULATION O(1) -------------------------------

def recurrence_t(n):
    # base cases
    t_array = [1, 0, 16]

    for i in range (3, n + 1):
        t_array.append((2 * i) * (2 * i - 2) * ((2 * i - 2) * t_array[i - 2] + t_array[i - 1]))
    return t_array

#print("Valid Arrangements (Recurrence with T(n - 1) and T(n - 2)):", recurrence_t(3))
#print("Valid Arrangements (Recurrence with T(n - 1) and T(n - 2)):", recurrence_t(4))
#print("Valid Arrangements (Recurrence with T(n - 1) and T(n - 2)):", recurrence_t(15))




