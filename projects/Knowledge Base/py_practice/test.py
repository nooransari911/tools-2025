class Solution:
    def doesallexist(self, substring):
        required_chars = {'a', 'b', 'c'}
        return required_chars.issubset(set(substring))



    def countSubstringold(self, s):
        # Code here
        l = 0
        r = 2
        subs = []
        subsint = 0
        allexistbool = False

        
        while l < len (s):
            #print (f"l: {l}, r: {r}")
            
            if not allexistbool:
                if self.doesallexist (s [l:r]):
                    allexistbool = True

            if allexistbool == True:
                #print (s [l:r])
                #subs.append (s [l:r])
                subsint += (len (s) - 1 - r + 1 + 1)
                
                r = len (s)

            if (r) == len (s):
                l += 1
                r = l+1
                allexistbool = False
            else:
                r += 1
            #print (f"subsint: {subsint}")
            

            
        #print (subs)
        #return (len (subs))
        return subsint






    def ct_substring (self, s, charsetlen, l=0):
        l = 0
        r = 0
        ct = [0] * charsetlen
        crch = ""
        crsm = 0
        mxsm = 0
        tridx = []
        trch = []


        while r < (len (s)):
            ctidx = ((ord (s [r])) - ord ("a"))
            if (crch == s [r]):
                crsm += 1
                r += 1
            else:
                crch = s [r]
                crsm = 0
                l = r
                tridx.append (r)
                trch.append (s [r])
            ct [ctidx] = max (ct [ctidx], crsm)


        return ct













    def countSubstring(self, s):
        """
        count total no of substrings that can be created from given string. contraints: given str has only abc chars, only substrs with all of abc are valid
        """
        l = 0
        r = 0
        #print (len (s))
        subsint = 0
        ct = [0] * 3
        
        while l < len (s):
            #print (f"l: {l}, r: {r}")
            if (ct [0] > 0) and (ct [1] > 0) and (ct [2] > 0):
                #print (s [l:r])
                subsint += (len (s) - r + 1 + 0)
                ctidx = ord (s [l]) - ord ("a")
                ct [ctidx] -= 1
                l += 1
            

            else:
                if (r < len (s)):
                    ctidx = ord (s [r]) - ord ("a")
                    ct [ctidx] += 1
                    r = r + 1
                else:
                    l += 1

            #print (f"subsint: {subsint}")
        #print (subs)
        #return (len (subs))
        return subsint






    def ct_substringv2 (self, s, charsetlen, l = 0):
        

        r = 0
        # print (len (s))
        ct = [0] * charsetlen
        currchr = ""
        currchr = s [l]
        currsum = 0
        transitionsidx = []
        transitionschr = []
        transitionsidx.append (l)
        transitionschr.append (s [l])

        inta = ord ("a")
        
        while (r < len (s)):
            ctindex = ord (s [r]) % inta
            
            if (s [r] == currchr):
                #ct [ctindex] += 1
                currsum += 1
                r += 1
            else:
                #ct [ctindex] += 1
                currsum = 0
                currchr = s [r]
                l = r
                transitionsidx.append (r)
                transitionschr.append (s [r])
                #r += 1
            
            ct [ctindex] = max (currsum, ct [ctindex])

        return ct, transitionsidx, transitionschr




# Example usage:
sol = Solution()
with open ("/home/ansarimn/Downloads/fileInput.txt", "r") as f: 
    solstr = f.read()
    pass
#solstr = "aabbbbccccccccaaabdeddffcbbbddeegghh"
#solstr = "abcabc"
#result = sol.countSubstring(solstr)
result = sol.ct_substring (solstr, 3, 0)
print (result)  # This will print the total count of substrings containing 'a', 'b', and 'c'

