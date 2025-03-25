from collections import deque  # Importa deque para implementar a fila na BFS.

class Graph:
    def __init__(self):
        self.adjList = {}  # Inicializa um dicionário vazio para armazenar a lista de adjacência.

    def addAresta(self, v1, v2):
        if v1 not in self.adjList:  # Verifica se o vértice v1 não está no dicionário.
            self.adjList[v1] = []  # Se não estiver, cria uma lista vazia para v1.
        if v2 not in self.adjList:  # Verifica se o vértice v2 não está no dicionário.
            self.adjList[v2] = []  # Se não estiver, cria uma lista vazia para v2.
        self.adjList[v1].append(v2)  # Adiciona v2 à lista de adjacência de v1.
        self.adjList[v2].append(v1)  # Adiciona v1 à lista de adjacência de v2.

def bfs(graph, start, end):
    visited = set()  # Cria um conjunto vazio para rastrear os vértices visitados.
    queue = deque([(start, 0)])  # Inicializa a fila com o vértice de início e a distância 0.
    visited.add(start)  # Marca o vértice de início como visitado.

    while queue:  # Continua até que a fila esteja vazia.
        current_node, distance = queue.popleft()  # Remove o primeiro elemento da fila (FIFO).

        if current_node == end:  # Se o vértice atual é o destino, retorna a distância.
            return distance

        for neighbor in graph.adjList.get(current_node, []):  # Para cada vizinho do vértice atual:
            if neighbor not in visited:  # Se o vizinho ainda não foi visitado:
                visited.add(neighbor)  # Marca o vizinho como visitado.
                queue.append((neighbor, distance + 1))  # Adiciona o vizinho à fila com a distância incrementada.

    return -1  # Se não houver caminho entre start e end.

def main():
    pontos, ligacoes = map(int, input("Insira valor P (4 <= P <= 4000) e L (4 <= L <= 5000):\n").split())
    # Lê os valores de `pontos` e `ligações` do usuário.

    graph = Graph()  # Cria um novo objeto `Graph`.

    for _ in range(ligacoes):
        v1, v2 = input("\nInsira origem (String) e destino (String):\n").split()
        # Lê as conexões entre os pontos como pares de strings.
        graph.addAresta(v1, v2)  # Adiciona a aresta (conexão) ao grafo.

    ent_to_star = bfs(graph, "Entrada", "*")  # Executa a BFS para encontrar a
    # distância de "Entrada" até "*".
    star_to_exit = bfs(graph, "*", "Saida")  # Executa a BFS para encontrar a
    # distância de "*" até "Saida".
    total_dist = ent_to_star + star_to_exit  # Calcula a distância total, somando as duas distâncias.

    print("\nDistancia minima:\n{}".format(total_dist))  # Imprime a distância mínima total.

if __name__ == "__main__":
    main()  # Chama a função `main` para executar o programa.
