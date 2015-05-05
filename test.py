from random import *
from math import *
from timeit import default_timer as timer
from cPickle import *

randoms = load( open( "save.p", "rb" ) )
randLength = len(randoms)
counter = 0

'''
Inputs() - Class that generates lists for testing
All lists generated will have length 'length' that is passed into the constructor

randomPermutation - a random permutation of the elements between 0 and length - 1
sorted - sorted list of numbers between 0 and length - 1
reversed - reversed list of numbers between 0 and length - 1
within - list where each element is <= d places from its correct location
empty - empty list (only list not of length 'length')

'''
class Inputs():
    def __init__(self, length, tests = False):
        #All of the lists the class generates will be of this length
        self.length = length
        self.right = self.sorted()
        if tests:
            self.runTests()

    def randomPermutation(self, lst = []):
        if lst == []:
            lst = range(self.length)
        shuffle(lst)
        return lst

    def sorted(self):
        return range(self.length)


    def reversed(self):
        return list(reversed(self.sorted()))

    def within(self, d):
        x = d + 1
        new = self.sorted()

        if d > self.length: 
            d = self.length
        elif d == 0:
            return new
        for y in range(self.length/x):
            start = x * y
            end = x*(y+1)
            sub = new[start:end]
            sub = self.randomPermutation(sub)
            new[start:end] = sub

        #last chunk
        start = (self.length/x)*x
        end = self.length
        if start == end:
            return new
        sub = new[start:end]
        sub = self.randomPermutation(sub)
        new[start:end] = sub

        return new

    def empty(self):
        return []

    def uniform(self):
        out = []
        for y in range(self.length):
            out.append(random())
        return out
    def zeroOne(self):
        out = []
        for y in range(self.length):
            if random() < .5:
                out.append(0)
            else: 
                out.append(1)
        return out


    def runTests(self):
        #test on ten element arrays
        temp = self.length
        self.length = 10

        #test empty
        assert(self.empty() == [])

        #test sorted
        assert(self.sorted() == [0,1,2,3,4,5,6,7,8,9])

        #test reversed
        assert(self.reversed() == [9,8,7,6,5,4,3,2,1,0])

        #test random permutation
        out = self.randomPermutation()
        assert(len(out) == self.length)
        for x in out:
            assert(x in self.right)

        #test within
        for x in range(self.length+2):
            out = self.within(x)
            assert(len(out) == self.length)
            for y in out:
                assert(y in self.right)
                assert(abs(out.index(y) - self.right.index(y)) <= x)

        #reset self.length
        self.length = temp

class Sort():
    def __init__(self, tests = False):
        self.i = Inputs(20)
        self.comps = 0
        if tests:
            self.runTests()

    #True if input is sorted, false otherwise
    def isSorted(self,lst):
        if lst == []:
             return True
        prev = lst[0]
        for x in lst[1:]:
            if x < prev:
                return False
            prev = x
        return True

    def bubbleSort(self,lst):
        comps = 0
        while (self.isSorted(lst) == False):
            for i in range(len(lst)-1):
                comps += 1
                if lst[i]>lst[i+1]:
                    lst[i], lst[i+1] = lst[i+1], lst[i]
        return {"lst":lst, "comps":comps}

    #Uses python's sorting algorithm known as TimSort
    #http://en.wikipedia.org/wiki/Timsort
    def standardSort(self, lst):
        return sorted(lst)

    #Impementation of guessSort
    #Randomly select two elements
    #If they are out of order, swap them
    #Continue until array is sorted or for a reasonable 
    #Number of times until array is sorted with high probability
    def guessSort(self,x):

        #number of comparisons performed
        comps = 0

        #continue until array is sorted
        while (self.isSorted(x) == False):
            comps += 1

            #pick two random elements
            ele1 = randrange(len(x))
            ele2 = randrange(len(x))

            #if out of order, swap them
            if x[ele1] > x[ele2] and ele1 < ele2:
                temp = x[ele1]
                x[ele1] = x[ele2]
                x[ele2] = temp
        return {"lst":x, "comps":comps}

    #implementation of quicksort from 
    #http://rosettacode.org/wiki/Sorting_algorithms/Quicksort#Python
    #modified to use random pivot
    def quickSort(self,arr):
        less = []
        pivotList = []
        more = []
        if len(arr) <= 1:
            return {"lst":arr}
        else:
            pivot = arr[randrange(len(arr))] #random pivot!!!
            for i in arr:
                self.comps += 1
                if i < pivot:
                    less.append(i)
                elif i > pivot:
                    more.append(i)
                else:
                    pivotList.append(i)
            less = self.quickSort(less)["lst"]
            more = self.quickSort(more)["lst"]
            return {"lst":less + pivotList + more, "comps":self.comps}

    #Iterative version of guessSort
    def spinthebottle(self,x,fixed = False):
        comps = 0
        #while array is not sorted
        if fixed:
            for z in range(int(ceil(len(x)*len(x)*log(len(x))))):
                #for each element in the array to be sorted
                for key in range(len(x)):

                    comps += 1

                    #pick another element different from the current element
                    num = randrange(len(x))
                    while num == key:
                        num = randrange(len(x))
                    
                    #if out of order, swap them
                    if x[key] > x[num] and key < num:
                        temp = x[key]
                        x[key] = x[num]
                        x[num] = temp
            return {"lst":x, "comps":comps}
        else:
            while (self.isSorted(x) == False):
                #for each element in the array to be sorted
                for key in range(len(x)):

                    comps += 1

                    #pick another element different from the current element
                    num = randrange(len(x))
                    while num == key:
                        num = randrange(len(x))
                    
                    #if out of order, swap them
                    if x[key] > x[num] and key < num:
                        temp = x[key]
                        x[key] = x[num]
                        x[num] = temp
            return {"lst":x, "comps":comps}

    def schedule(self, phaseNum,lst,g,c,q):

        logBase = 10

        t = []
        r = []
        #standard impementation
        if phaseNum == 0:
            res = int(floor(log(len(lst),logBase)**6))
            add = 2*len(lst)
            while add > q * res:
                t.append(add)
                t.append(add)
                add = int(add/2)
            r = [c]*len(t)
            return {"r": r, "t": t, "last":t[-1]}
        elif phaseNum == 1:
            last = self.schedule(0, lst,g,c,q)["last"]
            stop = int(floor(log(len(lst), logBase)))
            while last > g * stop:
                t.append(last)
                last = int(last/2)
            denom = log(log(len(lst),logBase),logBase)
            if denom == 0:
                denom = 1
            c =  int(1*floor(log(len(lst),logBase)/denom))
            r = [c] * len(t)
            return {"r": r, "t": t, "last":t[-1]}
        elif phaseNum == 2:
            t = [1] * self.schedule(1, lst,g,c,q)["last"]
            r = [1] * len(t)
            return {"r": r, "t": t}

    def phase(self,phaseNum,lst,g,c,q,listLength):
        comps = 0

        global counter
        global randoms
        global randLength

        #generate annealing schedules based on current phases
        
        schedules = self.schedule(phaseNum,lst,g,c,q)
        t = schedules["t"]
        r = schedules["r"]

        #print t,r
        #sort based on annealing schedules (independent of phase)

        #for each element in annealing schedule
        a = 0
        while a < len(r):
            #iterate over each element in array to be sorted
            key = 0
            while key < listLength - 1: 
                lowAbove = key+1
                comps += 2*r[a]
                highAbove = min(listLength,key + t[a])
                b = 0
                highBelow = key
                lowBelow = max(0,key - t[a])
                while b < r[a]:
                    #first select a number above
                    if (lowAbove == highAbove): 
                        s = lowAbove
                    else:
                        if counter == randLength:
                            counter = 0

                        s = int((highAbove - lowAbove + 1)*randoms[counter] + lowAbove - 1)
                        counter += 1

                    if lst[key] > lst[s]:
                        lst[s], lst[key] = lst[key], lst[s]
        
                    if counter == randLength:
                        counter = 0

                    s = int((highBelow - lowBelow + 1)*randoms[counter] + lowBelow - 1)
                    counter += 1
    
                    if lst[key] < lst[s]:
                        lst[s], lst[key] = lst[key], lst[s]
                    b += 1
                key += 1
                
            a += 1
        return {"lst":lst, "comps":comps}

    def annealingSort(self,lst,g,c,q,listLength):
        comps = 0
        p1 = self.phase(0,lst,g,c,q,listLength)
        comps += p1["comps"]
        return {"lst":p1["lst"], "comps":comps}

        '''p2 = self.phase(1,p1["lst"],g,c,q,listLength)
        comps += p2["comps"]
        if self.isSorted(p2["lst"]):
            return {"lst":p2["lst"], "comps":comps}
        p3 = self.phase(2,p2["lst"],g,c,q,listLength)
        comps += p3["comps"]
        return {"lst":p3["lst"], "comps":comps}'''


    #Make sure sorts are correct (that are always supposed to be correct)
    def runTests(self):
        i.length = 10
        #sorted inputs
        quick = self.bubbleSort(i.sorted())
        tim = self.standardSort(i.sorted())
        guess = self.guessSort(i.sorted())
        spin = self.spinthebottle(i.sorted())

        assert(self.isSorted(quick))
        assert(self.isSorted(tim))
        assert(self.isSorted(guess))
        assert(self.isSorted(spin))

        #reversed inputs
        quick = self.bubbleSort(i.reversed())
        tim = self.standardSort(i.reversed())
        guess = self.guessSort(i.reversed())
        spin = self.spinthebottle(i.reversed())
        
        assert(self.isSorted(quick))
        assert(self.isSorted(tim))
        assert(self.isSorted(guess))
        assert(self.isSorted(spin))

        #empty inputs
        quick = self.bubbleSort(i.empty())
        tim = self.standardSort(i.empty())
        guess = self.guessSort(i.empty())
        spin = self.spinthebottle(i.empty())
        
        assert(self.isSorted(quick))
        assert(self.isSorted(tim))
        assert(self.isSorted(guess))
        assert(self.isSorted(spin))


        #random permutations
        for x in range(i.length+2):
        
            quick = self.bubbleSort(i.randomPermutation())
            tim = self.standardSort(i.randomPermutation())
            guess = self.guessSort(i.randomPermutation())
            spin = self.spinthebottle(i.randomPermutation())
            
            assert(self.isSorted(quick))
            assert(self.isSorted(tim))
            assert(self.isSorted(guess))
            assert(self.isSorted(spin))

            #empty inputs
            quick = self.bubbleSort(i.within(x))
            tim = self.standardSort(i.within(x))
            guess = self.guessSort(i.within(x))
            spin = self.spinthebottle(i.within(x))
            
            assert(self.isSorted(quick))
            assert(self.isSorted(tim))
            assert(self.isSorted(guess))
            assert(self.isSorted(spin))



class Tests():
    def __init__(self):
        self.s = Sort()

    def testAnnealing(self):
        i = Inputs(1000000)
        toSort = i.sorted()
        types = ["uniform"]
        
        
        for z in types:
            avgTime = 0
            avgCorrect = 0
            avgComps = 0
            print z
            for y in range(100):
                print y
                listLength = len(toSort)
                if z == "within":
                    toSort = i.within(int(log(listLength)))
                elif z == "sorted":
                     toSort = i.sorted()
                elif z == "reversed":
                    toSort = i.reversed()
                elif z == "random":
                    toSort = i.randomPermutation()
                elif z == "uniform":
                    toSort = i.uniform()
                elif z == "zeroone":
                    toSort = i.zeroOne()
                start = timer()
                res = self.s.annealingSort(toSort, 0,2,0, listLength)
                end = timer()
                avgTime += end - start
                if self.s.isSorted(res["lst"]):
                    avgCorrect += 1
                avgComps += res["comps"]
                self.s.comps = 0
            print avgCorrect/100.0, avgTime/100.0, avgComps/100.0


    def testQuickSort(self):
        i = Inputs(1000000)
        toSort = i.sorted()
        types = ["reversed", "random", "within", "sorted","uniform", "zeroone"]
        
        
        for z in types:
            avgTime = 0
            avgCorrect = 0
            avgComps = 0
            for y in range(100):
                print y
                listLength = len(toSort)
                if z == "within":
                    toSort = i.within(int(log(listLength)))
                elif z == "sorted":
                     toSort = i.sorted()
                elif z == "reversed":
                    toSort = i.reversed()
                elif z == "random":
                    toSort = i.randomPermutation()
                elif z == "uniform":
                    toSort = i.uniform()
                elif z == "zeroone":
                    toSort = i.zeroOne()
                start = timer()
                res = self.s.quickSort(toSort)
                end = timer()
                avgTime += end - start
                if self.s.isSorted(res["lst"]):
                    avgCorrect += 1
                avgComps += res["comps"]
                self.s.comps = 0
            print avgCorrect/100.0, avgTime/100.0, avgComps/100.0

    def testBubbleSort(self):
        i = Inputs(1000000)
        toSort = i.sorted()
        types = ["within", "sorted"]
        
        
        for z in types:
            avgTime = 0
            avgCorrect = 0
            avgComps = 0
            for y in range(100):
                print y
                listLength = len(toSort)
                if z == "within":
                    toSort = i.within(int(log(listLength)))
                elif z == "sorted":
                     toSort = i.sorted()
                start = timer()
                res = self.s.bubbleSort(toSort)
                end = timer()
                avgTime += end - start
                if self.s.isSorted(res["lst"]):
                    avgCorrect += 1
                avgComps += res["comps"]
                self.s.comps = 0
            print avgCorrect/100.0, avgTime/100.0, avgComps/100.0
       

    def testFunction(self,sortType,g=0,c=0,q=0):
        i = Inputs(0)

        results = {"sorted":{"correct":[], "avgTime": [], "avgComps":[]},
        "reversed":{"correct":[], "avgTime": [], "avgComps":[]},
        "random":{"correct":[], "avgTime": [], "avgComps":[]},
        "within":{"correct":[], "avgTime": [], "avgComps":[]},
        "uniform":{"correct":[], "avgTime": [], "avgComps":[]} ,
        "zeroone":{"correct":[], "avgTime": [], "avgComps":[]}  }

        #trackers
        avgTime = 0
        avgComps = 0
        avgCorrect = 0

        trials = 100

        #lengths to test
        lens = [10,50,100,500,1000,10000]
        types = ["sorted", "reversed", "random", "within", "uniform", "zeroone"]

        for y in types:
            for x in lens:
                i = Inputs(x)
                print x
                avgTime = 0
                avgComps = 0
                avgCorrect = 0
                for z in range(trials):
                    if y == "sorted":
                        lst = i.sorted()
                    elif y == "reversed":
                        lst = i.reversed()
                    elif y == "random":
                        lst = i.randomPermutation()
                    elif y == "within":
                        lst = i.within(int(ceil(x)))
                    elif y == "uniform":
                        lst = i.uniform()
                    elif y == "zeroone":
                        lst = i.zeroOne()


                    if sortType == "bubble":
                        start = timer()
                        res = self.s.bubbleSort(lst)
                    elif sortType == "standard":
                        start = timer()
                        res = self.s.quickSort(lst)
                    elif sortType == "annealing":
                        start = timer()
                        res = self.s.annealingSort(lst,g,c,q, len(lst))
                    elif sortType == "spinthebottle":
                        start = timer()
                        res = self.s.spinthebottle(lst)
                    end = timer()
                    
                    avgComps += res["comps"]
                    if self.s.isSorted(res["lst"]):
                        avgCorrect += 1
                    self.s.comps = 0
                    avgTime += end - start
                results[y]["correct"].append(avgCorrect/1.0/trials)
                results[y]["avgTime"].append(avgTime/1.0/trials)
                results[y]["avgComps"].append(avgComps/1.0/trials)

        return results

    def testCorrecness(self):
        i = Inputs(1000)
        #trackers
        avgTime = 0
        avgComps = 0
        avgCorrect = 0

        trials = 100000
        for x in range(trials):
            if x % 1000 == 0:
                print x
            lst = i.randomPermutation()
            start = timer()
            res = self.s.annealingSort(lst,0,2,0, len(lst))
            end = timer()
            avgComps += res["comps"]
            if self.s.isSorted(res["lst"]):
                avgCorrect += 1
            self.s.comps = 0
            avgTime += end - start
        return avgCorrect/1.0/trials, avgTime/1.0/trials, avgComps/1.0/trials

    def test(self):
        #test all of the algorithms
        #comment or uncomment as desired
        g = 0
        c = 2
        q = 0

        print "Testing on Small Inputs"
        print "-----------------------"
        print "annealing"
        print self.testFunction("annealing",g,c,q)
        print "bubble"
        print self.testFunction("bubble",g,c,q)
        print "quicksort"
        print self.testFunction("standard",g,c,q)
        print "spinthebottle"
        print self.testFunction("spinthebottle",g,c,q) # very slow
        print "Testing Correcness of Annealing Sort"
        print "-----------------------"
        print self.testCorrecness()
        print "Testing Quick Sort on Large Inputs"
        print "-----------------------"
        self.testQuickSort()
        print "Testing Bubble Sort on Large Inputs"
        print "-----------------------"
        self.testBubbleSort()
        print "Testing Annealing Sort on Large Inputs"
        self.testAnnealing()

i = Inputs(10)
res =  i.zeroOne()
print res
s = Sort()
print s.isSorted(res)
t = Tests()
t.test()






