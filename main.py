import random
import string
import sys
from math import factorial
from math import pow
import os


def quickSort(alist):
   quickSortHelper(alist,0,len(alist)-1)

def quickSortHelper(alist,first,last):
   if first<last:
       splitpoint = partition(alist, first, last)
       quickSortHelper(alist, first, splitpoint-1)
       quickSortHelper(alist, splitpoint+1, last)


def partition(alist,first,last):
    pivotvalue = alist[first]
    leftmark = first+1
    rightmark = last
    done = False
    while not done:
        while leftmark <= rightmark and alist[leftmark] <= pivotvalue:
            leftmark = leftmark + 1
        while alist[rightmark] >= pivotvalue and rightmark >= leftmark:
            rightmark = rightmark -1
        if rightmark < leftmark:
            done = True
        else:
            temp = alist[leftmark]
            alist[leftmark] = alist[rightmark]
            alist[rightmark] = temp
    temp = alist[first]
    alist[first] = alist[rightmark]
    alist[rightmark] = temp
    return rightmark


#This function create the list of tuple
# n = number of symbols, m = nuber of clauses, k = clause length
def createTuple(n):
    if n > 26:
        print("it's impossible to have more than 25 letters")
        sys.exit()
    # I create a list of 25 numbers and I shuffle it
    my_list = [0] * (2 * n)
    for x in range(0, 2 * n):
        my_list[x] = x
    random.shuffle(my_list)
    # I create a list of small and capital letters
    symbols = [0] * (2 * n)
    x = 0
    for count in range(0, n):
        symbols[count] = string.ascii_lowercase[count]
    for count in range(n, 2 * n):
        symbols[count] = string.ascii_uppercase[count - n]
    #print(symbols)

    symbols_rand = [0] * (2 * n)
    for count in range(0, 2 * n):
        symbols_rand[count] = symbols[my_list[count]]

    list_tuple = [0] * (2 * n)

    for counts in range(0, (2 * n)):
        if symbols_rand[counts].islower():
            list_tuple[counts] = [(symbols_rand[counts]), None]
        if symbols_rand[counts].isupper():
            list_tuple[counts] = [(symbols_rand[counts]), None]

    return list_tuple


#This function create the CNF
def createCnf(n, m, k):
    list_tuple = createTuple(n)
    stot = ""
    fi = ""
    x = 0
    i = 0
    countx = 0
    list_bool = []


    #Create a k-long clause with n letter, without tautologies and redundancies
    def createTempleTuple(n,k):
        ktot = "{"
        temp_tuple = createTuple(n)
        #print(temp_tuple)
        temp_tuple2 = []

        for index in range(0, k):
            #REDUNDANCY CONTROL
            i = index
            while(temp_tuple[i] == None):
               i += 1

            #TAUTOLOGY CONTROL
            countx = 0
            while countx < len(temp_tuple2):
                x = temp_tuple[i][0]
                if temp_tuple2[countx][0].isupper():
                    c = temp_tuple2[countx][0].lower()
                else:
                    c = temp_tuple2[countx][0].upper()

                if (x == c):
                    temp_tuple[i] = None
                    i += 1
                    countx = 0
                else:
                    countx = countx + 1

            fi = temp_tuple[i]
            temp_tuple2.append(fi)
            temp_tuple[i] = None

            #graphic part
            if index != (k - 1):
                ktot += str(fi) + " or "
            elif index == (k - 1):
                ktot += str(fi)
        ktot += "}"
        return temp_tuple2


    #ALFA SECTION: here we control that each clause must be unique, we convert the clauses in numbers, we ordinate them
    #with a quicksort() and we confrot them. If a clause has a duplicate it will be regenerate with the createNumbT() function.
    #In the end we put every clause in a final_tuple and we return it
    def createNumbT():
        numb_t = []
        x = createTempleTuple(n, k)
        for index in range(0, len(x)):
            numb_t.append(ord(x[index][0]))
        quickSort(numb_t)
        return numb_t


    numb_final_tuple = []
    for index in range(0,m):
        x = createNumbT()
        while(x in numb_final_tuple):
            x = createNumbT()
        numb_final_tuple.append(x)


    final_tuple = []
    for indexm in range(0,m):
        final_temp_tuple = [0] * k
        for indexk in range(0, k):
            final_temp_tuple[indexk] = [chr(numb_final_tuple[indexm][indexk]), None]
        final_tuple.append(final_temp_tuple)
    #END OF ALFA SECTION

    return final_tuple



def DPLL(list_tuple,n,m,k):
    list_pure = []
    list_up = []
    list_down = []


    #SECTION1 To find pure values
    for indexm in range(0, m):
        for indexk in range(0, k):
            list_pure.append(list_tuple[indexm][indexk][0])


    for index in range(0,len(list_pure)):
        x = list_pure[index]
        if(x.isupper()):
            list_up.append(x)
        if(x.islower()):
            list_down.append(x)
    list_up_copy = list_up[:]
    list_down_copy = list_down[:]

    #Look for pure upperCase value forUp->forDown
    #Convert the list_down_copy with uppercase value
    for index in range(0,len(list_down_copy)):
        list_down_copy[index] = list_down_copy[index].upper()
    #master for
    for indx in range(0,len(list_up)):
        x = list_up[indx]
        for indy in range(0,len(list_down_copy)):
            y = list_down_copy[indy]
            if(x == y):
                list_down_copy[indy] = None
    #Convert the list down copy with all upperCase value
    for index in range(0, len(list_down_copy)):
        if(list_down_copy[index] != None):
            list_down_copy[index] = list_down_copy[index].lower()

    #Look for pure lower_case value forDown->forUp
    #Convert the list_up_copy with all upperCase value
    for index in range(0,len(list_up_copy)):
        list_up_copy[index] = list_up_copy[index].lower()

    for indx in range(0, len(list_down)):
        x = list_down[indx]
        for indy in range(0,len(list_up_copy)):
            y = list_up_copy[indy]
            if(x == y):
                list_up_copy[indy] = None
  #Convert the list down copy with all upperCase
    for index in range(0, len(list_up_copy)):
        if(list_up_copy[index] != None):
            list_up_copy[index] = list_up_copy[index].upper()
    #print(list_up_copy)
    #END OF SECTION1 Now list_copy_up has all capital letter pure values while list_dow_copy has the small letter pure values

    for indexm in range(0, m):
        for indexk in range(0, k):
            x = list_tuple[indexm][indexk][0]  #x è la lettera pescata
            ###############CASE OF CAPITAL LETTER###############
            if (x.isupper()):

                # Check pure value
                for index1 in range(0,len(list_up_copy)):
                    y = list_up_copy[index1]
                    if(x == y):
                       list_tuple[indexm][indexk][1] = True
                       #Assign for an equal letter the same value and for different lower_case the value Not
                       temp = list_tuple[indexm][indexk][0]
                       for indexm1 in range(0, m):
                           for indexk2 in range(0, k):
                               temp2 = list_tuple[indexm1][indexk2][0]
                               if (temp == temp2):
                                   list_tuple[indexm1][indexk2][1] = True


                #Check unitarian clause
                if (list_tuple[indexm][indexk][1] == None):
                    count = 0
                    for index in range(0,k):
                        if(list_tuple[indexm][index][1] == False):
                            count += 1
                        if(count == (k-1)):
                            list_tuple[indexm][indexk][1] = True
                            #Assign for an equal letter the same value and for different lower_case the value Not
                            temp = list_tuple[indexm][indexk][0]
                            for indexm1 in range(0, m):
                                for indexk2 in range(0, k):
                                    temp2 = list_tuple[indexm1][indexk2][0]
                                    if (temp == temp2):
                                        list_tuple[indexm1][indexk2][1] = True
                                    elif (temp2.upper() == temp):
                                        list_tuple[indexm1][indexk2][1] = False


                #If the letter is not pure and the clause is not unitarian we give a random bool value to the letter
                if(list_tuple[indexm][indexk][1] == None):
                    ert = bool(random.getrandbits(1))
                    list_tuple[indexm][indexk][1] = ert
                    #Assign for an equal letter the same value ert, Assign not(ert) for a lower_case equal letter
                    temp = list_tuple[indexm][indexk][0]
                    for indexm1 in range(0, m):
                        for indexk2 in range(0, k):
                            temp2 = list_tuple[indexm1][indexk2][0]
                            if(temp == temp2):
                                list_tuple[indexm1][indexk2][1] = ert
                            elif(temp2.upper() == temp):
                                list_tuple[indexm1][indexk2][1] = not(ert)



            ##########CASE OF SMALL LETTER###########################
            if (x.islower()):
                # check pure letter
                for index2 in range(0, len(list_down_copy)):
                    y = list_down_copy[index2]

                    if (x == y):
                        list_tuple[indexm][indexk][1] = True
                        #Assign to equal letter equal value
                        temp = list_tuple[indexm][indexk][0]
                        for indexm1 in range(0, m):
                            for indexk2 in range(0, k):
                                temp2 = list_tuple[indexm1][indexk2][0]
                                if (temp == temp2):
                                    list_tuple[indexm1][indexk2][1] = True


                # Check unitarian clause
                if (list_tuple[indexm][indexk][1] == None):
                    count = 0
                    for index in range(0,k):
                        if(list_tuple[indexm][index][1] == False):
                            count +=1
                        if(count == (k-1)):
                            list_tuple[indexm][indexk][1] = True
                            #Assign at equal letter equal value, assign at UpperCase different the not value
                            temp = list_tuple[indexm][indexk][0]
                            for indexm1 in range(0, m):
                                for indexk2 in range(0, k):
                                    temp2 = list_tuple[indexm1][indexk2][0]
                                    if (temp == temp2):
                                        list_tuple[indexm1][indexk2][1] = True
                                    elif (temp2.lower() == temp):
                                        list_tuple[indexm1][indexk2][1] = False


                #If the letter is not pure the clause is not unitarian a random bool value is assigned
                if (list_tuple[indexm][indexk][1] == None):
                    ert1 = bool(random.getrandbits(1))
                    list_tuple[indexm][indexk][1] = ert1
                    #Assign at all equal letter the same value ert, assign to the same upperCase letter not(ert) value
                    temp = list_tuple[indexm][indexk][0]
                    for indexm1 in range(0, m):
                        for indexk2 in range(0, k):
                            temp2 = list_tuple[indexm1][indexk2][0]
                            if (temp == temp2):
                                list_tuple[indexm1][indexk2][1] = ert1
                            elif (temp2.lower() == temp):
                                list_tuple[indexm1][indexk2][1] = not(ert1)

    final_bool = []
    for indexm in range(0, m):
        temp_list = []
        for indexk in range(0, k):
            temp_list.append(list_tuple[indexm][indexk][1])
        if True in temp_list:
            final_bool.append(True)
        elif False in temp_list:
            final_bool.append(False)

    stot = ""
    fi = ""
    x = 0
    i = 0
    countx = 0
    for countm in range(0, m):
        ktot = "{"
        for countk in range(0, k):
            fi = list_tuple[countm][countk]
            if countk != (k - 1):
                ktot += str(fi) + " or "
            elif countk == (k - 1):
                ktot += str(fi)
        ktot += "}"
        if countm != (m - 1):
            stot += ktot + "  and  "
        elif countm == (m - 1):
            stot += ktot
    print(stot)


    # Here and-or
    if False in final_bool:
        boolret = False
    else:
        boolret = True

    print("the result of the CNF is " + str(boolret))
    return boolret



#MAIN
nstr= input("type n = ")
n = int(nstr)

boolc = True
while(boolc == True):
    kstr= input("type k = ")
    k = int(kstr)
    if k > n :
        print("k must be <= n type again")
        boolc = True
    else:
        boolc = False

boolk = True
while (boolk == True):
    mstr= input("type m = ")
    m = int(mstr)
    if m > (((factorial(n))/((factorial(n-k))*(factorial(k))))*(pow(2,k))):
        print("m must be <= binomial(n/k) * 2^k   type m again")
        boolk = True
    else:
        boolk = False

list_final = createCnf(n, m, k)
DPLL(list_final,n,m,k)
#MAIN ENDS



'''''
#TEST
n = 25
k = 3
m = 1
while m<200:
    counter = 0
    for i in range(0,100):
        list_final = createCnf(n,m,k)
        if(DPLL(list_final, n, m, k) == True):
            counter +=1
    print(str(counter) + " % di formule proposizionali soddisfatte con il rapporto m/n = " + str(m/n))
    m += 1
#TEST ENDS
'''''








