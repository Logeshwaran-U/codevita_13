def bd_mps():
    fh_mp = {'0': '0', '2': '5', '5': '2', '8': '8'}
    fv_mp = {'0': '0', '1': '1', '2': '5', '3': '3', '5': '2', '8': '8'}
    i_mp = {str(d): str(d) for d in range(10)}
    return {'L': fh_mp, 'U': fh_mp, 'R': fv_mp, 'D': fv_mp, 'S': i_mp}

def mr_dgt(d, o_p, sd_mp):
    mp_tbl = sd_mp.get(o_p)
    if not mp_tbl:
        return None
    return mp_tbl.get(d)

def ty_nmbr(dgts):
    if not dgts:
        return '0'
    dgts.sort()
    if dgts[0] != '0':
        return ''.join(dgts)
    for ix in range(len(dgts)):
        if dgts[ix] != '0':
            nz = dgts[ix]
            zrs = dgts.count('0')
            tmp = dgts.copy()
            tmp.pop(ix)
            for _ in range(zrs):
                tmp.remove('0')
            return nz + '0' * zrs + ''.join(tmp)
    return '0'

def mn():
    import sys
    dta = sys.stdin.read().split()
    if len(dta) < 2:
        return
    nm, o_ps = dta[0], dta[1]
    sd_mp = bd_mps()
    ktp = []
    for i in range(len(nm)):
        mpd = mr_dgt(nm[i], o_ps[i], sd_mp)
        if mpd:
            ktp.append(mpd)
    print(ty_nmbr(ktp), end='')

if __name__ == "__main__":
    mn()
