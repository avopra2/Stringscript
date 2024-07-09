def evaluatePrint(expr, variables, variableMap):
        printExpr = []

        for i in range(len(expr)):
                current = expr[i]

                if expr[i] in variableMap:
                        if isinstance(variables[variableMap[expr[i]]], int):
                                current = str(variables[variableMap[expr[i]]])
                        elif isinstance(variables[variableMap[expr[i]]], list):
                                current = ", ".join([str(item) for item in variables[variableMap[expr[i]]]])
                        elif isinstance(variables[variableMap[expr[i]]], str):
                                current = variables[variableMap[expr[i]]]

                printExpr.append(current)
        
        for printItem in printExpr:
                print(printItem, end = " ")
        print()



def expressionInt(expr, variables, variableMap):
        return 0

def expressionList(expr, variables, variableMap):
        return []

def expressionStr(expr, variables, variableMap):
        return ""

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
                if split_line[0] == "pr":
                        evaluatePrint(split_line[1:], variables, variableMap)

                # int variable
                if len(split_line[0]) == 1 and split_line[0].isalpha():
                        if split_line[0] not in variableMap:
                                variableMap[split_line[0]] = variable_ct
                                variables.append(0)
                                variable_ct += 1
                        current_var = variableMap[split_line[0]]

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
                
                print("Your result is", result)
        else:
                _ = runEval(lines, "")

        print("Thanks for using Stringscript!")





"""
Run the code to Stringscript!
"""
run()