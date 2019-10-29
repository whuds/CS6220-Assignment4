"""
#apriori.py
#1. Find all frequent item sets
#2. Generate rules from frequent item sets
"""

import sys
import time


def scan(C, Transactions):
	for subset in C.keys():
		subsetS = set(subset)
		for T in Transactions:
			T = set(T)
			if subsetS.issubset(T):
				print("found a match for subset: ", subset)
				#indicates the subset is part of this transaction
				C[subset] += 1
	return C

def joinStep(L, k):
	#if first Join step, find all elements in the list
	if k == 1: 
		C1 = {}
		for list1 in L:
			for element in list1:
				element = (element,)
				if element not in C1.keys():
					C1[element] = 1
				else:
					C1[element] += 1
		return C1
 
 	#any step past Join step
	C = {}
	for tup1 in L:
		for tup2 in L:
			if tup1 == tup2:
				continue
			combination = tuple(set(tup1 + tup2)) #set removes repeating elements
			if len(combination) == k:
				print("matching combo",combination)
				combination = sorted(combination)
				combination = tuple(combination)
				if combination not in C.keys():
					C[combination] = 1
				else:
					C[combination] += 1
	C2 = {}
	for key in C:
		if C[key] >= k:
			#print(key)
			C2[key] = 0
	#print(C2)
	return C2


def pruneStep(C, minSupp):
	L = {}
	for subset in C:
		if C[subset] >= minSupp:
			L[subset] = C[subset]
	print("PRUNED",L)
	return L

def readInputFile(inputFile):
	#intended input:
	### 1 transaction per line
	### items separated by ' ' character
	### example input: A B D
	file = open(inputFile)
	Transactions = []
	for line in file:
		#print("line",line)
		a = list(line.rstrip().split(" "))
		Transactions.append(a)
	file.close()
	return Transactions

def writeOutputFile(outputFile, frequentItemsets):
	#outputs all frequent itemsets
	### 1 itemset per line and the support in parentheses
	### example output: A (4)
	file = open(outputFile, 'w')

	for i, freqSet in enumerate(frequentItemsets):
		s = ""
		for element in freqSet:
			s += str(element) + " "
		s += "(" +  str(frequentItemsets[freqSet]) + ")"
		#print(s)

		if i == len(frequentItemsets)-1:
			file.write(s) #check if last line
		else:
			file.write(s+'\n') #write our formatted string
	file.close()



def main(argv):
	inputFile = str(argv[1])
	minSupp = int(argv[2])
	outputFile = str(argv[3])

	#Transactions = [ ['A', 'C', 'D'], ['B', 'C', 'E'], ['A', 'B', 'C', 'E'], ['B', 'E'] ]
	#minSupp = 2

	if(minSupp == 0):
		writeOutputFile(outputFile,{})
		return 0

	Transactions = readInputFile(inputFile)
	#print("Transactions from in file", Transactions)

	frequentItemsets = {}

	maxLen = 0
	for T in Transactions:
		if len(T) > maxLen:
			maxLen = len(T)

	C = joinStep(Transactions, 1)
	#print("Transactions", Transactions)
	#inp = input("enter to continue\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
	#print("C 1: ",C)
	
	k = 2
	while(k <= maxLen) or L:
		#print(" for k = ", k)
		L = pruneStep(C, minSupp)
		#print("L",k-1,": ", L)

		frequentItemsets.update(L)

		if not L:
			break

		C = joinStep(L, k)
		#print("C",k,": ", C)

		C = scan(C,Transactions)
		#print("C",k," after scan: ", C)

		k+=1
		print("k",k)

	#print("Frequent itemsets: ", frequentItemsets)

	writeOutputFile(outputFile, frequentItemsets)




if __name__ == "__main__":
	start_time = time.time()
	main(sys.argv)
	print ("---%s  seconds---" %(time.time()-start_time))