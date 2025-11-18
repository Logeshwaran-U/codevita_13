import sys
from collections import deque

def expnd_wl_rw(s):
    tmp, rst = "", []
    for chr in s:
        if chr.isdigit():
            tmp += chr
        else:
            rst.append((int(tmp), chr))
            tmp = ""
    return rst

def bld_wl(n, rws):
    gd = [[-1]*n for vr in range(n)]
    bs, pp = {}, {}
    bid = 0

    for r in range(n):
        pts = expnd_wl_rw(rws[r])
        c = 0
        for ln, tp in pts:
            for _ in range(ln):
                gd[r][c] = bid
                c += 1
            bs[bid] = tp
            bid += 1
    return gd, bs

def bl_cns(grd, n):
    cnt = {}
    drs = [(1,0),(-1,0),(0,1),(0,-1)]
    for i in range(n):
        for j in range(n):
            a = grd[i][j]
            if a not in cnt:
                cnt[a] = set()
            for dx, dy in drs:
                ni, nj = i+dx, j+dy
                if 0 <= ni < n and 0 <= nj < n:
                    b = grd[ni][nj]
                    if a != b:
                        cnt[a].add(b)
    return cnt

def soln():
    n = int(sys.stdin.readline().strip())
    rws = [sys.stdin.readline().strip() for vr in range(n)]

    grd, byp = bld_wl(n, rws)
    cn = bl_cns(grd, n)

    strt = [bid for bid, tp in byp.items() if tp == 'S']
    ends = {bid for bid, tp in byp.items() if tp == 'D'}
    if not strt or not ends:
        print(-1, end="")
        return

    sn = set(strt)
    q = deque([(s, 0) for s in strt])

    while q:
        brk, cst = q.popleft()
        for nb in cn.get(brk, []):
            tp = byp[nb]
            if tp == 'D':
                print(cst, end="")
                return
            if tp == 'G' and nb not in sn:
                sn.add(nb)
                q.append((nb, cst + 1))

    print(-1, end="")

if __name__ == "__main__":
    soln()
