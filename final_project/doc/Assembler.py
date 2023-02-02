import os
import sys

# reference : https://github.com/rose/nand2tetris/blob/master/assembler.py

table = {
    "SP"    :0,    
    "LCL"   :1,    
    "ARG"   :2,
    "THIS"  :3,
    "THAT"  :4,
    "SCREEN":16384,
    "KBD"   :24576,
    }

dest = {    #ADM
    "null"  : "000",
    "M"     : "001",
    "D"     : "010",
    "A"     : "100",
    "MD"    : "011",
    "AM"    : "101",
    "AD"    : "110",
    "AMD"   : "111"
    }

comp = {
    "0"     : "0101010",
    "1"     : "0111111",
    "-1"    : "0111010",
    "D"     : "0001100",
    "A"     : "0110000",
    "!D"    : "0001101",
    "!A"    : "0110001",
    "-D"    : "0001111",
    "-A"    : "0110011",
    "D+1"   : "0011111",
    "A+1"   : "0110111",
    "D-1"   : "0001110",
    "A-1"   : "0110010",
    "D+A"   : "0000010",
    "D-A"   : "0010011",
    "A-D"   : "0000111",
    "D&A"   : "0000000",
    "D|A"   : "0010101",
    "M"     : "1110000",
    "!M"    : "1110001",
    "-M"    : "1110011",
    "M+1"   : "1110111",
    "M-1"   : "1110010",
    "D+M"   : "1000010",
    "D-M"   : "1010011",
    "M-D"   : "1000111",
    "D&M"   : "1000000",
    "D|M"   : "1010101"
    }

jump = {
    "null": "000",
    "JGT" : "001",
    "JEQ" : "010",
    "JGE" : "011",
    "JLT" : "100",
    "JNE" : "101",
    "JLE" : "110",
    "JMP" : "111"
    }

variable_N = 16
filename = sys.argv[1]

def strip(line):
#去掉空格和註解、換行
    head = line[0]
    if head == "\n" or head == "/":
        return ""
    elif head == " ":
        return strip(line[1:])
    else:
        return head + strip(line[1:])

def clear():
#開檔案、去掉註解
    infile = open(filename + ".asm")
    outfile = open(filename + ".tmp", "w")

    line_N = 0
    for line in infile:
        strip_line = strip(line)
        if strip_line != "":
            if strip_line[0] == "(":
                label = strip_line[1:-1]
                table[label] = line_N
                strip_line = ""
            else:
                line_N += 1
                outfile.write(strip_line + "\n")

def addVariable(label):
    global variable_N
    table[label] = variable_N
    variable_N += 1
    return table[label]

def aTranslate(line):
    
    if line[1].isalpha():
        label = line[1:-1]
        a_N = table.get(label, -1)
        if a_N == -1:
            a_N = addVariable(label)
    else:
        a_N = int(line[1:])
    b_N = bin(a_N)[2:].zfill(16)
    return b_N

def cTranslate(line):
#把=;加進去(如果需要的話)
#translate
    line = normalize(line)
    temp = line.split("=")
    destReturn = dest.get(temp[0], "destFAIL")
    temp = temp[1].split(";")
    compReturn = comp.get(temp[0], "compFAIL")
    jumpReturn = jump.get(temp[1], "jumpFAIL")
    return compReturn, destReturn, jumpReturn

def normalize(line):
#加入NULL dest % jump
    line = line[:-1]
    if not "=" in line:
        line = "null="+line
    if not ";" in line:
        line = line + ";null"
    return line

def translate(line):
#分成A C指令
    if line[0] == "@":
        return aTranslate(line)
    else:
        R = cTranslate(line)
        return "111" + R[0] + R[1] + R[2]

def assemble():
#接收乾淨的code再轉成.hack
    infile = open(filename + ".tmp")
    outfile= open(filename + ".hack", "w")

    for line in infile:
        translate_line = translate(line)
        outfile.write(translate_line + "\n")
    
    infile.close()
    outfile.close()
    os.remove(filename + ".tmp")

for i in range(0,16):
    label = "R" + str(i)
    table[label] = i

clear()
assemble()