import random
import time
import statistics
from collections import defaultdict

def parse_dag_file(filepath):
    import re
    def is_numeric_line(line):
        return bool(re.match(r'^[\d\.\s\-]+$', line.strip()))
    
    with open(filepath, 'r', encoding='big5', errors='ignore') as f:
        lines = [line.strip() for line in f if is_numeric_line(line) and line.strip() != '']

    ptr = 0
    p_count = int(float(lines[ptr])); ptr += 1
    t_count = int(float(lines[ptr])); ptr += 1
    e_count = int(float(lines[ptr])); ptr += 1

    comm_matrix = []
    for i in range(p_count):
        row = list(map(float, lines[ptr].split()))
        comm_matrix.append(row)
        ptr += 1

    comp_cost = []
    for i in range(t_count):
        row = list(map(float, lines[ptr].split()))
        comp_cost.append(row)
        ptr += 1

    edges = []
    for i in range(e_count):
        parts = lines[ptr].split()
        edges.append((int(float(parts[0])), int(float(parts[1])), float(parts[2])))
        ptr += 1

    return p_count, t_count, comm_matrix, comp_cost, edges

def random_topological_sort(t_count, edges):
    in_deg = [0]*t_count
    graph = defaultdict(list)
    for frm,to,_ in edges:
        graph[frm].append(to)
        in_deg[to] += 1
    zero_in_deg = [i for i in range(t_count) if in_deg[i]==0]
    order = []
    while zero_in_deg:
        u = random.choice(zero_in_deg)
        zero_in_deg.remove(u)
        order.append(u)
        for v in graph[u]:
            in_deg[v] -= 1
            if in_deg[v]==0:
                zero_in_deg.append(v)
    if len(order)!=t_count:
        raise RuntimeError("有環，無法做拓撲排序")
    return order

def evaluate(chromosome, p_count, t_count, comm_matrix, comp_cost, edges):
    ss, ms = chromosome
    task_proc_map = dict(zip(ss, ms))
    start_times = [0.0]*t_count
    finish_times = [0.0]*t_count

    for task_id in ss:
        proc = task_proc_map[task_id]
        earliest_start = 0.0
        for frm,to,comm_cost_edge in edges:
            if to == task_id:
                pred = frm
                pred_proc = task_proc_map[pred]
                comm_delay = 0 if pred_proc==proc else comm_cost_edge * comm_matrix[pred_proc][proc]
                earliest_start = max(earliest_start, finish_times[pred]+comm_delay)
        start_times[task_id] = earliest_start
        finish_times[task_id] = earliest_start + comp_cost[task_id][proc]
    return max(finish_times)

def generate_individual(t_count, p_count, edges):
    ss = random_topological_sort(t_count, edges)
    ms = [random.randint(0,p_count-1) for _ in range(t_count)]
    return (ss, ms)

def tournament_selection(population, fitness, k=3):
    selected = random.sample(list(zip(population, fitness)), k)
    selected.sort(key=lambda x: x[1])
    return selected[0][0]

def crossover(parent1, parent2):
    ss1, ms1 = parent1
    ss2, ms2 = parent2
    point = random.randint(1, len(ss1)-2)
    child_ss = ss1[:]
    child_ms = ms1[:point] + ms2[point:]
    return (child_ss, child_ms)

def mutate(chromosome, p_count, mutation_rate):
    ss, ms = chromosome
    for i in range(len(ms)):
        if random.random() < mutation_rate:
            ms[i] = random.randint(0, p_count-1)
    return (ss, ms)

def genetic_algorithm(p_count, t_count, comm_matrix, comp_cost, edges,
                      pop_size=50, generations=250, mutation_rate=0.1):

    population = [generate_individual(t_count, p_count, edges) for _ in range(pop_size)]
    fitness = [evaluate(ind, p_count, t_count, comm_matrix, comp_cost, edges) for ind in population]

    best = population[fitness.index(min(fitness))]
    best_score = min(fitness)

    for gen in range(generations):
        new_population = []
        elite_index = fitness.index(min(fitness))
        new_population.append(population[elite_index])

        while len(new_population) < pop_size:
            parent1 = tournament_selection(population, fitness)
            parent2 = tournament_selection(population, fitness)
            child = crossover(parent1, parent2)
            child = mutate(child, p_count, mutation_rate)
            new_population.append(child)

        population = new_population
        fitness = [evaluate(ind, p_count, t_count, comm_matrix, comp_cost, edges) for ind in population]

        gen_best = min(fitness)
        if gen_best < best_score:
            best_score = gen_best
            best = population[fitness.index(gen_best)]

    return best, best_score

def run_multiple_times(p_count, t_count, comm_matrix, comp_cost, edges,
                       pop_size, mutation_rate, generations, repeat=5):

    best_scores = []
    durations = []

    for i in range(repeat):
        start = time.perf_counter()
        best_sol, best_score = genetic_algorithm(p_count, t_count, comm_matrix, comp_cost, edges,
                                                 pop_size=pop_size,
                                                 generations=generations,
                                                 mutation_rate=mutation_rate)
        end = time.perf_counter()
        best_scores.append(best_score)
        durations.append(end - start)
        print(f"第 {i+1} 次執行最佳 makespan: {best_score:.2f}, 耗時: {durations[-1]:.4f} 秒")

    print("\n===== 多次執行統計結果 =====")
    print(f"最佳值 (Best): {min(best_scores):.2f}")
    print(f"最差值 (Worst): {max(best_scores):.2f}")
    print(f"平均值 (Mean): {statistics.mean(best_scores):.2f}")
    print(f"標準差 (Std Dev): {statistics.stdev(best_scores):.4f}")
    print(f"平均耗時: {statistics.mean(durations):.4f} 秒")

def main():
    filename = input("請輸入 DAG 檔案名稱 (例如 n4_00.dag.txt)：").strip()
    p_count, t_count, comm_matrix, comp_cost, edges = parse_dag_file(filename)

    pop_size = 30
    mutation_rate = 0.7
    generations = 250

    run_multiple_times(p_count, t_count, comm_matrix, comp_cost, edges,
                      pop_size, mutation_rate, generations, repeat=5)

if __name__ == "__main__":
    main()
