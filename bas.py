#! /usr/bin/env python3.6

import sys
readline = sys.stdin.readline

NUMBER = 1
STRING = 2
KEYWORD = 3
OPERATOR = 4
VARIABLE = 5
COLON = 6
FUNCTION = 7

class Brain:
    def __init__(t_for):
        self.t_for = t_for

    def exec():
        print("Not implemented")
        sys.exit(1)


class DoPrnt(Brain):
    def __init__():
        super(KEYWORD);

    def exec():
        t = next_token()
        while t and t != ":":
            if t.ttype == STRING:
                print("%s" % t.tval, end="")
            else:
                print("%s" % eval_expression(t), end="")

            t = next_token()
        print("")

operators = {
    '*' : 1,
    '/' : 1,
    '+' : 2,
    '-' : 2,
    '(' : 3,
}

vars = dict()

keywords = {
    'ABS('      : None,
    'ATN('      : None,
    'COS('      : None,
    'DATA'      : None,
    'DEF'       : None,
    'END'       : None,
    'EXP('      : None,
    'FN'        : None,
    'FOR'       : None,
    'GOSUB'     : None,
    'GOTO'      : None,
    'IF'        : None,
    'INPUT'     : None,
    'INT('      : None,
    'LET'       : None,
    'LIST'      : None,
    'LOG('      : None,
    'NEW'       : None,
    'NEXT'      : None,
    'PRINT'     : DoPrnt,
    'REM'       : None,
    'RETURN'    : None,
    'RND('      : None,
    'SIN('      : None,
    'SQR('      : None,
    'STEP'      : None,
    'TAN('      : None,
    'THEN'      : None,
    'TO'        : None,
}

class Token():
    ttype = 0
    tval = 0

d = list()
curline = None
curpos = 0

def start_line(inp):
    global curline, curpos
    curline = list(inp)
    curpos = 0

def next_char():
    global curline, curpos
    if curpos >= len(curline):
        return None
    ret = curline[curpos]
    curpos += 1
    return ret

def unget_char():
    global curpos
    curpos -= 1

def next_token():
    tok = Token()

    ch = next_char()
    if not ch:
        return None

    lex = ch.upper()

    while ch and lex == " ":
        ch = next_char()
        lex = ch.upper()

    if not ch:
        return None

    if lex == '?':
        tok.ttype = KEYWORD
        tok.tval = "PRINT"
        return tok

    if (lex >= '0' and lex <= '9'):
        is_neg = False
        tok.ttype = NUMBER
        if lex == '-':
            is_neg = True
        tok.tval = int(ch)
        ch = next_char()
        while ch and ch >= '0' and ch <= '9':
            tok.tval *= 10
            tok.tval += int(ch)
            ch = next_char()
        if ch:
            unget_char()
        if is_neg:
            tok.tval = -tok.tval
        return tok

    if lex == '"':
        tok.ttype = STRING
        tok.tval = ""
        ch = next_char()
        while ch and ch != '"':
            tok.tval += ch
            ch = next_char()
        if ch:
            unget_char()
        return tok

    if lex == ':':
        tok.ttype = COLON
        tok.tval = lex
        return tok

    if lex >= 'A' and lex <= 'Z':
        tok.ttype = VARIABLE
        tok.tval = "%s" % lex
        ch = next_char()
        if not ch:
            return tok
        ch = ch.upper()
        while ch and ((ch >= 'A' and ch <= 'Z') or ch == '%' or ch == '$' or ch == '('):
            tok.tval += ch
            if ch == '%' or ch == '$':
                return tok
            if ch == '(':
                if tok.tval in keywords:
                    tok.ttype = KEYWORD
                    return tok
            ch = next_char()
            if ch:
                ch = ch.upper()
        if ch:
            unget_char()
        if tok.tval in keywords:
            tok.ttype = KEYWORD
        return tok

    if lex == '(' or lex == ')' or lex == '+' or lex == '-' or lex == '*' or lex == '/' or lex == '=':
        tok.ttype = OPERATOR
        tok.tval = lex
        return tok

    return None

def parsecheck(inp):
    start_line(inp)
    t = next_token()
    while t:
        print("Token ", end="")
        if t.ttype == NUMBER:
            print("[number] %s" % t.tval)
        elif t.ttype == STRING:
            print("[string] '%s'" % t.tval)
        elif t.ttype == KEYWORD:
            print("[keyword] %s -> %s" % (t.tval, keywords[t.tval]))
        elif t.ttype == OPERATOR:
            print("[oper] %s" % t.tval)
        elif t.ttype == VARIABLE:
            print("[variable] %s" % t.tval)
        elif t.ttype == COLON:
            print("[colon]")
        else:
            print("syntax error?")
        t = next_token()
    return False

def store_line(lineno):
    # store or replace a line in internal memory
    pass

def var_get(v):
    global vars
    if v not in vars:
        vars[v] = 0
    return vars[v]

def store_result(v, val):
    global vars
    vars[v] = val

def op_do(opr, arg1, arg2):
    if opr.tval == '+':
        return arg1 + arg2
    if opr.tval == '-':
        return arg1 - arg2
    if opr.tval == '*':
        return arg1 * arg2
    if opr.tval == '/':
        return arg1 / arg2
    print("opr %s unimplemented" % opr.tval)
    sys.exit(1)

def eval_expression(t):
    opr_stack = list()
    val_stack = list()

    while t and t.ttype != COLON:
        if t.ttype == NUMBER:
            val_stack.append(t.tval)
        elif t.ttype == VARIABLE:
            val_stack.append(var_get(t.tval))
        elif t.ttype == OPERATOR:
            if len(opr_stack) == 0:
                opr_stack.append(t)
                t = next_token()
                continue
            if t.tval == ')':
                op = opr_stack.pop()
                while op.tval != "(":
                    a1 = val_stack.pop()
                    a2 = val_stack.pop()
                    val_stack.append(op_do(op, a1, a2))
                    op = opr_stack.pop()
            else:
                peek = opr_stack[len(opr_stack) - 1]
                while peek.ttype == OPERATOR and operators[peek.tval] < operators[t.tval]:
                    op = opr_stack.pop()
                    a1 = val_stack.pop()
                    a2 = val_stack.pop()
                    val_stack.append(op_do(op, a1, a2))
                    if len(opr_stack) == 0:
                        break
                    peek = opr_stack[len(opr_stack) - 1]
                opr_stack.append(t)
        elif t.ttype == FUNCTION:
            t = next_token()
            if not t:
                print("ran out of tokens")
                return NaN
            val_stack.append(operators[t.tval].exec(eval_expression(t)))
        t = next_token()

    while len(opr_stack) > 0 and len(val_stack) > 1:
        op = opr_stack.pop()
        a1 = val_stack.pop()
        a2 = val_stack.pop()
        val_stack.append(op_do(op, a1, a2))
    if len(opr_stack) != 0 or len(val_stack) != 1:
        print("too many oprs(%s) or vals(%s)" % (len(opr_stack), len(val_stack)))
        sys.exit(1)
    return val_stack[0]

def exec_keyword(key):
    # call keyword func
    if keywords[key]:
        keywords[key].exec()
    else:
        print("'%s' not yet implemented" % key)

def parse(inp):
    start_line(inp)
    t = next_token()
    while t:
        if t.ttype == NUMBER:
            while t.ttype == NUMBER:
                store_line(t.tval)
                start_line()
                t = next_token()
            continue

        if t.ttype == VARIABLE:
            varname = t.tval
            t = next_token()
            if t.ttype != OPERATOR or t.tval != '=':
                print("?syntax error [%s]" % t.tval)
                return None
            t = next_token()
            if not t:
                print("?syntax error")
                return None
            value = eval_expression(t)
            store_result(varname, value)
            t = next_token()
            continue

        if t.ttype == KEYWORD:
            exec_keyword(t.tval)
            t = next_token()
            continue

        print("?syntax error")



def handle_line(inp):
    while parse(inp):
        pass

while True:
    print("Ready.")
    r = readline().strip()
    if r.lower() == "x":
        break
    cmd = handle_line(r)

