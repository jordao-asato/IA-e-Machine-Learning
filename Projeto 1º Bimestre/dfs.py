# chaves do dicionário são os vértices (ou nós) do grafo.
# valores associados a cada chave são as listas de adjacência, que contêm os vizinhos desse vértice.
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

def dfs(graph, atual, dest, visited):
    if atual == dest:  # Verifica se o vértice atual é o destino.
        return 0  # Se for, retorna 0, indicando que o destino foi alcançado.
    visited.add(atual)  # Marca o vértice atual como visitado adicionando-o ao conjunto `visited`.
    min_dist = -1  # Inicializa a distância mínima com -1 (significando que o caminho ainda não foi encontrado).

    for neighbor in graph.adjList.get(atual, []):  # Para cada vizinho do vértice atual na lista de adjacência:
        if neighbor not in visited:  # Se o vizinho não foi visitado:
            distance = dfs(graph, neighbor, dest, visited)  # Realiza uma busca DFS recursiva a partir do vizinho.
            if distance != -1:  # Se um caminho foi encontrado:
                #distancia total = distance + 1 -> soma o caminho ate o vizinho e a aresta que leva à ele
                #distancia atual do nó de origem até o nó alcançado pela busca
                #o +1 indica que a busca avançou um passo a mais ao visitar um vizinho do atual
                if min_dist == -1 or (distance + 1 < min_dist):  # Atualiza a distância mínima se necessário.
                    min_dist = distance + 1
                    #att se ainda não foi definido ou se esse caminho é + curto do que o caminho mínimo encontrado

    #após explorar todos os caminhos possíveis a partir do nó atual
    visited.remove(atual)  # Remove o vértice atual do conjunto `visited` para permitir backtracking.
    return min_dist  # Retorna a distância mínima encontrada.

def main():
    pontos, ligacoes = map(int, input("Insira valor P e L:\n").split())
    # Lê os valores de `pontos` e `ligações` do usuário.

    graph = Graph()  # Cria um novo objeto `Graph`.

    for _ in range(ligacoes):
        v1, v2 = input("\nInsira origem (String) e destino (String):\n").split()
        # Lê as conexões entre os pontos como pares de strings.
        graph.addAresta(v1, v2)  # Adiciona a aresta (conexão) ao grafo.

    visited = set()  # Cria um conjunto vazio para rastrear os vértices visitados durante a DFS.

    ent_to_star = dfs(graph, "Entrada", "*", visited)  # Executa a DFS para encontrar a
    # distância de "Entrada" até "*".
    star_to_exit = dfs(graph, "*", "Saida", visited)  # Executa a DFS para encontrar a
    # distância de "*" até "Saida".
    total_dist = ent_to_star + star_to_exit  # Calcula a distância total, somando as duas distâncias.

    if ent_to_star == -1:
        print("Não foi possível encontrar o queijo.")
    elif star_to_exit == -1:
        print("Não foi possível encontrar a saída.")
    else:
        total_dist = ent_to_star + star_to_exit
        print("\nDistância mínima:\n{}".format(total_dist))

    #print("\nDistancia minima:\n{}".format(total_dist))  # Imprime a distância mínima total.

if __name__ == "__main__":
    main()  # Chama a função `main` para executar o programa.
