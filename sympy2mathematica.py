import re
import ast


def replace_underscore(line: str):
    def helper(content_with_underscore: str):
        left, right = content_with_underscore.split('_')
        return 'Subscript[{}, {}]'.format(left, right)

    p = re.compile(r'\w+_\w+', re.S)
    while True:
        matched = p.search(line)
        if not matched:
            break
        left, right = line[:matched.start()], line[matched.end():]
        m = matched.group()
        line = left.strip() + helper(m).strip() + right.strip()
    return line


def find_all_in_brace(s: str):
    res = []
    in_brace = False 
    for ch in s:
        if ch == '(':
            in_brace = True 
        elif ch == ')':
            in_brace = False 
        elif in_brace:
            res.append(ch)
        elif ch == '\n':
            res.append('\0')
    return [line for line in ''.join(res).split('\0') if line.strip()]


def read_python_code(filename):
    """deprecated"""
    with open(filename) as f:
        code = ''
        for line in f:
            line = line.strip()
            if not line:
                continue

            if line.startswith('from') or line.startswith('import'):
                continue

            code += line
            if is_valid_code(code):
                yield code
                code = ''


def is_valid_code(line: str):
    try:
        ast.parse(line)
    except SyntaxError:
        return False
    else:
        return True


def transform_in_brace(s: str):
    s = s.strip()
    p = re.compile(r'\w+\s?=')
    variables = p.findall(s)
    return '\n'.join(v +e.replace('[', '{').replace(']', '}') for v, e in zip(variables, find_all_in_brace(s)))


def transform_for_A(s: str):
    """
    ** ==> ^
    []  ==> [[]]
    replace "_"
    e.g.: A11_11 = A11  ~~~~~>   Subscript[A11, 11] = A11
    """
    s = s.strip()
    res = []
    for line in s.split('\n'):
        line = line.replace('**', '^').replace('[', '[[').replace(']', ']]')
        try:
            equals_idx = line.index('=')
        except ValueError:
            res.append(line)
            continue
        else:
            res.append(replace_underscore(line))
    return '\n'.join(res)


s = '''
Bmat = Matrix([
        [Omega2**2+Omega3**2-gamma1, -
            (2*Omega1*Omega2)/(1+h1**2), -(2*Omega1*Omega3)/(1+h1**2*h2**2)],
        [-(2*h1**2*Omega1*Omega2)/(1+h1**2), Omega1**2 +
         Omega3**2-gamma2, -(2*Omega1*Omega3)/(1+h2**2)],
        [-(2*h1**2*h2**2*Omega1*Omega3)/(1+h1**2*h2**2), -
         (2*h2**2*Omega1*Omega3)/(1+h2**2), Omega1**2+Omega2**2-gamma3]
    ])
'''

s = '''
A12 = (1-(1+nv)/(2*h1**2*h2**4+(3+h2**2+h1**2*h2**2)*(1+nv)))*Bmat[0, 1]*h1**2/2
A13 = (1-(1+nv)*h2**2/(2*h1**2+(1+3*h2**2+h1**2*h2**2)*(1+nv)))*Bmat[0, 2]*h1**2*h2**2/2
A23 = (1-(1+nv)*h1**4*h2**2/(2+(3+h1**2+h1**2*h2**2+3*h1**4*h2**2)*(1+nv)))*Bmat[1, 2]*h1**2*h2**2/2

B001 = (Bmat[0, 0]+Bmat[1, 1]-Bmat[2, 2])/2
B010 = (Bmat[0, 0]-Bmat[1, 1]+Bmat[2, 2])/2
B100 = (-Bmat[0, 0]+Bmat[1, 1]+Bmat[2, 2])/2

A11_11 = A11
A11_12 = A12
A11_13 = A13
A11_22 = h1**2*A11 + 2*A22 -  A33/h2**2 - h1**2*B001
A11_23 = 3*A23 - h1**2*h2**2*Bmat[1, 2]
A11_33 = h1**2*h2**2*A11 - h2**2*A22 + 2*A33 - h1**2*h2**2*B010

A22_11 = 2*A11 + A22/h1**2 - A33/(h1**2*h2**2) - B001
A22_12 = A12
A22_13 = 3*A13 - h1**2*h2**2*Bmat[0, 2]
A22_22 = A22
A22_23 = A23
A22_33 = -h1**2*h2**2*A11 + h2**2*A22 + 2*A33 - h1**2*h2**2*B100

A33_11 = 2*A11 - A22/h1**2 + A33/(h1**2*h2**2) - B010
A33_12 = 3*A12 - h1**2*Bmat[0, 1]
A33_13 = A13
A33_22 = -h1**2*A11 + 2*A22 + A33/h2**2 - h1**2*B100
A33_23 = A23
A33_33 = A33

A12_11 = 0
A12_12 = -h1*(A11 + A22/h1**2 - A33/h1**2/h2**2 - B001)
A12_13 = -(2*A23 - h1**2*h2**2*Bmat[1, 2])/h1
A12_22 = 0
A12_23 = -h1*(2*A13-h1**2*h2**2*Bmat[0, 2])
A12_33 = 2*h1**2*h2**2*(2*A12/h1 - h1*Bmat[0, 1])

A23_11 = 2*(2*A23/h1/h2 - h1*h2*Bmat[1, 2])/h1
A23_12 = -h1*(2*A13/h1/h2 - h1*h2*Bmat[0, 2])
A23_13 = -h1*h2*(2*A12/h1 - h1*Bmat[0, 1])
A23_22 = 0
A23_23 = h1**2*h2*(A11 - A22/h1**2 - A33/h1**2/h2**2 + B100)
A23_33 = 0

A13_11 = 0
A13_12 = -2*A23/h1/h2 + h1*h2*Bmat[1, 2]
A13_13 = -h1*h2*(A11 - A22/h1**2 + A33/h1**2/h2**2 - B010)
A13_22 = 2*h1**2*(2*A13/h1/h2 - h1*h2*Bmat[0, 2])
A13_23 = -h1*h2*(2*A12 - h1**2*Bmat[0, 1])
A13_33 = 0
'''


s = """
S_00 = Matrix([[A11, A12, A13], [A12, A22, A23], [A13, A23, A33]])
S_11 = Matrix([[A11_11, A11_12, A11_13], [
              A11_12, A11_22, A11_23], [A11_13, A11_23, A11_33]])
S_12 = Matrix([[A12_11, A12_12, A12_13], [
              A12_12, A12_22, A12_23], [A12_13, A12_23, A12_33]])
S_13 = Matrix([[A13_11, A13_12, A13_13], [
              A13_12, A13_22, A13_23], [A13_13, A13_23, A13_33]])
S_22 = Matrix([[A22_11, A22_12, A22_13], [
              A22_12, A22_22, A22_23], [A22_13, A22_23, A22_33]])
S_23 = Matrix([[A23_11, A23_12, A23_13], [
              A23_12, A23_22, A23_23], [A23_13, A23_23, A23_33]])
S_33 = Matrix([[A33_11, A33_12, A33_13], [
              A33_12, A33_22, A33_23], [A33_13, A33_23, A33_33]])


"""

s = '''
sigma = a**2*S_00 - x**2*S_11 - y**2/h1**2*S_22 - z**2/h1**2 / h2**2*S_33 - x*y/h1*S_12 - x*z/h1/h2*S_13 - y*z/h1**2/h2*S_23
'''

print(transform_for_A(s))
