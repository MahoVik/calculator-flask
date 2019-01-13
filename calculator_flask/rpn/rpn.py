

acceptable_symbols = [
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '-', '*', '/', '^', '.', '(', ')'
]
ops = ['+', '-', '*', '/', '^']
special_symbols = ['(', ')']
priority = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}

def split_on_elements(expression):
    """Example: "10+10 * 10" -> ["10", "+", "10", "*", "10"]

    :param expression:
    :return:
    """
    num = ''
    symbols = []

    for sublist in expression.split():
        for elem in sublist:
            if elem not in acceptable_symbols:
                raise RuntimeError('Typed invalid symbol: %s' % elem)
            if elem.isdigit() or elem == '.':
                num += elem
            else:
                if num:
                    symbols.append(num)
                num = ''
                symbols.append(elem)
        if num:
            symbols.append(num)
            num = ''

    if len(num) > 0:
        symbols.append(num)

    return symbols


def build_rpn(symbols):
    output_str = []
    stack = []
    for sym in symbols:
        if sym in ops:
            if len(stack) > 0:
                top_stack = stack[-1]
                while top_stack in ops and priority[top_stack] > priority[sym]:
                    output_str.append(stack.pop())
                    if len(stack) == 0:
                        break
                    top_stack = stack[-1]
            stack.append(sym)

        elif sym == '(':
            stack.append(sym)
        elif sym == ')':
            if len(stack) == 0:
                raise RuntimeError('Error, mismatched brackets')
            top_stack = stack[-1]
            while top_stack != '(':
                output_str.append(stack.pop())
                if len(stack) == 0:
                    raise RuntimeError('Error, mismatched brackets')
                top_stack = stack[-1]
            stack.pop()
        else:
            output_str.append(sym)

    while len(stack) != 0:
        top_stack = stack[-1]
        if top_stack in ops:
            output_str.append(stack.pop())
        else:
            raise RuntimeError('Error, mismatched brackets')
    return output_str


def stack_calculations(output_str):
    stack = []
    for sym in output_str:
        if sym not in ops:
            stack.append(float(sym))
        if sym in ops:
            if len(stack) < 2:
                raise RuntimeError('Error: mismatched operators or operands')
            if sym == '+':
                res = stack[-2] + stack[-1]
                stack[-2:] = [res]
            if sym == '-':
                res = stack[-2] - stack[-1]
                stack[-2:] = [res]
            if sym == '*':
                res = stack[-2] * stack[-1]
                stack[-2:] = [res]
            if sym == '/':
                res = stack[-2] / stack[-1]
                stack[-2:] = [res]
            if sym == '^':
                res = stack[-2] ** stack[-1]
                stack[-2:] = [res]
    if len(stack) > 1:
        raise RuntimeError('Error: mismatched operators or operands')
    return stack[0]


def evaluate(expression):
    split = split_on_elements(expression)
    rpn = build_rpn(split)
    answer = stack_calculations(rpn)
    return answer
