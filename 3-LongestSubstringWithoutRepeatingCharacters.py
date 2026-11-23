class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        start=0
        letters={}
        maximum=0

        for i,letter in enumerate(s):
            if s[i] in letters and letters[s[i]]>=start:
                maximum = max(i-start,maximum)
                start=letters[s[i]]+1
                letters.pop(s[i])
            letters[s[i]]=i
        maximum = max(len(s)-start,maximum)

        return maximum