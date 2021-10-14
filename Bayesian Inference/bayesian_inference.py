def permutate(domain,rowCount,varCount):
    prmSet = [['0' for i in range(varCount)] for j in range(int(rowCount))]

    repeatNum = rowCount
    for i in range(varCount):
        repeatNum = int(repeatNum/len(domain[i]))
        #print("repeatNum: ",repeatNum)
        domainValue =0
        count = 0
        for j in range(int(rowCount)):
            prmSet[j][i]= domain[i][domainValue]
            count+=1
            if count == repeatNum:
                count=0
                domainValue+=1
                if domainValue>= len(domain[i]):
                    domainValue=0
    return prmSet

def rowCountFind(domain):
    totalRows = 1 #no of rows in cbt matrix
    for i in range(len(domain)):
            totalRows*= len(domain[i])
    return totalRows

def getCountList(cpt,parentPrmSet,varIndex,parentIndexList):
    countList = []
    indexList= []
    #print("parentPrmSet",parentPrmSet)
    for i in range(len(parentPrmSet)):
        count =0
        for key,value in cpt.items():
            keyList = key.split(',')
            vList=[keyList[varIndex]]
            for j in parentIndexList:
                vList.append(keyList[j])
            if vList == parentPrmSet[i]:
                count+= value
        countList.append(count)
    return countList
            


"""
input code start
"""

n = int(input()) #no. of variables
domain = []  #domain of each variable
for i in range(n):
    domain.append(list(input().replace(" ", "").split(',')))
#print("domains: ",domain)

"""
taking input child relationship and converting into parent relationship
"""
#relationship matrix
child = []
for i in range(n):
    child.append(list(input().split(' ')))
#print("child: ",child)
#finding parent from child
parent = {}
for i in range(n):
    p = []
    for j in range(n):
        if child[j][i] == '1':
            p.append(j)
    parent[i] = p
#print("parent set: ",parent)

m = int(input()) #no. of training examples
#print("m: ",m)

"""
input code ends
"""

"""
constructing CPT matrix
"""

cpt = {}
for i in range(m):
    trainExp = str(input())
    objValue = cpt.get(trainExp)
    if objValue == None:
        cpt[trainExp]= 1
    else:
        cpt[trainExp]= objValue+1
#print(cpt)

for i in range(n):
    if len(parent[i])==0:
        for j in domain[i]:
            count=0
            for key,value in cpt.items():
                if key.split(',')[i]== j:
                    count+=value
            print("{:.4f}".format(count/m), end =" ")
        print()
    else:
        parentDomain = []
        parentDomain.append(domain[i])
        for j in range(len(parent[i])):
            parentDomain.append(domain[parent[i][j]])
        #print(parentDomain)
        #permutation of parent set
        pTotalRows = rowCountFind(parentDomain)
        #print(pTotalRows)
        parentPrmSet = permutate(parentDomain,pTotalRows,len(parent[i])+1)
        #print(parentPrmSet)
        countList = getCountList(cpt,parentPrmSet,i,parent[i])
        #print("countList: ",countList)
        parentCombCount = int(pTotalRows/len(domain[i]))
        tCountList = [0]*parentCombCount
        
        for a in range(parentCombCount):
            for c in range(len(domain[i])):
                tCountList[a]+=countList[a+c*parentCombCount]
        #print("tCountList: ",tCountList)
        b=0
        for a in range(len(countList)):
            if b==parentCombCount:
                b=0
            if tCountList[b]!= 0:
                print("{:.4f}".format(countList[a]/tCountList[b]), end =" ")
            else:
                print(0.0000, end =" ")
            b+=1
        print()
            
        
        
     

