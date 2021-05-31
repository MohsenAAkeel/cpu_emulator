def genConditionOrForLoop(self, flag, source):
    assemblyCode = []
    # generate condition labels
    topLabel = "L" + str(self.genLabelCount())
    bottomLabel = "L" + str(self.genLabelCount())

    #generate assembly comment
    initialization = "int " + source["initialization"]["dataName"] + "=" + source["initialization"][
        "dataValue"] + ";"
    termination = source["termination"] + ";"
    increment = (source["increment"]["destination"] + "=" + source["increment"]["operand1"] +
                 source["increment"]["operator"] + source["increment"]["operand2"])
    og_comment = " # for(" + initialization + termination + increment + ")"

    #########################################################
    # initialize for loop conditional value in memory with value in source
    for x in self.genDeclaration(source["initialization"]):
        assemblyCode.append(x)

    # add the label name
    assemblyCode.append(topLabel + ":" + og_comment)

    # make comparison
    curr_op = ""
    op_ctr = 0
    while curr_op == "":
        (operand1, operator, operand2) = source["termination"].partition(self.operators[op_ctr])
        curr_op = operator
        op_ctr += 1

    comment = " # " + operand1 + operator + operand2
    if operand1.isdigit():
        if operand2.isdigit():  # both op1 and op2 are numbers
            assemblyCode.append("mov " + REG1 + ", " + operand1)
            assemblyCode.append("mov " + REG2 + ", " + operand2)
            assemblyCode.append("cmp " + REG1 + ", " + REG2 + comment)
        else:  # op1 is a number but op2 is a variable
            assemblyCode.append("mov " + REG1 + ", " + operand1)
            assemblyCode.append(
                "cmp " + REG1 + ", DWORD PTR [rbp" + str(self.varTable.address(operand2)) + "]" + comment)
    else:
        if operand2.isdigit():  # op2 is a number but op1 is a variable
            assemblyCode.append("mov " + REG1 + ", " + operand2)
            assemblyCode.append("cmp DWORD PTR [rbp" + str(self.varTable.address(operand1)) + "], " + REG1 + comment)
        else:  # both op1 and op2 are variables
            assemblyCode.append("cmp DWORD PTR [rbp" + str(self.varTable.address(operand1)) + "], DWORD PTR [rbp" + str(
                self.varTable.address(operand2)) + "]" + comment)

    # jump on opposite condition (e.g. opposite of < is >=, so do jge)
    if operator == "<=":
        assemblyCode.append("jg " + bottomLabel)
    elif operator == ">=":
        assemblyCode.append("jl " + bottomLabel)
    elif operator == "<":
        assemblyCode.append("jge " + bottomLabel)
    elif operator == ">":
        assemblyCode.append("jle " + bottomLabel)
    elif operator == "==":
        assemblyCode.append("jne " + bottomLabel)
    elif operator == "!=":
        assemblyCode.append("je " + bottomLabel)

    # body
    for item in source["statement"]:
        codeType = item["codeType"]
        if codeType == "declaration":
            tmpCode = self.genDeclaration(item)
        elif codeType == "if":
            tmpCode = self.genCondition(item)
        elif codeType == "for":
            tmpCode = self.genForLoop(item)
        elif codeType == "logicOperation":
            tmpCode = self.genLogical(item)
        else:
            tmpCode = self.genReturn(item)
        for x in tmpCode:
            assemblyCode.append(x)

    if flag == "for":
        # incrememnt conditional variable
        tmpCode = self.genLogical(source["increment"])
        for x in tmpCode:
            assemblyCode.append(x)

        assemblyCode.append("jmp " + topLabel)

    comment = " # end of " + topLabel + ":" + og_comment.split("#")[1]
    assemblyCode.append(bottomLabel + ":" + comment)
    return assemblyCode


def genCondition():
    og_comment = " # if(" + source["termination"] + ")"