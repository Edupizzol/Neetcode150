class Solution:
    def reverse(self, x: int) -> int:
        import math
        def count_digits(n: int) -> int:
            count=0
            while(n>=1):
                n=n//10
                count+=1
            return count-1

        isNegative=False
        if(x<0):    
            isNegative=True
        if(isNegative):
            x*=-1

        index = pow(10,count_digits(x))
        num=0
        
        while(x>=1):
            num+=(x%10)*index
            x=x//10
            index=index//10

        if(num>2**31-1):
            return 0

        if(isNegative):
            return num*(-1)
        else:
            return num

if __name__=="__main__":
    num = int(input())
    s = Solution()
    print(s.reverse(num))