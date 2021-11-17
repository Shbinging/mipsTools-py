from funcCheckGenerator import jType, rFuncName,iOpName,jOpName,str2,to10U

def wOut(instr, help=""):
    if len(help): help = "//" + help
    fp.write(f"{instr}{help}\n")
def rType(opName, rs, rt, rd, shamt, sep = "\n"):
    instr = str2(0, 6) + str2(rs, 5) + str2(rt, 5) + str2(rd, 5) + str2(shamt, 5) + rFuncName[opName]
    help = f"{opName} ${rd}, ${rs}, ${rt}, {shamt}"
    wOut(int(instr, 2), help)

def iType(opName, rs, rt, imm, sep = "\n"):
    rtStr = ""
    if (opName == "begz"):
        rtStr = "00001"
    elif(opName == "bltz"):
        rtStr = "00000"
    else:
        rtStr = str2(rt, 5)
    global iOpName
    instr = iOpName[opName] + str2(rs, 5) + rtStr + str2(imm, 16)
    help =  f"{opName} ${rt}, ${rs}, {imm}"
    wOut(int(instr, 2), help)

def jType(opName, target, sep = "\n"):
    instr = jOpName[opName] + str2(target, 26)
    global cpu
    help = f"{opName} {target}"
    wOut(int(instr, 2), help)

def findList(lst:list, target:str):
    for word in lst:
        if (target.find(word) != -1): return True
    return False

def formatCode(st:str):
    global allOpList
    st = st.replace("\n", "")
    st = st.split("//")[0]
    st = st.replace("$", "")
    st = st.replace(",", " ")
    st = st.replace(":", " ")
    st = " ".join(st.split())
    if (len(st) == 0): return "-1"
    if (st[0] == "//"): return "-1"
    if (findList(allOpList, st)): return st
    else: return "-1"

def parseFile():
    global instrList
    with open("ori.as", "r") as fp:
        for line in fp:
            codeStr = formatCode(line)
            if (codeStr != "-1"):
                instrList.append(codeStr)

def getLabel():
    global instrList
    for i in range(0, len(instrList)):
        instr:str = instrList[i]
        lst = instr.split()
        if (not findList(allOpList, lst[0])):
            labelList[lst[0]] = i
            instrList[i] = " ".join(lst[1:])

def convert():
    for instr in instrList:
        lst = instr.split()
        if (lst[0] in rFuncName.keys()):
            shamt = 0
            if (len(lst) == 5):
                shamt = lst[4]
            rType(lst[0], int(lst[1]), int(lst[2]), int(lst[3]), shamt)
        if (lst[0] in iOpName.keys()):
            iType(lst[0], int(lst[1]), int(lst[2]), to10U(str2(int(lst[3]))[16:]))
        if (lst[0] in jOpName.keys()):
            jType(lst[0], 0)

def brachReplace():
    for i in range(0, len(instrList)):
        lst = instrList[i].split()
        if (lst[0] in ["begz", "bltz", "beq", "bne"]):
            targetPos = labelList[lst[3]]
            offset = targetPos - i - 1
            lst[3] = str(to10U(str2(offset)[16:]))
        instrList[i] = " ".join(lst)

if (__name__ == "__main__"):
    allOpList = []
    allOpList += list(rFuncName.keys())
    allOpList += list(iOpName.keys())
    allOpList += list(jOpName.keys())
    print(allOpList)
    instrList = []
    labelList = {}
    parseFile()
    getLabel()
    print(instrList)
    brachReplace()
    fp = open("ori.o", "w")
    convert()
    #fp.close()
    print(instrList)
    print(labelList)
