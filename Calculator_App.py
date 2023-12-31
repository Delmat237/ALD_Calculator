#Importation des modules
import tkinter as tk
from math import sin,cos,tan,sqrt,fabs,log,factorial,pi

#Definitions des fonctions 
def action(text_button):
    global result
    #association des fonctions oux boutons
    if text_button == '=':
        if texte_variable.get() == 'Ans':
            texte_variable.set(result)
        else:
            try :
                var  = texte_variable.get().replace("√","sqrt").replace("Abs","fabs").replace('ln','log').replace('facto','factorial').replace('π','pi')
                result = eval(var)
                texte_variable.set(result)
            except :
                texte_variable.set("Math Error")
                       
    elif text_button == 'CE':
        texte_variable.set('')
    elif text_button == '-->':
        frame.config(bg='black')
    elif text_button == 'DEL':
        if texte_variable.get() == 'Math Error':
            texte_variable.set('')
        else :
            texte_variable.set(texte_variable.get()[:-1])
    elif text_button == 'ALPHA' or text_button == 'SHIFT':
        pass
    elif text_button == 'sin' or text_button == 'cos' or text_button == 'tan' \
                or text_button == 'ln' or text_button == '√' or text_button == 'Abs' or text_button == 'facto':
        texte_variable.set(texte_variable.get()+text_button+"(")
    elif text_button == '<--':
        entry.icursor(len(str(texte_variable))-1)
    elif text_button == 'x²':
        texte_variable.set(texte_variable.get()+'²')
    elif text_button == '2nd':
        frame.grid_forget()
        frame2.grid(row = 2 ,column = 0)
    elif text_button == '1st':
        frame2.grid_forget()
        frame.grid(row = 2 ,column = 0)
    else :
        texte_variable.set(texte_variable.get()+text_button)
    
    
#Initialisation de la fenetre
fen = tk.Tk()
fen.title('ALD Calculator')

texte_variable = tk.StringVar()
frame1=tk.Frame(fen,bg='navy')
entry = tk.Entry(frame1,textvariable = texte_variable,width=20,bd=5,justify='right',font = 'Arial 14 bold')

frame = tk.Frame(fen,bg='light yellow')

frame2 = tk.Frame(fen,bg='light yellow',width = 200 , height = 200)

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
              '{}','〖[]〗','lim┬','(',')',
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

#creation des boutons
for i,text in enumerate(text_button):
    buttons[i]=tk.Button(frame,text = text, bg = 'dark grey',fg='navy',width=5,bd=1,command = lambda m = text : action(m))
    if text == 'SHIFT':
        buttons[i].config(bg='yellow')
    elif text == 'ALPHA':
        buttons[i].config(bg='green',fg="white")
    elif text == 'DEG':
        buttons[i].config(bg='royal blue',fg="white")
    elif text == 'CE' or text == 'DEL':
        buttons[i].config(bg='orange')
    elif text == '*' or text == '/' or text == '+' or text == '-':
        buttons[i].config(bg='pink',fg="black")
    buttons[i].grid(row = row,column=column,padx =5,pady =10)
    column += 1
    if not  column % 5:
        row += 1
        column = 0
        
row ,column = 2,0

for i,text in enumerate(text_button2):
    buttons2[i]=tk.Button(frame2,text = text, bg = 'dark grey',fg='navy',width=5,bd=1,command = lambda m = text : action(m))
    buttons2[i].grid(row = row,column=column,padx =5,pady =10)
    if text == 'SHIFT':
            buttons2[i].config(bg='yellow')
    elif text == 'ALPHA':
        buttons2[i].config(bg='green',fg="white")
    elif text == 'True'or text == 'False':
        buttons2[i].config(bg='royal blue',fg="white")
    elif text == 'CE' or text == 'Not':
        buttons2[i].config(bg='orange')
    elif text == '*' or text == '/' or text == '+' or text == '-':
        buttons2[i].config(bg='pink',fg="black")
    column += 1
    if not  column % 5:
        row += 1
        column = 0
        
#Mise à jour de la fenetre
fen.mainloop()