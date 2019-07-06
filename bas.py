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

prog = dict()

class Brain(object):
    def __init__(self, t_for):
        self.t_for = t_for

    def expect(self, ttype, tval=None):
        t = next_token()
        if not t:
            return None
        if t.ttype != ttype:
            print("{expecting %s, got %s)" % (ttype, t.ttype))
            return None
        if tval and tval != t.tval:
            print("{expecting %s, got %s)" % (tval, t.tval))
            return None
        return t

    def exec(self):
        print("Not implemented")
        sys.exit(1)


class DoPrnt(Brain):
    def __init__(self):
        super().__init__(KEYWORD);

    def exec(self):
        t = next_token()
        while t and t.ttype != COLON:
            if t.ttype == STRING:
                print("%s" % t.tval, end="")
            else:
                print("%g" % eval_expression(t), end="")

            t = next_token()
        print("")
        return True

class DoLet(Brain):
    def __init__(self):
        super().__init__(KEYWORD)

    def exec(self, gotvar=None):
        if not gotvar:
            t = self.expect(VARIABLE)
            if not t:
                return False
            varname = t.tval
        else:
            varname = gotvar.tval
        if not self.expect(OPERATOR, '='):
            return False
        store_result(varname, eval_expression(next_token()))
        return True

class DoAbs(Brain):
    def __init__(self):
        super().__init__(FUNCTION)

    def exec(self, val):
        if val > 0:
            return val
        return -val


operators = {
    '!' : (0, False),    # internal "unary minus" operator
    '*' : (1, True),
    '/' : (1, True),
    '+' : (2, True),
    '-' : (2, True),
    '(' : (3, False)
}

vars = dict()

keywords = {
    'ABS('      : DoAbs(),
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
    'LET'       : DoLet(),
    'LIST'      : None,
    'LOG('      : None,
    'NEW'       : None,
    'NEXT'      : None,
    'PRINT'     : DoPrnt(),
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

    def __str__(self):
        if self.ttype == NUMBER or self.ttype == OPERATOR:
            return "[Tok:%s]" % self.tval
        elif self.ttype == STRING:
            return "[Tok:\"%s\"]" % self.tval
        elif self.ttype == KEYWORD:
            return "[Tok:%s]" % self.tval
        elif self.ttype == VARIABLE:
            return "[Tok:(%s=%s)]" % (self.tval, var_get(self.tval))
        elif self.ttype == COLON:
            return "[Tok:<colon>]"
        elif self.ttype == FUNCTION:
            return "[Tok:%s)]" % keywords[self.tval]


d = list()
curline = None
curpos = 0
untok = None

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
    global untok, totalt

    if untok:
        tok = untok
        untok = None
        return tok

    tok = Token()

    ch = next_char()
    if not ch:
        return None

    lex = ch.upper()

    while ch and lex == " ":
        ch = next_char()
        lex = ch.upper()

    if not ch or ch == '\n':
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
        if ch and ch != '"':
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
                    tok.ttype = FUNCTION
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


def unget_token(t):
    global untok
    assert(untok == None)
    untok = t


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
    if opr.tval == '!':
        return -arg1
    print("opr %s unimplemented" % opr.tval)
    sys.exit(1)


def eval_expression(t, single=False):
    opr_stack = list()
    val_stack = list()

    def apply_op(op):
        right = val_stack.pop()
        if operators[op.tval][1]:
            left = val_stack.pop()
            val_stack.append(op_do(op, left, right))
        else:
            val_stack.append(op_do(op, right, 0))

    def push_opr(op):
        while len(opr_stack) > 0:
            peek = opr_stack[len(opr_stack) - 1]
            if operators[peek.tval][0] > operators[op.tval][0]:
                break
            apply_op(opr_stack.pop())
        opr_stack.append(op)

    def dump_stack(title, stack):
        print("%s:" % title, end="")
        for s in stack:
            print("%s" % s, end=" ")
        print("")


    sawval = False
    while t:
        # dump_stack("v", val_stack)
        # dump_stack("o", opr_stack)
        if t.ttype == NUMBER:
            val_stack.append(t.tval)
            sawval = True
        elif t.ttype == VARIABLE:
            val_stack.append(var_get(t.tval))
            sawval = True
        elif t.ttype == OPERATOR and t.tval == '+':
            if sawval:
                push_opr(t)
            sawval = False
        elif t.ttype == OPERATOR and t.tval == '-':
            if not sawval:
                t.tval = '!'
            push_opr(t)
            sawval = False
        elif t.ttype == OPERATOR:
            if t.tval == '(':
                opr_stack.append(t)
                sawval = False
            elif not sawval:
                print("sawval: syntax error")
                sys.exit(1)
            elif t.tval == ')':
                while len(opr_stack) > 0 and opr_stack[len(opr_stack) - 1] != '(':
                    op = opr_stack.pop()
                    if op.tval == '(':
                        break
                    if len(opr_stack) == 0:
                        print("unbalanced parens")
                        sys.exit(1)
                    apply_op(op)
                if single and len(opr_stack) == 0 and len(val_stack) == 1:
                    return val_stack[0]
            else:
                push_opr(t)
                sawval = False
        elif t.ttype == FUNCTION:
            func = keywords[t.tval]
            if not func:
                print("function not implemented")
                sys.exit(1)
            t.ttype = OPERATOR
            t.tval = '('
            val_stack.append(func.exec(eval_expression(t, True)))
            sawval = True
        else:
            break

        t = next_token()

    while len(opr_stack) > 0:
        apply_op(opr_stack.pop())

    if len(opr_stack) > 0 or len(val_stack) != 1:
        print("too many oprs(%s) or vals(%s)" % (len(opr_stack), len(val_stack)))
        sys.exit(1)

    return val_stack[0]

def exec_keyword(key):
    # call keyword func
    if keywords[key]:
        keywords[key].exec()
    else:
        print("'%s' not yet implemented" % key)

def add_line(linenum):
    l = list()
    t = next_token()
    while t and t.ttype != COLON:
        l.append(t)
        print("%s" % t)
        t = next_token()
    prog[linenum] = l

def parse(inp):
    # all lines entered by the user will start with one of:
    # - a keyword (e.g. list, print, run, &c)
    # - a positive number (to insert a new line or replace an existing one)
    # - a variable (as a shortcut for 'let')
    # everything else is a syntax error
    implied_let = DoLet()
    start_line(inp)
    t = next_token()
    while t:
        if t.ttype == KEYWORD:
            exec_keyword(t.tval)
            t = next_token()
            continue

        if t.ttype == NUMBER:
            add_line(t.tval)
            return True

        if t.ttype == VARIABLE:
            if not implied_let.exec(t):
                return False
            t = next_token()
            continue

        if t.ttype == COLON:
            t = next_token()
            continue

        print("?syntax error")
        return False



def handle_line(inp):
    while parse(inp):
        inp = readline().strip()

while True:
    if sys.stdin.isatty():
        print("Ready.")
    r = readline().strip()
    if r == "":
        sys.exit(0)
    if r.lower() == "x":
        break
    cmd = handle_line(r)

