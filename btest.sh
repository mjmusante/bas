#! /bin/ksh

function testexpr {
    expect_result="$1"
    got_result="$(echo $2 | ./bas.py)"
    if [ $? != 0 ]
    then
        print $3: execution failed: $got_result
        exit 1
    fi
    if [ "$expect_result" != "$got_result" ]
    then
        print $3: Expected \"$expect_result\" but got \"$got_result\"
        exit 1
    fi
}

testexpr 1 "?1" $LINENO
testexpr 2 "?1+1" $LINENO
testexpr 3 "?1+1+1" $LINENO
testexpr 4 "?9-5" $LINENO
testexpr 5 "?10/2" $LINENO
testexpr 6 "?2*3" $LINENO
testexpr 7 "?1+2*3" $LINENO
testexpr 8 "?(1+1)*4" $LINENO
testexpr 9 "a=3:?a*3" $LINENO

testexpr 10 "a=20:?a/2" $LINENO
testexpr 11 "a=4:?15-a" $LINENO
testexpr 12 "a=-12:?-a" $LINENO
testexpr 13 "a=+3:?+10+a" $LINENO
testexpr 14 "a=-24:?-10-a" $LINENO

testexpr 15 "?abs(-15)" $LINENO
testexpr 16 "?3*abs(6)-abs(-2)" $LINENO
