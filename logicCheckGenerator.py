import pandas as pd


df = pd.read_csv("logicCheck.csv", dtype=int)
columnsName = list(df.columns)

s = 0


def wIn(fp, port, value):
    global s
    s = s + 1
    fp.write(f' poke(c.io.{port}, {value}.U)\n')


def wOut(fp, port, value):
    global s
    fp.write(f' expect(c.io.{port}, {value}.U, "{s}")\n')


with open("check.in", "w") as fp:
    for i in range(0, len(df)):
        line = df.iloc[i]
        instr = str(line["op"]).zfill(6) + "0" * 5 + \
            str(line["rt"]).zfill(5) + "0" * 5 + \
            "0" * 5 + str(line["func"]).zfill(6)
        if (line["rt"] == 1):
            print(instr)
        instr = int(instr, 2)
        wIn(fp, "instr", instr)
        for j in range(3, len(columnsName)):
            port = columnsName[j]
            value = line[port]
            if (value == -1):
                continue
            try:
                value = int(str(value), 2)
            except:
                value = value
            wOut(fp, port, value)

# print(df)
