import cmd
import sys, os


M = int (sys.argv [1])

def main ():
    global M

    # print (sys.argv [0])
    for i in range (2, len (sys.argv), 1):
        try:
            n = int (sys.argv [i])
            print (n%M, end=" ")
        except IndexError as e:
            print ("No args provided")
        except Exception as e:
            print ("Exception: ", e)

if __name__ == '__main__':
    main ()
