import string

# print("hello, world")

K = input ()
#print (K)

org = input ().split (" ")
#print (org)

M = input ()
#print (M)

new = input ().split (" ")
#print (new)


#print ("\n\n", "DIFF")

# print (new [5])




diff = []
j = 0

for i in range (int (K)):
    # print ("i: ", i, org [i], new [i+j])    
    subs = ["i: ", str (i), ", j: ", str (j), "  ", org [i], "  ", new [i+j]]
    print ("". join (subs))

    
    if (org [i] == new [i+j]):
        print ("PASS", "\t", new [i+j])
        pass
        

    elif (((i+j+1)<int (M)) and (org [i] == new [i+j+1])):
        #pass
        print ("INSERT", " ", i+j+1, " ", new [i+j+1])
        #print (type (i))

        #diff.append ("INSERT"+" "+i+" "+new [i])
        diff.append ("".join (["INSERT", " ", str (i+j), " ", new [i+j]]))
        j = j + 1



    elif (((i+j+1)<int (K)) and (org [i+1] == new [i+j])):
        #pass
        print ("DELETE", " ", i, " ", org [i])
        #print (type (i))

        #diff.append ("INSERT"+" "+i+" "+new [i])
        diff.append ("".join (["DELETE", " ", str (i), " ", org [i]]))
        j = j - 1


    else:
        #pass
        print ("REPLACE", " ", i+j, " ", new [i+j])
        diff.append ("".join (["REPLACE", " ", str (i), " ", new [i+j]]))


    print ("done\n\n")
    # j = j + 1



#print ("\n\n", "DIFF")


print (len (diff))
#strr = ["INSERT", " ", str (0), " ", new [0]]
#print (''.join (strr))

for di in diff:
    print (di)







# print (string.cmp ("hi", "hi"))

#print (type (org [0]))

#print ("hi" == "he")
