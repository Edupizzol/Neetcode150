class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        dictionary = {}
        for i,num in enumerate(nums):
            index = target-num
            if index in dictionary:
                return [i,dictionary[index]]
            dictionary[num]=i