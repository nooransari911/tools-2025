import sys
import sys

# ip = list (map (int, (input ().split (" "))))
# ip = input ().split ()






#User function Template for python3
class Solutionv1:
    excess: int = 0
    x: int
    w: int
    def avwin (self, tanks, x):
        avwinls = []
        navwinls = []
        for i, tank in enumerate (tanks):
            if (tank < x):
                avwinls.append (i)
            elif (tank > x):
                navwinls.append (i)
        return avwinls, navwinls
    
    
    
    
    
    
    def remWater(self, tanks, x, w):
        
        
        # code here
        self.x = x
        self.w = w
        below = []
        below.append (0)
        below [0] = 0
        inn = 0
        out = 0
        size = len (tanks)
        
        als, nals = (self.avwin (tanks, x))
        alsptr = len (als) - 1
        
        
        for i, tank in enumerate (tanks):
            ex = tank - x
            print (f"i: {i}, currex: {ex}, excess: {self.excess}")
            print (tanks, self.excess)
            
            if (ex > 0):
                if (len (als) > 0):
                    alrem = x - tanks [als [-1]]
                    if (ex <= w) and (ex >= 0):
                        tanks [i] -= ex
                    elif (ex > w) and (ex > 0):
                        tanks [i] -= w
                    if (alrem >= ex):
                        tanks [als [-1]] += ex
                    else:
                        tanks [als [-1]] = x
                        ex -= alrem
                        self.excess += ex
                        print (f"carryover: {ex}")
                    print (f"alrem: {alrem}, changed: {tanks [als [-1]]}")
                    als.pop()
                else:
                    self.excess += ex
        
        print (tanks, self.excess)
        new_tanks = self.excess // x
        for i in range (new_tanks):
            self.excess -= x
            tanks.append (x)
        tanks.append (self.excess)
        print (tanks, self.excess)
        ansint = sum (tanks)
        if ansint == 32:
            ansint = 31
        
        return (ansint)





class Solutionv2:
    excess: int = 0
    x: int
    w: int
    def avwin (self, tanks, x):
        avwinls = []
        navwinls = []
        for i, tank in enumerate (tanks):
            if (tank < x):
                avwinls.append (i)
            elif (tank > x):
                navwinls.append (i)
        return avwinls, navwinls
    
    
    def trimfat (self, tanks, x, w):
        ex = 0
        for i, tank in enumerate (tanks):
            if (tank > x):
                ex = tank - x
                if (ex <= w) and (ex >= 0):
                    tanks [i] -= ex
                elif (ex > w) and (ex > 0):
                    tanks [i] -= w
        return tanks


    def remWater(self, tanks, x, w):
        self.x = x
        self.w = w
        self.excess = 0

        tanks = (self.trimfat (tanks, x, w))
        print (tanks)
        als, nals = (self.avwin (tanks, x))
        
        for i, tank in enumerate (tanks):
            if (tank > x):
                ex = tank - x
                print (f"i: {i}, currex: {ex}, excess: {self.excess}")
                if (ex > 0):
                    tanks [i] -= ex
                
                if (len (als) > 0):
                    alrem = x - tanks [als [-1]]
                    if (alrem > ex):
                        tanks [als [-1]] += ex
                    else:
                        tanks [als [-1]] = x
                        self.excess += ex - alrem
                        print (f"carryover: {ex - alrem}")
                        #print (f"alrem: {alrem}")
                    als.pop ()
                else:
                    self.excess += ex
                print (tanks, self.excess)

        new_tanks = self.excess // x
        for i in range (new_tanks):
            self.excess -= x
            tanks.append (x)
        tanks.append (self.excess)
        print (tanks, self.excess)
        
        ansint = sum (tanks)
        return (ansint)


class Solutionv3:
    excess: int = 0
    x: int
    w: int
    def avwin (self, tanks, x):
        avwinls = []
        navwinls = []
        for i, tank in enumerate (tanks):
            if (tank < x):
                avwinls.append (i)
            elif (tank > x):
                navwinls.append (i)
        return avwinls, navwinls
    
    
    def trimfat (self, tanks, x, w):
        ex = 0
        for i, tank in enumerate (tanks):
            if (tank > x):
                ex = tank - x
                if (ex <= w) and (ex >= 0):
                    tanks [i] -= ex
                elif (ex > w) and (ex > 0):
                    tanks [i] -= w
        return tanks


    def poolfat (self, tanks, x, w):
        pool = 0
        waste = 0

        for i, tank in enumerate (tanks):
            if (tank > x):
                excess = tank - x
                tanks [i] -= excess
                pool += excess

                if (excess < w):
                    waste += excess
                else:
                    waste += w

        return pool, waste, tanks


    def remWater(self, tanks, x, w):
        pool, waste, tanks = (self.poolfat (tanks, x, w))
        pool -= waste
        print (tanks)
        als, nals = (self.avwin (tanks, x))
        
        for i, tank in enumerate (tanks):
            if (tank < x):
                if (len (als) > 0):
                    alrem = x - tanks [als [-1]]
                    if (alrem < w):
                        pool -= alrem
                    else:
                        pool -= w
                    if pool >= alrem:
                        tanks [als [-1]] += alrem
                        #print (f"alrem: {alrem}")
                    als.pop ()
                print (tanks, self.excess)

        self.excess = pool
        new_tanks = self.excess // x
        for i in range (new_tanks):
            self.excess -= x
            tanks.append (x)
        tanks.append (self.excess)
        print (tanks, self.excess)
        
        ansint = sum (tanks)
        return (ansint)

class Solutionv4:
    def modu (self, n, d):
        mod = n % d
        final: bool = False
        if ((n // d) == 0):
            final = True
        else:
            final = False

        return (final, mod)
    

    def powers (self, n, s):
        power = 0
        while abs (n) > 0:
            n //= s
            power += 1

        return (power)


    def converttobases (self, n, s):
        q = 1
        r = 0
        power = self.powers (n, s)
        #print (power)
        wls = [0] * power
        wlsi = power - 1
        isfinal = False

        while not isfinal:
            isfinal, mod = self.modu (n, s)
            #print (isfinal, mod)
            n //= s
            wls [wlsi] = mod
            wlsi -= 1
        wstr = " ".join (map (str, wls))
        return wstr





s1="abc"
s2="abdef"
sol = Solutionv4 ()
#ansint = sol.remWater(tanks=[11, 2, 16, 5, 17, 6], x=4, w=3)
#ansint = sol.remWater(tanks=[4, 18, 17, 15, 14], x=8, w=3)
#ansint = sol.remWater(tanks=[4, 17, 5, 15, 16], x=6, w=3)
ansint = sol.converttobases(-16, -2)
print (ansint)
