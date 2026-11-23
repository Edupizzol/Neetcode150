class Solution:
    def longestPalindrome(self, s: str) -> str:
        maximum=0
        begin=0
        end=0
        n = len(s)
        i=0
        while(i<n):
            right=i-1
            left=i+1
            temp=1
            while(right>=0 and left<n and s[right]==s[left]):
                temp+=2
                right-=1
                left+=1
            if(left-right>maximum):
                maximum=left-right
                begin=right+1
                end=left
            if(i<n-1 and s[i]==s[i+1]):
                right=i
                left=i+1
                temp=0
                while(right>=0 and left<n and s[right]==s[left]):
                    temp+=2
                    right-=1
                    left+=1
                if(left-right>maximum):
                    maximum=left-right
                    begin=right+1
                    end=left
            i+=1
        return s[begin:end]