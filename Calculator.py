#Importation des modules
import tkinter as tk
from math import sin,cos,tan,sqrt,fabs
#Definitions des fonctions 
def action(text_button):
    if text_button == '=':
        try :
            var  = texte_variable.get().replace("√","sqrt").replace("Abs","fabs")
            print(var)
            result = eval(var)
            print(result)
        except :
            result = "Syntax Error"
        finally:
            texte_variable.set(result)
    elif text_button == 'CE':
        texte_variable.set('')
    elif text_button == '2nd':
        frame.config(bg='black')
    elif text_button == 'DEL':
        texte_variable.set(texte_variable.get()[:-1])
    elif text_button == 'ALPHA' or text_button == 'SHIFT':
        pass
    elif text_button == 'sin' or text_button == 'cos' or text_button == 'tan' \
                or text_button == 'ln' or text_button == '√' or text_button == 'Abs' :
        texte_variable.set(texte_variable.get()+text_button+"(")
    else :
        texte_variable.set(texte_variable.get()+text_button)
    
    
#Initialisation de la fenetre
fen = tk.Tk()
fen.title('ALD Calculator')

texte_variable = tk.StringVar()
frame1=tk.Frame(fen,bg='navy')
entry = tk.Entry(frame1,textvariable = texte_variable,width=20,bd=5,justify='right',font = 'Arial 14 bold')

frame = tk.Frame(fen,bg='light yellow')

text_button= ['SHIFT','ALPHA','DEG','MORE','2nd',
              'sin','cos','tan','ln','',
              '!','Abs','√','(',')',
              '7','8','9','CE','DEL',
              '4','5','6','*','/',
              '1','2','3','+','-',
              '0','.','Exp','Ans','=']
buttons =[None for _ in range(len(text_button))]     

frame1.grid(row=0,column=0,columnspan=5)
entry.grid(row=0,column=0,columnspan=5)
tk.Label(fen,text=' \n' ).grid(row=1,column=0,columnspan=5)
frame.grid(row=2,column=0, columnspan=5)
row ,column = 2,0

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

#Mise à jour de la fenetre
fen.mainloop()