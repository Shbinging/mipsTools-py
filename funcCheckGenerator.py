import pandas as pd
from random import randrange as rr
import numpy
rFuncName = {
    "add": "100000",
    "sub": "100010",
    "and":"100100",
    "or":"100101",
    "xor":"100110",
    "slt":"101010",
    "sltu":"101011",
    "sll":"000000",
    "srl":"000010",
    "sra":"000011",
    "sllv":"000100",
    "srlv":"000110",
    "srav":"000111",
    "jalr":"001001"
}
iOpName = {
    "begz":"000001",
    "bltz":"000001",
    "beq":"000100",
    "bne":"000101",
    "addi":"001000",
    "andi":"001100",
    "ori":"001101",
    "xori":"001110",
    "slti":"001010",
    "sltiu":"001011",
    "lui":"001111"
}

jOpName = {
    "jal":"000011",
    "halt":"111111"
}
def to10S(st):
    return int(st[0]) * (-2**31) + int(st[1:], 2)
def to10U(st):
    return int(st, 2)

def str2(n, m = 32):
    if (n < 0):
        return str(bin(0xffffffff + n + 1)[2:]).zfill(m)
    return str(bin(n)[2:]).zfill(m)

def extend(st, sign):
    if (sign == 0):
        return st.zfill(16)
    else:
        return st[0] * 16 + st
def stoU(n):
    return to10U(str2(n, 32))

def utoS(n):
    return to10S(str2(n, 32))

def rType(opName, rs, rt, rd, shamt, sep = "\n"):
    instr = str2(0, 6) + str2(rs, 5) + str2(rt, 5) + str2(rd, 5) + str2(shamt, 5) + rFuncName[opName]
    cpu.run(int(instr, 2))
    help = f"{opName} ${rd}, ${rs}, ${rt}, {shamt}"
    wIn(int(instr, 2), help, sep)

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
    cpu.run(int(instr, 2))
    help =  f"{opName} ${rt}, ${rs}, {imm}"
    wIn(int(instr, 2), help, sep)

def jType(opName, target, sep = "\n"):
    instr = jOpName[opName] + str2(target, 26)
    global cpu
    cpu.run(int(instr, 2))
    help = f"{opName} {target}"
    wIn(int(instr, 2), help, sep)

class cpuStd:
    regs = [0] * 32
    pc = 0
    def rTypeCalc(self, instr):
        rs = int(instr[6:11], 2)
        rt = int(instr[11:16], 2)
        rd = int(instr[16:21], 2)
        shamt = int(instr[21:26], 2)
        func = instr[26:32]
        
        if (func == "100000"):
            if ((self.regs[rs] + self.regs[rt] < 2**31) and (self.regs[rs] + self.regs[rt] >= -2**31)):
                self.regs[rd] = self.regs[rs] + self.regs[rt]
        if (func == "100010"):
            if ((self.regs[rs] - self.regs[rt] < 2**31) and (self.regs[rs] - self.regs[rt] >= -2**31)):
                self.regs[rd] = self.regs[rs] - self.regs[rt]
        if (func == "100100"):
            self.regs[rd] = utoS(stoU(self.regs[rs]) & stoU(self.regs[rt]))
        if (func == "100101"):
            self.regs[rd] = utoS(stoU(self.regs[rs]) | stoU(self.regs[rt]))
        if (func == "100110"):
            self.regs[rd] = utoS(stoU(self.regs[rs]) ^ stoU(self.regs[rt]))
        if (func == "101010"):
            if(self.regs[rs] < self.regs[rt]):
                self.regs[rd] = 1
            else:
                self.regs[rd] = 0

        if (func == "101011"):
            if (stoU(self.regs[rs]) < stoU(self.regs[rt])):
                self.regs[rd] = 1
            else:
                self.regs[rd] = 0

        if (func == "000000"):
            self.regs[rd] = to10S(str2(self.regs[rt], 32)[shamt:] + "0" * shamt)
        if (func == "000010"):
            if (shamt != 0):
                self.regs[rd] = to10S("0"*shamt + str2(self.regs[rt], 32)[:-shamt])
            else:
                self.regs[rd] = self.regs[rt]
        if (func == "000011"):
            self.regs[rd] = self.regs[rt] >> shamt
        
        if (func == "000100"):
            self.regs[rd] = to10S(str2(self.regs[rt], 32)[self.regs[rs]:] + "0" * self.regs[rs])
        
        if (func == "000110"):
            if(self.regs[rs] != 0):
                self.regs[rd] = to10S("0"*self.regs[rs] + str2(self.regs[rt], 32)[:-self.regs[rs]])
            else:
                self.regs[rd] = self.regs[rt]
        
        if (func == "000111"):
            self.regs[rd] = self.regs[rt] >> self.regs[rs]
        
        if (func == "001001"):
            self.regs[rd] = self.pc + 8
            self.pc = self.regs[rs]
            return
        self.pc += 4

    def iTypeCalc(self, instr):
        op = instr[0:6]
        rs = int(instr[6:11], 2)
        rt = int(instr[11:16], 2)
        imm = instr[16:32]
        imm32s = to10S(extend(imm, 1))
        imm32u = to10U(extend(imm, 0))
        if (op == "000001"):
            if (rt == 1 and self.regs[rs] >= 0):
                self.pc = self.pc + 4 + to10S(extend(imm, 1)) * 4
                return
            if (rt == 0 and self.regs[rs] < 0):
                self.pc = self.pc + 4 + to10S(extend(imm, 1)) * 4
                return
            
        if (op == "000100"):
            if (self.regs[rs] == self.regs[rt]):
                self.pc = self.pc + 4 + to10S(extend(imm, 1)) * 4
                return
        if (op == "000101"):
            if (self.regs[rs] != self.regs[rt]):
                self.pc = self.pc + 4 + to10S(extend(imm, 1)) * 4
                return
        if (op == "001000"):
            if ((self.regs[rs] + imm32s < 2**31) and (self.regs[rs] + imm32s >= -2**31)):
                self.regs[rt] = self.regs[rs] + imm32s
        if (op == "001010"):
            if (self.regs[rs] < imm32s):
                self.regs[rt] = 1
            else:
                self.regs[rt] = 0
        if (op == "001011"):
            if (stoU(self.regs[rs]) < stoU(imm32s)):
                self.regs[rt] = 1
            else:
                self.regs[rt] = 0
        if (op == "001100"):
            self.regs[rt] = utoS(stoU(self.regs[rs]) & imm32u)
        if (op == "001101"):
            self.regs[rt] = utoS(stoU(self.regs[rs]) | imm32u)
        if (op == "001110"):
            self.regs[rt] = utoS(stoU(self.regs[rs]) ^ imm32u)
        if (op == "001111"):
            self.regs[rt] = to10S(imm + "0" * 16)
        self.pc += 4
    
    def jTypeCalc(self, instr):
        op = instr[0:6]
        instr_index = instr[6:]
        if (op == "000011"):
            self.regs[31] = self.pc + 8
            self.pc = to10S(str2(self.pc, 32)[0:4] + instr_index + "00")
        if (op == "111111"):
            pass

        
    def run(self, instrInt):
        instr = str2(instrInt, 32)
        op = instr[0:6]
        if (op == "000000"):
            self.rTypeCalc(instr)
        elif (op in jOpName.values()):
            self.jTypeCalc(instr)
        else:
            self.iTypeCalc(instr)
    
    def getReg(self, num):
        return stoU(self.regs[num])
    
    def getPC(self):
        return stoU(self.pc)
        

import ctypes
def int_overflow(val):
    maxint = 2147483647
    if not -maxint-1 <= val <= maxint:
        val = (val + (maxint + 1)) % (2 * (maxint + 1)) - maxint - 1
    return val


def unsigned_right_shitf(n,i):
    # 数字小于0，则转为32位无符号uint
    if n<0:
        n = ctypes.c_uint32(n).value
    # 正常位移位数是为正数，但是为了兼容js之类的，负数就右移变成左移好了
    if i<0:
        return -int_overflow(n << abs(i))
    #print(n)
    return int_overflow(n >> i)
# 参数分别是要移的数字和移多少位


def wIn(value, mess = "", sep = "\n", port = "instr"):
    global fp
    global s
    #print(value)
    # valueList = []
    # for i in range(0, 4):
    #     valueList.append(str(value & 0xff) + "L.U")
    #     value = unsigned_right_shitf(value, 8)
    if (sep == "\n"):
        fp.write(f"//{mess}\n")
        #fp.write(f'{",".join(valueList)}L.U,')
        fp.write(f'{value}L.U,')
        wClock(sep)
    else:
        #fp.write(f'{",".join(valueList)},')
        fp.write(f'{value}L.U,')
        wClock(sep)
    


def wOut(value, mess = "", port = "instr"):
    global fp
    global s
    s = s + 1
    fp.write(f"//{mess} expect {value}U {utoS(value)}S\n")
    fp.write(f'expect(c.io.{port}, {value}L.U, "{s}")\n')

def wClock(sep):
    pass

value32List = [0x80000000, 0xFFFFFFFF, 0, 1, 0x7FFFFFFF]#8
value16List = [0, 1, 0xffff, 0x7fff, 0x8000, 0x8001]#7

def setReg(index, val, hide = 0):
    global fp
    valH = (val >> 16) & 0xffff
    valL = val & 0xffff
    if (not hide):
        fp.write(f"//set reg({index}) = {val}U, {utoS(val)}S\n")
    iType("lui", 0, index, valH, ";")
    iType("ori", index, index, valL, ";")
    if (not hide):
        fp.write("\n")
    

def setPc(val, hide = 0):
    global fp
    val -= 16
    val1 = cpu.getReg(1)
    val2 = cpu.getReg(2)
    if (not hide):
        fp.write(f"//set pc = {val + 16} \n")
    setReg(1, val, 1)
    rType("jalr", 1, 0, 2, 0, ";")
    setReg(1, val1, 1)
    setReg(2, val2, 1)
    if (not hide):
        fp.write("\n")


def checkRType(instrName, rs, rt, rd, rsVal, rtVal, rdVal, pcVal = 256, shamt = 0):
    global cpu
    setReg(rd, rdVal)
    setReg(rs, rsVal)
    setReg(rt, rtVal)

    setPc(pcVal)
    rType(instrName, rs, rt, rd, shamt)
    checkReg(rs, cpu.getReg(rs))
    checkReg(rt, cpu.getReg(rt))
    checkReg(rd, cpu.getReg(rd))
    checkPc(cpu.getPC())

def checkIType(instrName, rs, rt, imm, rsVal, rtVal, pcVal = 256):
    global cpu
    setReg(rs, rsVal)
    setReg(rt, rtVal)

    setPc(pcVal)

    iType(instrName, rs, rt, imm)

    checkReg(rs, cpu.getReg(rs))
    checkReg(rt, cpu.getReg(rt))
    checkPc(cpu.getPC())

def checkJType(instrName, instr_target, pcVal = 0xf0000000):
    global cpu
    setPc(pcVal)

    jType(instrName, instr_target)

    checkPc(cpu.getPC())

def checkReg(index, val):
    wOut(val, f"watch.regs({index})", f"watch.regs({index})")

def checkPc(val):
    wOut(val, f"watch.pc", f"watch.pc")

"""
rFuncName = {
    "add": "100000",
    "sub": "100010",
    "and":"100100",
    "or":"100101",
    "xor":"100110",
    "slt":"100110",
    "sltu":"101011",
    "sll":"000000",
    "srl":"000010",
    "sra":"000011",
    "sllv":"000100",
    "srlv":"000110",
    "srav":"000111",
    "jalr":"001001"
}
"""
cpu = cpuStd()
fp = open("instr.in", "w")
if (__name__ == "__main__"):
    s = 0
    #setReg(1, 1)
    #setPc(128)
    #checkPc(cpu.getPC())
    #checkRType("sll", 1, 2, 3, 1, 1, 3, 256, 10)
    """
    for i in range(0, len(value32List)):
        for j in range(0, len(value32List)):
            checkRType("srav", rr(1, 30), rr(1, 30), rr(1, 30), rr(0, (2**5) - 1), value32List[j], value32List[i], rr(100, 0xffffff) * 4, rr(0, (2**5) - 1))

    """
    iType("addi", 0, 1, 10)
    iType("addi", 1, 2, 10)
    #checkRType("add", 1, 2, 3, 1 ,2, 3, 0, 0)
    # for i in range(0, len(value32List)):
    #     for j in range(0, len(value32List)):
    #         checkRType("jalr", 1, 2, 3, rr(0, (2**31) - 1) // 4 * 4, 0, value32List[i], rr(100, 0xffffff) * 4, rr(0, (2**5) - 1))
    
    # for i in range(0, 1):
    #     for k in range(1, 2):
    #         if (i >= k):continue
    #         for j in range(0, 1):
    #             checkIType("lui", 1, 2, value16List[j], value32List[i], value32List[k], 0xfffff * 4)
    
    #for i in range(0,len(value32List)):
        #checkJType("halt", value32List[i] & 0x3ffffff)
    """
    iType("addi", 1, 1, 16)
    """

    fp.close()
    
