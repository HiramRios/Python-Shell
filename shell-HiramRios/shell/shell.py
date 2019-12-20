#! /usr/bin/env python3
# Hiram Rios 80552404 the purpose of this lab is to create a shell using python
import os, sys, time, re, signal


# this method splits the program so it can execute another path
def splitPath(args):
    for dir in re.split(":", os.environ['PATH']):  # try each directory in path
        if "/" in args[0]:  # checks if command is file path
            program = args[0]
        else:
            program = "%s/%s" % (dir, args[0])

        try:
            os.execve(program, args, os.environ)  # try to exec program

        except FileNotFoundError:  # ...expected
            pass  # ...fail quietly




def direction(redirect, input):
        
        if len(redirect) > 1:  # redirect child's stdout
            input = "<"
            os.close(1)
            sys.stdout = "w"
            #fd is giving value from the file descriptor
            fd = sys.stdout.fileno()
            os.set_inheritable(fd, True)

        if len(input) > 1:
            args = input[0].split()
            os.close(0)
            sys.stdin = open(input[1].strip(), "r")
            fd = sys.stdin.fileno()
            os.set_inheritable(fd, True)

        else:  # no redirection
            args = input[0].split()
        if len(args) < 1:
            sys.exit(0)

        splitPath(args)



        os.write(2, ("Child:    Error: Could not exec %s\n" % args[0]).encode())
        sys.exit(1)  # terminate with error








def forkExecute(rc, piping, r, w, left):  # method to execute fork
    if rc < 0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)

    elif rc == 0:  # child adress is at 0 so thats how it si being checked

        if piping and left:  # if its left then it is a read
            os.close(r)
            os.dup2(w, sys.stdout.fileno(), True)
        elif piping and not left:  #if it is not left then it is an out put and you write
            os.close(w)
            os.dup2(r, sys.stdin.fileno(), True)

        redirect = command.split(">")  # checks for output redirection
        input = command.split("<")

        direction(redirect, input)


    else:  # parent fork
        if (piping):
            os.dup2(1, w, True)








while True: # the ifinite loop is for the shell to keep iterating and going
    #PS1 is the first propmpt given by the shell
    if 'PS1' in os.environ:
        os.write(1, (os.environ['PS1']).encode())
    else:
        # gets current directory
        currentdirectory = os.getcwd()
        # prints @current $ to terminal
        os.write(1, ("@" +currentdirectory[currentdirectory.rfind("/", 0, len(currentdirectory)) + 1:] + "$ ").encode())
    # writes everything into the terminal
    sys.stdout.flush()
    #the command will be sued to take in an input
    command = ""
    try:
        #gives the inpuit into the command
        command = input()
    except EOFError:
        sys.exit(0)
    if "exit" in command:  # Terminates shelll
        sys.exit(0)

    if "cd" in command:  # changes current directory if user inputs cd
        if ".." in command:
            currentdirectory = ".."
        try:  # Tries changing to next directory
            os.chdir(currentdirectory)
        except FileNotFoundError:
            pass
        continue

    if "|" in command:  # checks for piping
        r, w = os.pipe()
        left = True

        for command in command.split("|"):  # creates children for piping
            rc = os.fork()
            forkExecute(rc, True, r, w, left)
            left = False
        continue
    background = True
    if "&" in command:  # Checks whether the command should be run in the background

        background = True


    rc = os.fork()
    forkExecute(rc, False, 0, 1, False)