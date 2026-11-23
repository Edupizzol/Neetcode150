class Solution:
    
    def coinChange(self, coins: list[int], amount: int) -> int:
        n = len(coins)
        dp = [[-1] * (amount+1) for i in range(len(coins))]
        INF = float('inf')

        def memo(a, i):

            if(a==0):
                return 0
            if(a<0 or i>=len(coins)):
                return INF

            if(dp[i][a]!=-1):
                return dp[i][a]

            use = 1+memo(a-coins[i],i)
            skip = memo(a,i+1)

            dp[i][a]=min(use,skip)
            return dp[i][a]

        res = memo(amount, 0)
        return -1 if res == INF else res

if __name__=="__main__":

    n = int(input())    
    amount = int(input())
    coins=[]
    for i in range(n):
        num = int(input())
        coins.append(num)

    s = Solution()
    print(s.coinChange(coins, amount))
