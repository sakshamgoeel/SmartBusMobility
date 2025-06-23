# dijkstra_logic.py

def dijkstra(graph, start, end):
    import heapq

    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    previous = {node: None for node in graph}
    pq = [(0, start)]

    while pq:
        current_distance, current_node = heapq.heappop(pq)

        if current_distance > distances[current_node]:
            continue

        for neighbor, details in graph[current_node].items():
            weight = details['cost']
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))

    path, node = [], end
    while node:
        path.insert(0, node)
        node = previous[node]

    if distances[end] == float('inf'):
        return {"path": [], "totalCost": -1}

    return {"path": path, "totalCost": distances[end]}
