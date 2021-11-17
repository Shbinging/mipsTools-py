from funcCheckGenerator import utoS

def wIn(value, mess = "", port = "instr", sep = "\n"):
    global fp
    global s
    if (sep == "\n"):
        fp.write(f"//{mess}\n")
        fp.write(f'poke(c.io.{port}, {value}L.U);')
        wClock(sep)
    else:
        fp.write(f'poke(c.io.{port}, {value}L.U){sep}')
    


def wOut(value, mess = "", port = "instr"):
    global fp
    global s
    s = s + 1
    fp.write(f"//{mess} expect {value}U {utoS(value)}S\n")
    fp.write(f'expect(c.io.{port}, {value}L.U, "{s}")\n')

def wClock(sep = "\n"):
    global fp
    fp.write(f"step(1){sep}")

def loadToMem(addr, instr = "", help = ""):
    if (addr == -1):
        port = "init.writeEn"
        value = "1"
        fp.write(f'poke(c.io.{port}, {value}L.U)\n')
        wClock()
    else:
        fp.write(f"//{help}\n")
        port = "init.addr"
        value = addr
        fp.write(f'poke(c.io.{port}, {value}L.U);')
        port = "init.instr"
        value = instr
        fp.write(f'poke(c.io.{port}, {value}L.U);')
        wClock()
        

if (__name__ == "__main__"):
    fp = open("ori.in", "w")
    loadToMem(-1)
    s = -1
    with open("ori.o", "r") as fp1:
        for line in fp1:
            s += 1
            lst = line.split("//")
            loadToMem(s, lst[0], lst[1][:-1])
        fp.write("""
//set pc to 0
poke(c.io.init.pcInit, 0.U)
poke(c.io.init.cpuReset, 1.U)
step(1)
poke(c.io.init.cpuReset, 0.U)
        """)
    for i in range(0, 60):
        fp.write("step(1);")

