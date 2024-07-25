#!/usr/bin/env python3

import math
from collections import defaultdict, deque

# Small helper functions
def isinteger(s):
        try:
                int(s)
                return True
        except ValueError:
                return False

def validParens(s):
        st = deque()
        for char in s:
                if char == "(":
                        st.append(char)
                elif not st:
                        return False
                else:
                        st.pop()
        return len(st) == 0

def productList(lst):
        pro = 1
        for elem in lst:
                pro *= elem
        return pro

def avgAllList(lst):
        if not lst:
                return -1
        return sum(lst) // len(lst)

def gcdAllList(lst):
        if not lst:
                return -1
        gcd = lst[0]
        for i in range(1, len(lst)):
                gcd = math.gcd(gcd, lst[i])
        return gcd

def lcmAllList(lst):
        if not lst:
                return -1
        lcm = lst[0]
        for i in range(1, len(lst)):
                # lcm formula
                lcm = abs(lcm * lst[i]) // math.gcd(lcm, lst[i])
        return lcm



def evaluatePrint(expr, variables, variableMap):
        printExpr = []

        for i in range(len(expr)):
                current = expr[i]
                newCurrent = current

                if current in variableMap:
                        if isinstance(variables[variableMap[current]], int):
                                newCurrent = str(variables[variableMap[current]])
                        elif isinstance(variables[variableMap[current]], list):
                                newCurrent = ", ".join([str(item) for item in variables[variableMap[current]]])
                        elif isinstance(variables[variableMap[current]], str):
                                newCurrent = variables[variableMap[current]]
                
                elif len(current) == 4 and current[0] in variableMap and current[1:4] == "len":
                        newCurrent = str(expressionInt([current], variables, variableMap))
                
                elif len(current) > 2 and current[0] in variableMap and current[1] == "*":
                        desired_scaling = expressionInt([current[2:]], variables, variableMap)
                        newCurrent = expressionStr([current[0]], variables, variableMap) * desired_scaling
                
                elif len(current) == 3 and current[0] in variableMap and current[1:] == "id":
                        newCurrent = str(variableMap[current[0]])
                
                elif len(current) > 1 and current[0] in variableMap and isinstance(variables[variableMap[current[0]]], list):
                        newCurrent = str(expressionInt([current], variables, variableMap))
                
                elif len(current) > 2 and current.count("*") == 1:
                        scale_ind = current.index("*")
                        if 1 <= scale_ind < len(current) - 1:
                                desired_scaling = expressionInt([current[scale_ind + 1:]], variables, variableMap)
                                newCurrent = current[:scale_ind] * desired_scaling

                printExpr.append(newCurrent)
        
        for printItem in printExpr:
                print(printItem, end = " ")
        print()





def updateExpressionInt(op, v, st):
        # Same level of order of operations
        if op == "+":
                st.append(v)
        if op == "-":
                st.append(-v)
        
        # Same level of order of operations
        if op == "*":
                st.append(st.pop() * v)
        if op == "/" and v != 0:
                st.append(st.pop() // v)
        if op == "%" and v != 0:
                st.append(st.pop() % v)
        
def helperExpressionInt(expr):
        i = 0
        currentTermValue = 0
        st = deque()
        sign = "+"
        
        while i < len(expr):
                currentItem = expr[i]

                if isinteger(currentItem):
                        currentTermValue = int(currentItem)

                elif currentItem in "+-*/%":
                        updateExpressionInt(sign, currentTermValue, st)
                        currentTermValue = 0
                        sign = currentItem

                elif currentItem == "(":
                        currentTermValue, j = helperExpressionInt(expr[i + 1:])
                        i += j

                elif currentItem == ")":
                        updateExpressionInt(sign, currentTermValue, st)
                        return sum(st), i + 1
                
                i += 1

        updateExpressionInt(sign, currentTermValue, st)

        return sum(st), i

def expressionInt(expr, variables, variableMap):
        # Credit https://leetcode.com/u/DBabichev/ for inspiration

        # Eval-int variables
        SUPPORTED_OPS = {"+", "-", "*", "/", "%", "(", ")", "^", "=", "!", "<", ">", "{", "}"}
        SUPPORTED_LISTOPS = {"sum", "pro", "min", "max", "avg", "gcd", "lcm", "pow", "ncr", "npr"}
        
        transformedExpr = []
        parenS = ""

        for i in range(len(expr)):
                current = expr[i]
                newCurrent = current

                if current in variableMap:
                        if isinstance(variables[variableMap[current]], int):
                                newCurrent = str(variables[variableMap[current]])
                        elif isinstance(variables[variableMap[current]], list):
                                print("Error: List variable " + current + " in int epression")
                                continue
                        elif isinstance(variables[variableMap[current]], str):
                                print("Error: String variable " + current + " in int epression")
                                continue
                
                # length
                elif len(current) == 4 and current[0] in variableMap and current[1:4] == "len":
                        current_var = variableMap[current[0]]
                        if isinstance(variables[current_var], int):
                                print("Error: Attempt to get length of int variable " + current[0])
                                continue
                        elif isinstance(variables[current_var], str):
                                newCurrent = str(len(variables[current_var]))
                        elif isinstance(variables[current_var], list):
                                newCurrent = str(len(variables[current_var]))
                
                # sum, product, min, max, ...
                elif len(current) == 4 and current[0] in variableMap and current[1:4] in SUPPORTED_LISTOPS:
                        current_var = variableMap[current[0]]
                        if isinstance(variables[current_var], list):
                                if current[1:4] == "sum":
                                        newCurrent = str(sum(variables[current_var]))
                                elif current[1:4] == "pro":
                                        newCurrent = str(productList(variables[current_var]))
                                elif current[1:4] == "min":
                                        newCurrent = str(min(variables[current_var]))
                                elif current[1:4] == "max":
                                        newCurrent = str(max(variables[current_var]))
                                elif current[1:4] == "avg":
                                        newCurrent = str(avgAllList(variables[current_var]))
                                elif current[1:4] == "gcd":
                                        newCurrent = str(gcdAllList(variables[current_var]))
                                elif current[1:4] == "lcm":
                                        newCurrent = str(lcmAllList(variables[current_var]))
                                elif len(variables[current_var]) == 2:
                                        first, second = variables[current_var]
                                        if current[1:4] == "pow":
                                                newCurrent = str(first ** second)
                                        elif current[1:4] == "ncr":
                                                newCurrent = str(math.comb(first, second))
                                        elif current[1:4] == "npr":
                                                newCurrent = str(math.perm(first, second))
                
                # count
                elif len(current) > 4 and current[0] in variableMap and current[1:4] == "cnt":
                        current_var = variableMap[current[0]]
                        if isinstance(variables[current_var], int):
                                print("Error: Attempt to get count for int variable " + current[0])
                                continue
                        elif isinstance(variables[current_var], list):
                                newCurrent = str(variables[current_var].count(expressionInt([current[4:]], variables, variableMap)))
                        elif isinstance(variables[current_var], str):
                                newCurrent = str(variables[current_var].count(expressionStr([current[4:]], variables, variableMap)))
                
                # element index
                elif len(current) > 4 and current[0] in variableMap and current[1:4] == "ind":
                        current_var = variableMap[current[0]]
                        if isinstance(variables[current_var], int):
                                print("Error: Attempt to get index for int variable " + current[0])
                                continue
                        elif isinstance(variables[current_var], list):
                                desired_result = expressionInt([current[4:]], variables, variableMap)
                                if desired_result not in variables[current_var]:
                                        newCurrent = str(-1)
                                else:
                                        newCurrent = str(variables[current_var].index(desired_result))
                        elif isinstance(variables[current_var], str):
                                newCurrent = str(variables[current_var].find(expressionStr([current[4:]], variables, variableMap)))
                
                # list index
                elif len(current) > 1 and current[0] in variableMap and isinstance(variables[variableMap[current[0]]], list):
                        current_var = variableMap[current[0]]
                        if isinteger(current[1:]):
                                desired_index = int(current[1:])
                                if -1 * len(variables[current_var]) <= desired_index < len(variables[current_var]):
                                        newCurrent = str(variables[current_var][desired_index])
                                else:
                                        print("Error: Index out of bounds in list ", current[0])
                                
                        elif current[1] == "[" and len(current) > 2:
                                desired_index = expressionInt([current[2:]], variables, variableMap)
                                if -1 * len(variables[current_var]) <= desired_index < len(variables[current_var]):
                                        newCurrent = str(variables[current_var][desired_index])
                                else:
                                        print("Error: Index out of bounds in list ", current[0])

                
                elif isinteger(current) and transformedExpr and isinteger(transformedExpr[-1]):
                        print("Error: two ints in a row in int expression")
                        continue
                
                # negative
                elif not isinteger(current) and len(current) > 1 and current[0] == "-":
                        newCurrent = str(-1 * expressionInt([current[1:]], variables, variableMap))
                
                # absolute value
                elif not isinteger(current) and len(current) > 1 and current[0] == "|":
                        newCurrent = str(abs(expressionInt([current[1:]], variables, variableMap)))
                
                # factorial
                elif not isinteger(current) and len(current) > 1 and current[-1] == "!":
                        newCurrent = str(math.factorial(abs(expressionInt([current[:-1]], variables, variableMap))))
                
                elif not isinteger(current) and current not in SUPPORTED_OPS:
                        continue
                

                if current == "(" or current == ")":
                        parenS += current

                transformedExpr.append(newCurrent)
        
        if not validParens(parenS):
                print("Error: Invalid parentheses in int expression")
                return 0
        
        return helperExpressionInt(transformedExpr)[0]





def expressionList(expr, variables, variableMap):
        finalList = []

        if not expr:
                return finalList
        
        listVariables = set()
        intVariables = set()
        for variable, enc in variableMap.items():
                if isinstance(variables[enc], list):
                        listVariables.add(variable)
                if isinstance(variables[enc], int):
                        intVariables.add(variable)
        
        commas = [-1]
        for i in range(len(expr)):
                if expr[i] == ",":
                        commas.append(i)
        commas.append(len(expr))

        for i in range(len(commas) - 1):
                first_comma = commas[i]
                second_comma = commas[i + 1]
                inside_commas = second_comma - first_comma - 1

                if inside_commas == 0:
                        continue

                elif inside_commas == 1 and expr[first_comma + 1] in variableMap:
                        current_var = variableMap[expr[first_comma + 1]]

                        if isinstance(variables[current_var], int):
                                finalList.append(variables[current_var])
                        elif isinstance(variables[current_var], list):
                                for intElem in variables[current_var]:
                                        finalList.append(intElem)
                        elif isinstance(variables[current_var], str):
                                if isinteger(variables[current_var]):
                                        finalList.append(int(variables[current_var]))
                                else:
                                        print("Error: String variable " + expr[first_comma + 1] + " in int-based list")
                                        finalList.append(0)
                

                elif inside_commas == 1 and len(expr[first_comma + 1]) > 2 and expr[first_comma + 1][0] in listVariables:
                        current_var = variableMap[expr[first_comma + 1][0]]

                        if isinstance(variables[current_var], list):
                                if expr[first_comma + 1][1:] in {"sort", "tros", "rev"}:
                                        if expr[first_comma + 1][1:5] == "sort":
                                                for intElem in sorted(variables[current_var]):
                                                        finalList.append(intElem)
                                        elif expr[first_comma + 1][1:5] == "tros":
                                                for intElem in sorted(variables[current_var], reverse = True):
                                                        finalList.append(intElem)
                                        elif expr[first_comma + 1][1:4] == "rev":
                                                for intElem in list(reversed(variables[current_var])):
                                                        finalList.append(intElem)

                                elif expr[first_comma + 1][1] == "*":
                                        desired_scaling = expressionInt([expr[first_comma + 1][2:]], variables, variableMap)
                                        for _ in range(desired_scaling):
                                                for intElem in variables[current_var]:
                                                        finalList.append(intElem)
                

                elif inside_commas == 1 and len(expr[first_comma + 1]) > 2 and expr[first_comma + 1][0] in intVariables:
                        current_var = variableMap[expr[first_comma + 1][0]]

                        if isinstance(variables[current_var], int) and expr[first_comma + 1][1] == "*":
                                desired_scaling = expressionInt([expr[first_comma + 1][2:]], variables, variableMap)
                                for _ in range(desired_scaling):
                                        finalList.append(variables[current_var])
                

                elif inside_commas == 1 and len(expr[first_comma + 1]) > 2 and expr[first_comma + 1].count("*") == 1:
                        scale_ind = expr[first_comma + 1].index("*")
                        desired_scaling = expressionInt([expr[first_comma + 1][scale_ind + 1:]], variables, variableMap)
                        for _ in range(desired_scaling):
                                finalList.append(expressionInt([expr[first_comma + 1][:scale_ind]], variables, variableMap))


                elif inside_commas > 0:
                        finalList.append(expressionInt(expr[first_comma + 1: second_comma], variables, variableMap))

        return finalList





def expressionStr(expr, variables, variableMap):
        # Eval-string variables
        LIMIT_SPACE = 5
        
        finalStr = ""
        strExpr = []

        for i in range(len(expr)):
                current = expr[i]
                newCurrent = current

                if current in variableMap:
                        if isinstance(variables[variableMap[current]], int):
                                newCurrent = str(variables[variableMap[current]])
                        elif isinstance(variables[variableMap[current]], list):
                                newCurrent = ", ".join([str(item) for item in variables[variableMap[current]]])
                        elif isinstance(variables[variableMap[current]], str):
                                newCurrent = variables[variableMap[current]]
                
                elif len(current) == 4 and current[0] in variableMap and current[1:4] == "len":
                        newCurrent = str(expressionInt([current], variables, variableMap))
                
                elif len(current) > 1 and current[0] in variableMap and isinstance(variables[variableMap[current[0]]], list):
                        newCurrent = str(expressionInt([current], variables, variableMap))
                
                elif len(current) > 2 and current[0] in variableMap and isinstance(variables[variableMap[current[0]]], str):
                        current_var = variableMap[current[0]]

                        if current[1:4] in {"stp", "upp", "low", "ttl", "cap", "rev"}:
                                if current[1:4] == "stp":
                                        newCurrent = variables[current_var].strip()
                                elif current[1:4] == "upp":
                                        newCurrent = variables[current_var].upper()
                                elif current[1:4] == "low":
                                        newCurrent = variables[current_var].lower()
                                elif current[1:4] == "ttl":
                                        newCurrent = variables[current_var].title()
                                elif current[1:4] == "cap":
                                        newCurrent = variables[current_var].capitalize()
                                elif current[1:4] == "rev":
                                        newCurrent = variables[current_var][::-1]
                        
                        elif current[1] == "*":
                                desired_scaling = expressionInt([current[2:]], variables, variableMap)
                                newCurrent = variables[current_var] * desired_scaling
                
                #space
                elif "_" in current:
                        for numSpaces in range(1, LIMIT_SPACE + 1):
                                if "_" * numSpaces == current:
                                        newCurrent = " " * numSpaces
                
                elif len(current) > 2 and current.count("*") == 1:
                        scale_ind = current.index("*")
                        if 1 <= scale_ind < len(current) - 1:
                                desired_scaling = expressionInt(current[scale_ind + 1:], variables, variableMap)
                                newCurrent = current[:scale_ind] * desired_scaling


                strExpr.append(newCurrent)
        
        for strTerm in strExpr:
                finalStr += strTerm
        
        return finalStr





def runEval(l, returnType):
        variables = []
        variableMap = {}
        variable_ct = 0

        for line in l:
                if not line:
                        continue

                split_line = line.split()

                # Return
                if split_line[0] == "re":
                        if len(split_line) == 1:
                                return ""
                        elif returnType == "int":
                                reInt = expressionInt(split_line[1:], variables, variableMap)
                                return returnType + str(reInt)
                        elif returnType == "lis":
                                reList = expressionList(split_line[1:], variables, variableMap)
                                return returnType + ", ".join([str(item) for item in reList])
                        elif returnType == "str":
                                reStr = expressionStr(split_line[1:], variables, variableMap)
                                return returnType + reStr
                        else:
                                return ""
                
                # Print
                elif split_line[0] == "pr":
                        evaluatePrint(split_line[1:], variables, variableMap)
                
                # Debug
                elif split_line[0] == "bug":
                        print("Variables mapped to their ids:", variableMap, "; Variable values:", variables)
                
                # Swap
                elif split_line[0] == "swap" and len(split_line) == 3 and split_line[1] in variableMap and split_line[2] in variableMap:
                        current_var1 = variableMap[split_line[1]]
                        current_var2 = variableMap[split_line[2]]

                        temp = variables[current_var1]
                        variables[current_var1] = variables[current_var2]
                        variables[current_var2] = temp
                
                # Delete variable(s)
                elif split_line[0] == "del":
                        for i in range(1, len(split_line)):
                                if split_line[i] in variableMap:
                                        variables[variableMap[split_line[i]]] = None
                                        del variableMap[split_line[i]]

                # Variable (I)
                elif len(split_line[0]) == 1 and split_line[0].isalpha():
                        
                        # default to int
                        if split_line[0] not in variableMap:
                                variableMap[split_line[0]] = variable_ct
                                variables.append(0)
                                variable_ct += 1
                        current_var = variableMap[split_line[0]]

                        # int case
                        if isinstance(variables[current_var], int):

                                if len(split_line) > 1:
                                        # special incrementers
                                        if split_line[1] == "++":
                                                variables[current_var] += 1
                                                continue
                                        elif split_line[1] == "--":
                                                variables[current_var] -= 1
                                                continue
                                        elif split_line[1] == "+-":
                                                variables[current_var] *= 1
                                                continue
                                        elif split_line[1] == "-+":
                                                variables[current_var] *= (-1)
                                                continue

                                        # Assignment
                                        elif split_line[1] == "<-" or split_line[1] == "=":
                                                if split_line[2:]:
                                                        variables[current_var] = expressionInt(split_line[2:], variables, variableMap)
                                        
                                        # Assignment-enhanced increment
                                        elif split_line[1] == "+=":
                                                if split_line[2:]:
                                                        variables[current_var] += expressionInt(split_line[2:], variables, variableMap)
                                        elif split_line[1] == "-=":
                                                if split_line[2:]:
                                                        variables[current_var] -= expressionInt(split_line[2:], variables, variableMap)
                                        elif split_line[1] == "*=":
                                                if split_line[2:]:
                                                        variables[current_var] *= expressionInt(split_line[2:], variables, variableMap)
                                        elif split_line[1] == "/=":
                                                if split_line[2:]:
                                                        desired_result = expressionInt(split_line[2:], variables, variableMap)
                                                        if desired_result == 0:
                                                                variables[current_var] = desired_result
                                                        else:    
                                                                variables[current_var] //= desired_result
                                        elif split_line[1] == "%=":
                                                if split_line[2:]:
                                                        variables[current_var] %= expressionInt(split_line[2:], variables, variableMap)
                                        elif split_line[1] == "^=":
                                                if split_line[2:]:
                                                        variables[current_var] **= expressionInt(split_line[2:], variables, variableMap)

                        # list case
                        elif isinstance(variables[current_var], list):
                                if len(split_line) > 2:

                                        # Assignment
                                        if (split_line[1] == "<-" or split_line[1] == "="):
                                                variables[current_var] = expressionList(split_line[2:], variables, variableMap)
                                        
                                        # Assignment-enhanced increment
                                        elif split_line[1] == "+=" or split_line[1] == "ext":
                                                variables[current_var] += expressionList(split_line[2:], variables, variableMap)
                                        
                                        # Append
                                        elif split_line[1] == "app":
                                                variables[current_var].append(expressionInt(split_line[2:], variables, variableMap))
                                        
                                        # Prepend
                                        elif split_line[1] == "pre":
                                                variables[current_var].insert(0, expressionInt(split_line[2:], variables, variableMap))
                                        
                                        # Insert
                                        elif split_line[1] == "ins" and len(split_line) > 3:
                                                desired_index = expressionInt([split_line[2]], variables, variableMap)
                                                if -1 * len(variables[current_var]) <= desired_index <= len(variables[current_var]):
                                                        variables[current_var].insert(desired_index, expressionInt(split_line[3:], variables, variableMap))
                                                else:
                                                        print("Error: Index out of bounds in list ", split_line[0])
                                        
                                        # Set
                                        elif split_line[1] == "set" and len(split_line) > 3:
                                                desired_index = expressionInt([split_line[2]], variables, variableMap)
                                                if -1 * len(variables[current_var]) <= desired_index < len(variables[current_var]):
                                                        variables[current_var][desired_index] = expressionInt(split_line[3:], variables, variableMap)
                                                else:
                                                        print("Error: Index out of bounds in list ", split_line[0])
                                        
                                        # Pop
                                        elif split_line[1] == "pop":
                                                desired_index = expressionInt(split_line[2:], variables, variableMap)
                                                if -1 * len(variables[current_var]) <= desired_index < len(variables[current_var]):
                                                        variables[current_var].pop(desired_index)
                                                else:
                                                        print("Error: Index out of bounds in list ", split_line[0])
                                
                                if len(split_line) >= 2:

                                        # Pop
                                        if split_line[1] == "pop" and len(split_line) == 2:
                                                variables[current_var].pop()
                                        
                                        # Sort
                                        elif split_line[1] == "sort":
                                                variables[current_var].sort()
                                        elif split_line[1] == "tros":
                                                variables[current_var].sort(reverse = True)
                                        
                                        # Reverse
                                        elif split_line[1] == "rev":
                                                variables[current_var].reverse()
                                        
                                        # Clear
                                        elif split_line[1] == "clr":
                                                variables[current_var].clear()
                        
                        # string case
                        elif isinstance(variables[current_var], str):
                                if len(split_line) > 2:

                                        # Assignment
                                        if (split_line[1] == "<-" or split_line[1] == "="):
                                                variables[current_var] = expressionStr(split_line[2:], variables, variableMap)
                                        
                                        # Assignment-enhanced increment
                                        elif split_line[1] == "+=":
                                                variables[current_var] += expressionStr(split_line[2:], variables, variableMap)
                                
                                if len(split_line) >= 2:

                                        # strip
                                        if split_line[1] == "stp":
                                                variables[current_var] = variables[current_var].strip()
                                        
                                        # cases
                                        elif split_line[1] == "upp":
                                                variables[current_var] = variables[current_var].upper()
                                        elif split_line[1] == "low":
                                                variables[current_var] = variables[current_var].lower()
                                        elif split_line[1] == "ttl":
                                                variables[current_var] = variables[current_var].title()
                                        elif split_line[1] == "cap":
                                                variables[current_var] = variables[current_var].capitalize()
                                        
                                        # reverse
                                        elif split_line[1] == "rev":
                                                variables[current_var] = variables[current_var][::-1]
                

                # Variable (Index)
                elif len(split_line[0]) > 1 and split_line[0][0] in variableMap and len(split_line) > 2 and (split_line[1] == "<-" or split_line[1] == "="):
                        current_var = variableMap[split_line[0][0]]

                        if isinstance(variables[current_var], list):
                                if isinteger(split_line[0][1:]):
                                        desired_index = int(split_line[0][1:])
                                        if -1 * len(variables[current_var]) <= desired_index < len(variables[current_var]):
                                                variables[current_var][desired_index] = expressionInt(split_line[2:], variables, variableMap)
                                        else:
                                                print("Error: Index out of bounds in list ", split_line[0][0])
                                
                                elif split_line[0][1] == "[" and len(split_line[0]) > 2:
                                        desired_index = expressionInt([split_line[0][2:]], variables, variableMap)
                                        if -1 * len(variables[current_var]) <= desired_index < len(variables[current_var]):
                                                variables[current_var][desired_index] = expressionInt(split_line[2:], variables, variableMap)
                                        else:
                                                print("Error: Index out of bounds in list ", split_line[0][0])
                
                
                # Variable (Declarations)
                elif split_line[0] == "int" and len(split_line) > 1 and len(split_line[1]) == 1 and split_line[1].isalpha():
                        if split_line[1] in variableMap:
                                print("Error: " + split_line[1] + " has already been declared")
                                continue
                        else:
                                variableMap[split_line[1]] = variable_ct
                                variables.append(0)
                                variable_ct += 1
                                current_var = variableMap[split_line[1]]

                                if len(split_line) > 3 and (split_line[2] == "<-" or split_line[2] == "="):
                                        variables[current_var] = expressionInt(split_line[3:], variables, variableMap)
                
                elif split_line[0] == "list" and len(split_line) > 1 and len(split_line[1]) == 1 and split_line[1].isalpha():
                        if split_line[1] in variableMap:
                                print("Error: " + split_line[1] + " has already been declared")
                                continue
                        else:
                                variableMap[split_line[1]] = variable_ct
                                variables.append([])
                                variable_ct += 1
                                current_var = variableMap[split_line[1]]

                                if len(split_line) > 3 and (split_line[2] == "<-" or split_line[2] == "="):
                                        variables[current_var] = expressionList(split_line[3:], variables, variableMap)
                
                elif split_line[0] == "str" and len(split_line) > 1 and len(split_line[1]) == 1 and split_line[1].isalpha():
                        if split_line[1] in variableMap:
                                print("Error: " + split_line[1] + " has already been declared")
                                continue
                        else:
                                variableMap[split_line[1]] = variable_ct
                                variables.append("")
                                variable_ct += 1
                                current_var = variableMap[split_line[1]]

                                if len(split_line) > 3 and (split_line[2] == "<-" or split_line[2] == "="):
                                        variables[current_var] = expressionStr(split_line[3:], variables, variableMap)
        
        # no return
        return ""
                                


def deserializeInt(ser):
        if len(ser) >= 3 and ser[:3] == "int":
                if len(ser) == 3:
                        return 0
                else:
                        return int(ser[3:])
       
        raise ValueError("Error: Expected return\n")

def deserializeList(ser):
        if len(ser) >= 3 and ser[:3] == "lis":
                if len(ser) == 3:
                        return []
                else:
                        return [int(item.strip()) for item in ser[3:].split(",")]
       
        raise ValueError("Error: Expected return\n")

def deserializeStr(ser):
        if len(ser) >= 3 and ser[:3] == "str":
                return ser[3:]
       
        raise ValueError("Error: Expected return\n")



def run():
        # Run-code variables
        TYPES_SUPPORTED = {"int", "list", "str"}
        lines_supported = 20
        end_program = "done"
        undo_program = "UNDO"
        
        # Eval-code variables
        # LIMITS = [10, 1] # 0: vars, 1: funcs

        # Variables
        returns = False

        print(f"Enter your script (type '{end_program}' on a new line to finish):")

        lines = []
        num_lines = 0
        while True:
                if num_lines == lines_supported:
                        print("Line limit reached. Calculating...")
                        break
                
                line = input().strip()
                
                if line == end_program:
                        break
                
                elif line == undo_program and lines:
                        lines.pop()
                        num_lines -= 1
                
                else:
                        lines.append(line)
                        num_lines += 1
        
        if lines:
                if lines[0] in TYPES_SUPPORTED:
                        returns = True

        print()

        # Evaluate
        if returns:
                serializedResult = runEval(lines[1:], lines[0][:3])

                if lines[0] == "int":
                        try:
                                result = deserializeInt(serializedResult)
                        except ValueError as e:
                                print(e)
                
                elif lines[0] == "list":
                        try:
                                result = deserializeList(serializedResult)
                        except ValueError as e:
                                print(e)
                
                else:
                        try:
                                result = deserializeStr(serializedResult)
                        except ValueError as e:
                                print(e) 
                
                print("Your result is...")
                print(result)
        else:
                _ = runEval(lines, "")

        print("Thanks for using Stringscript!")





"""
Run the code to Stringscript!
"""
run()