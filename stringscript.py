#!/usr/bin/env python3

import math
from collections import deque

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

def evaluateRange(expr, variables, variableMap):
        if not (expr.startswith(('(', '[')) and expr.endswith((')', ']'))):
                print("Error: Invalid range format: must start with ( or [ and end with ) or ]")
                return 0, -1

        core = expr[1:-1]

        core_parts = core.split(',')
        if len(core_parts) != 2:
                print("Error: Invalid range format: must contain two numbers")
                return 0, -1
        
        start_index = expressionInt([core_parts[0].strip()], variables, variableMap)
        end_index = expressionInt([core_parts[1].strip()], variables, variableMap)

        if expr.startswith('('):
                start_index += 1  # Exclusive start, so increment
        if expr.endswith(')'):
                end_index -= 1  # Exclusive end, so decrement

        if start_index > end_index:
                print("Error: Invalid range format: start cannot be greater than end")
                return 0, -1

        return start_index, end_index





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
                
                elif len(current) == 3 and current[0] in variableMap and current[1:] == "id":
                        newCurrent = str(variableMap[current[0]])
                
                elif len(current) > 2 and current[0] in variableMap and current[1] == "*":
                        desired_scaling = expressionInt([current[2:]], variables, variableMap)
                        newCurrent = expressionStr([current[0]], variables, variableMap) * desired_scaling
                
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
                        
                        elif current[1] == "[":
                                desired_index = expressionInt([current[2:]], variables, variableMap)
                                if -1 * len(variables[current_var]) <= desired_index < len(variables[current_var]):
                                        newCurrent = variables[current_var][desired_index]
                                else:
                                        print("Error: Index out of bounds in string " + current[0])
                
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
        SUPPORTED_OPS = {"+", "-", "*", "/", "%", "(", ")", "^"}
        SUPPORTED_LISTOPS = {"sum", "pro", "min", "max", "avg", "gcd", "lcm", "pow", "ncr", "npr"}
        COMPARISON_OPS = {"=", "!", "<", ">", "{", "}"}
        OTHERCOMPARISON_TYPES = {"list", "str"}
        comp_op_present = False

        # Contains or
        if "@" in expr:
                or_exprs = []
                current_expr = []

                for i in range(len(expr)):
                        current = expr[i]

                        if current == "@":
                                if current_expr:
                                        or_exprs.append(current_expr)
                                        current_expr = []
                        else:
                                current_expr.append(current)
                if current_expr:
                        or_exprs.append(current_expr)
                
                evaluation = 0
                for or_expr in or_exprs:
                        evaluation = int(bool(evaluation) or bool(expressionInt(or_expr, variables, variableMap)))

                return evaluation
        
        # Contains and
        if "&" in expr:
                and_exprs = []
                current_expr = []

                for i in range(len(expr)):
                        current = expr[i]

                        if current == "&":
                                if current_expr:
                                        and_exprs.append(current_expr)
                                        current_expr = []
                        else:
                                current_expr.append(current)
                if current_expr:
                        and_exprs.append(current_expr)
                
                # 0 and 0 = 0, p and 0 = 0
                if len(and_exprs) < 2:
                        return 0
                else:
                        evaluation = 1
                        for and_expr in and_exprs:
                                evaluation = int(bool(evaluation) and bool(expressionInt(and_expr, variables, variableMap)))
                        return evaluation
        
        # Contains not
        if "#" in expr:
                not_exprs = []
                current_expr = []
                modified_expr = []
                prefix = False

                if expr[0] != "#":
                        prefix = True

                for i in range(len(expr)):
                        current = expr[i]

                        if current == "#":
                                if not prefix and current_expr:
                                        not_exprs.append(current_expr)
                                        current_expr = []
                                prefix = False
                        elif prefix:
                                modified_expr.append(current)
                        else:
                                current_expr.append(current)
                if not prefix and current_expr:
                        not_exprs.append(current_expr)
                
                for not_expr in not_exprs:
                        modified_expr.append(str(int(not(expressionInt(not_expr, variables, variableMap)))))

                return expressionInt(modified_expr, variables, variableMap)
        
        # Custom comparison
        if len(expr) > 3 and expr[0] == "cmp" and expr[1] in OTHERCOMPARISON_TYPES:
                if expr[1] == "list":
                        return int(expressionList([expr[2]], variables, variableMap) == expressionList([expr[3]], variables, variableMap))
                if expr[1] == "str":
                        return int(expressionStr([expr[2]], variables, variableMap) == expressionStr([expr[3]], variables, variableMap))

        # Contains comparison operator
        for comp_op in COMPARISON_OPS:
                if comp_op in expr:
                        comp_op_present = True
                        break
        
        if comp_op_present:
                comp_exprs = []
                current_expr = []
                comp_ops = []

                for i in range(len(expr)):
                        current = expr[i]

                        if current in COMPARISON_OPS:
                                if current_expr:
                                        comp_exprs.append(current_expr)
                                        current_expr = []
                                
                                if i > 0 and expr[i - 1] in COMPARISON_OPS:
                                        print("Error: two comparison operators in a row in int expression")
                                        return -1
                                
                                comp_ops.append(current)

                        else:
                                current_expr.append(current)
                if current_expr:
                        comp_exprs.append(current_expr)
                
                # Case that expression starts with comparison -> start with 0
                if expr[0] in COMPARISON_OPS:
                        comp_exprs.insert(0, ["0"])
                
                # Case that expression ends with comparison -> ends with 0
                if expr[-1] in COMPARISON_OPS:
                        comp_exprs.append(["0"])
                
                evaluation = expressionInt(comp_exprs[0], variables, variableMap)

                for i in range(1, len(comp_exprs)):
                        current_op = comp_ops[i - 1]

                        if current_op == "=":
                                evaluation = int(evaluation == expressionInt(comp_exprs[i], variables, variableMap))
                        if current_op == "!":
                                evaluation = int(evaluation != expressionInt(comp_exprs[i], variables, variableMap))
                        if current_op == "<":
                                evaluation = int(evaluation < expressionInt(comp_exprs[i], variables, variableMap))
                        if current_op == ">":
                                evaluation = int(evaluation > expressionInt(comp_exprs[i], variables, variableMap))
                        if current_op == "{":
                                evaluation = int(evaluation <= expressionInt(comp_exprs[i], variables, variableMap))
                        if current_op == "}":
                                evaluation = int(evaluation >= expressionInt(comp_exprs[i], variables, variableMap))

                return evaluation

        
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
                                        print("Error: Index out of bounds in list " + current[0])
                                
                        elif current[1] == "[" and len(current) > 2:
                                desired_index = expressionInt([current[2:]], variables, variableMap)
                                if -1 * len(variables[current_var]) <= desired_index < len(variables[current_var]):
                                        newCurrent = str(variables[current_var][desired_index])
                                else:
                                        print("Error: Index out of bounds in list " + current[0])

                
                elif isinteger(current) and transformedExpr and isinteger(transformedExpr[-1]):
                        print("Error: two ints in a row in int expression")
                        continue
                
                # negative
                elif not isinteger(current) and len(current) > 1 and current[0] == "-":
                        newCurrent = str(-1 * expressionInt([current[1:]], variables, variableMap))
                
                # absolute value
                elif not isinteger(current) and len(current) > 1 and current[0] == "|" and current[-1] == "|":
                        newCurrent = str(abs(expressionInt([current[1:-1]], variables, variableMap)))
                
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
                return -1
        
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
                                
                                # Next, slices
                

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
                
                elif inside_commas > 0 and expr[first_comma + 1][0] == "[" or expr[first_comma + 1][0] == "(":
                        range_start_inclusive, range_end_inclusive = evaluateRange(expr[first_comma + 1], variables, variableMap)
                        step_size = 1
                        if inside_commas > 1:
                                step_size = expressionInt([expr[first_comma + 2]], variables, variableMap)

                        if step_size == 0:
                                for iteration in range(range_start_inclusive, range_end_inclusive + 1):
                                        finalList.append(iteration)
                        elif step_size > 0:
                                for iteration in range(range_start_inclusive, range_end_inclusive + 1, step_size):
                                        finalList.append(iteration)
                        else:
                                for iteration in range(range_end_inclusive, range_start_inclusive - 1, step_size):
                                        finalList.append(iteration)           

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
                        
                        elif current[1] == "[":
                                desired_index = expressionInt([current[2:]], variables, variableMap)
                                if -1 * len(variables[current_var]) <= desired_index < len(variables[current_var]):
                                        newCurrent = variables[current_var][desired_index]
                                else:
                                        print("Error: Index out of bounds in string " + current[0])

                # Next, slices
                
                #space
                elif "_" in current:
                        for numSpaces in range(1, LIMIT_SPACE + 1):
                                if "_" * numSpaces == current:
                                        newCurrent = " " * numSpaces
                
                elif len(current) > 2 and current.count("*") == 1:
                        scale_ind = current.index("*")
                        if 1 <= scale_ind < len(current) - 1:
                                desired_scaling = expressionInt([current[scale_ind + 1:]], variables, variableMap)
                                newCurrent = current[:scale_ind] * desired_scaling


                strExpr.append(newCurrent)
        
        for strTerm in strExpr:
                finalStr += strTerm
        
        return finalStr





def runEval(l, returnType, variables, variableMap, variable_ct):
        i_line = 0
        while i_line < len(l):
                line = l[i_line]

                if not line:
                        i_line += 1
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
                                                i_line += 1
                                                continue
                                        elif split_line[1] == "--":
                                                variables[current_var] -= 1
                                                i_line += 1
                                                continue
                                        elif split_line[1] == "+-":
                                                variables[current_var] *= 1
                                                i_line += 1
                                                continue
                                        elif split_line[1] == "-+":
                                                variables[current_var] *= (-1)
                                                i_line += 1
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
                                                        print("Error: Index out of bounds in list " + split_line[0])
                                        
                                        # Set
                                        elif split_line[1] == "set" and len(split_line) > 3:
                                                desired_index = expressionInt([split_line[2]], variables, variableMap)
                                                if -1 * len(variables[current_var]) <= desired_index < len(variables[current_var]):
                                                        variables[current_var][desired_index] = expressionInt(split_line[3:], variables, variableMap)
                                                else:
                                                        print("Error: Index out of bounds in list " + split_line[0])
                                        
                                        # Pop
                                        elif split_line[1] == "pop":
                                                desired_index = expressionInt(split_line[2:], variables, variableMap)
                                                if -1 * len(variables[current_var]) <= desired_index < len(variables[current_var]):
                                                        variables[current_var].pop(desired_index)
                                                else:
                                                        print("Error: Index out of bounds in list " + split_line[0])
                                
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
                                                print("Error: Index out of bounds in list " + split_line[0][0])
                                
                                elif split_line[0][1] == "[" and len(split_line[0]) > 2:
                                        desired_index = expressionInt([split_line[0][2:]], variables, variableMap)
                                        if -1 * len(variables[current_var]) <= desired_index < len(variables[current_var]):
                                                variables[current_var][desired_index] = expressionInt(split_line[2:], variables, variableMap)
                                        else:
                                                print("Error: Index out of bounds in list " + split_line[0][0])
                
                
                # Variable (Declarations)
                elif split_line[0] == "int" and len(split_line) > 1 and len(split_line[1]) == 1 and split_line[1].isalpha():
                        if split_line[1] in variableMap:
                                print("Error: " + split_line[1] + " has already been declared")
                                i_line += 1
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
                                i_line += 1
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
                                i_line += 1
                                continue
                        else:
                                variableMap[split_line[1]] = variable_ct
                                variables.append("")
                                variable_ct += 1
                                current_var = variableMap[split_line[1]]

                                if len(split_line) > 3 and (split_line[2] == "<-" or split_line[2] == "="):
                                        variables[current_var] = expressionStr(split_line[3:], variables, variableMap)
                
                # If statement
                elif split_line[0] == "if" and len(split_line) > 1:
                        endif_index = -1
                        will_return = False

                        for future_i_line in range(i_line + 1, len(l)):
                                future_line = l[future_i_line]

                                if not future_line:
                                        continue

                                future_split_line = future_line.split()

                                if future_split_line[0] == "endif":
                                        endif_index = future_i_line
                                        break

                                if future_split_line[0] == "re":
                                        will_return = True
                        
                        if endif_index != -1:
                                if_block = l[i_line + 1: endif_index]
                                
                                if expressionInt(split_line[1:], variables, variableMap) != 0:
                                        # Case that there is no return yet, evaluate regularly
                                        if not will_return:
                                                _ = runEval(if_block, "", variables, variableMap, variable_ct)
                                        
                                        # Case that there is a return statement in the block
                                        else:
                                                return runEval(if_block, returnType, variables, variableMap, variable_ct)
                                
                                i_line = endif_index
                        else:
                                print("Error: if statement block never ends")
                                break
                
                # For loop
                elif split_line[0] == "for" and len(split_line) > 2 and len(split_line[1]) == 1:
                        endfor_index = -1
                        will_return = False
                        step_size = 1
                        is_enhanced_list = False
                        is_enhanced_str = False
                        range_start_inclusive = None
                        range_end_inclusive = None

                        # Check if enhanced for loop
                        if split_line[2] in variableMap:
                                current_var = variableMap[split_line[2]]

                                if isinstance(variables[current_var], int):
                                        print("Error: Attempt to iterate through int variable " + split_line[2])
                                        i_line += 1
                                        continue
                                elif isinstance(variables[current_var], list):
                                        is_enhanced_list = True
                                elif isinstance(variables[current_var], str):
                                        is_enhanced_str = True
                        
                        # Check range
                        if not is_enhanced_list and not is_enhanced_str:
                                range_start_inclusive, range_end_inclusive = evaluateRange(split_line[2], variables, variableMap)

                                if range_start_inclusive > range_end_inclusive:
                                        i_line += 1
                                        continue
                        
                        # Check iteration variable
                        if split_line[1] in variableMap:
                                current_var = variableMap[split_line[1]]

                                if not isinstance(variables[current_var], int) and not is_enhanced_str:
                                        print("Error: Attempt to iterate using non-int variable " + split_line[1])
                                        i_line += 1
                                        continue
                                if not isinstance(variables[current_var], str) and is_enhanced_str:
                                        print("Error: Attempt to string-iterate using non-str variable " + split_line[1])
                                        i_line += 1
                                        continue
                        else:
                                if is_enhanced_str:
                                        variableMap[split_line[1]] = variable_ct
                                        variables.append("")
                                        variable_ct += 1
                                else:
                                        variableMap[split_line[1]] = variable_ct
                                        variables.append(0)
                                        variable_ct += 1

                        # Check iteration step size
                        if len(split_line) > 3:
                                step_size = expressionInt(split_line[3:], variables, variableMap)

                                if step_size == 0:
                                        print("Error: Attempt to iterate infinitely")
                                        i_line += 1
                                        continue

                        # Look through the for loop block
                        for future_i_line in range(i_line + 1, len(l)):
                                future_line = l[future_i_line]

                                if not future_line:
                                        continue

                                future_split_line = future_line.split()

                                if future_split_line[0] == "endfor":
                                        endfor_index = future_i_line
                                        break

                                if future_split_line[0] == "re":
                                        will_return = True
                        
                        if endfor_index != -1:
                                for_block = l[i_line + 1: endfor_index]
                                current_var = variableMap[split_line[1]]

                                # Evaluate enhanced for loop
                                if is_enhanced_list or is_enhanced_str:
                                        range_start_inclusive = 0
                                        range_end_inclusive = len(variables[variableMap[split_line[2]]]) - 1

                                        if will_return:
                                                if step_size > 0:
                                                        for iteration in range(range_start_inclusive, range_end_inclusive + 1, step_size):
                                                                variables[current_var] = variables[variableMap[split_line[2]]][iteration]
                                                                evalMaybe = runEval(for_block, returnType, variables, variableMap, variable_ct)
                                                                if evalMaybe != "":
                                                                        return evalMaybe
                                                else:
                                                        for iteration in range(range_end_inclusive, range_start_inclusive - 1, step_size):
                                                                variables[current_var] = variables[variableMap[split_line[2]]][iteration]
                                                                evalMaybe = runEval(for_block, returnType, variables, variableMap, variable_ct)
                                                                if evalMaybe != "":
                                                                        return evalMaybe
                                        else:
                                                if step_size > 0:
                                                        for iteration in range(range_start_inclusive, range_end_inclusive + 1, step_size):
                                                                variables[current_var] = variables[variableMap[split_line[2]]][iteration]
                                                                _ = runEval(for_block, "", variables, variableMap, variable_ct)
                                                else:
                                                        for iteration in range(range_end_inclusive, range_start_inclusive - 1, step_size):
                                                                variables[current_var] = variables[variableMap[split_line[2]]][iteration]
                                                                _ = runEval(for_block, "", variables, variableMap, variable_ct)
                                
                                # Evaluate range for loop
                                else:
                                        if will_return:
                                                if step_size > 0:
                                                        for iteration in range(range_start_inclusive, range_end_inclusive + 1, step_size):
                                                                variables[current_var] = iteration
                                                                evalMaybe = runEval(for_block, returnType, variables, variableMap, variable_ct)
                                                                if evalMaybe != "":
                                                                        return evalMaybe
                                                else:
                                                        for iteration in range(range_end_inclusive, range_start_inclusive - 1, step_size):
                                                                variables[current_var] = iteration
                                                                evalMaybe = runEval(for_block, returnType, variables, variableMap, variable_ct)
                                                                if evalMaybe != "":
                                                                        return evalMaybe
                                        else:
                                                if step_size > 0:
                                                        for iteration in range(range_start_inclusive, range_end_inclusive + 1, step_size):
                                                                variables[current_var] = iteration
                                                                _ = runEval(for_block, "", variables, variableMap, variable_ct)
                                                else:
                                                        for iteration in range(range_end_inclusive, range_start_inclusive - 1, step_size):
                                                                variables[current_var] = iteration
                                                                _ = runEval(for_block, "", variables, variableMap, variable_ct)
                                
                                i_line = endfor_index
                        else:
                                print("Error: for loop block never ends")
                                break
                                        
                i_line += 1
        
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
        remove_program = "REMOVE"
        # edit_program = "EDITTO"
        clear_program = "CLEAR"
        
        # Eval-code variables
        # LIMITS = [20, 1] # 0: vars, 1: funcs

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
                
                elif line == undo_program and num_lines > 0:
                        lines.pop()
                        num_lines -= 1
                
                elif len(line) > 7 and line[:6] == remove_program and line[6] == " " and line[7:].isdigit() and num_lines > 0:
                        desired_line_num = int(line[7:])

                        if 0 <= desired_line_num < num_lines:
                                lines.pop(desired_line_num)
                                num_lines -= 1
                        else:
                                continue
                
                elif line == clear_program:
                        lines = []
                        num_lines = 0
                
                else:
                        lines.append(line)
                        num_lines += 1
        
        if lines:
                if lines[0] in TYPES_SUPPORTED:
                        returns = True

        print()

        # Evaluate
        variables = []
        variableMap = {}
        variable_ct = 0

        if returns:
                serializedResult = runEval(lines[1:], lines[0][:3], variables, variableMap, variable_ct)
                result = None

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
                
                if result is not None:
                        print("Your result is...")
                        print(result)
        else:
                _ = runEval(lines, "", variables, variableMap, variable_ct)

        print("Thanks for using Stringscript!")





"""
Run the code to Stringscript!
"""
try:
        run()
except KeyboardInterrupt:
        print("\nStringscript interrupted by user keyboard")
        print("Thanks for using Stringscript!")