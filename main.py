import customtkinter as ctk
import json, os
import cypher

########################################
############## FUNCTIONS ###############
########################################

def add_account(net, user, email, pwd, keyName, tkey):
    user = cypher.cifrar('RSA', keyName, user)
    email = cypher.cifrar('RSA', keyName, email)
    pwd = cypher.cifrar('RSA', keyName, pwd)

    fu = open(f'data/users/{net}.bin', 'wb')
    fu.write(user) 
    fu.close()
    
    fp = open(f'data/passwords/{net}.bin', 'wb')
    fp.write(pwd)
    fp.close()

    fe = open(f'data/emails/{net}.bin', 'wb')
    fe.write(email)
    fe.close()

add_account('google', 'ramon', 'ram@gmail.com', 'aña123', 'google', '090')
########################################
################ FRAMES ################
########################################

def add_key_frm():
    Frame = ctk.CTk()
    Frame.title("Añadir Clave | PwD_MaN")
    Frame.geometry("380x380")

    ktype = ctk.CTkLabel(Frame, text="Tipo de Clave: RSA", width=220, bg_color='gray20', text_color='white')
    ktype.grid(row=0, column=0, padx=5, pady=5, columnspan=2)
    name = ctk.CTkEntry(Frame, placeholder_text="Nombre de la clave", width=100)
    name.grid(row=1, column=0, padx=5, pady=5)
    length = ctk.CTkOptionMenu(Frame, values=["1024", "2048", "4096", "8192", "16384"], width=100)
    length.grid(row=1, column=1, padx=5, pady=5)
    create = ctk.CTkButton(Frame, text="Crear Clave", command=lambda:(cypher.create_key('RSA', int(length.get()), name.get())), width=100)
    create.grid(row=2, column=0, padx=5, pady=5, columnspan=2)
    
    Frame.mainloop()

def add_account_frm():
    keysList = [i.split('.')[0] for i in os.listdir('data/keys')]
    keysList = list(set(keysList))

    Frame = ctk.CTk()
    Frame.title("Añadir Cuenta | PwD_MaN")
    Frame.geometry("600x600")

    social_net = ctk.CTkEntry(Frame, placeholder_text="Red Social", width=150)
    social_net.grid(row=0, column=0, padx=5, pady=5)
    user_net = ctk.CTkEntry(Frame, placeholder_text="Usuario", width=150)
    user_net.grid(row=0, column=1, padx=5, pady=5)
    email_net = ctk.CTkEntry(Frame, placeholder_text="Correo Electronico", width=150)
    email_net.grid(row=1, column=0, padx=5, pady=5)
    password_net = ctk.CTkEntry(Frame, placeholder_text="Contraseña", width=150)
    password_net.grid(row=1, column=1, padx=5, pady=5)
    key_sel = ctk.CTkOptionMenu(Frame, values=[i for i in keysList], width=150)
    key_sel.grid(row=2, column=0, padx=5, pady=5)
    add_net = ctk.CTkButton(Frame, text="Añadir Cuenta", command=lambda:(add_account(social_net.get(), user_net.get(), email_net.get(), 
            password_net.get(), key_sel.get(), cypher.gen_key())), width=150)
    add_net.grid(row=2, column=1, padx=5, pady=5)

    Frame.mainloop()


def get_account_frm():
    Frame = ctk.CTk()
    Frame.title("Mostrar Cuenta | PwD_MaN")
    Frame.geometry("600x600")
    fe = open(f'data/users/google.bin', 'rb')
    dato = fe.read()
    fe.close()
    data = cypher.descifrar('RSA', 'facebook', dato.encode())
    print(data)

    Frame.mainloop()


########################################
############### MAIN APP ###############
########################################
    
App = ctk.CTk()
App.title("PwD_MaN")
App.geometry("430x430")

btn1 = ctk.CTkButton(App, text="Añadir Cuenta", command=add_account_frm, width=100)
btn1.configure(state="disabled", fg_color='#144870') if len(os.listdir('data/keys/')) < 3 else None
btn1.grid(row=0, column=0, padx=5, pady=5)

btn2 = ctk.CTkButton(App, text="Consultar Cuenta", command=get_account_frm, width=100)
btn2.configure(state="disabled", fg_color='#144870') if not len(os.listdir('data/users')) > 0 else None
btn2.grid(row=0, column=1, padx=5, pady=5)

btn3 = ctk.CTkButton(App, text="Añadir Clave", command=add_key_frm, width=220)
btn3.grid(row=1, column=0, padx=5, pady=5, columnspan=2)

cypher.create_key('AES', 256, 'user') if os.listdir('data/keys/').count('user_key.bin') == 0 else None
cypher.create_key('AES', 256, 'password') if os.listdir('data/keys/').count('password_key.bin') == 0 else None

App.mainloop()