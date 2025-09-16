# Importation des modules
import tkinter as tk
from tkinter import messagebox, simpledialog
import numpy as np
from math import *
import re
from fractions import Fraction
import cmath

class AdvancedCalculator:
    def __init__(self):
        self.fen = tk.Tk()
        self.fen.title('ALD CALCULATRICE Scientifique Avancée')
        self.fen.geometry('600x700')
        self.fen.resizable(True, True)
        
        # Configuration de base des couleurs multiplateformes
        self.colors = {
            'bg_main': '#f0f0f0',
            'bg_button': 'lightgray',
            'bg_entry': 'white',
            'fg_main': 'black',
            'bg_operator': 'lightgreen',
            'bg_function': 'lightcyan',
            'bg_control': 'orange',
            'bg_danger': 'red',
            'bg_result': 'yellow'
        }
        # Variables
        self.texte_variable = tk.StringVar()
        self.result = 0
        self.choix_DEG = tk.IntVar(value=0)  # 0=deg, 1=rad, 2=grad
        self.hyp_value = tk.IntVar(value=0)
        self.memory = {}
        self.ans = 0
        self.history = []
        
        # Interface utilisateur
        self.setup_ui()
        self.setup_bindings()
        
    def setup_ui(self):
        # Zone d'affichage principal
        self.display_frame = tk.Frame(self.fen, bg='white', relief='sunken', bd=2)
        self.display_frame.pack(fill='x', padx=5, pady=5)
        
        # Historique
        self.history_text = tk.Text(self.display_frame, height=3, bg='lightgray', 
                                   font=('Arial', 10), state='disabled')
        self.history_text.pack(fill='x', padx=2, pady=2)
        
        # Champ d'entrée principal
        self.entry = tk.Entry(self.display_frame, textvariable=self.texte_variable, 
                             width=40, bd=3, justify='right', font=('Arial', 16, 'bold'))
        self.entry.pack(fill='x', padx=2, pady=2)
        
        # Frame pour les options
        self.options_frame = tk.Frame(self.fen)
        self.options_frame.pack(fill='x', padx=5, pady=2)
        
        # Options d'angle
        tk.Label(self.options_frame, text='Angle:', font=('Arial', 10, 'bold')).pack(side='left')
        for i, text in enumerate(['DEG', 'RAD', 'GRAD']):
            rb = tk.Radiobutton(self.options_frame, text=text, value=i, 
                               variable=self.choix_DEG, font=('Arial', 9))
            rb.pack(side='left', padx=5)
        
        # Option hyperbolique
        self.hyp_cb = tk.Checkbutton(self.options_frame, text='HYP', 
                                    variable=self.hyp_value, font=('Arial', 9, 'bold'))
        self.hyp_cb.pack(side='left', padx=20)
        
        # Frame principal pour les boutons
        self.main_frame = tk.Frame(self.fen)
        self.main_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Notebook pour différentes pages
        self.create_basic_page()
        self.create_advanced_page()
        self.create_matrix_page()
        
        # Boutons de navigation
        self.nav_frame = tk.Frame(self.main_frame)
        self.nav_frame.pack(fill='x', pady=5)
        
        self.current_page = 'basic'
        self.page_buttons = {}
        
        for page_name, text in [('basic', 'Basique'), ('advanced', 'Avancé'), ('matrix', 'Matrices')]:
            btn = tk.Button(self.nav_frame, text=text, width=12, 
                           command=lambda p=page_name: self.show_page(p))
            btn.pack(side='left', padx=2)
            self.page_buttons[page_name] = btn
        
        self.show_page('basic')
        
    def create_basic_page(self):
        self.basic_frame = tk.Frame(self.main_frame, bg='lightblue')
        
        # Boutons de la ALD CALCULATRICE de base
        basic_buttons = [
            ['C', 'CE', 'DEL', '(', ')'],
            ['x²', '√', 'ln', 'log', 'e^x'],
            ['sin', 'cos', 'tan', 'π', 'e'],
            ['7', '8', '9', '/', 'x!'],
            ['4', '5', '6', '*', '1/x'],
            ['1', '2', '3', '-', 'x^y'],
            ['0', '.', '+/-', '+', '='],
            ['Ans', 'M+', 'MR', 'MC', 'MS']
        ]
        
        for i, row in enumerate(basic_buttons):
            for j, text in enumerate(row):
                btn = tk.Button(self.basic_frame, text=text, width=8, height=2,
                               font=('Arial', 12, 'bold'),
                               command=lambda t=text: self.handle_input(t))
                btn.grid(row=i, column=j, padx=2, pady=2, sticky='nsew')
                
                # Couleurs spéciales avec couleurs multiplateformes
                if text in ['=']:
                    btn.config(bg=self.colors['bg_result'], fg='black')
                elif text in ['+', '-', '*', '/', '(', ')']:
                    btn.config(bg=self.colors['bg_operator'])
                elif text in ['C', 'CE', 'DEL']:
                    btn.config(bg=self.colors['bg_danger'], fg='white')
                elif text in ['sin', 'cos', 'tan', 'ln', 'log', '√', 'x²', 'e^x']:
                    btn.config(bg=self.colors['bg_function'])
        
        # Configuration de la grille
        for i in range(8):
            self.basic_frame.grid_rowconfigure(i, weight=1)
        for j in range(5):
            self.basic_frame.grid_columnconfigure(j, weight=1)
    
    def create_advanced_page(self):
        self.advanced_frame = tk.Frame(self.main_frame, bg='lightyellow')
        
        advanced_buttons = [
            ['asin', 'acos', 'atan', 'sinh', 'cosh'],
            ['tanh', 'asinh', 'acosh', 'atanh', 'γ'],
            ['∫', 'd/dx', 'lim', '∑', '∏'],
            ['⌊x⌋', '⌈x⌉', 'gcd', 'lcm', 'mod'],
            ['nPr', 'nCr', 'rand', 'max', 'min'],
            ['Re', 'Im', 'arg', 'conj', '|z|'],
            ['→rect', '→polar', 'deg→rad', 'rad→deg', 'bin'],
            ['oct', 'hex', 'frac', 'solve', 'plot']
        ]
        
        for i, row in enumerate(advanced_buttons):
            for j, text in enumerate(row):
                btn = tk.Button(self.advanced_frame, text=text, width=8, height=2,
                               font=('Arial', 10, 'bold'),
                               command=lambda t=text: self.handle_advanced_input(t))
                btn.grid(row=i, column=j, padx=2, pady=2, sticky='nsew')
                btn.config(bg=self.colors['bg_function'])
        
        for i in range(8):
            self.advanced_frame.grid_rowconfigure(i, weight=1)
        for j in range(5):
            self.advanced_frame.grid_columnconfigure(j, weight=1)
    
    def create_matrix_page(self):
        self.matrix_frame = tk.Frame(self.main_frame, bg='lightcoral')
        
        matrix_buttons = [
            ['Mat A', 'Mat B', 'Mat C', 'A+B', 'A-B'],
            ['A*B', 'A^T', 'A^-1', 'det(A)', 'rank(A)'],
            ['trace(A)', 'eigen', 'diag', 'zeros', 'ones'],
            ['eye', 'rref', 'solve', 'cross', 'dot'],
            ['norm', 'cond', 'QR', 'SVD', 'LU'],
            ['[', ']', ';', ',', 'size'],
            ['reshape', 'concat', 'split', 'sort', 'sum'],
            ['mean', 'std', 'var', 'min', 'max']
        ]
        
        for i, row in enumerate(matrix_buttons):
            for j, text in enumerate(row):
                btn = tk.Button(self.matrix_frame, text=text, width=8, height=2,
                               font=('Arial', 10, 'bold'),
                               command=lambda t=text: self.handle_matrix_input(t))
                btn.grid(row=i, column=j, padx=2, pady=2, sticky='nsew')
                btn.config(bg=self.colors['bg_function'])
        
        for i in range(8):
            self.matrix_frame.grid_rowconfigure(i, weight=1)
        for j in range(5):
            self.matrix_frame.grid_columnconfigure(j, weight=1)
    
    def show_page(self, page_name):
        # Cacher toutes les pages
        for frame in [self.basic_frame, self.advanced_frame, self.matrix_frame]:
            frame.pack_forget()
        
        # Afficher la page sélectionnée
        if page_name == 'basic':
            self.basic_frame.pack(fill='both', expand=True)
        elif page_name == 'advanced':
            self.advanced_frame.pack(fill='both', expand=True)
        elif page_name == 'matrix':
            self.matrix_frame.pack(fill='both', expand=True)
        
        # Mettre à jour les boutons de navigation
        for btn_name, btn in self.page_buttons.items():
            if btn_name == page_name:
                btn.config(relief='sunken', bg='yellow')
            else:
                btn.config(relief='raised', bg='lightgray')
        
        self.current_page = page_name
    
    def setup_bindings(self):
        # Liaisons clavier
        self.fen.bind('<Return>', lambda e: self.handle_input('='))
        self.fen.bind('<KP_Enter>', lambda e: self.handle_input('='))
        self.fen.bind('<BackSpace>', lambda e: self.handle_input('DEL'))
        self.fen.bind('<Delete>', lambda e: self.handle_input('C'))
        self.fen.bind('<Escape>', lambda e: self.handle_input('CE'))
        
        # Chiffres et opérateurs
        for key in '0123456789+-*/.()':
            self.fen.bind(key, lambda e, k=key: self.handle_input(k))
        
        self.entry.focus_set()
    
    def convert_angle(self, angle):
        """Convertit l'angle selon le mode sélectionné"""
        if self.choix_DEG.get() == 0:  # DEG
            return radians(angle)
        elif self.choix_DEG.get() == 2:  # GRAD
            return radians(angle * 0.9)  # 1 grad = 0.9 deg
        return angle  # RAD
    
    def convert_angle_back(self, angle):
        """Convertit l'angle de radians vers le mode sélectionné"""
        if self.choix_DEG.get() == 0:  # DEG
            return degrees(angle)
        elif self.choix_DEG.get() == 2:  # GRAD
            return degrees(angle) / 0.9
        return angle  # RAD
    
    def preprocess_expression(self, expr):
        """Prétraite l'expression avant évaluation"""
        from math import e as euler_number
        
        expr = str(expr)
        
        # Remplacements de base
        replacements = {
            '×': '*', '÷': '/', '√': 'sqrt', '²': '**2',
            'π': 'pi', 'Ans': str(self.ans),
            'mod': '%'
        }
        
        # Gestion spéciale de 'e' pour éviter les conflits
        expr = expr.replace('e', str(euler_number))
        
        for old, new in replacements.items():
            expr = expr.replace(old, new)
        
        # Gestion des fonctions trigonométriques
        trig_funcs = ['sin', 'cos', 'tan', 'asin', 'acos', 'atan']
        hyp_funcs = ['sinh', 'cosh', 'tanh', 'asinh', 'acosh', 'atanh']
        
        if self.hyp_value.get():  # Mode hyperbolique
            for func in trig_funcs[:3]:  # sin, cos, tan
                expr = expr.replace(func, func + 'h')
        
        # Conversion d'angles pour les fonctions trigonométriques
        for func in trig_funcs[:3]:  # sin, cos, tan seulement
            pattern = f'{func}\\(([^)]+)\\)'
            matches = re.findall(pattern, expr)
            for match in matches:
                try:
                    angle_val = eval(match.replace('pi', str(pi)).replace('e', str(e)))
                    converted = self.convert_angle(float(angle_val))
                    expr = expr.replace(f'{func}({match})', f'{func}({converted})')
                except:
                    pass
        
        # Ajout de multiplications implicites
        expr = re.sub(r'(\d)([a-zA-Z(])', r'\1*\2', expr)
        expr = re.sub(r'([)])(\d)', r'\1*\2', expr)
        expr = re.sub(r'([)])([a-zA-Z(])', r'\1*\2', expr)
        
        return expr
    
    def safe_eval(self, expr):
        """Évaluation sécurisée d'expression"""
        try:
            # Import des constantes mathématiques
            from math import e as euler_number
            
            # Environnement sécurisé avec fonctions mathématiques
            safe_dict = {
                '__builtins__': {},
                'abs': abs, 'round': round, 'min': min, 'max': max,
                'sum': sum, 'pow': pow, 'divmod': divmod,
                'sin': sin, 'cos': cos, 'tan': tan,
                'asin': asin, 'acos': acos, 'atan': atan, 'atan2': atan2,
                'sinh': sinh, 'cosh': cosh, 'tanh': tanh,
                'asinh': asinh, 'acosh': acosh, 'atanh': atanh,
                'exp': exp, 'log': log, 'log10': log10, 'log2': log2,
                'sqrt': sqrt, 'ceil': ceil, 'floor': floor,
                'factorial': factorial, 'gamma': gamma, 'lgamma': lgamma,
                'pi': pi, 'e': euler_number, 'tau': tau, 'inf': inf, 'nan': nan,
                'degrees': degrees, 'radians': radians,
                'gcd': gcd, 'isfinite': isfinite, 'isinf': isinf, 'isnan': isnan,
                'fmod': fmod, 'remainder': remainder, 'fabs': fabs,
                'copysign': copysign, 'frexp': frexp, 'ldexp': ldexp, 'modf': modf,
                'trunc': trunc, 'erf': erf, 'erfc': erfc,
                'hypot': hypot, 'dist': dist,
                # Fonctions complexes
                'complex': complex, 
                'real': lambda x: x.real if isinstance(x, complex) else x,
                'imag': lambda x: x.imag if isinstance(x, complex) else 0,
                'conjugate': lambda x: x.conjugate() if isinstance(x, complex) else x,
                'phase': cmath.phase, 'polar': cmath.polar, 'rect': cmath.rect
            }
            
            processed_expr = self.preprocess_expression(expr)
            result = eval(processed_expr, safe_dict)
            
            return result
            
        except ZeroDivisionError:
            return "Division par zéro"
        except ValueError as error:
            return f"Erreur de valeur: {str(error)}"
        except OverflowError:
            return "Dépassement de capacité"
        except TypeError as error:
            return f"Erreur de type: {str(error)}"
        except Exception as error:
            return f"Erreur de syntaxe: {str(error)}"
    
    def handle_input(self, text):
        """Gestion des entrées de base"""
        current = self.texte_variable.get()
        
        if text == '=':
            if current:
                result = self.safe_eval(current)
                if isinstance(result, (int, float, complex)):
                    self.ans = result
                    self.add_to_history(f"{current} = {result}")
                    self.texte_variable.set(str(result))
                else:
                    self.texte_variable.set(str(result))
        
        elif text == 'C':
            self.texte_variable.set('')
            self.ans = 0
            
        elif text == 'CE':
            self.texte_variable.set('')
            
        elif text == 'DEL':
            self.texte_variable.set(current[:-1])
            
        elif text == '+/-':
            if current and current[0] == '-':
                self.texte_variable.set(current[1:])
            else:
                self.texte_variable.set('-' + current)
                
        elif text == 'Ans':
            self.texte_variable.set(current + str(self.ans))
            
        elif text in ['M+', 'MS', 'MR', 'MC']:
            self.handle_memory(text)
            
        elif text in ['x²', '√', 'ln', 'log', 'e^x', 'x!', '1/x', 'x^y']:
            self.handle_function(text)
            
        elif text in ['sin', 'cos', 'tan', 'π', 'e']:
            if text in ['π', 'e']:
                self.texte_variable.set(current + text)
            else:
                self.texte_variable.set(current + text + '(')
                
        else:
            self.texte_variable.set(current + text)
    
    def handle_function(self, func):
        """Gestion des fonctions mathématiques"""
        current = self.texte_variable.get()
        
        if func == 'x²':
            if current:
                self.texte_variable.set(f'({current})**2')
        elif func == '√':
            self.texte_variable.set(current + 'sqrt(')
        elif func == 'ln':
            self.texte_variable.set(current + 'log(')
        elif func == 'log':
            self.texte_variable.set(current + 'log10(')
        elif func == 'e^x':
            if current:
                self.texte_variable.set(f'exp({current})')
        elif func == 'x!':
            if current:
                self.texte_variable.set(f'factorial({current})')
        elif func == '1/x':
            if current:
                self.texte_variable.set(f'1/({current})')
        elif func == 'x^y':
            self.texte_variable.set(current + '**')
    
    def handle_memory(self, operation):
        """Gestion de la mémoire"""
        current = self.texte_variable.get()
        
        if operation == 'MS':  # Memory Store
            if current:
                result = self.safe_eval(current)
                if isinstance(result, (int, float, complex)):
                    self.memory['main'] = result
                    messagebox.showinfo("Mémoire", f"Valeur {result} stockée en mémoire")
        elif operation == 'M+':  # Memory Add
            if current:
                result = self.safe_eval(current)
                if isinstance(result, (int, float, complex)):
                    self.memory['main'] = self.memory.get('main', 0) + result
                    messagebox.showinfo("Mémoire", f"Valeur ajoutée. Mémoire = {self.memory['main']}")
        elif operation == 'MR':  # Memory Recall
            if 'main' in self.memory:
                self.texte_variable.set(current + str(self.memory['main']))
            else:
                messagebox.showwarning("Mémoire", "Aucune valeur en mémoire")
        elif operation == 'MC':  # Memory Clear
            self.memory.clear()
            messagebox.showinfo("Mémoire", "Mémoire effacée")
    
    def handle_advanced_input(self, text):
        """Gestion des fonctions avancées"""
        current = self.texte_variable.get()
        
        advanced_funcs = {
            'asin': 'asin(', 'acos': 'acos(', 'atan': 'atan(',
            'sinh': 'sinh(', 'cosh': 'cosh(', 'tanh': 'tanh(',
            'asinh': 'asinh(', 'acosh': 'acosh(', 'atanh': 'atanh(',
            '⌊x⌋': 'floor(', '⌈x⌉': 'ceil(',
            'γ': 'gamma(', 'Re': 'real(', 'Im': 'imag(',
            'arg': 'phase(', 'conj': 'conjugate(', '|z|': 'abs('
        }
        
        if text in advanced_funcs:
            self.texte_variable.set(current + advanced_funcs[text])
        elif text == 'gcd':
            self.handle_two_arg_function('gcd')
        elif text == 'lcm':
            self.handle_two_arg_function('lcm')
        elif text == 'nPr':
            self.handle_permutation()
        elif text == 'nCr':
            self.handle_combination()
        elif text == 'rand':
            import random
            self.texte_variable.set(current + str(random.random()))
        elif text in ['deg→rad', 'rad→deg']:
            self.handle_angle_conversion(text)
        elif text == 'frac':
            self.handle_fraction()
        elif text == 'solve':
            self.handle_equation_solver()
        else:
            self.texte_variable.set(current + text)
    
    def handle_two_arg_function(self, func_name):
        """Gestion des fonctions à deux arguments"""
        try:
            args = simpledialog.askstring(f"Fonction {func_name}", 
                                        f"Entrez deux nombres séparés par une virgule:")
            if args:
                a, b = map(float, args.split(','))
                if func_name == 'gcd':
                    result = gcd(int(a), int(b))
                elif func_name == 'lcm':
                    result = abs(int(a) * int(b)) // gcd(int(a), int(b))
                self.texte_variable.set(str(result))
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur dans {func_name}: {str(e)}")
    
    def handle_permutation(self):
        """Gestion des permutations nPr"""
        try:
            args = simpledialog.askstring("Permutation nPr", 
                                        "Entrez n,r séparés par une virgule:")
            if args:
                n, r = map(int, args.split(','))
                result = factorial(n) // factorial(n - r)
                self.texte_variable.set(str(result))
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur dans nPr: {str(e)}")
    
    def handle_combination(self):
        """Gestion des combinaisons nCr"""
        try:
            args = simpledialog.askstring("Combinaison nCr", 
                                        "Entrez n,r séparés par une virgule:")
            if args:
                n, r = map(int, args.split(','))
                result = factorial(n) // (factorial(r) * factorial(n - r))
                self.texte_variable.set(str(result))
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur dans nCr: {str(e)}")
    
    def handle_angle_conversion(self, conversion_type):
        """Gestion de la conversion d'angles"""
        current = self.texte_variable.get()
        if current:
            try:
                value = float(self.safe_eval(current))
                if conversion_type == 'deg→rad':
                    result = radians(value)
                else:  # rad→deg
                    result = degrees(value)
                self.texte_variable.set(str(result))
            except:
                messagebox.showerror("Erreur", "Impossible de convertir la valeur")
    
    def handle_fraction(self):
        """Conversion en fraction"""
        current = self.texte_variable.get()
        if current:
            try:
                value = float(self.safe_eval(current))
                frac = Fraction(value).limit_denominator()
                self.texte_variable.set(str(frac))
            except:
                messagebox.showerror("Erreur", "Impossible de convertir en fraction")
    
    def handle_equation_solver(self):
        """Solveur d'équations simple"""
        equation = simpledialog.askstring("Solveur d'équation", 
                                         "Entrez une équation (ex: x**2 - 4 = 0):")
        if equation:
            try:
                # Implémentation basique pour les équations du second degré
                messagebox.showinfo("Solveur", "Fonctionnalité en développement")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur dans le solveur: {str(e)}")
    
    def handle_matrix_input(self, text):
        """Gestion des opérations matricielles"""
        if text in ['Mat A', 'Mat B', 'Mat C']:
            self.create_matrix(text)
        elif text in ['A+B', 'A-B', 'A*B']:
            self.matrix_operation(text)
        elif text == 'A^T':
            self.matrix_transpose('A')
        elif text == 'A^-1':
            self.matrix_inverse('A')
        elif text == 'det(A)':
            self.matrix_determinant('A')
        elif text == 'eye':
            self.create_identity_matrix()
        elif text == 'zeros':
            self.create_zero_matrix()
        elif text == 'ones':
            self.create_ones_matrix()
        else:
            current = self.texte_variable.get()
            self.texte_variable.set(current + text)
    
    def create_matrix(self, matrix_name):
        """Création d'une matrice"""
        try:
            size = simpledialog.askstring("Taille de la matrice", 
                                        "Entrez les dimensions (lignes,colonnes):")
            if size:
                rows, cols = map(int, size.split(','))
                matrix_str = simpledialog.askstring("Éléments de la matrice", 
                    f"Entrez les éléments de la matrice {matrix_name} séparés par des espaces\n"
                    f"(une ligne par ligne de la matrice):")
                
                if matrix_str:
                    elements = list(map(float, matrix_str.split()))
                    matrix = np.array(elements).reshape(rows, cols)
                    
                    if not hasattr(self, 'matrices'):
                        self.matrices = {}
                    self.matrices[matrix_name[-1]] = matrix  # 'A', 'B', ou 'C'
                    
                    messagebox.showinfo("Matrice créée", 
                                      f"Matrice {matrix_name} créée:\n{matrix}")
                    
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur dans la création de matrice: {str(e)}")
    
    def matrix_operation(self, operation):
        """Opérations entre matrices"""
        try:
            if not hasattr(self, 'matrices') or 'A' not in self.matrices or 'B' not in self.matrices:
                messagebox.showerror("Erreur", "Les matrices A et B doivent être définies")
                return
            
            A, B = self.matrices['A'], self.matrices['B']
            
            if operation == 'A+B':
                result = A + B
            elif operation == 'A-B':
                result = A - B
            elif operation == 'A*B':
                result = A @ B
            
            messagebox.showinfo("Résultat", f"Résultat de {operation}:\n{result}")
            self.matrices['C'] = result
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur dans l'opération matricielle: {str(e)}")
    
    def matrix_transpose(self, matrix_name):
        """Transposée d'une matrice"""
        try:
            if hasattr(self, 'matrices') and matrix_name in self.matrices:
                result = self.matrices[matrix_name].T
                messagebox.showinfo("Transposée", f"Transposée de {matrix_name}:\n{result}")
            else:
                messagebox.showerror("Erreur", f"La matrice {matrix_name} n'existe pas")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur dans la transposition: {str(e)}")
    
    def matrix_inverse(self, matrix_name):
        """Inverse d'une matrice"""
        try:
            if hasattr(self, 'matrices') and matrix_name in self.matrices:
                matrix = self.matrices[matrix_name]
                if matrix.shape[0] != matrix.shape[1]:
                    messagebox.showerror("Erreur", "La matrice doit être carrée pour calculer l'inverse")
                    return
                
                det = np.linalg.det(matrix)
                if abs(det) < 1e-10:
                    messagebox.showerror("Erreur", "La matrice n'est pas inversible (déterminant = 0)")
                    return
                
                result = np.linalg.inv(matrix)
                messagebox.showinfo("Inverse", f"Inverse de {matrix_name}:\n{result}")
                self.matrices[f'{matrix_name}_inv'] = result
            else:
                messagebox.showerror("Erreur", f"La matrice {matrix_name} n'existe pas")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur dans l'inversion: {str(e)}")
    
    def matrix_determinant(self, matrix_name):
        """Déterminant d'une matrice"""
        try:
            if hasattr(self, 'matrices') and matrix_name in self.matrices:
                matrix = self.matrices[matrix_name]
                if matrix.shape[0] != matrix.shape[1]:
                    messagebox.showerror("Erreur", "La matrice doit être carrée pour calculer le déterminant")
                    return
                
                det = np.linalg.det(matrix)
                messagebox.showinfo("Déterminant", f"Déterminant de {matrix_name}: {det}")
                self.texte_variable.set(str(det))
            else:
                messagebox.showerror("Erreur", f"La matrice {matrix_name} n'existe pas")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur dans le calcul du déterminant: {str(e)}")
    
    def create_identity_matrix(self):
        """Création d'une matrice identité"""
        try:
            size = simpledialog.askinteger("Matrice identité", "Entrez la taille de la matrice identité:")
            if size:
                result = np.eye(size)
                messagebox.showinfo("Matrice identité", f"Matrice identité {size}x{size}:\n{result}")
                if not hasattr(self, 'matrices'):
                    self.matrices = {}
                self.matrices['I'] = result
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur dans la création de la matrice identité: {str(e)}")
    
    def create_zero_matrix(self):
        """Création d'une matrice de zéros"""
        try:
            size = simpledialog.askstring("Matrice de zéros", "Entrez les dimensions (lignes,colonnes):")
            if size:
                rows, cols = map(int, size.split(','))
                result = np.zeros((rows, cols))
                messagebox.showinfo("Matrice de zéros", f"Matrice de zéros {rows}x{cols}:\n{result}")
                if not hasattr(self, 'matrices'):
                    self.matrices = {}
                self.matrices['Z'] = result
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur dans la création de la matrice de zéros: {str(e)}")
    
    def create_ones_matrix(self):
        """Création d'une matrice de uns"""
        try:
            size = simpledialog.askstring("Matrice de uns", "Entrez les dimensions (lignes,colonnes):")
            if size:
                rows, cols = map(int, size.split(','))
                result = np.ones((rows, cols))
                messagebox.showinfo("Matrice de uns", f"Matrice de uns {rows}x{cols}:\n{result}")
                if not hasattr(self, 'matrices'):
                    self.matrices = {}
                self.matrices['O'] = result
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur dans la création de la matrice de uns: {str(e)}")
    
    def add_to_history(self, entry):
        """Ajout d'une entrée à l'historique"""
        self.history.append(entry)
        if len(self.history) > 10:  # Limiter l'historique à 10 entrées
            self.history.pop(0)
        
        # Mise à jour de l'affichage de l'historique
        self.history_text.config(state='normal')
        self.history_text.delete('1.0', tk.END)
        for hist_entry in self.history[-3:]:  # Afficher les 3 dernières entrées
            self.history_text.insert(tk.END, hist_entry + '\n')
        self.history_text.config(state='disabled')
        self.history_text.see(tk.END)
    
    def show_help(self):
        """Affichage de l'aide"""
        help_text = """
        ALD CALCULATRICE SCIENTIFIQUE AVANCÉE
        
        FONCTIONS DE BASE:
        • Opérations arithmétiques: +, -, *, /
        • Parenthèses pour priorités
        • Fonctions: sin, cos, tan, ln, log, √, x², e^x
        • Constantes: π, e
        • Mémoire: M+, MS, MR, MC
        
        FONCTIONS AVANCÉES:
        • Fonctions hyperboliques: sinh, cosh, tanh
        • Fonctions inverses: asin, acos, atan, etc.
        • Nombres complexes: Re, Im, arg, conj, |z|
        • Conversions: deg↔rad, fractions
        • Fonctions gamma, factorielles
        
        MATRICES:
        • Création de matrices A, B, C
        • Opérations: +, -, *, transposée, inverse
        • Déterminant, matrices spéciales (identité, zéros, uns)
        
        RACCOURCIS CLAVIER:
        • Entrée: Calculer (=)
        • Retour arrière: Effacer dernier caractère
        • Échap: Effacer tout
        • Delete: Effacer et remettre à zéro
        """
        messagebox.showinfo("Aide", help_text)
    
    def show_constants(self):
        """Affichage des constantes"""
        constants_text = """
        CONSTANTES MATHÉMATIQUES:
        
        π (pi) ≈ 3.14159265359
        e (nombre d'Euler) ≈ 2.71828182846
        τ (tau = 2π) ≈ 6.28318530718
        φ (nombre d'or) ≈ 1.61803398875
        
        CONSTANTES PHYSIQUES:
        c (vitesse de la lumière) = 299792458 m/s
        h (constante de Planck) = 6.626×10⁻³⁴ J·s
        k (constante de Boltzmann) = 1.381×10⁻²³ J/K
        """
        messagebox.showinfo("Constantes", constants_text)
    
    def create_menu(self):
        """Création du menu"""
        menubar = tk.Menu(self.fen)
        self.fen.config(menu=menubar)
        
        # Menu Fichier
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Fichier", menu=file_menu)
        file_menu.add_command(label="Nouveau", command=lambda: self.texte_variable.set(''))
        file_menu.add_command(label="Copier résultat", command=self.copy_result)
        file_menu.add_separator()
        file_menu.add_command(label="Quitter", command=self.fen.quit)
        
        # Menu Affichage
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Affichage", menu=view_menu)
        view_menu.add_command(label="Basique", command=lambda: self.show_page('basic'))
        view_menu.add_command(label="Avancé", command=lambda: self.show_page('advanced'))
        view_menu.add_command(label="Matrices", command=lambda: self.show_page('matrix'))
        
        # Menu Outils
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Outils", menu=tools_menu)
        tools_menu.add_command(label="Convertisseur d'unités", command=self.unit_converter)
        tools_menu.add_command(label="Graphiques", command=self.plot_function)
        tools_menu.add_command(label="Statistiques", command=self.statistics_tool)
        
        # Menu Aide
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Aide", menu=help_menu)
        help_menu.add_command(label="Aide", command=self.show_help)
        help_menu.add_command(label="Constantes", command=self.show_constants)
        help_menu.add_command(label="À propos", command=self.about)
    
    def copy_result(self):
        """Copier le résultat dans le presse-papiers"""
        try:
            self.fen.clipboard_clear()
            self.fen.clipboard_append(self.texte_variable.get())
            messagebox.showinfo("Copié", "Résultat copié dans le presse-papiers")
        except:
            messagebox.showerror("Erreur", "Impossible de copier le résultat")
    
    def unit_converter(self):
        """Convertisseur d'unités simple"""
        converter_window = tk.Toplevel(self.fen)
        converter_window.title("Convertisseur d'unités")
        converter_window.geometry("300x200")
        
        tk.Label(converter_window, text="Convertisseur d'unités", font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Frame pour la conversion
        conv_frame = tk.Frame(converter_window)
        conv_frame.pack(pady=10)
        
        tk.Label(conv_frame, text="Valeur:").grid(row=0, column=0, padx=5)
        value_entry = tk.Entry(conv_frame, width=15)
        value_entry.grid(row=0, column=1, padx=5)
        
        tk.Label(conv_frame, text="De:").grid(row=1, column=0, padx=5)
        from_var = tk.StringVar(value="m")
        from_combo = tk.OptionMenu(conv_frame, from_var, "m", "cm", "mm", "km", "in", "ft")
        from_combo.grid(row=1, column=1, padx=5)
        
        tk.Label(conv_frame, text="Vers:").grid(row=2, column=0, padx=5)
        to_var = tk.StringVar(value="cm")
        to_combo = tk.OptionMenu(conv_frame, to_var, "m", "cm", "mm", "km", "in", "ft")
        to_combo.grid(row=2, column=1, padx=5)
        
        result_label = tk.Label(conv_frame, text="Résultat: ", font=('Arial', 12, 'bold'))
        result_label.grid(row=4, column=0, columnspan=2, pady=10)
        
        def convert():
            try:
                val = float(value_entry.get())
                from_unit = from_var.get()
                to_unit = to_var.get()
                
                # Facteurs de conversion vers mètres
                factors = {
                    'm': 1, 'cm': 0.01, 'mm': 0.001, 'km': 1000,
                    'in': 0.0254, 'ft': 0.3048
                }
                
                # Conversion
                meters = val * factors[from_unit]
                result = meters / factors[to_unit]
                
                result_label.config(text=f"Résultat: {result} {to_unit}")
                
            except Exception as e:
                result_label.config(text=f"Erreur: {str(e)}")
        
        tk.Button(conv_frame, text="Convertir", command=convert, bg='lightblue').grid(row=3, column=0, columnspan=2, pady=5)
    
    def plot_function(self):
        """Tracé de fonctions (basique)"""
        try:
            import matplotlib.pyplot as plt
            import numpy as np
            
            func_str = simpledialog.askstring("Tracé de fonction", 
                                            "Entrez une fonction de x (ex: x**2, sin(x), etc.):")
            if func_str:
                x = np.linspace(-10, 10, 1000)
                
                # Remplacements pour numpy
                func_str = func_str.replace('^', '**')
                
                # Environnement sécurisé avec numpy
                safe_dict = {
                    'x': x, 'sin': np.sin, 'cos': np.cos, 'tan': np.tan,
                    'exp': np.exp, 'log': np.log, 'sqrt': np.sqrt,
                    'pi': np.pi, 'e': np.e, 'abs': np.abs
                }
                
                y = eval(func_str, safe_dict)
                
                plt.figure(figsize=(10, 6))
                plt.plot(x, y, 'b-', linewidth=2)
                plt.grid(True, alpha=0.3)
                plt.xlabel('x')
                plt.ylabel('f(x)')
                plt.title(f'Graphique de f(x) = {func_str}')
                plt.axhline(y=0, color='k', linewidth=0.5)
                plt.axvline(x=0, color='k', linewidth=0.5)
                plt.show()
                
        except ImportError:
            messagebox.showerror("Erreur", "Matplotlib n'est pas installé")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur dans le tracé: {str(e)}")
    
    def statistics_tool(self):
        """Outil de statistiques"""
        stats_window = tk.Toplevel(self.fen)
        stats_window.title("Statistiques")
        stats_window.geometry("400x300")
        
        tk.Label(stats_window, text="Outil de statistiques", font=('Arial', 14, 'bold')).pack(pady=10)
        
        tk.Label(stats_window, text="Entrez les données (séparées par des virgules):").pack()
        data_entry = tk.Entry(stats_window, width=50)
        data_entry.pack(pady=5)
        
        results_text = tk.Text(stats_window, height=10, width=50)
        results_text.pack(pady=10)
        
        def calculate_stats():
            try:
                data_str = data_entry.get()
                data = list(map(float, data_str.split(',')))
                
                # Calculs statistiques
                n = len(data)
                mean_val = sum(data) / n
                median_val = sorted(data)[n//2] if n % 2 == 1 else (sorted(data)[n//2-1] + sorted(data)[n//2]) / 2
                variance = sum((x - mean_val)**2 for x in data) / n
                std_dev = sqrt(variance)
                min_val = min(data)
                max_val = max(data)
                
                # Affichage des résultats
                results = f"""Statistiques pour {n} valeurs:
                
Moyenne: {mean_val:.6f}
Médiane: {median_val:.6f}
Variance: {variance:.6f}
Écart-type: {std_dev:.6f}
Minimum: {min_val}
Maximum: {max_val}
Étendue: {max_val - min_val}
Somme: {sum(data)}
"""
                
                results_text.delete('1.0', tk.END)
                results_text.insert('1.0', results)
                
            except Exception as e:
                results_text.delete('1.0', tk.END)
                results_text.insert('1.0', f"Erreur: {str(e)}")
        
        tk.Button(stats_window, text="Calculer", command=calculate_stats, bg='lightgreen').pack(pady=5)
    
    def about(self):
        """À propos"""
        about_text = """
        ALD CALCULATRICE SCIENTIFIQUE AVANCÉE
        Version 2.0
        
        Fonctionnalités:
        • Calculs mathématiques de base et avancés
        • Fonctions trigonométriques et hyperboliques
        • Calculs matriciels complets
        • Nombres complexes
        • Conversions d'unités
        • Statistiques
        • Tracé de fonctions
        • Historique des calculs
        • Mémoire et constantes
        
        Développé avec Python et Tkinter
        Utilise NumPy pour les calculs matriciels
        """
        messagebox.showinfo("À propos", about_text)
    
    def run(self):
        """Démarrage de l'application"""
        self.create_menu()
        self.fen.mainloop()


# Point d'entrée principal
if __name__ == "__main__":
    try:
        calc = AdvancedCalculator()
        calc.run()
    except ImportError as e:
        print(f"Erreur d'importation: {e}")
        print("Assurez-vous d'avoir installé numpy: pip install numpy")
        print("Pour les graphiques, installez matplotlib: pip install matplotlib")
    except Exception as e:
        print(f"Erreur lors du démarrage: {e}")