# Robert Boutillier
# Regular expression parsing
# Due 11/27/18

import re
import sys

if len(sys.argv) < 2:
    print("You need to enter a file in the command line")
elif len(sys.argv) > 2:
    print("Only enter one file in the command line")
else:
    try:
        inputfile = open(sys.argv[1], "r")
        intmatcher = re.compile(r"(int )")
        namematcher = re.compile(r"(,[a-zA-Z][\w]+|(,[a-zA-Z])+)+")

        firstline = inputfile.readline()
        f = intmatcher.search(firstline)
        f1 = namematcher.search(firstline)
        if f is None:
            print("The first line variable is not int followed by a space")
            exit(0)

        realmatcher = re.compile(r"(real )")

        secondline = inputfile.readline()
        if secondline in "":
            print("No second line in " + sys.argv[1] + " found")
            exit(0)

        s = realmatcher.search(secondline)

        if s is None:
            print("The second line variable is not real followed by a space")
            exit(0)
        s1 = namematcher.search(secondline)

        intlist = f1.group(0).split(",")
        intlist = intlist[1:]

        reallist = s1.group(0).split(",")
        reallist = reallist[1:]

        linelist = inputfile.readlines()
        intlinematcher = re.compile(r'([1-9][0-9]+)|([0-9])')
        reallinematcher = re.compile(r'[0-9]+[.][0-9]+')
        equalmatcher = re.compile(r'[=]')
        addmatcher = re.compile(r'[+]')
        submatcher = re.compile(r'[-]')
        multmatcher = re.compile(r'[*]')
        expmatcher = re.compile(r'[*][*]')
        idivmatcher = re.compile(r'[/][/]')
        rdivmatcher = re.compile(r'[/]')

        # Replacing int variable names from the first line that are found in the lines after line 2
        for i in range(0, len(intlist)):
            for x in range(0, len(linelist)):

                line = linelist[x]

                intvarmatcher = re.compile(re.escape(intlist[i]))
                intvarline = intvarmatcher.search(line)
                if intvarline is not None:
                    line = line.replace(line[intvarline.start():intvarline.end()], "intvar")
                    linelist[x] = line

        # Replacing real variable names from the second line that are found in the lines after line 2
        for i in range(0, len(reallist)):
            for x in range(0, len(linelist)):

                line = linelist[x]

                realvarmatcher = re.compile(re.escape(reallist[i]))
                realvarline = realvarmatcher.search(line)
                if realvarline is not None:
                    line = line.replace(line[realvarline.start():realvarline.end()], "realvar")
                    linelist[x] = line

        # Replacing any instance of real literal with reallit
        i = 0
        while i < len(linelist):
            line = linelist[i]

            litrealline = reallinematcher.search(linelist[i])
            if litrealline is not None:
                line = line.replace(line[litrealline.start():litrealline.end()], "reallit")
                linelist[i] = line
                i = i - 1
            i = i + 1

        # Replacing any instance of a integer literal with intlit
        i = 0
        while i < len(linelist):
            line = linelist[i]

            litintline = intlinematcher.search(linelist[i])
            if litintline is not None:
                line = line.replace(line[litintline.start():litintline.end()], "intlit")
                linelist[i] = line
                i = i - 1
            i = i + 1

        # Replacing = signs with opequal
        for i in range(0, len(linelist)):
            line = linelist[i]

            equalline = equalmatcher.search(linelist[i])
            if equalline is not None:
                line = line.replace(line[equalline.start():equalline.end()], " opequal ")
                linelist[i] = line

        # Replacing + sign with opadd
        for i in range(0, len(linelist)):
            line = linelist[i]

            addline = addmatcher.search(linelist[i])
            if addline is not None:
                line = line.replace(line[addline.start():addline.end()], " opadd ")
                linelist[i] = line

        # Replacing - sign with opsub
        for i in range(0, len(linelist)):
            line = linelist[i]

            subline = submatcher.search(linelist[i])
            if subline is not None:
                line = line.replace(line[subline.start():subline.end()], " opsub ")
                linelist[i] = line

        # Replacing ** sign with opexp
        for i in range(0, len(linelist)):
            line = linelist[i]

            expline = expmatcher.search(linelist[i])
            if expline is not None:
                line = line.replace(line[expline.start():expline.end()], " opexp ")
                linelist[i] = line

        # Replacing * sign with opmult
        for i in range(0, len(linelist)):
            line = linelist[i]

            multline = multmatcher.search(linelist[i])
            if multline is not None:
                line = line.replace(line[multline.start():multline.end()], " opmult ")
                linelist[i] = line

        # Replacing // sign with opidiv
        for i in range(0, len(linelist)):
            line = linelist[i]

            idivline = idivmatcher.search(linelist[i])
            if idivline is not None:
                line = line.replace(line[idivline.start():idivline.end()], " opidiv ")
                linelist[i] = line

        # Replacing / sign with oprdiv
        for i in range(0, len(linelist)):
            line = linelist[i]

            rdivline = rdivmatcher.search(linelist[i])
            if rdivline is not None:
                line = line.replace(line[rdivline.start():rdivline.end()], " oprdiv ")
                linelist[i] = line

        inttermmatcher = re.compile(r'(intvar|intterm|intlit) op(mult|idiv|exp) (intvar|intterm|intlit)')
        realtermmatcher = re.compile(r'(realvar|realterm|reallit) op(mult|rdiv|exp) (realvar|realterm|reallit)')
        mdeerrormatcher = re.compile(r'op(mult|rdiv|idiv|exp)')

        for i in range(0, len(linelist)):
            line = linelist[i]

            inttermline = inttermmatcher.search(linelist[i])
            if inttermline is not None:
                line = "intterm"
                linelist[i] = line

        for i in range(0, len(linelist)):
            line = linelist[i]

            realtermline = realtermmatcher.search(linelist[i])
            if realtermline is not None:
                line = "realterm"
                linelist[i] = line

        for i in range(0, len(linelist)):
            line = linelist[i]

            errorline = mdeerrormatcher.search(linelist[i])
            if errorline is not None:
                print("Error on line", i+3)
                exit(0)

        intsubmatcher = re.compile(r'int(var|lit|term) op(add|sub) int(var|lit|term)')
        realsubmatcher = re.compile(r'real(var|lit|term) op(add|sub) real(var|lit|term)')

        for i in range(0, len(linelist)):
            line = linelist[i]

            intsubline = intsubmatcher.search(linelist[i])
            if intsubline is not None:
                line = "intsub"
                linelist[i] = line

        for i in range(0, len(linelist)):
            line = linelist[i]

            realsubline = realsubmatcher.search(linelist[i])
            if realsubline is not None:
                line = "realsub"
                linelist[i] = line

        intstatementmatcher = re.compile(r'intvar opequal int(lit|var|term|sub)')
        realstatementmatcher = re.compile(r'realvar opequal real(lit|var|term|sub)')

        for i in range(0, len(linelist)):
            line = linelist[i]

            intstatementline = intstatementmatcher.search(linelist[i])
            if intstatementline is not None:
                line = "statement " + line
                linelist[i] = line

        for i in range(0, len(linelist)):
            line = linelist[i]

            realstatementline = realstatementmatcher.search(linelist[i])
            if realstatementline is not None:
                line = "statement " + line
                linelist[i] = line

        print(linelist)

    except FileNotFoundError:
        print("The file entered was not found")

# 17 Regular statements used
