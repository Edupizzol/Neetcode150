# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def goodNodes(self, root: TreeNode) -> int:
        maximum = root.val
        count=0

        def count_good_nodes(root: TreeNode, maximum):
            nonlocal count
            if(root is None):
                return 

            if(root.val>=maximum):
                count+=1
            maximum = max(root.val, maximum)
            count_good_nodes(root.left,maximum)
            count_good_nodes(root.right,maximum)

        count_good_nodes(root,maximum)           
        return count

