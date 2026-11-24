class Solution:
    def orangesRotting(self, grid: list[list[int]]) -> int:

        n,m = len(grid), len(grid[0])
        from collections import deque
        def bfs(grid, q : deque, fresh_oranges_count: int):
            count=0
            while(q) and fresh_oranges_count>0:
                count+=1
                for _ in range(len(q)):
                    i,j = q.popleft()
                    if(i>0 and grid[i-1][j]==1):
                        grid[i-1][j]=2
                        q.append((i-1,j))
                        fresh_oranges_count-=1
                    if(j<m-1 and grid[i][j+1]==1):
                        grid[i][j+1]=2                        
                        q.append((i,j+1))
                        fresh_oranges_count-=1
                    if(i<n-1 and grid[i+1][j]==1):
                        grid[i+1][j]=2
                        q.append((i+1,j))
                        fresh_oranges_count-=1
                    if(j>0 and grid[i][j-1]==1):
                        grid[i][j-1]=2
                        q.append((i,j-1))   
                        fresh_oranges_count-=1

            return count if fresh_oranges_count==0 else -1

        q = deque()
        fresh_orange_count=0
        for i in range(n):
            for j in range(m):
                if grid[i][j]==2:
                    q.append((i,j))
                elif grid[i][j]==1:
                    fresh_orange_count+=1

        return bfs(grid,q,fresh_orange_count)

if __name__ == "__main__":
    sol = Solution()
    
    print("Example 1:", sol.orangesRotting([[2, 1, 1], [1, 1, 0], [0, 1, 1]])) 
    print("Example 2:", sol.orangesRotting([[2, 1, 1], [0, 1, 1], [1, 0, 1]]))  
    print("Example 3:", sol.orangesRotting([[0, 2]]))