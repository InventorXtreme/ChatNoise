import tkinter
from tkinter import *

def main(filename):
    #Init file
    mainfile = open(filename, "r")
    filestring = mainfile.read()
    linelist = filestring.split("\n")

    #Init lbl lists
    lbls = {}

    #Label PreParse
    lbllinecount = 0
    for i in linelist:
        i2 = i.split(",")
        if i2[0] == "lbl" or i2[0] == "label":
            lbls[i2[1]] = lbllinecount
        lbllinecount = lbllinecount + 1

    # Init Str Vars lists
    strvars = {}

    def get_str_var(name):
        return strvars[name]

    def add_str_var(name, data):
        strvars[name] = data
    run = True
    count = 0
    #
    while run == True:
        goto = False
        line = linelist[count]
        command = line.split(",")

        if command[0] == "goto":
            goto = True
            if command[1] == "line":
                count = int(command[2])
            if command[1] == "label" or command[1] == "lbl":
                count = int(lbls[command[2]])
        elif command[0] == "lbl" or command[0] == "label":
            yee=1
        elif command[0] == "run":
            main(command[1])

        elif command[0] == "end":
            run = False
        elif command[0] == "print":
            print(command[1])

        else:
            print("error in line "+str(count) + "")
            print("command "+line+" not found")
            break

        if goto == False or run == False:
            count = count + 1