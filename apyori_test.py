#apyori_test.py 

import sys
import time
from apyori import apriori

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
	return {}

def readInputFile(inputFile):
	#intended input:
	### 1 transaction per line
	### items separated by ' ' character
	### example input: A B D
	file = open(inputFile)
	Transactions = []
	i = 0
	for line in file:
		#print("line",line)
		a = list(line.rstrip().split(" "))
		Transactions.append(a)
		i+=1
	file.close()
	return Transactions,i

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

	if(minSupp == 0):
		writeOutputFile(outputFile,{})
		return 0

	Transactions,totalNumTransactions = readInputFile(inputFile)
	#print("Transactions from in file", Transactions)

	frequentItemsets = {}

	maxLen = 0
	for T in Transactions:
		if len(T) > maxLen:
			maxLen = len(T)

	C = joinStep(Transactions, 1)
	#print("Transactions", Transactions)

	association_rules = list( apriori(Transactions,min_support = minSupp/totalNumTransactions) )

	frequentItemsets = {}
	for i in range(len(association_rules)):
		frequentSet = tuple(association_rules[i][0])
		support = int(association_rules[i][1]*totalNumTransactions)
		frequentItemsets[frequentSet] = support

	#print("frequent itemsets:",frequentItemsets)

	writeOutputFile(outputFile, frequentItemsets)


if __name__ == "__main__":
	start_time = time.time()
	main(sys.argv)
	print ("---%s  seconds---" %(time.time()-start_time))