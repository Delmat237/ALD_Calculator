#Importation des modules
import tkinter as tk
from math import sin,cos,tan,sqrt,fabs,log,factorial,pi,log10,sinh,cosh,tanh

#Definitions des fonctions 
def index(terme, expression):
    indices = []
    indice = expression.find(terme)

    while indice != -1:
        indices.append(indice)
        indice= expression.find(terme, indice + 1)
 
    return indices


def evaluate(expression : str):
    #Fonction permettant d'evaluer les expresions du champ d'entré
    for car in ['√','sin','cos','tan','ln','Log','sh','ch','facto']:
        if car in expression: #verifie si le car est dans l'expression
            indices,i = index(car,expression),0 #si c'est le cas , on cherche toutes les positions
            for p in indices:
                if expression[p-1]  in ['*','+','-','/','(',')'] or  p == 0:
                    continue
                else :
                    expression = expression[:p+i] +'*' + expression[p+i:]
                    i += 1
    return expression
           
def action(text_button):
    global result,cursor,choix_DEG
    #association des fonctions aux boutons
    if text_button == '=':
        if texte_variable.get() == 'Ans':
            
            texte_variable.set(result)
        else:
            #Gestion des erreurs
            try :
                var = evaluate(texte_variable.get()).replace("√","sqrt").replace("Abs","fabs").replace('ln','log')\
                    .replace('facto','factorial').replace('π','pi').replace('sh','sinh').replace('ch','cosh')\
                    .replace('th','tanh').replace('Log','log10')
                result = eval(var)
                texte_variable.set(result)
                
            except ZeroDivisionError:
                texte_variable.set("Infinity")
            except ValueError:
                texte_variable.set("Value Error")
            except :
                texte_variable.set("Syntax Error")
                       
    elif text_button == 'CE':
        texte_variable.set('')
        
    elif text_button == '-->':
        frame.config(bg='black')
        
    elif text_button == 'DEL':
        if 'Math Error' in texte_variable.get():
            texte_variable.set('')
        else :
            texte_variable.set(texte_variable.get()[:-1])
            
    elif text_button in ['ALPHA','SHIFT','MORE','Exp']:
        pass
    
    elif text_button in [ 'sin', 'cos','tan', 'ln','√' ,'Abs', 'facto','Log']:
        if hyp_value.get(): # Lorsque la touche hyp est activée ou non
            mes = text_button.replace("sin","sh").replace("cos","ch").replace("tan","th")
        else :
            mes = text_button.replace("sh","sin").replace("ch","cos").replace("th","tan")
            
        texte_variable.set(texte_variable.get()+mes+"(")
        
    elif text_button == '<--':
        entry.icursor(len(str(texte_variable))-1)
        
    elif text_button == 'x²':
        texte_variable.set(texte_variable.get()+'²')
        
    elif text_button == '2nd':
        frame.grid_forget()
        frame2.grid(row = 2 ,column = 0,columnspan=5)
        
    elif text_button == '1st':
        frame2.grid_forget()
        frame.grid(row = 2 ,column = 0,columnspan=5)
        
    elif text_button == 'DEG':
        choix = choix_DEG.get()
        choix_DEG.set((choix+1)%3)
        
    elif text_button == 'hyp':
        if hyp_value.get():
            hyp_value.set(0)
            for i,text in [(17,'sin'),(18,'cos'),(19,'tan')]:
                buttons[i].config(text = text)
        else :
            hyp_value.set(1)
            for i,text in [(17,'sh'),(18,'ch'),(19,'th')]:
                buttons[i].config(text = text)
    
   
    else :
        #texte_variable.set(texte_variable.get()+text_button)
        entry.insert(cursor,text_button)
   
    
#Initialisation de la fenetre
fen = tk.Tk()
fen.title('ALD Calculator')

texte_variable = tk.StringVar()
frame1=tk.Frame(fen,bg='navy')
entry = tk.Entry(frame1,textvariable = texte_variable,width=20,bd=5,justify='right',font = 'Arial 14 bold')

frame = tk.Frame(fen,bg='light yellow')

frame2 = tk.Frame(fen,bg='light yellow',width = frame.winfo_width() , height = frame.winfo_height())

# Bouton de la premiere page
text_button= ['SHIFT','ALPHA','DEG','MORE','2nd',
              'π','','<--','-->','',
              'd/dx','%','x²','Log','ln',
              'hyp','°','sin','cos','tan',
              'facto','Abs','√','(',')',
              '7','8','9','CE','DEL',
              '4','5','6','*','/',
              '1','2','3','+','-',
              '0','.','Exp','Ans','=']

#bouton de la deuxieme page contenant le calcul matriciel et l'analyse numerique
text_button2 = ['SHIFT','ALPHA','x','y','1st',
              'Factor','and','or','xor','Not',
              'd/dx','∫','Det','Cross','Tr',
              'r','s','t','u','v',
              '{}','〖[]〗','lim','(',')',
              '7','8','9','False','True',
              '4','5','6','∑','∏',
              '1','2','3','∛','dy/dx',
              '0','.','Exp','Ans','=']

buttons =[None for _ in range(len(text_button))]
buttons2 =[None for _ in range(len(text_button2))]     

frame1.grid(row=0,column=0,columnspan=5)
entry.grid(row=0,column=0,columnspan=5)
tk.Label(fen,text=' \n' ).grid(row=1,column=0,columnspan=5)
frame.grid(row=2,column=0, columnspan=5)
row ,column = 2,0
result = None
cursor = tk.END

#Creation des radiobuttons pour les touches hyp et DEG
choix_DEG = tk.IntVar()
for i,text in enumerate(['D','r','G']):
    DEG_button = tk.Radiobutton(fen,text =text ,value = i , variable  = choix_DEG)      
    DEG_button.grid(row = 1, column =i)
    
hyp_value = tk.IntVar()
hyp_button = tk.Checkbutton(fen,text = 'hyp',variable = hyp_value)
hyp_button.grid(row=1, column= 3)

#creation des boutons
for i,text in enumerate(text_button):
    buttons[i]=tk.Button(frame,text = text, bg = 'dark grey',fg='navy',width=5,bd=1)
    buttons[i]['command'] = lambda m = buttons[i].cget('text') : action(m)
    
    #mise en forme des boutons
    if text == 'SHIFT':
        buttons[i].config(bg='yellow')
        
    elif text == 'ALPHA':
        buttons[i].config(bg='green',fg="white")
        
    elif text == 'DEG':
        buttons[i].config(bg='royal blue',fg="white")
        
    elif text == 'CE' or text == 'DEL':
        buttons[i].config(bg='orange')
        
    elif text in ['*' ,'/' ,'+' ,'-']:
        buttons[i].config(bg='pink',fg="black")
    
                
    buttons[i].grid(row = row,column=column,padx =5,pady =10)
    column += 1
    if not  column % 5:
        row += 1
        column = 0
        
row ,column = 2,0

for i,text in enumerate(text_button2):
    buttons2[i]=tk.Button(frame2,text = text, bg = 'dark grey',fg='navy',width=5,bd=1)
    buttons2[i].grid(row = row,column=column,padx =5,pady =10)
    buttons2[i]['command'] = lambda m = buttons2[i].cget('text') : action(m)
    
    if text == 'SHIFT':
            buttons2[i].config(bg='yellow')
            
    elif text == 'ALPHA':
        buttons2[i].config(bg='green',fg="white")
        
    elif text == 'True'or text == 'False':
        buttons2[i].config(bg='royal blue',fg="white")
        
    elif text == 'CE' or text == 'Not':
        buttons2[i].config(bg='orange')
        
    column += 1
    if not  column % 5:
        row += 1
        column = 0


#Mise à jour de la fenetre
fen.mainloop()