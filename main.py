import customtkinter as ctk
import json, os
import cypher

########################################
############## FUNCTIONS ###############
########################################

def add_account(net, user, email, pwd, keyName, tkey):
    user = cypher.cifrar('RSA', keyName, user)
    pwd = cypher.cifrar('RSA', keyName, pwd)
    email = cypher.cifrar('RSA', keyName, email)
    tkey = cypher.cifrar('RSA', keyName, str(tkey))    

    fu = open(f'data/users/{net}.bin', 'wb')
    fu.write(user) 
    fu.close()
    
    fp = open(f'data/passwords/{net}.bin', 'wb')
    fp.write(pwd)
    fp.close()

    fe = open(f'data/emails/{net}.bin', 'wb')
    fe.write(email)
    fe.close()

    fk = open(f'data/keys/{net}.bin', 'wb')
    fk.write(tkey)
    fk.close()

########################################
################ FRAMES ################
########################################

def add_key_frm():
    Frame = ctk.CTk()
    Frame.title("Añadir Clave | Tr1x-5ec")
    Frame.geometry("380x380")
    
    def change_sizes(secret):
        if secret == "RSA":
            length.configure(values=["1024", "2048", "4096", "8192", "16384"])
            length.set('Longitudes RSA')
        elif secret == "AES":
            length.configure(values=["64", "128", "256"])
            length.set('Longitudes AES')

    def create_key(algoritmo, name, size):
        if algoritmo == "AES":
            cypher.create_key('AES', 'user', size, name)
            cypher.create_key('AES', 'password', size, name)
            cypher.create_key('AES', 'emails', size, name)
            cypher.create_key('AES', 'keys', size, name)
        else:
            cypher.create_key('RSA', longitud=size, name=name)
    ktype = ctk.CTkComboBox(Frame, values=["RSA", "AES"], width=220, command=change_sizes)
    ktype.set('Algoritmo')
    ktype.grid(row=0, column=0, padx=5, pady=5, columnspan=2)
    name = ctk.CTkEntry(Frame, placeholder_text="Nombre de la clave", width=100)
    name.grid(row=1, column=0, padx=5, pady=5)
    length = ctk.CTkOptionMenu(Frame, values=[], width=100)
    length.set('Longitud')
    length.grid(row=1, column=1, padx=5, pady=5)
    create = ctk.CTkButton(Frame, text="Crear Clave", command=lambda:(create_key(ktype.get(), name.get(), int(length.get()))), width=100)
    create.grid(row=2, column=0, padx=5, pady=5, columnspan=2)

    Frame.mainloop()

def add_account_frm():
    tkey = cypher.gen_key()
    keysList = [i.split('.')[0] for i in os.listdir('tray/')]
    keysList = list(set(keysList))

    Frame = ctk.CTk()
    Frame.title("Añadir Cuenta | Tr1x-5ec")
    Frame.geometry("600x600")

    tkey_net = ctk.CTkLabel(Frame, text=f"Clave: {tkey}", width=150)
    tkey_net.grid(row=0, column=0, padx=5, pady=5)
    social_net = ctk.CTkEntry(Frame, placeholder_text="Red Social", width=150)
    social_net.grid(row=0, column=1, padx=5, pady=5)
    user_net = ctk.CTkEntry(Frame, placeholder_text="Usuario", width=150)
    user_net.grid(row=1, column=0, padx=5, pady=5)
    email_net = ctk.CTkEntry(Frame, placeholder_text="Correo Electronico", width=150)
    email_net.grid(row=1, column=1, padx=5, pady=5)
    password_net = ctk.CTkEntry(Frame, placeholder_text="Contraseña", width=150)
    password_net.grid(row=2, column=0, padx=5, pady=5)
    key_sel = ctk.CTkOptionMenu(Frame, values=[i for i in keysList], width=150)
    key_sel.grid(row=2, column=1, padx=5, pady=5)
    add_net = ctk.CTkButton(Frame, text="Añadir Cuenta", command=lambda:(add_account(social_net.get(), user_net.get(), email_net.get(), 
            password_net.get(), key_sel.get(), tkey)), width=320)
    add_net.grid(row=3, column=0, padx=5, pady=5, columnspan=2)

    Frame.mainloop()


def get_account_frm():
    Frame = ctk.CTk()
    Frame.title("Mostrar Cuenta | Tr1x-5ec")
    Frame.geometry("370x330")

    tabs = ctk.CTkTabview(Frame)
    tabs.grid(row=0, column=0, padx=20, pady=18)
    tabs.add('Usuario')
    tabs.add('Email')
    tabs.add('Contraseña')
    tabs.add('Clave')

    email_user = ctk.CTkEntry(tabs.tab('Usuario'), placeholder_text="Correo Electronico", width=150)
    password_user = ctk.CTkEntry(tabs.tab('Usuario'), placeholder_text="Contraseña", width=150)
    key_user = ctk.CTkEntry(tabs.tab('Usuario'), placeholder_text="Clave", width=150)
    btn_user = ctk.CTkButton(tabs.tab('Usuario'), text="Ingresar", width=150)
    email_user.grid(row=0, column=0, padx=5, pady=5)
    password_user.grid(row=0, column=1, padx=5, pady=5)
    key_user.grid(row=1, column=0, padx=5, pady=5)
    btn_user.grid(row=1, column=1, padx=5, pady=5)

    user_email = ctk.CTkEntry(tabs.tab('Email'), placeholder_text="Usuario", width=150)
    password_email = ctk.CTkEntry(tabs.tab('Email'), placeholder_text="Contraseña", width=150)
    key_email = ctk.CTkEntry(tabs.tab('Email'), placeholder_text="Clave", width=150)
    btn_email = ctk.CTkButton(tabs.tab('Email'), text="Ingresar", width=150)
    user_email.grid(row=0, column=0, padx=5, pady=5)
    password_email.grid(row=0, column=1, padx=5, pady=5)
    key_email.grid(row=1, column=0, padx=5, pady=5)
    btn_email.grid(row=1, column=1, padx=5, pady=5)

    user_pwd = ctk.CTkEntry(tabs.tab('Contraseña'), placeholder_text="Usuario", width=150)
    email_pwd = ctk.CTkEntry(tabs.tab('Contraseña'), placeholder_text="Correo Electronico", width=150)
    key_pwd = ctk.CTkEntry(tabs.tab('Contraseña'), placeholder_text="Clave", width=150)
    btn_pwd = ctk.CTkButton(tabs.tab('Contraseña'), text="Ingresar", width=150)
    user_pwd.grid(row=0, column=0, padx=5, pady=5)
    email_pwd.grid(row=0, column=1, padx=5, pady=5)
    key_pwd.grid(row=1, column=0, padx=5, pady=5)
    btn_pwd.grid(row=1, column=1, padx=5, pady=5)

    user_key = ctk.CTkEntry(tabs.tab('Clave'), placeholder_text="Usuario", width=150)
    email_key = ctk.CTkEntry(tabs.tab('Clave'), placeholder_text="Correo Electronico", width=150)
    password_key = ctk.CTkEntry(tabs.tab('Clave'), placeholder_text="Contraseña", width=150)
    btn_key = ctk.CTkButton(tabs.tab('Clave'), text="Ingresar", width=150)
    user_key.grid(row=0, column=0, padx=5, pady=5)
    email_key.grid(row=0, column=1, padx=5, pady=5)
    password_key.grid(row=1, column=0, padx=5, pady=5)
    btn_key.grid(row=1, column=1, padx=5, pady=5)

    Frame.mainloop()


########################################
############### MAIN APP ###############
########################################
    
App = ctk.CTk()
App.title("Tr1x-5ec")
App.geometry("430x430")

btn1 = ctk.CTkButton(App, text="Añadir Cuenta", command=add_account_frm, width=100)
btn1.configure(state="disabled", fg_color='#144870') if len(os.listdir('data/keys/')) >= 4 and len(os.listdir('tray/')) >= 1 else None
btn1.grid(row=0, column=0, padx=5, pady=5)

btn2 = ctk.CTkButton(App, text="Consultar Cuenta", command=get_account_frm, width=100)
btn2.configure(state="disabled", fg_color='#144870') if not len(os.listdir('data/users')) > 0 else None
btn2.grid(row=0, column=1, padx=5, pady=5)

btn3 = ctk.CTkButton(App, text="Añadir Clave", command=add_key_frm, width=220)
btn3.grid(row=1, column=0, padx=5, pady=5, columnspan=2)

try:
    conf = open('config.json', 'r').read()
    config = json.loads(conf)
except FileNotFoundError:
    config = {"singleaesforfile":1, "aesforrsa":1, "singleaesforrsa":1,
    "singlersaforkey":0, "restorekey":0,"fieldsforaccount":1}
App.mainloop()