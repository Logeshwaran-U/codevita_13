import collections
import math

def get_minimum_holes():
    
    try:
        # Read N_box and M_box (box dimensions)
        line = input().split()
        if not line: return "Invalid"
        N_box, M_box = int(line[0]), int(line[1])

        # Read number of partitions lines
        N_lines = int(input())

        # Read N partition lines (x1, y1, x2, y2)
        partitions_input = []
        for _ in range(N_lines):
            line = input().split()
            if not line: return "Invalid"
            partitions_input.append(tuple(map(int, line)))

    except Exception:
        return "Invalid"

    if N_box <= 0 or M_box <= 0: return "Invalid"

    # --- Step 1: Discretization ---
    x_coords = {0, N_box}
    y_coords = {0, M_box}
    for x1, y1, x2, y2 in partitions_input:
        x_coords.add(x1); x_coords.add(x2)
        y_coords.add(y1); y_coords.add(y2)
    
    sorted_x = sorted(list(x_coords))
    sorted_y = sorted(list(y_coords))
    
    x_map = {x: i for i, x in enumerate(sorted_x)}
    y_map = {y: i for i, y in enumerate(sorted_y)}
    
    W = len(sorted_x) - 1 # Grid columns
    H = len(sorted_y) - 1 # Grid rows

    
    horizontal_lines = [[0] * (H + 1) for _ in range(W)]
    vertical_lines = [[0] * H for _ in range(W + 1)]
    

    for x1, y1, x2, y2 in partitions_input:
        nx1, nx2 = min(x1, x2), max(x1, x2)
        ny1, ny2 = min(y1, y2), max(y1, y2)
        
        idx1, idx2 = x_map.get(nx1), x_map.get(nx2)
        idy1, idy2 = y_map.get(ny1), y_map.get(ny2)
        
        if nx1 == nx2: # Vertical line
            x_idx = idx1
            for j in range(idy1, idy2):
                if 0 <= x_idx <= W and 0 <= j < H:
                    vertical_lines[x_idx][j] = 1
        elif ny1 == ny2: # Horizontal line
            y_idx = idy1
            for i in range(idx1, idx2):
                if 0 <= i < W and 0 <= y_idx <= H:
                    horizontal_lines[i][y_idx] = 1

    # region_id_grid[i][j] stores the ID of the partition cell (i, j) belongs to
    region_id_grid = [[-1] * H for _ in range(W)]
    num_partitions = 0
    
    for i in range(W):
        for j in range(H):
            if region_id_grid[i][j] == -1:
                # New partition found
                num_partitions += 1
                current_region_id = num_partitions
                queue = collections.deque([(i, j)])
                region_id_grid[i][j] = current_region_id
                
                while queue:
                    ci, cj = queue.popleft() 

                    for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        ni, nj = ci + di, cj + dj # next cell
                        
                        if 0 <= ni < W and 0 <= nj < H and region_id_grid[ni][nj] == -1:
                            is_boundary = False
                            
                            # Corrected Adjacency/Boundary Check
                            if dj == 1: # Moving Right: check vertical boundary segment at x=sorted_x[ci+1]
                                if vertical_lines[ci + 1][cj] == 1: is_boundary = True
                            elif dj == -1: # Moving Left: check vertical boundary segment at x=sorted_x[ci]
                                if vertical_lines[ci][cj] == 1: is_boundary = True
                            elif di == 1: # Moving Down: check horizontal boundary segment at y=sorted_y[cj+1]
                                if horizontal_lines[ci][cj + 1] == 1: is_boundary = True
                            elif di == -1: # Moving Up: check horizontal boundary segment at y=sorted_y[cj]
                                if horizontal_lines[ci][cj] == 1: is_boundary = True
                            
                            if not is_boundary:
                                region_id_grid[ni][nj] = current_region_id
                                queue.append((ni, nj))

    # --- Validity Check (Incomplete Partitions) ---
    if N_lines > 0 and num_partitions == 1:
        return "Invalid"
    
    if num_partitions == 0:
        return "Invalid"
        
    adj = collections.defaultdict(set)
    
    for i in range(W):
        for j in range(H):
            r1 = region_id_grid[i][j]
            if r1 == -1: continue # Should not happen

            # Check Right neighbor
            if i + 1 < W:
                r2 = region_id_grid[i+1][j]
                if r2 != -1 and r1 != r2 and vertical_lines[i + 1][j] == 1:
                    adj[r1].add(r2)
                    adj[r2].add(r1)

            # Check Down neighbor
            if j + 1 < H:
                r2 = region_id_grid[i][j+1]
                if r2 != -1 and r1 != r2 and horizontal_lines[i][j + 1] == 1:
                    adj[r1].add(r2)
                    adj[r2].add(r1)

    color = {} # 0 or 1
    is_bipartite = True
    for start_node in range(1, num_partitions + 1):
        if start_node not in color:
            queue = collections.deque([(start_node, 0)])
            color[start_node] = 0
            while queue:
                u, c = queue.popleft()
                for v in adj[u]:
                    if v not in color:
                        color[v] = 1 - c
                        queue.append((v, 1 - c))
                    elif color[v] == c:
                        is_bipartite = False
                        break
        if not is_bipartite: break
        
    if not is_bipartite:
        pass

    set_a = {node for node, c in color.items() if c == 0}
    set_b = {node for node, c in color.items() if c == 1}
    
    match = {} # Stores match[v] = u for v in set_b, u in set_a
    
    def dfs_match(u, visited):
        """Finds an augmenting path starting from u in set_a."""
        visited.add(u)
        for v in adj[u]:
            if v not in match or (match[v] not in visited and dfs_match(match[v], visited)):
                match[v] = u
                return True
        return False

    max_matching_size = 0
    for u in set_a:
        if dfs_match(u, set()):
            max_matching_size += 1

    min_holes = max_matching_size

    return str(min_holes)


print(get_minimum_holes())