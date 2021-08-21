import re
import sys

f = open('calc.in', 'r')
content = f.read()
full_list = content.split('\n')
keyWords = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'sifir', 'bir', 'iki', 'uc', 'dort', 'bes', 'alti', 'yedi', 'sekiz', 'dokuz', 'dogru', 'yanlis', '+', '-', '*', 'arti', 'eksi', 'carpi', 've', 'veya', '(', ')', 'ac-parantez', 'kapa-parantez', 'AnaDegiskenler', 'YeniDegiskenler', 'Sonuc', 'degeri', 'olsun', 'nokta']

def wrong():
    f.close()
    output = open('calc.out', 'w')
    output.write('Dont Let Me Down')
    output.close()
    sys.exit()

def is_repeating(lst):
    reps = {}
    for i in lst:
        if i in reps:
            reps[i] += 1
        else:
            reps[i] = 1
    for value in reps.values():
        if value > 1:
            return True
    return False

# the titles
if not re.search(r'\bAnaDegiskenler\b', content) or not re.search(r'\bYeniDegiskenler\b',content) or not re.search(r'\bSonuc\b',content):
    wrong()

var_list = re.findall(r'[a-zA-Z0-9]{1,10}(?=\s+degeri)', content)

# cannot assign a variable twice
if is_repeating(var_list):
    wrong()

# cannot use key words as a variable
for j in var_list:
    if j in keyWords:
        wrong()

for ind in range(len(full_list)):
    if full_list[ind].strip() == 'AnaDegiskenler':
        ind_in = ind
    elif full_list[ind].strip() == 'YeniDegiskenler':
        ind_mid = ind
    elif full_list[ind].strip() == 'Sonuc':
        ind_final = ind

intro_vars = {}
for k in range(ind_in + 1, ind_mid):
    if re.search('.+', full_list[k]) != None:
        check = re.search(r'^[a-zA-Z0-9]{1,10}\s+degeri\s+(([0-9]|sifir|bir|iki|uc|dort|bes|alti|yedi|sekiz|dokuz)|(dogru|yanlis)|(\d\.\d)|((sifir|bir|iki|uc|dort|bes|alti|yedi|sekiz|dokuz)\s+nokta\s+(sifir|bir|iki|uc|dort|bes|alti|yedi|sekiz|dokuz)))\s+olsun$',full_list[k].strip())

        if check == None:
            wrong()

        # trying to capture the variable names
        if len(re.findall(r'\b(dogru|yanlis)\b', full_list[k])) != 0:
            intro_vars[''.join(re.findall(r'[a-zA-Z0-9]{1,10}(?=\s+degeri)', full_list[k]))] = '_'
        elif len(re.findall(r'\b([0-9]|sifir|bir|iki|uc|dort|bes|alti|yedi|sekiz|dokuz|(\d\.\d)|((sifir|bir|iki|uc|dort|bes|alti|yedi|sekiz|dokuz)\s+nokta\s+(sifir|bir|iki|uc|dort|bes|alti|yedi|sekiz|dokuz)))\b', full_list[k])) != 0:
            intro_vars[''.join(re.findall(r'[a-zA-Z0-9]{1,10}(?=\s+degeri)', full_list[k]))] = '#'

my_vars = {}
para_num1 = 0
for l in range(ind_mid + 1, ind_final):

    if re.search('.+', full_list[l]) != None:

        if len(re.findall(r'(\B#\B|\b_\b)', full_list[l])) != 0:
            wrong()

        new_list = full_list[l].split()
        for ii in range(len(new_list)):
            if new_list[ii] in intro_vars:
                new_list[ii] = intro_vars[new_list[ii]]
            elif new_list[ii] in my_vars:
                new_list[ii] = my_vars[new_list[ii]]
        my_str = ' '.join(new_list)

        lst = re.findall(r'^[a-zA-Z0-9]{1,10}\s+degeri\s+(((#|_|[0-9]|sifir|bir|iki|uc|dort|bes|alti|yedi|sekiz|dokuz|dogru|yanlis|(\d\.\d)|((sifir|bir|iki|uc|dort|bes|alti|yedi|sekiz|dokuz)\s+nokta\s+(sifir|bir|iki|uc|dort|bes|alti|yedi|sekiz|dokuz)))|(ac-parantez|kapa-parantez|\)|\(|\*|-|\+|arti|carpi|eksi|ve|veya))\s+)+olsun$', my_str.strip())
        if len(lst) == 0:
            wrong()

        # there must be a non-value between two values
        if len(re.findall(r'\s((#|_|dogru|yanlis|[0-9]|sifir|bir|iki|uc|dort|bes|alti|yedi|sekiz|dokuz|((sifir|bir|iki|uc|dort|bes|alti|yedi|sekiz|dokuz)\s+nokta\s+(sifir|bir|iki|uc|dort|bes|alti|yedi|sekiz|dokuz))|\d\.\d)\s+){2}', my_str)) != 0:
            wrong()

        #paranthesis rules
        if len(re.findall(r'(\(|ac-parantez|\)|kapa-parantez)', my_str)) != 0:

            for g in my_str.split():
                if g == '(' or g == 'ac-parantez':
                    para_num1 += 1
                elif g == ')' or g == 'kapa-parantez':
                    para_num1 -= 1
                    if para_num1 < 0:
                        wrong()

            if (len(re.findall(r'\(', my_str)) + len(re.findall('ac-parantez', my_str))) != (len(re.findall(r'\)', my_str)) + len(re.findall('kapa-parantez', my_str))):
                wrong()

            if re.search(r'(\(|ac-parantez)\s*(\)|kapa-parantez)', my_str) != None:
                wrong()

            if re.search(r'(\(|ac-parantez)\s+(\*|-|\+|arti|carpi|eksi|ve|veya)\s+(\)|kapa-parantez)', my_str) != None:
                wrong()

            if re.search(r'(\(|ac-parantez)\s+(\*|-|\+|arti|carpi|eksi|ve|veya)\s+(\(|ac-parantez)', my_str) != None:
                wrong()

            if re.search(r'(\)|kapa-parantez)\s+(\*|-|\+|arti|carpi|eksi|ve|veya)\s+(\)|kapa-parantez)',my_str) != None:
                wrong()

        # there should be a non-operator between two operators
        if re.search(r'(\*|-|\+|arti|carpi|eksi|ve|veya)\s+(\*|-|\+|arti|carpi|eksi|ve|veya)', my_str) != None:
            wrong()

        # arithmetic and logic expressions cannot be together
        if len(re.findall(r'\s(\*|-|\+|arti|carpi|eksi)\s', my_str)) != 0:
            if len(re.findall(r'\b(_|dogru|yanlis|ve|veya)\b', my_str)) != 0:
                wrong()
        if len(re.findall(r'\b(ve|veya)\b', my_str)) != 0:
            if len(re.findall(r'\s([0-9]|\*|carpi|-|eksi|\+|arti|#|sifir|bir|iki|uc|dort|bes|alti|yedi|sekiz|dokuz|(\d\.\d)|((sifir|bir|iki|uc|dort|bes|alti|yedi|sekiz|dokuz)\s+nokta\s+(sifir|bir|iki|uc|dort|bes|alti|yedi|sekiz|dokuz)))\s', my_str)) != 0:
                wrong()

        if len(re.findall(r'[a-zA-Z0-9]{1,10}(?=\s+degeri\s)', my_str)) != 0:
            if len(re.findall(r'\s(ve|veya|_|dogru|yanlis)\s', my_str)) != 0:
                my_vars[''.join(re.findall(r'\s*[a-zA-Z0-9]{1,10}(?=\s+degeri\s)', my_str))] = '_'
            elif len(re.findall(r'\s+(\*|-|\+|carpi|arti|eksi|#|[0-9]|sifir|bir|iki|uc|dort|bes|alti|yedi|sekiz|dokuz|(\d\.\d)|((sifir|bir|iki|uc|dort|bes|alti|yedi|sekiz|dokuz)\s+nokta\s+(sifir|bir|iki|uc|dort|bes|alti|yedi|sekiz|dokuz)))\s+', my_str)) != 0:
                my_vars[''.join(re.findall(r'\s*[a-zA-Z0-9]{1,10}(?=\s+degeri\s)', my_str))] = '#'

para_num2 = 0
fin_count = 0
for m in range(ind_final+1, len(full_list)):
    if len(re.findall(r'(.+)', full_list[m])) != 0:
        fin_count += 1
        if fin_count > 1:
            wrong()

        if len(re.findall(r'(\B#\B|\b_\b)', full_list[m])) != 0:
            wrong()

        new_list = full_list[m].split()
        for ii in range(len(new_list)):
            if new_list[ii] in intro_vars:
                new_list[ii] = intro_vars[new_list[ii]]
            elif new_list[ii] in my_vars:
                new_list[ii] = my_vars[new_list[ii]]
        my_str = ' '.join(new_list)

        if len(re.findall(r'^((\(|\)|ac-parantez|kapa-parantez|#|_|[0-9]|sifir|bir|iki|uc|dort|bes|alti|yedi|sekiz|dokuz|\d\.\d|((sifir|bir|iki|uc|dort|bes|alti|yedi|sekiz|dokuz)\s+nokta\s+(sifir|bir|iki|uc|dort|bes|alti|yedi|sekiz|dokuz))|arti|\+|carpi|\*|eksi|-|ve|veya|dogru|yanlis)\s*){1,}$', my_str)) == 0:
            wrong()

        # parantheses
        if len(re.findall(r'(\(|ac-parantez|\)|kapa-parantez)', my_str)) != 0:

            for g in my_str.split():
                if g == '(' or g == 'ac-parantez':
                    para_num2 += 1
                elif g == ')' or g == 'kapa-parantez':
                    para_num2 -= 1
                    if para_num2 < 0:
                        wrong()

            if len(re.findall('\(', my_str)) + len(re.findall('ac-parantez', my_str)) != len(re.findall('\)', my_str)) + len(re.findall('kapa-parantez', my_str)):
                wrong()

            if re.search(r'(\(|ac-parantez)\s*(\)|kapa-parantez)', my_str) != None:
                wrong()

            if re.search(r'(\(|ac-parantez)\s+(\*|-|\+|arti|carpi|eksi|ve|veya)\s+(\)|kapa-parantez)', my_str) != None:
                wrong()

            if re.search(r'(\(|ac-parantez)\s+(\*|-|\+|arti|carpi|eksi|ve|veya)\s+(\(|ac-parantez)', my_str) != None:
                wrong()

            if re.search(r'(\)|kapa-parantez)\s+(\*|-|\+|arti|carpi|eksi|ve|veya)\s+(\)|kapa-parantez)', my_str) != None:
                wrong()

        # there must be a non-value between two values
        if len(re.findall(r'\b((#|_|dogru|yanlis|[0-9]|sifir|bir|iki|uc|dort|bes|alti|yedi|sekiz|dokuz|((sifir|bir|iki|uc|dort|bes|alti|yedi|sekiz|dokuz)\s+nokta\s+(sifir|bir|iki|uc|dort|bes|alti|yedi|sekiz|dokuz))|\d\.\d)\s+){2}', my_str)) != 0:
            wrong()

        # there must be a non-operator between two operators
        if re.search(r'(\*|-|\+|arti|carpi|eksi|ve|veya)\s+(\*|-|\+|arti|carpi|eksi|ve|veya)', my_str) != None:
            wrong()

        #arithmetic and logical expressions cannot be together
        if len(re.findall(r'\s(\*|-|\+|arti|carpi|eksi)\s', my_str)) != 0:
            if len(re.findall(r'\s(_|dogru|yanlis|ve|veya)\s', my_str)) != 0:
                wrong()
        if len(re.findall(r'\b(ve|veya)\b', my_str)) != 0:
            if len(re.findall(r'\s([0-9]|\*|carpi|-|eksi|\+|arti|#|sifir|bir|iki|uc|dort|bes|alti|yedi|sekiz|dokuz|(\d\.\d)|((sifir|bir|iki|uc|dort|bes|alti|yedi|sekiz|dokuz)\s+nokta\s+(sifir|bir|iki|uc|dort|bes|alti|yedi|sekiz|dokuz)))', my_str)) != 0:
                wrong()

f.close()
output = open('calc.out', 'w')
output.write('Here Comes the Sun')
output.close()