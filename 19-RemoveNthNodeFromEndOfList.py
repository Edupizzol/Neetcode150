# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:

    def removeNthFromEnd(self, head: ListNode | None, n: int) -> ListNode | None:
        temp = head
        count = 0
        while(head is not None):
            head = head.next
            count+=1

        index = count - n  
        if index==0:
            return temp.next

        head = temp
        prev = head
        while(index>0):
            prev = head
            head = head.next
            index-=1
        prev.next = head.next

        return temp
