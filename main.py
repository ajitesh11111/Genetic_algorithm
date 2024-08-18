import random
import numpy as np

# Constants
NUM_CITIES = 9  # 4 state capitals + 5 other cities
NUM_AIRCRAFT_TYPES = 2  # 170-seater and 300-seater
POPULATION_SIZE = 100
NUM_GENERATIONS = 1000  # Increased for better accuracy
MUTATION_RATE = 0.1
CROSSOVER_RATE = 0.8
TIME_SLOTS = 18  # 24 hours, 30-minute slots

# Define cities
cities = [
    "Chennai", "Bengaluru", "Thiruvananthapuram", "Amaravati",
    "Cochin", "Mangalore", "Trichy", "Coimbatore", "Vijayawada"
]

# Initialize the demand matrix
DEMAND_MATRIX = np.zeros((NUM_CITIES, NUM_CITIES))

# Demand between state capitals
for i in range(4):
    for j in range(4):
        if i != j:
            DEMAND_MATRIX[i, j] = 1200

# Demand between city and its state capital
for i in range(4, 9):
    DEMAND_MATRIX[i, i % 4] = 450
    DEMAND_MATRIX[i % 4, i] = 450

# Specific demand between Coimbatore and Trichy
coimbatore_idx = cities.index("Coimbatore")
trichy_idx = cities.index("Trichy")
DEMAND_MATRIX[coimbatore_idx, trichy_idx] = 300
DEMAND_MATRIX[trichy_idx, coimbatore_idx] = 300

AIRCRAFT_CAPACITY = [170, 300]
TURNAROUND_TIME = {170: 30, 300: 45}  # in minutes

def create_chromosome():
    return [(random.randint(1, 10), random.choice(AIRCRAFT_CAPACITY), random.randint(0, TIME_SLOTS-1)) for _ in range(NUM_CITIES**2)]

def fitness(chromosome):
    total_coverage = 0
    total_cost = 0
    aircraft_utilization = [0] * len(AIRCRAFT_CAPACITY)

    for i in range(NUM_CITIES):
        for j in range(NUM_CITIES):
            if i != j:
                flights, aircraft, time_slot = chromosome[i * NUM_CITIES + j]
                demand = DEMAND_MATRIX[i][j]
                capacity_coverage = min(flights * aircraft, demand)
                total_coverage += capacity_coverage
                total_cost += flights * (aircraft * 5)  # Example cost model
                aircraft_utilization[AIRCRAFT_CAPACITY.index(aircraft)] += flights * (TURNAROUND_TIME[aircraft] + 60)  # 60 mins for flight

    fitness_value = total_coverage - (total_cost / 1000)  # Adjust the scale if needed

    return max(fitness_value, 1e-6)

def create_population():
    return [create_chromosome() for _ in range(POPULATION_SIZE)]

def crossover(parent1, parent2):
    if random.random() < CROSSOVER_RATE:
        point = random.randint(0, len(parent1) - 1)
        return parent1[:point] + parent2[point:], parent2[:point] + parent1[point:]
    return parent1, parent2

def mutate(chromosome):
    for i in range(len(chromosome)):
        if random.random() < MUTATION_RATE:
            chromosome[i] = (random.randint(1, 10), random.choice(AIRCRAFT_CAPACITY), random.randint(0, TIME_SLOTS-1))
    return chromosome

def selection(population):
    fitness_values = [fitness(ch) for ch in population]

    # Ensure there are no zero fitness values
    if sum(fitness_values) == 0:
        fitness_values = [1e-6] * len(fitness_values)

    return random.choices(population, weights=fitness_values, k=2)

def evolve_population(population):
    new_population = []
    for _ in range(POPULATION_SIZE // 2):
        parent1, parent2 = selection(population)
        child1, child2 = crossover(parent1, parent2)
        new_population.append(mutate(child1))
        new_population.append(mutate(child2))
    return new_population

def run_genetic_algorithm():
    population = create_population()
    best_solution = None
    best_fitness = float('-inf')

    for generation in range(NUM_GENERATIONS):
        population = evolve_population(population)
        for chromosome in population:
            fit = fitness(chromosome)
            if fit > best_fitness:
                best_fitness = fit
                best_solution = chromosome
        if generation % 100 == 0:
            print(f'Generation {generation}: Best fitness = {best_fitness:.4f}')

    return best_solution, best_fitness

def minutes_to_time(minutes):
    hours = (minutes // 60) + 6  # Adding 6 hours to start from 6:00 AM
    mins = minutes % 60
    return f"{hours:02}:{mins:02}"
def generate_timetable(best_solution):
    timetable = {i: [] for i in range(NUM_CITIES)}
    aircraft_count = {capacity: 0 for capacity in AIRCRAFT_CAPACITY}
    total_flights = 0
    flight_count_by_type = {capacity: 0 for capacity in AIRCRAFT_CAPACITY}

    for i in range(NUM_CITIES):
        for j in range(NUM_CITIES):
            if i != j:
                flights, aircraft, time_slot = best_solution[i * NUM_CITIES + j]
                for flight_num in range(flights):
                    departure_time = time_slot + flight_num * (TURNAROUND_TIME[aircraft] // 30)
                    arrival_time = departure_time + (1 if DEMAND_MATRIX[i][j] > 400 else 0.5)
                    timetable[i].append((f"Flight {i}-{j}", aircraft, minutes_to_time(departure_time*30), minutes_to_time(arrival_time*30)))
                    aircraft_count[aircraft] += flights
                    flight_count_by_type[aircraft] += flights
                    total_flights += flights

    return timetable, aircraft_count, total_flights, flight_count_by_type

def print_timetable(timetable):
    for city, schedule in timetable.items():
        print(f"City {city} Timetable:")
        for flight in schedule:
            print(f"  {flight[0]}: Aircraft {flight[1]} - Departure: {flight[2]}, Arrival: {flight[3]}")
        print()

def print_aircraft_summary(aircraft_count, flight_count_by_type, total_flights):
    print("Aircraft Summary:")
    for capacity in AIRCRAFT_CAPACITY:
        print(f"  Number of {capacity}-seater aircraft required: {aircraft_count[capacity] // (total_flights // 100)}")  # Example calculation
        print(f"  Total flights with {capacity}-seater aircraft: {flight_count_by_type[capacity]}")
    print(f"Total number of flights: {total_flights}")

def print_efficiency(fitness_value):
    print(f"Efficiency of the solution: {fitness_value:.4f}")

# Run the Genetic Algorithm
best_solution, best_fitness = run_genetic_algorithm()

# Generate and print the timetable
timetable, aircraft_count, total_flights, flight_count_by_type = generate_timetable(best_solution)
print_timetable(timetable)

# Print aircraft summary
print_aircraft_summary(aircraft_count, flight_count_by_type, total_flights)

# Print efficiency
print_efficiency(best_fitness)
