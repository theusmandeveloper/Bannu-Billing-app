#=======================imports====================
from tkinter import*
import tkinter as tk
from tkinter import messagebox
import time
import random,os,smtplib,tempfile
from threading import Thread


date=time.strftime('%d/%m/%Y')

#=======================calculator==================

LARGE_FONT_STYLE = ("Arial", 40, "bold")
SMALL_FONT_STYLE = ("Arial", 16)
DIGITS_FONT_STYLE = ("Arial", 24, "bold")
DEFAULT_FONT_STYLE = ("Arial", 20)

OFF_WHITE = "chocolate3"
WHITE = "chocolate"
LIGHT_BLUE = "white"
LIGHT_GRAY = "white"
LABEL_COLOR = "black"


class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("375x630+800+0")
        self.window.resizable(0, 0)
        self.window.title("Calculator")
        self.window.iconbitmap('Images/cal.ico')
        self.window.config(bd=1)

        self.total_expression = ""
        self.current_expression = ""
        self.display_frame = self.create_display_frame()

        self.total_label, self.label = self.create_display_labels()

        self.digits = {
            7: (1, 1), 8: (1, 2), 9: (1, 3),
            4: (2, 1), 5: (2, 2), 6: (2, 3),
            1: (3, 1), 2: (3, 2), 3: (3, 3),
            0: (4, 2), '.': (4, 1)
        }
        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}
        self.buttons_frame = self.create_buttons_frame()
        self.buttons_frame.config(bd=3)

        self.buttons_frame.rowconfigure(0, weight=1)
        for x in range(1, 5):
            self.buttons_frame.rowconfigure(x, weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)
        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()
        self.bind_keys()

    def bind_keys(self):
        self.window.bind("<Return>", lambda event: self.evaluate())
        for key in self.digits:
            self.window.bind(str(key), lambda event, digit=key: self.add_to_expression(digit))

        for key in self.operations:
            self.window.bind(key, lambda event, operator=key: self.append_operator(operator))

    def create_special_buttons(self):
        self.create_clear_button()
        self.create_equals_button()
        self.create_square_button()
        self.create_sqrt_button()

    def create_display_labels(self):
        total_label = tk.Label(self.display_frame, text=self.total_expression, anchor=tk.E, bg=LIGHT_GRAY,
                               fg=LABEL_COLOR, padx=24, font=SMALL_FONT_STYLE)
        total_label.pack(expand=True, fill='both')

        label = tk.Label(self.display_frame, text=self.current_expression, anchor=tk.E, bg=LIGHT_GRAY,
                         fg=LABEL_COLOR, padx=24, font=LARGE_FONT_STYLE)
        label.pack(expand=True, fill='both')

        return total_label, label

    def create_display_frame(self):
        frame = tk.Frame(self.window, height=221, bg=LIGHT_GRAY, bd=1)
        frame.pack(expand=True, fill="both")
        return frame

    def add_to_expression(self, value):
        self.current_expression += str(value)
        self.update_label()

    def create_digit_buttons(self):
        for digit, grid_value in self.digits.items():
            button = tk.Button(self.buttons_frame, text=str(digit), bg=WHITE, fg=LABEL_COLOR, font=DIGITS_FONT_STYLE,
                               borderwidth=0, bd=3, command=lambda x=digit: self.add_to_expression(x))
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)

    def append_operator(self, operator):
        self.current_expression += operator
        self.total_expression += self.current_expression
        self.current_expression = ""
        self.update_total_label()
        self.update_label()

    def create_operator_buttons(self):
        i = 0
        for operator, symbol in self.operations.items():
            button = tk.Button(self.buttons_frame, text=symbol, bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                               borderwidth=0, bd=3, command=lambda x=operator: self.append_operator(x))
            button.grid(row=i, column=4, sticky=tk.NSEW)
            i += 1

    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.update_label()
        self.update_total_label()

    def create_clear_button(self):
        button = tk.Button(self.buttons_frame, text="C", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, bd=3, command=self.clear)
        button.grid(row=0, column=1, sticky=tk.NSEW)

    def square(self):
        self.current_expression = str(eval(f"{self.current_expression}**2"))
        self.update_label()

    def create_square_button(self):
        button = tk.Button(self.buttons_frame, text="x\u00b2", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, bd=3, command=self.square)
        button.grid(row=0, column=2, sticky=tk.NSEW)

    def sqrt(self):
        self.current_expression = str(eval(f"{self.current_expression}**0.5"))
        self.update_label()

    def create_sqrt_button(self):
        button = tk.Button(self.buttons_frame, text="\u221ax", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, bd=3, command=self.sqrt)
        button.grid(row=0, column=3, sticky=tk.NSEW)

    def evaluate(self):
        try:
            self.total_expression += self.current_expression
            self.update_total_label()
            self.current_expression = str(eval(self.total_expression))
            self.total_expression = ""
        except Exception as e:
            self.current_expression = "Error"
        finally:
            self.update_label()

    def create_equals_button(self):
        button = tk.Button(self.buttons_frame, text="=", bg=LIGHT_BLUE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, bd=3, command=self.evaluate)
        button.grid(row=4, column=3, columnspan=2, sticky=tk.NSEW)

    def create_buttons_frame(self):
        frame = tk.Frame(self.window, bd=1)
        frame.pack(expand=True, fill="both")
        return frame

    def update_total_label(self):
        expression = self.total_expression
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f' {symbol} ')
        self.total_label.config(text=expression)

    def update_label(self):
        self.label.config(text=self.current_expression[:11])

    def run(self):
        self.window.mainloop()








#=======================Email_Button==================

def send_email():
    def send_gmail():
        try:
            ob=smtplib.SMTP('smtp.gmail.com',587)
            ob.starttls()
            ob.login(senderEntry.get(),passswordEntry.get())
            message=email_textarea.get(1.0,END)
            reciever_adress=recieverEntry.get()
            ob.sendmail(senderEntry.get(),recieverEntry.get(),message)
            ob.quit()
            messagebox.showinfo('success','Bill sent successfuly',parent=root1)
            root1.destroy()
        except:
            messagebox.showerror('Error','Something went wrong, Please try again.',parent=root1)
    if textarea.get(1.0,END)=='\n':
        messagebox.showerror("Error","Bill is Empty.")
    else:
        root1=Toplevel()
        root1.grab_set()
        root1.title('Send Email')
        root1.config(bg='chocolate3')
        root1.iconbitmap('Images/mail.ico')
        root1.resizable(0,0)
        
        senderframe=LabelFrame(root1,text='SENDER',font=('arial',16,'bold'),bd=6,bg='chocolate3',fg='white')
        senderframe.grid(row=0,column=0,padx=40,pady=20)
        
        senderLabel=Label(senderframe,text="Sender's Email",font=('arial',14,'bold'),bg='chocolate3',fg='white')
        senderLabel.grid(row=0,column=0,padx=10,pady=8)
        
        senderEntry=Entry(senderframe,font=('arial,14,bold'),bd=2,width=23,relief=RIDGE)
        senderEntry.grid(row=0,column=1,padx=10,pady=8)
        
        
        passswordLabel=Label(senderframe,text="Password",font=('arial',14,'bold'),bg='chocolate3',fg='white')
        passswordLabel.grid(row=1,column=0,padx=10,pady=8)
        
        passswordEntry=Entry(senderframe,font=('arial,14,bold'),bd=2,width=23,relief=RIDGE,show='*')
        passswordEntry.grid(row=1,column=1,padx=10,pady=8)


        recieverframe=LabelFrame(root1,text='RECIEVER',font=('arial',16,'bold'),bd=6,bg='chocolate3',fg='white')
        recieverframe.grid(row=1,column=0,padx=40,pady=20)
        
        
        recieverLabel=Label(recieverframe,text="Email Adress",font=('arial',14,'bold'),bg='chocolate3',fg='white')
        recieverLabel.grid(row=0,column=0,padx=10,pady=8)
        
        recieverEntry=Entry(recieverframe,font=('arial,14,bold'),bd=2,width=23,relief=RIDGE)
        recieverEntry.grid(row=0,column=1,padx=10,pady=8)
        
        
        messageLabel=Label(recieverframe,text="Message",font=('arial',14,'bold'),bg='chocolate3',fg='white')
        messageLabel.grid(row=1,column=0,padx=10,pady=8)
        
        email_textarea=Text(recieverframe,font=('arial',14,'bold'),bd=2,relief=SUNKEN,width=42,height=9)
        email_textarea.grid(row=2,column=0,columnspan=2)
        email_textarea.delete(1.0,END)
        email_textarea.insert(END,textarea.get(1.0,END).replace('━','').replace('\t\t\t','\t\t').replace('Software by Muhammad Usman | Tel:) 03277179560',''))
        
        sendbutton=Button(root1,text='SEND',font=('arial',14,'bold'),width=9,command=send_gmail,cursor='hand2')
        sendbutton.grid(row=2,column=0,pady=20)
        
#=======================darkmodebutton==================

def toggle_dark_mode():
    current_color = root.cget("bg")
    new_color = "#212121" if current_color == "white" else "white"
    root.configure(bg=new_color)
    headingLabel.configure(bg='chocolate3' if new_color == "white" else "black", fg='white' if new_color == "white" else 'chocolate3')
    nameLabel.configure(bg='chocolate3' if new_color == "white" else "black", fg='white' if new_color == "white" else 'chocolate3')
    phoneLabel.configure(bg='chocolate3' if new_color == "white" else "black", fg='white' if new_color == "white" else 'chocolate3')
    billnumberLabel.configure(bg='chocolate3' if new_color == "white" else "black", fg='white' if new_color == "white" else 'chocolate3')
    aikpaoLabel.configure(bg='chocolate3' if new_color == "white" else "black", fg='white' if new_color == "white" else 'chocolate3')
    adhakiloLabel.configure(bg='chocolate3' if new_color == "white" else "black", fg='white' if new_color == "white" else 'chocolate3')
    aikkiloLabel.configure(bg='chocolate3' if new_color == "white" else "black", fg='white' if new_color == "white" else 'chocolate3')
    chaplikababLabel.configure(bg='chocolate3' if new_color == "white" else "black", fg='white' if new_color == "white" else 'chocolate3')
    raitaLabel.configure(bg='chocolate3' if new_color == "white" else "black", fg='white' if new_color == "white" else 'chocolate3')
    saladLabel.configure(bg='chocolate3' if new_color == "white" else "black", fg='white' if new_color == "white" else 'chocolate3')
    regularLabel.configure(bg='chocolate3' if new_color == "white" else "black", fg='white' if new_color == "white" else 'chocolate3')
    halflitreLabel.configure(bg='chocolate3' if new_color == "white" else "black", fg='white' if new_color == "white" else 'chocolate3')
    litreLabel.configure(bg='chocolate3' if new_color == "white" else "black", fg='white' if new_color == "white" else 'chocolate3')
    dlitreLabel.configure(bg='chocolate3' if new_color == "white" else "black", fg='white' if new_color == "white" else 'chocolate3')
    halfmineralLabel.configure(bg='chocolate3' if new_color == "white" else "black", fg='white' if new_color == "white" else 'chocolate3')
    fullmineralLabel.configure(bg='chocolate3' if new_color == "white" else "black", fg='white' if new_color == "white" else 'chocolate3')
    kababpricelabel.configure(bg='chocolate3' if new_color == "white" else "black", fg='white' if new_color == "white" else 'chocolate3')
    rspricelabel.configure(bg='chocolate3' if new_color == "white" else "black", fg='white' if new_color == "white" else 'chocolate3')
    drinkspricelabel.configure(bg='chocolate3' if new_color == "white" else "black", fg='white' if new_color == "white" else 'chocolate3')
    
    
    pulaopricelabel.configure(bg='chocolate3' if new_color == "white" else "black", fg='white' if new_color == "white" else 'chocolate3')
    customer_details_frame.configure(bg='chocolate3' if new_color == "white" else "black")
    productFrame.configure(bg='chocolate3' if new_color == "white" else "black")
    pulaoFrame.configure(bg='chocolate3' if new_color == "white" else "black")
    kababFrame.configure(bg='chocolate3' if new_color == "white" else "black")
    raitaSaladFrame.configure(bg='chocolate3' if new_color == "white" else "black")
    drinksframe.configure(bg='chocolate3' if new_color == "white" else "black")
    mineralframe.configure(bg='chocolate3' if new_color == "white" else "black")
    billmenuFrame.configure(bg='chocolate3' if new_color == "white" else "black")
    printButton.configure(bg='chocolate3' if new_color == "white" else "black")
    sendButton.configure(bg='chocolate3' if new_color == "white" else "black")
    totalButton.configure(bg='chocolate3' if new_color == "white" else "black")
    billButton.configure(bg='chocolate3' if new_color == "white" else "black")
    clearButton.configure(bg='chocolate3' if new_color == "white" else "black")
    calculatorButton.configure(bg='chocolate3' if new_color == "white" else "black")
    
    
    darkmode.configure(bg='red4' if new_color == "white" else "white", fg='white' if new_color == "white" else 'black')


#=======================clearbutton==================

def clear():
    nameEntry.delete(0,END)
    phoneEntry.delete(0,END)
    billnumberEntry.delete(0,END)
    aikpaoEntry.delete(0,END)
    adhakiloEntry.delete(0,END)
    aikkiloEntry.delete(0,END)
    chaplikababEntry.delete(0,END)
    raitaEntry.delete(0,END)
    saladEntry.delete(0,END)
    regularEntry.delete(0,END)
    halflitreEntry.delete(0,END)
    litreEntry.delete(0,END)
    dlitreEntry.delete(0,END)
    halfmineralEntry.delete(0,END)
    fullmineralEntry.delete(0,END)
    
    
    
    aikpaoEntry.insert(0,0)
    adhakiloEntry.insert(0,0)
    aikkiloEntry.insert(0,0)
    chaplikababEntry.insert(0,0)
    raitaEntry.insert(0,0)
    saladEntry.insert(0,0)
    regularEntry.insert(0,0)
    halflitreEntry.insert(0,0)
    litreEntry.insert(0,0)
    dlitreEntry.insert(0,0)
    halfmineralEntry.insert(0,0)
    fullmineralEntry.insert(0,0)
    
    textarea.delete(1.0,END)
    pulaopriceEntry.delete(0,END)
    kababpriceEntry.delete(0,END)
    rspriceEntry.delete(0,END)
    drinkspriceEntry.delete(0,END)
    
#=======================printbillbutton==================

def print_bill():
    if textarea.get(1.0, END) == '\n':
        messagebox.showerror("Error", "Bill is Empty.")
    else:
        # Replace '━' character with an empty string
        bill_content = textarea.get(1.0, END).replace('━', '━━')
        
        file = tempfile.mktemp('.txt')
        with open(file, 'w', encoding="utf-8") as f:
            f.write(bill_content)
        os.startfile(file, 'print')
        
#=======================searchbillbutton==================

def search_bill():
    bill_number = billnumberEntry.get()
    if not os.path.exists('bills/'):
        messagebox.showerror('Error', 'Bills directory not found.')
        return
    
    for filename in os.listdir('bills/'):
        if filename.split('.')[0] == bill_number:
            try:
                with open(os.path.join('bills', filename), 'r', encoding='utf-8') as file:
                    textarea.delete(1.0, END)
                    for line in file:
                        textarea.insert(END, line)
            except FileNotFoundError:
                messagebox.showerror('Error', f'Bill file not found: {filename}')
            except Exception as e:
                messagebox.showerror('Error', f'Error occurred while reading bill file: {e}')
            break
    else:
        messagebox.showerror('Error', 'Invalid bill number.')

if not os.path.exists('bills'):
    os.mkdir('bills')


def save_bill():
    global billnumber
    result=messagebox.askyesno("confirm","Do You Want to Save The BIll?")
    if result:
        bill_content=textarea.get(1.0,END)
        file=open(f'bills/{billnumber}.txt','w',encoding="utf-8")
        file.write(bill_content)
        file.close()
        messagebox.showinfo('Success',f'Bill number {billnumber} is saved successfully')
        billnumber=random.randint(500,1000)
billnumber=random.randint(500,1000)

def bill_area(): 
    if aikpaoEntry.get()=='0'and adhakiloEntry.get()=='0'and aikkiloEntry.get()=='0'and chaplikababEntry.get()=='0'and raitaEntry.get()=='0'and saladEntry.get()=='0' and regularEntry.get()=='0' and halflitreEntry.get()=='0' and litreEntry.get()=='0' and dlitreEntry.get()=='0' and halfmineralEntry.get()=='0'and fullmineralEntry.get()=='0':
        messagebox.showinfo('INfo','Please select Items and then hit the total Button')
    elif pulaopriceEntry.get()=='':
        messagebox.showerror('Error,','Please hit the Total button')
    elif nameEntry.get()==''or phoneEntry.get()=='':
        messagebox.showinfo('INfo','Please Provide customer details')
    else:
        textarea.delete(1.0,END) 
        textarea.insert(END,f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")  
        textarea.insert(END,f"\n\t      ❖ 𝙅&𝙆 𝘽𝙖𝙣𝙣𝙪 𝙋𝙪𝙡𝙖𝙤 ❖   \t\t{date}\n")
        textarea.insert(END,f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━") 
        textarea.insert(END,f'\n Bill Number:\t{billnumber}\n')
        textarea.insert(END,f'\n Customer Name:\t{nameEntry.get()}\n')
        textarea.insert(END,f'\n Phone Number:\t{phoneEntry.get()}\n')
        textarea.insert(END,f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
        textarea.insert(END,f"    𝙄𝙩𝙚𝙢𝙨\t\t\t𝙌𝙮𝙩\t\t𝙋𝙧𝙞𝙘𝙚\n")
        textarea.insert(END,f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
        
        textarea.insert(END,f"    𝙋𝙪𝙡𝙖𝙤\n\n")
        textarea.insert(END,f"   Aik pao\t\t\t{aikpaoEntry.get()}\t\t{_aikpaoprice_}RS\n")
        textarea.insert(END,f"   Aadha Kilo\t\t\t{adhakiloEntry.get()}\t\t{_adhakiloprice_}RS\n")
        textarea.insert(END,f"   Aik kilo\t\t\t{aikkiloEntry.get()}\t\t{_aikkiloprice_}RS\n")
        textarea.insert(END,f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
        textarea.insert(END,f"    𝘾𝙝𝙖𝙥𝙡𝙞 𝙆𝙖𝙗𝙖𝙗\t\t\t{chaplikababEntry.get()}\t\t{_chaplikababprice_}RS\n\n")
        textarea.insert(END,f"    𝙍𝙖𝙞𝙩𝙖\t\t\t{raitaEntry.get()}\t\t{_raitaaprice_}RS\n\n")
        textarea.insert(END,f"    𝙎𝙖𝙡𝙖𝙙\t\t\t{saladEntry.get()}\t\t{_saladprice_}RS\n\n")
        textarea.insert(END,f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
        textarea.insert(END,f"    𝘾𝙤𝙡𝙙 𝘿𝙧𝙞𝙣𝙠𝙨\n\n")
        textarea.insert(END,f"   Regular\t\t\t{regularEntry.get()}\t\t{_regulardrinkprice_}RS\n")
        textarea.insert(END,f"   Half Litre\t\t\t{halflitreEntry.get()}\t\t{_halflitreprice_}RS\n")
        textarea.insert(END,f"   Litre\t\t\t{litreEntry.get()}\t\t{_litreprice_}RS\n")
        textarea.insert(END,f"   1.5 Litre\t\t\t{dlitreEntry.get()}\t\t{_dlitreprice_}RS\n")
        textarea.insert(END,f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
        textarea.insert(END,f"    𝙈𝙞𝙣𝙚𝙧𝙖𝙡 𝙒𝙖𝙩𝙚𝙧\n\n")
        textarea.insert(END,f"   500ml\t\t\t{halfmineralEntry.get()}\t\t{_mineral500mlprice_}RS\n")
        textarea.insert(END,f"   1000ml\t\t\t{fullmineralEntry.get()}\t\t{_mineral1000mlprice_}RS\n")
        textarea.insert(END,f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
        textarea.insert(END,f"    𝙏𝙤𝙩𝙖𝙡\t\t\t{total} RS\n")
        textarea.insert(END,f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n")
        textarea.insert(END,f"  Software by Muhammad Usman | Tel:) 03277179560\n")
        
        save_bill()

#=======================totalbutton==================


def total():
    global total,_adhakiloprice_,_aikkiloprice_,_chaplikababprice_,_raitaaprice_,_saladprice_,_regulardrinkprice_,_halflitreprice_,_litreprice_,_dlitreprice_,_mineral500mlprice_,_mineral1000mlprice_
    global _aikpaoprice_
    aikpaoprice=180
    adhakiloprice=360
    aikkiloprice=720
    chaplikababprice=130
    raitaprice=40
    saladprice=40
    regulardrinkprice=60
    halflitredrinkprice=100
    litredrinkprice=150
    dlitredrinkprice=200
    min500mlprice=60
    min1000mlprice=100
    
    if aikpaoEntry.get()=='' or aikpaoEntry.get()==str:
        _aikpaoprice_=0  
    else:
        try:
            _aikpaoprice_=int(aikpaoEntry.get())*aikpaoprice    
        except ValueError:
            messagebox.showerror("Error",'Please Enter a digit to product entry')
    if adhakiloEntry.get()=='':
        _adhakiloprice_=0
    else:
        try:
            _adhakiloprice_=int(adhakiloEntry.get())*adhakiloprice
        except ValueError:
            messagebox.showerror("Error",'Please Enter a digit to product entry')
    if aikkiloEntry.get()=='':
        _aikkiloprice_=0
    else:
        try:
            _aikkiloprice_=int(aikkiloEntry.get())*aikkiloprice
        except ValueError:
            messagebox.showerror("Error",'Please Enter a digit to product entry')
    
    
    _totalpulaoprice_=_aikpaoprice_+_adhakiloprice_+_aikkiloprice_
    
    
    pulaopriceEntry.delete(0,END)
    pulaopriceEntry.insert(0,str(_totalpulaoprice_)+" RS")
    
    if chaplikababEntry.get()=='':
        _chaplikababprice_=0
    else:
        try:
            _chaplikababprice_=int(chaplikababEntry.get())*chaplikababprice
        except ValueError:
            messagebox.showerror("Error",'Please Enter a digit to product entry')
    
    kababpriceEntry.delete(0,END)
    kababpriceEntry.insert(0,str(_chaplikababprice_)+" RS")
    
    
    if raitaEntry.get()=='':
        _raitaaprice_=0
    else:
        try:
            _raitaaprice_=int(raitaEntry.get())*raitaprice
        except ValueError:
            messagebox.showerror("Error",'Please Enter a digit to product entry')
        
    if saladEntry.get()=='':
        _saladprice_=0
    else:
        try:
            _saladprice_=int(saladEntry.get())*saladprice
        except ValueError:
            messagebox.showerror("Error",'Please Enter a digit to product entry')
    
    _totalRandSprice_=_raitaaprice_+_saladprice_
    
    rspriceEntry.delete(0,END)
    rspriceEntry.insert(0,str(_totalRandSprice_)+" RS")
    
    if regularEntry.get()=='':
        _regulardrinkprice_=0
    else:
        try:
            _regulardrinkprice_=int(regularEntry.get())*regulardrinkprice
        except ValueError:
            messagebox.showerror("Error",'Please Enter a digit to product entry')
    if halflitreEntry.get()=='':
        _halflitreprice_=0
    else:
        try:
            _halflitreprice_=int(halflitreEntry.get())*halflitredrinkprice
        except ValueError:
            messagebox.showerror("Error",'Please Enter a digit to product entry')
    if litreEntry.get()=='':
        _litreprice_=0 
    else:
        try:
            _litreprice_=int(litreEntry.get())*litredrinkprice
        except ValueError:
            messagebox.showerror("Error",'Please Enter a digit to product entry')
    if dlitreEntry.get()=='':
        _dlitreprice_=0
    else:
        try:
            _dlitreprice_=int(dlitreEntry.get())*dlitredrinkprice
        except ValueError:
            messagebox.showerror("Error",'Please Enter a digit to product entry')
    if halfmineralEntry.get()=='':
        _mineral500mlprice_=0
    else:
        try:
            _mineral500mlprice_=int(halfmineralEntry.get())*min500mlprice
        except ValueError:
            messagebox.showerror("Error",'Please Enter a digit to product entry')
    if fullmineralEntry.get()=='':
        _mineral1000mlprice_=0
    else:
        try:
            _mineral1000mlprice_=int(fullmineralEntry.get())*min1000mlprice
        except ValueError:
            messagebox.showerror("Error",'Please Enter a digit to product entry')
    _totaldrinkprice_=_regulardrinkprice_+_litreprice_+_halflitreprice_+_dlitreprice_+_mineral500mlprice_+_mineral1000mlprice_
    
    
    drinkspriceEntry.delete(0,END)
    drinkspriceEntry.insert(0,str(_totaldrinkprice_)+" RS")
    
    
    

    total=_totalpulaoprice_+_chaplikababprice_+_totalRandSprice_+_totaldrinkprice_
    







root=Tk()
root.title("J&K Bannu Pulao")
root.geometry('1270x685')
root.iconbitmap('Images/main.ico')

#Heading

headingLabel=Label(root,text='J&K Bannu Pulao',font=('times new roman',25,'bold'),bg='chocolate3',fg='white',relief=GROOVE,bd=10)
headingLabel.pack(fill=X)

#customerDetailsFrame

customer_details_frame=LabelFrame(root,text='Customer Details',font=('times new roman',12,"bold"),fg="gold",bd=6,relief=GROOVE,bg='chocolate3')
customer_details_frame.pack(fill=X)

#namelabel&entry

nameLabel=Label(customer_details_frame,text='Customer Name',font=('times new roman',12,"bold"),bg="chocolate3",fg='white')
nameLabel.grid(row=0,column=0,padx=20)
nameEntry=Entry(customer_details_frame,font=('arial',15),bd=7,width=18)
nameEntry.grid(row=0,column=1,padx=8)

#phoneEntry&Label

phoneLabel=Label(customer_details_frame,text='Phone Number',font=('times new roman',12,"bold"),bg="chocolate3",fg='white')
phoneLabel.grid(row=0,column=2,padx=20,pady=2)
phoneEntry=Entry(customer_details_frame,font=('arial',15),bd=7,width=18)
phoneEntry.grid(row=0,column=3,padx=8)

#billlabel&Entry

billnumberLabel=Label(customer_details_frame,text='Bill Number',font=('times new roman',12,"bold"),bg="chocolate3",fg='white')
billnumberLabel.grid(row=0,column=4,padx=20,pady=2)
billnumberEntry=Entry(customer_details_frame,font=('arial',15),bd=7,width=18)
billnumberEntry.grid(row=0,column=5,padx=8)

#searchButton

searchButton=Button(customer_details_frame,text='SEARCH',font=('arial',12,'bold'),bd=7,cursor='hand2',command=search_bill)
searchButton.grid(row=0,column=6,padx=25,pady=6)


productFrame=Frame(root)
productFrame.pack()


pulaoFrame=LabelFrame(productFrame,text='Pulao',font=('times new roman',15,"bold"),fg="gold",bd=5,relief=GROOVE,bg='chocolate3')
pulaoFrame.grid(row=0,column=0)

aikpaoLabel=Label(pulaoFrame,text='    Aik Pao pulao',font=('times new roman',15,"bold"),bg="chocolate3",fg='white')
aikpaoLabel.grid(row=0,column=0,pady=10,padx=8,sticky='w')
aikpaoEntry=Entry(pulaoFrame,font=('times new roman',15,"bold"),width=10,bd=5)
aikpaoEntry.grid(row=0,column=1,pady=10,padx=8)
aikpaoEntry.insert(0,0)

adhakiloLabel=Label(pulaoFrame,text='    Aadha kilo pulao',font=('times new roman',15,"bold"),bg="chocolate3",fg='white')
adhakiloLabel.grid(row=1,column=0,pady=10,padx=8,sticky='w')
adhakiloEntry=Entry(pulaoFrame,font=('times new roman',15,"bold"),width=10,bd=5)
adhakiloEntry.grid(row=1,column=1,padx=8,pady=10)
adhakiloEntry.insert(0,0)


aikkiloLabel=Label(pulaoFrame,text='    Aik Kilo pulao',font=('times new roman',15,"bold"),bg="chocolate3",fg='white')
aikkiloLabel.grid(row=2,column=0,padx=8,pady=10,sticky='w')
aikkiloEntry=Entry(pulaoFrame,font=('times new roman',15,"bold"),width=10,bd=5)
aikkiloEntry.grid(row=2,column=1,padx=8,pady=10)
aikkiloEntry.insert(0,0)


kababFrame=LabelFrame(pulaoFrame,text='Kabab',font=('times new roman',15,"bold"),fg="gold",bd=5,relief=GROOVE,bg='chocolate3')
kababFrame.grid(row=3,column=0)




chaplikababLabel=Label(kababFrame,text=' Chapli Kabab',font=('times new roman',15,"bold"),bg="chocolate3",fg='white')
chaplikababLabel.grid(row=0,column=0,pady=10,padx=8,sticky='w')
chaplikababEntry=Entry(kababFrame,font=('times new roman',15,"bold"),width=10,bd=5)
chaplikababEntry.grid(row=0,column=1,padx=15,pady=10)
chaplikababEntry.insert(0,0)



raitaSaladFrame=LabelFrame(pulaoFrame,text='Raita&Salad',font=('times new roman',15,"bold"),fg="gold",bd=5,relief=GROOVE,bg='chocolate3')
raitaSaladFrame.grid(row=4,column=0)




raitaLabel=Label(raitaSaladFrame,text='    Raita',font=('times new roman',15,"bold"),bg="chocolate3",fg='white')
raitaLabel.grid(row=0,column=0,pady=10,padx=10,sticky='w')
raitaEntry=Entry(raitaSaladFrame,font=('times new roman',15,"bold"),width=10,bd=5)
raitaEntry.grid(row=0,column=1,pady=10,padx=40)
raitaEntry.insert(0,0)

saladLabel=Label(raitaSaladFrame,text='    Salad',font=('times new roman',15,"bold"),bg="chocolate3",fg='white')
saladLabel.grid(row=1,column=0,pady=10,padx=10,sticky='w')
saladEntry=Entry(raitaSaladFrame,font=('times new roman',15,"bold"),width=10,bd=5)
saladEntry.grid(row=1,column=1,pady=10,padx=40,)
saladEntry.insert(0,0)



drinksframe=LabelFrame(productFrame,text='Cold Drinks',font=('times new roman',15,"bold"),fg="gold",bd=5,relief=GROOVE,bg='chocolate3')
drinksframe.grid(row=0,column=1)




regularLabel=Label(drinksframe,text='    Regular',font=('times new roman',15,"bold"),bg="chocolate3",fg='white')
regularLabel.grid(row=0,column=0,pady=10,padx=5,sticky='w')
regularEntry=Entry(drinksframe,font=('times new roman',15,"bold"),width=10,bd=5)
regularEntry.grid(row=0,column=1,pady=10,padx=8)
regularEntry.insert(0,0)
                


halflitreLabel=Label(drinksframe,text='    Half Litre',font=('times new roman',15,"bold"),bg="chocolate3",fg='white')
halflitreLabel.grid(row=1,column=0,pady=10,padx=5,sticky='w')
halflitreEntry=Entry(drinksframe,font=('times new roman',15,"bold"),width=10,bd=5)
halflitreEntry.grid(row=1,column=1,pady=10,padx=8)
halflitreEntry.insert(0,0)


litreLabel=Label(drinksframe,text='    Litre',font=('times new roman',15,"bold"),bg="chocolate3",fg='white')
litreLabel.grid(row=2,column=0,pady=10,padx=5,sticky='w')
litreEntry=Entry(drinksframe,font=('times new roman',15,"bold"),width=10,bd=5)
litreEntry.grid(row=2,column=1,pady=10,padx=8)
litreEntry.insert(0,0)



dlitreLabel=Label(drinksframe,text='    1.5 Litre',font=('times new roman',15,"bold"),bg="chocolate3",fg='white')
dlitreLabel.grid(row=3,column=0,pady=10,padx=5,sticky='w')
dlitreEntry=Entry(drinksframe,font=('times new roman',15,"bold"),width=10,bd=5)
dlitreEntry.grid(row=3,column=1,pady=10,padx=8)
dlitreEntry.insert(0,0)



mineralframe=LabelFrame(drinksframe,text='Mineral Water',font=('times new roman',15,"bold"),fg="gold",bd=5,relief=GROOVE,bg='chocolate3')
mineralframe.grid(row=4,column=0,pady=15)

halfmineralLabel=Label(mineralframe,text='    500ml',font=('times new roman',15,"bold"),bg="chocolate3",fg='white')
halfmineralLabel.grid(row=0,column=0,pady=10,padx=5,sticky='w')
halfmineralEntry=Entry(mineralframe,font=('times new roman',15,"bold"),width=10,bd=5)
halfmineralEntry.grid(row=0,column=1,pady=10,padx=8)
halfmineralEntry.insert(0,0)

fullmineralLabel=Label(mineralframe,text='    1000ml',font=('times new roman',15,"bold"),bg="chocolate3",fg='white')
fullmineralLabel.grid(row=1,column=0,pady=10,padx=5,sticky='w')
fullmineralEntry=Entry(mineralframe,font=('times new roman',15,"bold"),width=10,bd=5)
fullmineralEntry.grid(row=1,column=1,pady=10,padx=20)
fullmineralEntry.insert(0,0)


billframe=Frame(productFrame,bd=8,relief=GROOVE)
billframe.grid(row=0,column=2,padx=5)
billareaLabel=Label(billframe,text='Bill Area',font=('times new roman',15,'bold'),bd=7,relief=GROOVE)
billareaLabel.pack()

scrollbar=Scrollbar(billframe,orient=VERTICAL)
scrollbar.pack(side=RIGHT,fill=Y)

textarea=Text(billframe,height=22,width=50,yscrollcommand=scrollbar.set)
scrollbar.config(command=textarea.yview)
textarea.pack()


billmenuFrame=LabelFrame(root,text='Total Prices',font=('times new roman',15,"bold"),fg="gold",bd=8,relief=GROOVE,bg='chocolate3')
billmenuFrame.pack(fill=X)



pulaopricelabel=Label(billmenuFrame,text='Pulao ',font=('times new roman',15,"bold"),bg="chocolate3",fg='white')
pulaopricelabel.grid(row=0,column=0,pady=4,padx=10,sticky='w')
pulaopriceEntry=Entry(billmenuFrame,font=('times new roman',12,"bold"),width=9,bd=5)
pulaopriceEntry.grid(row=0,column=1)


kababpricelabel=Label(billmenuFrame,text='Kabab ',font=('times new roman',15,"bold"),bg="chocolate3",fg='white')
kababpricelabel.grid(row=0,column=2,pady=4,padx=10,sticky='w')
kababpriceEntry=Entry(billmenuFrame,font=('times new roman',12,"bold"),width=9,bd=5)
kababpriceEntry.grid(row=0,column=3)



rspricelabel=Label(billmenuFrame,text='Raita&\nSalad ',font=('times new roman',15,"bold"),bg="chocolate3",fg='white')
rspricelabel.grid(row=0,column=4,pady=4,padx=10,sticky='w')
rspriceEntry=Entry(billmenuFrame,font=('times new roman',12,"bold"),width=9,bd=5)
rspriceEntry.grid(row=0,column=5)


drinkspricelabel=Label(billmenuFrame,text='Cold drinks&\nmineral ',font=('times new roman',15,"bold"),bg="chocolate3",fg='white')
drinkspricelabel.grid(row=0,column=6,pady=4,padx=10,sticky='w')
drinkspriceEntry=Entry(billmenuFrame,font=('times new roman',12,"bold"),width=9,bd=5)
drinkspriceEntry.grid(row=0,column=7)



buttonFrame=Frame(billmenuFrame,bd=5,relief=GROOVE)
buttonFrame.grid(row=0,column=8,padx=10,pady=5)



totalButton=Button(buttonFrame,text='Total',font=('arial',10,'bold'),bg='chocolate3',fg='white',bd=5,width=5,cursor='hand2',command=total)
totalButton.grid(row=0,column=9,padx=5)


billButton=Button(buttonFrame,text='Bill',font=('arial',10,'bold'),bg='chocolate3',fg='white',bd=5,width=5,cursor='hand2',command=bill_area)
billButton.grid(row=0,column=10,padx=5)


printButton=Button(buttonFrame,text='Print',font=('arial',10,'bold'),bg='chocolate3',fg='white',bd=5,width=5,cursor='hand2',command=print_bill)
printButton.grid(row=0,column=11,padx=5)


sendButton=Button(buttonFrame,text='Send',font=('arial',10,'bold'),bg='chocolate3',fg='white',bd=5,width=5,cursor='hand2',command=send_email)
sendButton.grid(row=0,column=12,padx=4)


clearButton=Button(buttonFrame,text='Clear',font=('arial',10,'bold'),bg='chocolate3',fg='white',bd=5,width=5,cursor='hand2',command=clear)
clearButton.grid(row=0,column=13,padx=4)


darkmode=Button(buttonFrame,text='Dark Mode',font=('arial',10,'bold'),bg='chocolate3',fg='white',bd=5,width=8,cursor='hand2',command=toggle_dark_mode)
darkmode.grid(row=0,column=14,padx=4)


calculatorButton=Button(buttonFrame,text='Calculator',font=('arial',13,'bold'),bg='chocolate3',fg='white',bd=5,width=8,cursor='hand2',command=Calculator)
calculatorButton.grid(row=0,column=15,padx=4)



























root.mainloop()
