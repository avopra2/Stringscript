def evaluatePrint(expr, variables, variableMap):
        printExpr = []

        for i in range(len(expr)):
                current = expr[i]

                if current in variableMap:
                        if isinstance(variables[variableMap[current]], int):
                                current = str(variables[variableMap[current]])
                        elif isinstance(variables[variableMap[current]], list):
                                current = ", ".join([str(item) for item in variables[variableMap[current]]])
                        elif isinstance(variables[variableMap[current]], str):
                                current = variables[variableMap[current]]
                
                elif len(current) > 1 and current[0] in variableMap and current[1:].isdigit():
                        desired_index = int(current[1:])
                        if 0 <= desired_index < len(variables[variableMap[current[0]]]):
                                current = variables[variableMap[current[0]]][desired_index]
                
                elif len(current) > 2 and current[0] in variableMap and current[1] == "*" and current[2:].isdigit():
                        desired_scaling = int(current[2:])
                        current = variables[variableMap[current[0]]] * desired_scaling
                
                elif len(current) == 3 and current[0] in variableMap and current[1:] == "id":
                        current = str(variableMap[current[0]])
                
                elif len(current) > 2 and current.count("*") == 1:
                        scale_ind = current.index("*")
                        if 1 <= scale_ind < len(current) - 1 and current[scale_ind + 1:].isdigit():
                                desired_scaling = int(current[scale_ind + 1:])
                                current = current[:scale_ind] * desired_scaling

                printExpr.append(current)
        
        for printItem in printExpr:
                print(printItem, end = " ")
        print()





def expressionInt(expr, variables, variableMap):
        return 0





def expressionList(expr, variables, variableMap):
        finalList = []
        
        commas = [-1]
        for i in range(len(expr)):
                if expr[i] == ",":
                        commas.append(i)
        commas.append(len(expr))

        for i in range(len(commas) - 1):
                first_comma = commas[i]
                second_comma = commas[i + 1]

                if second_comma - first_comma == 2 and expr[first_comma + 1] in variableMap:
                        current_var = variableMap[expr[first_comma + 1]]

                        if isinstance(variables[current_var], int):
                                finalList.append(variables[current_var])
                        elif isinstance(variables[current_var], list):
                                for intElem in variables[current_var]:
                                        finalList.append(intElem)
                        elif isinstance(variables[current_var], str):
                                if variables[current_var].isdigit():
                                        finalList.append(int(variables[current_var]))
                                else:
                                        print("Error: String variable " + expr[first_comma + 1] + " in int-based list")
                                        finalList.append(0)

                elif second_comma - first_comma > 1:
                        finalList.append(expressionInt(expr[first_comma + 1: second_comma], variables, variableMap))

        return finalList

def expressionStr(expr, variables, variableMap):
        # Eval-string variables
        LIMIT_SPACE = 5
        
        finalStr = ""
        strExpr = []

        for i in range(len(expr)):
                current = expr[i]

                if current in variableMap:
                        if isinstance(variables[variableMap[current]], int):
                                current = str(variables[variableMap[current]])
                        elif isinstance(variables[variableMap[current]], list):
                                current = ", ".join([str(item) for item in variables[variableMap[current]]])
                        elif isinstance(variables[variableMap[current]], str):
                                current = variables[variableMap[current]]
                
                elif len(current) > 1 and current[0] in variableMap and current[1:].isdigit():
                        desired_index = int(current[1:])
                        if 0 <= desired_index < len(variables[variableMap[current[0]]]):
                                current = variables[variableMap[current[0]]][desired_index]
                
                elif len(current) > 2 and current[0] in variableMap and current[1] == "*" and current[2:].isdigit():
                        desired_scaling = int(current[2:])
                        current = variables[variableMap[current[0]]] * desired_scaling
                
                elif len(current) > 2 and current.count("*") == 1:
                        scale_ind = current.index("*")
                        if 1 <= scale_ind < len(current) - 1 and current[scale_ind + 1:].isdigit():
                                desired_scaling = int(current[scale_ind + 1:])
                                current = current[:scale_ind] * desired_scaling

                #space
                elif "_" in current:
                        for numSpaces in range(1, LIMIT_SPACE + 1):
                                if "_" * numSpaces == current:
                                        current = " " * numSpaces


                strExpr.append(current)
        
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
                                                        variables[current_var] //= expressionInt(split_line[2:], variables, variableMap)
                                        elif split_line[1] == "%=":
                                                if split_line[2:]:
                                                        variables[current_var] %= expressionInt(split_line[2:], variables, variableMap)
                                        elif split_line[1] == "?=":
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
                                        elif split_line[1] == "ins" and len(split_line) > 3 and split_line[2].isdigit():
                                                desired_index = int(split_line[2])
                                                if 0 <= desired_index <= len(variables[current_var]):
                                                        variables[current_var].insert(desired_index, expressionInt(split_line[3:], variables, variableMap))
                                        
                                        # Set
                                        elif split_line[1] == "set" and len(split_line) > 3 and split_line[2].isdigit():
                                                desired_index = int(split_line[2])
                                                if 0 <= desired_index < len(variables[current_var]):
                                                        variables[current_var][desired_index] = expressionInt(split_line[3:], variables, variableMap)
                                        
                                        # Pop
                                        elif split_line[1] == "pop" and split_line[2].isdigit():
                                                desired_index = int(split_line[2])
                                                if 0 <= desired_index < len(variables[current_var]):
                                                        variables[current_var].pop(desired_index)
                                
                                if len(split_line) >= 2:

                                        # Pop
                                        if split_line[1] == "pop" and (len(split_line) == 2 or not split_line[2].isdigit()):
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
                                        if split_line[1] == "strp":
                                                variables[current_var] = variables[current_var].strip()
                                        
                                        # cases
                                        elif split_line[1] == "upp":
                                                variables[current_var] = variables[current_var].upper()
                                        elif split_line[1] == "low":
                                                variables[current_var] = variables[current_var].lower()
                                        elif split_line[1] == "titl":
                                                variables[current_var] = variables[current_var].title()
                                        elif split_line[1] == "cap":
                                                variables[current_var] = variables[current_var].capitalize()
                

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
        lines_supported = 10
        end_program = "done"
        
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