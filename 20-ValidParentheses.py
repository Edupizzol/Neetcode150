class Solution:
    def isValid(self, s: str) -> bool:
        stack = []
        n = len(s)
        if(n<=1):
            return False

        i=0
        while(i<n):
            if len(stack) == 0:
                stack.append(s[i])
            elif stack[-1] == '(' and s[i] == ')':
                stack.pop()
            elif stack[-1] == '[' and s[i] == ']':
                stack.pop()
            elif stack[-1] == '{' and s[i] == '}':
                stack.pop()
            else:
                stack.append(s[i])
            i+=1

        if len(stack)==0:
            return True
        return False


if __name__=="__main__":
    string = input()
    s = Solution()
    print(s.isValid(string))