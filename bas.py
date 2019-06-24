#! /usr/bin/env python3.6

import sys
readline = sys.stdin.readline

NUMBER = 1
STRING = 2
KEYWORD = 3
OPERATOR = 4
VARIABLE = 5
COLON = 6

def doprnt():
    t = next_token()
    while t and t != ":":
        if t.ttype == STRING:
            print("%s" % t.tval, end="")
        else:
            print("{can't handle type %s}" % t.ttype, end="")

        t = next_token()
    print("")



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
    'PRINT'     : doprnt,
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

    if lex >= '0' and lex <= '9':
        tok.ttype = NUMBER
        tok.tval = int(ch)
        ch = next_char()
        while ch and ch >= '0' and ch <= '9':
            tok.tval *= 10
            tok.tval += int(ch)
            ch = next_char()
        if ch:
            unget_char()
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

def eval_expression():
    # whee this'll be fun
    pass

def exec_keyword(key):
    # call keyword func
    if keywords[key]:
        keywords[key]()
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
            value = eval_expression()
            store_result(t.tval, value)
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
    if r.lower() == "xxx":
        break
    cmd = handle_line(r)

