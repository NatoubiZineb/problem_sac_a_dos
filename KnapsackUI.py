import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from knapsack import knapsack

class KnapsackUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Problème de sac à dos")

        file_frame = tk.Frame(self.window)
        file_frame.pack(pady=10)

        file_label = tk.Label(file_frame, text="Selectionner un fichier:")
        file_label.pack(side=tk.LEFT)

        self.file_path = tk.StringVar()
        self.file_entry = tk.Entry(file_frame, textvariable=self.file_path, width=60)
        self.file_entry.pack(side=tk.LEFT)

        file_button = tk.Button(file_frame, text="importer", command=self.browse_file)
        file_button.pack(side=tk.LEFT)

        
        method_frame = tk.LabelFrame(self.window, text="Select Methods")
        method_frame.pack(pady=10)

        self.method_vars = {
            "Brute Force": tk.IntVar(),
            "Best Improvement LS": tk.IntVar(),
            "First Improvement LS": tk.IntVar(),
            "Full Random": tk.IntVar(),
            "Homogene SA": tk.IntVar(),
            "No Homogene SA": tk.IntVar()
        }

        for method, var in self.method_vars.items():
            checkbox = tk.Checkbutton(method_frame, text=method, variable=var)
            checkbox.pack(anchor=tk.W)

        
        solve_button = tk.Button(self.window, text="Exécuter", command=self.solve_problem)
        solve_button.pack(pady=10)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        self.file_path.set(file_path)

    def solve_problem(self):
        file_path = self.file_path.get()

        if not file_path:
            messagebox.showerror("Error", "selectioner un fichier!!")
            return

        methods = []
        for method, var in self.method_vars.items():
            if var.get():
                methods.append(method)

        if not methods:
            messagebox.showerror("Error", "selectioner au moin une methode.")
            return

        try:
            problem = knapsack(file_path)
            result = ""

            for method in methods:
                if method == "Brute Force":
                    solution, value = problem.brute_force()
                elif method == "Best Improvement LS":
                    solution, value = problem.best_improvement_ls()
                elif method == "First Improvement LS":
                    solution, value = problem.first_improvement_ls()
                elif method == "Full Random":
                    solution, value = problem.full_random()
                elif method == "Homogene SA":
                    solution, value = problem.homogene_sa()
                elif method == "No Homogene SA":
                    solution, value = problem.no_homogene_sa()

                result += f"Méthode: {method}\n"
                result += f"Solution: {bin(solution)[2:]}\n"
                result += f"Valeur: {value}\n\n"

            with open(file_path, "a") as file:
                file.write(result)

            messagebox.showinfo("Résolu!!!", "Problème résolu, résultats dans le fichier :)")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def run(self):
        self.window.mainloop()

# Run l'application
app = KnapsackUI()
app.run()
