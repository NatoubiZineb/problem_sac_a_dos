

import math
import random

class knapsack:
    
    def __init__(self, *args):
                
        if len(args) == 1:
            with open(args[0], "r") as fp:
                ligne = fp.readline().strip().split(' ')
                self.nb_objects = int(ligne[0])
                self.capacity = int(ligne[1])
                lignes = fp.readlines()
                weights = []
                values = []
                for i in range(self.nb_objects):
                    ligne = lignes[i].strip().split(' ')
                    weights.append(int(ligne[1]))# j'ai fait un changement ici
                    values.append(int(ligne[0]))
                self.weights = weights
                self.values = values
        if len(args) == 4:
            self.capacity = int(args[0])
            self.nb_objects = int(args[1])
            self.weights = args[2]
            self.values = args[3]
    
    def __repr__(self):
        txt = "Number of objects    : "
        txt += str(self.nb_objects)
        txt += "\nCapacity of knapsack : "
        txt += str(self.capacity)
        txt += "\n   Weights \t Values :"
        for i in range(self.nb_objects): 
            txt += "\n\t" + str(self.weights[i]) + "\t\t  " + str(self.values[i])
        return txt        
        
    def is_feasible(self, solution):
        
        b = bin(solution)[2:]
        weight = 0
        N = len(b)
        i = N - 1
        while i >= 0:
            if b[i] == '1':
                weight += self.weights[N - 1 - i]
            i -= 1
        return weight <= self.capacity
    
    def print_solution(self, solution):
        
        b = bin(solution)[2:]
        print(b)
        objects = []
        N = len(b)
        i = N - 1
        while i >= 0:
            if b[i] == '1':
                objects.append(N - i)
            i -= 1
        print("Objets à prendre dans le sac ==>", objects)
        print("Valeur du sac ==>", self.eval_solution(solution))
        
    def eval_solution(self, solution):
                
        b = bin(solution)[2:]
        value = 0
        N = len(b)
        i = N - 1
        while i >= 0:
            if b[i] == '1':
                value += self.values[N - 1 - i]
            i -= 1
        return value

    def brute_force(self):
        
        optimal_value = 0
        optimal_solution = None
        for solution in range(0, 2 ** self.nb_objects):
            if self.is_feasible(solution):
                solution_value = self.eval_solution(solution)
                if solution_value > optimal_value:
                    optimal_value = solution_value
                    optimal_solution = solution
        return optimal_solution, optimal_value
                    
            
    def random_solution(self):
        
        while True:
            solution = random.randint(0, 2 ** self.nb_objects - 1)
            if self.is_feasible(solution):
                return solution        



# les méthodes à implémenter


    def full_random(self):
            best_solution = None
            best_value = 0
            
            for _ in range(1000):
                solution = self.random_solution()
                value = self.eval_solution(solution)
                
                if value > best_value and self.is_feasible(solution):
                    best_solution = solution
                    best_value = value
            
            return best_solution, best_value
    
    def move(self, solution, i):
        b = bin(solution)[2:]
        new_solution = list(b)

        if i == 1:
            j = random.randint(0, len(new_solution) - 1)
            new_solution[j] = '1' if b[j] == '0' else '0'
        elif i == 2:
            positions = random.sample(range(len(new_solution)), 2)
            new_solution[positions[0]], new_solution[positions[1]] = new_solution[positions[1]], new_solution[positions[0]]
        elif i == 3:
            p = random.randint(1, len(new_solution) // 2)  
            q = random.randint(1, len(new_solution) // 2)  
            indices_A = [index for index, bit in enumerate(new_solution) if bit == '1']
            indices_A_prime = [index for index, bit in enumerate(new_solution) if bit == '0']
            for _ in range(p):
                index = random.choice(indices_A)
                new_solution[index] = '0'
            for _ in range(q):
                index = random.choice(indices_A_prime)
                new_solution[index] = '1'
        elif i == 4:
            while True:
                start = random.randint(0, len(new_solution) - 1)
                end = random.randint(start + 1, len(new_solution))
                subsequence = new_solution[start:end]
                if subsequence != subsequence[::-1]:
                    new_solution[start:end] = new_solution[start:end][::-1]
                    break

        return int(''.join(new_solution), 2)

    
    def best_improvement_ls(self):
        current_solution = self.random_solution()
        current_value = self.eval_solution(current_solution)
        CA=False
        while not CA:
            best_solution = current_solution
            best_value = current_value
            
            for _ in range(10):#self.nb_objects
                new_solution = self.move(current_solution, 4)#choix de i 
                new_value = self.eval_solution(new_solution)
                
                if new_value > best_value and self.is_feasible(new_solution):
                    best_solution = new_solution
                    best_value = new_value

            CA=best_solution == current_solution
        current_solution = best_solution
        current_value = best_value
        
        return current_solution, current_value
    
    def first_improvement_ls(self):
        current_solution = self.random_solution()
        current_value = self.eval_solution(current_solution)
        improved = False

        while not improved:
           
            for i in range(100):#self.nb_objects
                new_solution = self.move(current_solution, 4)
                new_value = self.eval_solution(new_solution)
                
                if new_value > current_value and self.is_feasible(new_solution):
                    current_solution = new_solution
                    current_value = new_value
                    improved = True
                    break
        
        return current_solution, current_value
    
    
    
    def homogene_sa(self):
        current_solution = self.random_solution()
        current_value = self.eval_solution(current_solution)
        temperature = 1000
        alpha = 0.90
        
        while temperature > 0.1:

            for _ in range(100):
                new_solution = self.move(current_solution, 4)
                new_value = self.eval_solution(new_solution)
                delta = new_value - current_value
                
                if delta > 0 or random.uniform(0.95, 1) < math.exp(delta / temperature):
                    current_solution = new_solution
                    current_value = new_value
            
            temperature *= alpha
            
        return current_solution, current_value
    
    def no_homogene_sa(self):
        current_solution = self.random_solution()
        current_value = self.eval_solution(current_solution)
        temperature = 1000
        alpha = 0.90
        while temperature > 0.1:

            new_solution = self.move(current_solution, 4)
            new_value = self.eval_solution(new_solution)
            delta = new_value - current_value
                
            if delta > 0 or random.uniform(0.95, 1) < math.exp(delta / temperature):
                current_solution = new_solution
                current_value = new_value
            
            temperature *= alpha
            
        return current_solution, current_value
    


# Main program

# voici comment charger une instance pour le test à partir d'un fichier
instance_1 = knapsack("C:/Users/intel/Downloads/sac à dos/exs.txt")

#pour afficher les données de l'instance
print(instance_1)
print(instance_1.brute_force())
#print(instance_1.best_improvement_ls())
#print(instance_1.first_improvement_ls())
print(instance_1.full_random())
#print(instance_1.homogene_sa())
#print(instance_1.no_homogene_sa())

    

