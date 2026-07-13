# Word Break Problem

def wordBreakCount(str,dict):
    
    length = len(str)

    dp = [0]*(length+1) #stores numbers of ways to segement prefix str[0:i]
    dp[0]=1 #base case

    for i in range(1,length+1):
            for j in range(i):
                  #Extracting the partition
                  word = str[j:i]
                  if dp[j]>0 and word in dict:
                        dp[i]+=dp[j]
            print(dp)
    ways  = dp[length]
    return ways

string = "catsanddog"
dictionary = ["cat", "cats", "and", "sand", "dog"]

print(wordBreakCount(string,dictionary))