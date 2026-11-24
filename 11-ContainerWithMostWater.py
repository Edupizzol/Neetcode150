class Solution:
    def maxArea(self, height: list[int]) -> int:

        def calculate_area(height1, height2, i, j):
            return (min(height1,height2)*abs((i-j)))

        i,j = 0, len(height)-1
        maximum=0
        while(i<j):
            #print(maximum)
            #print(calculate_area(height[i],height[j],i,j))
            maximum=max(maximum,calculate_area(height[i],height[j],i,j))
            if(height[i]<height[j]):
                i+=1
            else:
                j-=1

        return maximum


if __name__=="__main__":
    n = int(input())
    height=[]
    for i in range(n):
        num = int(input())  
        height.append(num)
    s = Solution()
    print(s.maxArea(height))

