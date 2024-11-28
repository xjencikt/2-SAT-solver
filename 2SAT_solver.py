from collections import defaultdict


def read_file(file):
    a = []
    b = []
    with open(file, 'r') as file:
        lines = [line.strip() for line in file]
        first_line_values = lines[0].split()
        n = int(first_line_values[0])
        m = int(first_line_values[1])

        for i in range(1, len(lines)):
            split_line = lines[i].split()
            a.append(int(split_line[0]))
            b.append(int(split_line[1]))

        return n, m, a, b


# Konštanta
MAX = 100000

# Dátové štruktúry používané na implementáciu Kosarajuovho algoritmu
adj = defaultdict(list)
adj_inv = defaultdict(list)
visited = [False] * (MAX + 1)
visited_inv = [False] * (MAX + 1)
s = []
scc = [0] * (MAX + 1)
counter = 1


# Funkcia na pridanie hrán do pôvodného grafu
def add_edges(a, b):
    adj[a].append(b)


# Funkcia na pridávanie hrán na vytvorenie inverzného grafu
def add_edges_inverse(a, b):
    adj_inv[b].append(a)


# Krok 1 Kosarajuovho algoritmu - DFS na pôvodnom grafe
def dfs_first(u):
    if visited[u]:
        return

    visited[u] = True

    for neighbor in adj[u]:
        dfs_first(neighbor)

    s.append(u)


# Krok 2 Kosarajuovho algoritmu - DFS na inverznom grafe
def dfs_second(u):
    if visited_inv[u]:
        return

    visited_inv[u] = True

    for neighbor in adj_inv[u]:
        dfs_second(neighbor)

    scc[u] = counter


# Funkcia na kontrolu 2-SAT
def is_2_satisfiable(n, m, a, b):
    global counter  # Počítadlo ako globálna premenná
    # Sledovanie vyskytujúcich sa klauzúl a ich splniteľnosti
    clauses = {}

    # Pridávanie hrán do grafu
    for i in range(m):
        # Uistiť sa, že a[i] aj b[i] nie sú nulové
        if a[i] != 0 or b[i] != 0:
            # Skontrolujeme, či máme 2 klauzuly v tvare (x 0) a (-x 0)
            if b[i] == 0:
                clause = abs(a[i])
                is_positive = a[i] > 0
                # Ak sa už vyskytla klauzula s opačnou polaritou, je splniteľná
                if clauses.get(clause) == is_positive:
                    print("NESPLNITELNA")
                    return
                # Uloženie klauzuly s jej polaritou
                clauses[clause] = not is_positive
            # Ak má formula iba 1 klauzulu
            if a[i] > 0 and b[i] == 0:
                add_edges(a[i] + n, n - a[i]) # Implikácia: a -> True
                add_edges_inverse(a[i] + n, n - a[i])
            elif a[i] < 0 and b[i] == 0:
                add_edges(-a[i], n - a[i])  # Implikácia: NOT a -> False
                add_edges_inverse(-a[i], n - a[i])
            # Oba kladné literály
            elif a[i] > 0 and b[i] > 0:
                # Pridať hrany pre klauzuly typu (a ALEBO b)
                add_edges(a[i] + n, b[i])  # Implikácia: a -> b
                add_edges_inverse(a[i] + n, b[i])  # Inverzná hrana
                add_edges(b[i] + n, a[i])  # Implikácia: b -> a
                add_edges_inverse(b[i] + n, a[i])  # Inverzná hrana
            # Jeden kladný a jeden záporný literál
            elif a[i] > 0 and b[i] < 0:
                # Pridať hrany pre klauzuly typu (a ALEBO NOT b)
                add_edges(a[i] + n, n - b[i])  # Implikácia: a -> NOT b
                add_edges_inverse(a[i] + n, n - b[i])  # Inverzná hrana
                add_edges(-b[i], a[i])  # Implikácia: NOT b -> a
                add_edges_inverse(-b[i], a[i])  # Inverzná hrana

            # Jeden záporný a jeden kladný literál
            elif a[i] < 0 and b[i] > 0:
                # Pridať hrany pre klauzuly typu (NOT a ALEBO b)
                add_edges(-a[i], b[i])  # Implikácia: NOT a -> b
                add_edges_inverse(-a[i], b[i])  # Inverzná hrana
                add_edges(b[i] + n, n - a[i])  # Implikácia: b -> NOT a
                add_edges_inverse(b[i] + n, n - a[i])  # Inverzná hrana


            # Oba záporné literály
            else:
                # Pridať hrany pre klauzuly typu (NOT a ALEBO NOT b)
                add_edges(-a[i], n - b[i])  # Implikácia: NOT a -> NOT b
                add_edges_inverse(-a[i], n - b[i])  # Inverzná hrana
                add_edges(-b[i], n - a[i])  # Implikácia: NOT b -> NOT a
                add_edges_inverse(-b[i], n - a[i])  # Inverzná hrana

    # Krok 1 Kosarajuovho algoritmu - Prejsť pôvodný graf
    for i in range(1, 2 * n + 1):
        if not visited[i]:
            dfs_first(i)

    # Krok 2 Kosarajuovho algoritmu - prejsť inverzný graf
    while s:
        node = s.pop()
        if not visited_inv[node]:
            dfs_second(node)
            counter += 1

    # Kontrola, či existujú premenné x a -x v tom istom SCC:
    # Strongly Connected Component = Silne prepojená zložka
    for i in range(1, n + 1):
        if scc[i] == scc[i + n]:
            print("NESPLNITELNA")
            return

    # Určenie pravdivostných hodnôt pre každú premennú
    variable_truth_values = {}  # Slovník na ukladanie pravdivostných hodnôt premenných
    for i in range(1, n + 1):
        if scc[i] > scc[i + n]:
            variable_truth_values[i] = True
        else:
            variable_truth_values[i] = False

    # V tom istom SCC neexistujú žiadne takéto premenné x a -x
    print("SPLNITELNA")

    # Vypísanie pravdivostných hodnôt pre každú premennú
    for variable, truth_value in variable_truth_values.items():
        if truth_value:
            print("PRAVDA")
        else:
            print("NEPRAVDA")


# Main na testovanie 2-SAT problému
def main():
    file = "P13.txt"
    n, m, a, b = read_file(file)
    is_2_satisfiable(n, m, a, b)


if __name__ == "__main__":
    main()
