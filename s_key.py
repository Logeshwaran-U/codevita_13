import sys
from collections import deque

def mn():
    n, m = map(int, sys.stdin.readline().split())
    gd = [list(map(str.strip, sys.stdin.readline().split())) for _ in range(n)]
    T = int(sys.stdin.readline())
    I = int(sys.stdin.readline())

    alw = [set((r, c) for r in range(n) for c in range(m)) for _ in range(T)]

    for _ in range(I):
        t = int(sys.stdin.readline()) - 1
        x1, y1, x2, y2 = map(int, sys.stdin.readline().split())
        fbd = set()
        for r in range(x1-1, x2):
            for c in range(y1-1, y2):
                fbd.add((r, c))
        alw[t] -= fbd

    for t in range(T):
        if not alw[t]:
            print("Not enough clues")
            return

    ds1 = [(-1,0),(1,0),(0,-1),(0,1)]

    rble = [set() for _ in range(T)]
    rble[T-1] = alw[T-1].copy()

    for t in range(T-2, -1, -1):
        rble[t] = set()
        for r,c in alw[t]:
            for dr, dc in ds1:
                nr, nc = r+dr, c+dc
                if (nr,nc) in rble[t+1]:
                    rble[t].add((r,c))
                    break
        if not rble[t]:
            print("Not enough clues")
            return

    que = deque()
    for r,c in rble[0]:
        que.append( (0, r, c, [(r,c)]) )

    final_paths = []

    while que:
        t, r, c, path = que.popleft()
        if t == T-1:
            final_paths.append(path)
            if len(final_paths) > 1:
                print("Not enough clues")
                return
            continue

        for dr, dc in ds1:
            nr, nc = r+dr, c+dc
            if 0 <= nr < n and 0 <= nc < m and (nr,nc) in rble[t+1] and (nr,nc) not in path:
                que.append( (t+1, nr, nc, path + [(nr,nc)]) )

    if len(final_paths) == 1:
        key = ''.join(gd[r][c] for r,c in final_paths[0])
        print(key)
    else:
        print("Not enough clues")

if __name__ == "__main__":
    mn()
