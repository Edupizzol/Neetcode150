# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def addTwoNumbers(self, l1: ListNode | None, l2: ListNode | None) -> ListNode | None:
        remainder=0
        digits=[]
        while l1 is not None or l2 is not None:
            value1=0
            value2=0
            if(l1 is None):
                value1=0
            else:
                value1=l1.val
            if(l2 is None):
                value2=0
            else:
                value2=l2.val
            temp = remainder+value1+value2
            digits.append(temp%10)
            remainder=temp//10

            if l1 is not None:
                l1=l1.next
            if l2 is not None:
                l2=l2.next

        if remainder!=0:
            digits.append(remainder)

        i=1
        Origin=ListNode(digits[0])
        FinalResult=Origin
        while(i<len(digits)):
            NewNode=ListNode(digits[i])
            Origin.next=NewNode
            Origin=NewNode
            i+=1
        return FinalResult