def eval_balance(graph, individual):
    '''
    Function to compute the fitness of an individual for the balanced coloring problem. 
    Inputs: 
        individual: individual object from DEAP toolbox
        graph: graph object containing nodes and edges
    Outputs:
        fitness: fitness of an individual coloring
    '''
    
    n = graph.n
    m = sum(1 for i in range(n) for node in [graph.get_node(i)] if node is not None) // 2
    k = graph.k
    color_bits = int(math.ceil(math.log2(k)))
    
    # Decode individual genes into colors
    color_assignment = [int("".join(map(str, individual[i * color_bits:(i + 1) * color_bits])), 2) % k for i in range(n)]
    
    # Step 1: Calculate edge penalty for adjacent nodes with the same color
    edge_penalty = 0
    for i in range(n):
        node = graph.get_node(i)
        while node is not None:
            if color_assignment[i] == color_assignment[node.vertex]:
                edge_penalty += 1
            node = node.next
    edge_penalty /= 2  # Each edge is counted twice in an undirected graph

    # Step 2: Calculate balance term by assessing color usage distribution
    color_counts = [color_assignment.count(j) for j in range(k)]
    balance_term = 1
    for count in color_counts:
        # Avoid division by zero if no nodes are assigned a color
        balance_term *= (count / n) if n > 0 else 0
    
    # Step 3: Combine edge penalty and balance term into the final fitness calculation
    if m > 0:
        fitness = ((m - edge_penalty) / m) * balance_term
    else:
        # Handle cases where the graph has no edges
        fitness = balance_term
    
    return (fitness,)

