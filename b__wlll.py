import heapq

def rl_ds(top, left, front, drctn):
    if drctn == "right":
        return left, 7 - top, front
    elif drctn == "left":
        return 7 - left, top, front
    elif drctn == "top":
        return front, left, 7 - top
    elif drctn == "down":
        return 7 - front, left, top

def solve():
    n = int(input().strip())
    plmnts = []
    for _ in range(n):
        a, b, d = input().strip().split()
        plmnts.append((int(a), int(b), d))
    plmnts.sort(key=lambda x: (x[0], x[1]))
    pos = {plmnts[0][0]: (0, 0)}
    for a, b, d in plmnts:
        if a not in pos:
            continue
        x, y = pos[a]
        if d == "right":
            new_pos = (x + 1, y)
        elif d == "left":
            new_pos = (x - 1, y)
        elif d == "top":
            new_pos = (x, y + 1)
        else:
            new_pos = (x, y - 1)
        for k, v in list(pos.items()):
            if v == new_pos:
                del pos[k]
        pos[b] = new_pos

    adj = {c: {} for c in pos}
    dirs = {"right": (1, 0), "left": (-1, 0), "top": (0, 1), "down": (0, -1)}
    p_t_cube = {v: k for k, v in pos.items()}
    for c, (x, y) in pos.items():
        for d, (dx, dy) in dirs.items():
            nx, ny = x + dx, y + dy
            if (nx, ny) in p_t_cube:
                adj[c][d] = p_t_cube[(nx, ny)]
    src, dst = map(int, input().strip().split())
    top, left, front = map(int, input().strip().split())
    pq = [(0, src, top, left, front)]
    visited = {}
    while pq:
        cost, node, t, l, f = heapq.heappop(pq)
        state = (node, t, l, f)
        if state in visited and visited[state] <= cost:
            continue
        visited[state] = cost
        if node == dst:
            print(cost, end="")
            return
        for d, nxt in adj.get(node, {}).items():
            nt, nl, nf = rl_ds(t, l, f, d)
            heapq.heappush(pq, (cost + nt, nxt, nt, nl, nf))

if __name__ == "__main__":
    solve()
