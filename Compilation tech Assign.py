import re

code =  """<?php
class MyClass {
    function abc(){ $i=5;
    $z=$i*2;
    echo "One '$=".$z;}
}
?>""".splitlines()

token = []

lineNum = 1

def valueSet(code: str):

    value = code.replace("=", " = ")
    value = value.replace("*", " * ")
    valueSplit = value.split(" ")
    
    for val in valueSplit:
        
            
        if val == "=":
            token.append([lineNum, "assign"])
    
        elif val == "*":
            token.append([lineNum, "multiplication"])

        else:

            if val.isdigit():
                token.append([lineNum, "Number", val])

            else:
                token.append([lineNum, "String", val])

def functionName(code):

    emptystr = ""
    regText = re.search(emptystr, code)
    
    placement = regText.span()

    return code[placement[0]: placement[1] - 1]

def brackets(code): 

    if "(" in code:
        functionsName = functionName(code)
        token.append([lineNum, "type-identifier", functionsName])
        token.append([lineNum, "Opening Brackets"])

    if ")" in code:
        token.append([lineNum, "Closing Brackets"])

    if "{" in code:
        token.append([lineNum, "Opening Curly Brackets"])

    if "}" in code:
        token.append([lineNum, "Closing Curly Brackets"])



for i in code:
    
    newcode = i.split(" ")
    print(newcode)
    container = ""

    for t in newcode:

        if t == "<?php":
            token.append([lineNum, "php-opening-tag"])

        if t == "?>":
            token.append([lineNum, "php-closing-tag"])
            
        if "." in t:
            token.append([lineNum, "concatenate"])

            concatenate = t.index(".")
            concatenatecode = t[concatenate + 1:]

            valueSet(concatenatecode)
        if t != ''  and t[0] =='"':
            container = container + t


        if ";" in t:
            token.append([lineNum, "semicolon"])
        elif t == "class":
            token.append([lineNum, "class"])

        elif t == "function":
            token.append([lineNum, "function"])


        elif t == "echo":
            token.append([lineNum, "print-output"])

        elif "=" in t:
            valueSet(t)

            if ";" in t:
                token.append([lineNum, "semicolon"])

        elif ";" in t:
            token.append([lineNum, "semicolon"])

        elif re.match("[a-zA-Z]+", t) and "(" not in t:
            token.append([lineNum, "type-identifier", t])

        else:
            brackets(t)

    lineNum += 1

print(token)
