import sys
sys.setrecursionlimit(10**5)

class Solution:

    def change(self, amount: int, coins: list[int]) -> int:
        n = len(coins)
        dp = [[-1]*(amount+1) for i in range(n)]

        def memo(i,a):

            if(a==0):
                return 1
            if a<0 or i==n:
                return 0

            if(dp[i][a]!=-1):
                return dp[i][a]

            use = memo(i,a-coins[i])
            skip = memo(i+1,a)
            dp[i][a]=use+skip

            return dp[i][a]

        return memo(0,amount)

if __name__=="__main__":

    s=Solution()
    n=int(input())
    amount = int(input())
    coins=[]
    for i in range(n):
        num = int(input())
        coins.append(num)

    print(s.change(amount,coins))
    


