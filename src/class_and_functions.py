
import pdfplumber
import csv
import tkinter as tk
import tkinter.filedialog
import tkinter.scrolledtext
import re
import tkinter.messagebox
import customtkinter
import os
from PIL import Image
import shutil
import datetime

### CLASSES ###
class Client():
    def __init__(self, name, subname_01, subname_02, subname_03, subname_04, cnpj, email, number, representative, actived):
        super().__init__()

        self.ID = -1
        self.name = name
        self.subname_01 = subname_01
        self.subname_02 = subname_02
        self.subname_03 = subname_03
        self.subname_04 = subname_04
        self.cnpj = cnpj
        self.number = number
        self.email = email
        self.representative = representative
        self.cited = False
        self.selected = False
        self.actived = True
        if actived != "TRUE":
            self.actived = False

    ##--GETTERS--##

    def get_names(self, value):
        if value == 1:
            return self.name
        if value == 2:
            return self.subname_01
        if value == 3:
            return self.subname_02
        if value == 4:
            return self.subname_03
        if value == 5:
            return self.subname_04
    
    def qtd_names(self):
        qtd = 1
        if self.subname_01 != "NA":
            qtd += 1
        if self.subname_02 != "NA":
            qtd += 1
        if self.subname_03 != "NA":
            qtd += 1
        if self.subname_04 != "NA":
            qtd += 1
        return qtd

    def get_cnpj(self):
        return self.cnpj
    
    def get_number(self):
        return self.number
    
    def get_email(self):
        return self.email
    
    def get_representative(self):
        return self.representative

    def getID(self):
        return self.ID

    def is_active(self):
        return self.actived
    
    ##--SETTERS--##
    def set_ID(self, number):
        self.ID = number

    def change_name(self, new_name):
        self.name = new_name

    def change_cnpj(self, new_cnpj):
        self.cnpj = new_cnpj

    def change_number(self, new_number):
        self.number = new_number

    def change_email(self, new_email):
        self.email = new_email

    def swap_actived(self):
        if self.is_actived():
            self.actived = False
        else:
            self.actived = True

    def make_cited(self):
        self.cited = True

    def select(self):
        self.selected = True

    ##--OTHERS--##
    def get_info(self):
        self.email = self.email.replace('\n', '\n\t\t')
        info_string = (
            f'\nCNPJ:\t\t{self.cnpj} \nTelefone:\t\t{self.number} \nEmails:\t\t{self.email} \n\nRepresentante:\t{self.representative} \nAtivo:\t\t{self.actived}'
        )

        # Adicionar informações dos subclientes
        subclient_info = ""
        if self.subname_01 != "NA":
            subclient_info += f'\nSub-Cliente 01:\t{self.subname_01}'
        if self.subname_02 != "NA":
            subclient_info += f'\nSub-Cliente 02:\t{self.subname_02}'
        if self.subname_03 != "NA":
            subclient_info += f'\nSub-Cliente 03:\t{self.subname_03}'
        if self.subname_04 != "NA":
            subclient_info += f'\nSub-Cliente 04:\t{self.subname_04}'

        return subclient_info + info_string

    def print(self):
        print("Cited: ", self.cited, "|",self.ID, "|",
              self.name, " - ", self.cnpj, "Ativo: ", self.actived)
        
        # Seção de subclientes
        if self.subname_01 != "NA":
            print("\t|_Sub-Cliente 01: ", self.subname_01)
        if self.subname_02 != "NA":
            print("\t|_Sub-Cliente 02: ", self.subname_02)
        if self.subname_03 != "NA":
            print("\t|_Sub-Cliente 03: ", self.subname_03)
        if self.subname_04 != "NA":
            print("\t|_Sub-Cliente 04: ", self.subname_04)


class ClientsList():
    def __init__(self):
        super().__init__()

        self.clients = []
        self.actived_clients = []
        self.inactived_clients = []

    #Adiciona um novo cliente
    def add_client(self, client):
        #Define o ID na ordem de inserção
        client.set_ID(len(self.clients)+1)
        #Adiciona o cliente na lista
        self.clients.append(client)
        if client.is_active():
            self.actived_clients.append(client)
        else:
            self.inactived_clients.append(client)

    #Remove um cliente
    def remove_client(self, clientID):
        #Remove o clente baseado no seu ID
        self.pop(clientID)

    #Printa as informações de um cliente na tela
    def print(self):
        for client in self.clients:
            client.print()
    def get_client_info(self, name, type):
        for client in self.clients:
            if client.name == name:
                if type == 'text':
                    return client.get_info()
                if type == 'class':
                    return client
                else:
                    print('ERROR: unknown type IN get_client_info')

    #Gera uma lista com os nomes e ID's dos clientes ATIVOS
    def get_searchable_list(self):
        #Percorre a lista de clientes
        for i in range(len(self.clients)):

            if self.clients[i].is_active():
                #Adiciona os nomes à lista de pesquisáveis de acordo com a quantidade de nomes
                for j in range(1, ((self.clients[i].qtd_names())+1)):
                    SEARCHABLE_LIST.append((self.clients[i].getID(), self.clients[i].get_names(j)))

    #Define um cliente como citado pelo ID
    def finded(self, value):
        self.clients[value-1].make_cited()
    
    def swap(self, name):
        print("Swapping...")
        for client in self.clients:
            if client == name:
                print(name, ' está ', client.is_active())
                copia = client
                self.remove_client(copia.get_ID())
                copia.swap_actived()
                self.add_client(copia)

    def clean(self):
        self.clients.clear()
        self.actived_clients.clear()
        self.inactived_clients.clear()


class ScrollableRadiobuttonFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, item_list, command=None, **kwargs):
        super().__init__(master, **kwargs)

        self.command = command
        self.radiobutton_variable = customtkinter.StringVar()
        self.radiobutton_list = []
        for i, item in enumerate(item_list):
            self.add_item(item)

    def add_item(self, item):
        radiobutton = customtkinter.CTkRadioButton(self, text=item, value=item, variable=self.radiobutton_variable)
        if self.command is not None:
            radiobutton.configure(command=self.command)
        radiobutton.grid(row=len(self.radiobutton_list), column=0, padx=(5, 5), pady=(10, 10), stick="new")
        self.radiobutton_list.append(radiobutton)

    def remove_item(self, item):
        for radiobutton in self.radiobutton_list:
            if item == radiobutton.cget("text"):
                radiobutton.destroy()
                self.radiobutton_list.remove(radiobutton)
                return

    def get_checked_item(self):
        return self.radiobutton_variable.get()
    

### VARIÁBVEIS GLOBAIS ###
agora = datetime.datetime.now()
data_formatada = agora.strftime("%d-%m-%Y_%H-%M")
CLIENTS_CSV_FILE = './data/Clientes.csv'
BACKUP_CSV_FILE = './data/backup/Clientes_bkp_'+ data_formatada +'.csv'
NUM_SEARCHES = 0
CLIENTS = ClientsList()
SEARCHABLE_LIST = []
SEND_FORM = False


### FUNÇÕES GLOBAIS ###
#Preenche a lista de clientes na memória
def fill_list():
    
    #Buscar os dados do arquivo csv
    with open(CLIENTS_CSV_FILE, newline='', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        next(reader)  # pular a linha do cabeçalho

        for row in reader:
            #Para cada linha no arquivo CSV
            name, subname_01, subname_02, subname_03, subname_04, cnpj, email, number, representative, ativo = row
            #cria um cliente com as informações
            client = Client(name, subname_01, subname_02, subname_03,
                            subname_04, cnpj, email, number, representative, ativo)
            #Adiciona na classe clients
            CLIENTS.add_client(client)
            
#Obtem o caminho do arquivo pdf
def browse_pdf():
    global pdf_file
    pdf_file = tkinter.filedialog.askopenfilename(
        filetypes=[('Arquivos PDF', '*.pdf')])
    return pdf_file

#Busca os clientes no arquivo PDF
def seek_client(app):

    app.textbox.configure(state="normal")
    app.button_search.configure(text="Buscando...")
    
    #Limpa a caixa de texto ao iniciar uma nova busca
    app.textbox.delete(1.0, tk.END)
    
    global NUM_SEARCHES
    NUM_SEARCHES += 1
    app.update_search_button()

    # Abrir o arquivo PDF selecionado pelo usuário e criar um objeto PDFReader
    with pdfplumber.open(pdf_file) as pdf:
        # Numero de entidades encontradas
        finded_number = 0
        # Obter o número total de páginas do PDF
        num_paginas = len(pdf.pages)

        app.textbox.insert(
            tk.END, f'Iniciando busca...\n')

        # Iterar pelas páginas do arquivo PDF
        for page_num, page in enumerate(pdf.pages):
            text = page.extract_text()

            # Atualizar Barra de progresso
            app.update_progress_bar((page_num+1)/num_paginas)
            # Verificar se cada palavra do arquivo CSV está na página atual do PDF
            for i in range(len(SEARCHABLE_LIST)):
                # Utilizar expressão regular para buscar pela palavra completa no texto da página
                matches = re.findall(r'\b{}\b'.format(
                    SEARCHABLE_LIST[i][1]), text, re.IGNORECASE)
                if matches:
                    CLIENTS.finded(SEARCHABLE_LIST[i][0])
                    #Adicionar à lista de ID's encontrados
                    #CLIENTS.foundID(SEARCHABLE_LIST[i][0])
                    #print(SEARCHABLE_LIST[i][0], "->ID ENCONTRADO")
                
                    for match in matches:
                        finded_number += 1
                        app.textbox.insert(
                            tk.END, f'{match} - Página {page_num+1}.\n')

            if (page_num+1) == num_paginas:
                if finded_number > 1:
                    app.textbox.insert(
                        tk.END, f'_____________________________\n{finded_number} correspondências encontradas\n_____________________________\n')
                if finded_number == 1:
                    app.textbox.insert(
                        tk.END, f'_____________________________\nSomente uma correspondência encontrada\n_____________________________\n')
                if finded_number == 0:
                    app.textbox.insert(
                        tk.END, f'_____________________________\nNenhuma correspondência encontrada\n_____________________________\n')

                app.textbox.insert(
                    tk.END, f'Busca finalizada!\n')
                
                app.textbox.configure(state="disabled")
                app.button_search.configure(text="Nova Busca")
        CLIENTS.print()
        
#Gera um cliente dentro de um ferame parta aba de gestão
def generate_client_frame(app, i):
    client_frame = customtkinter.CTkFrame(app.scrollable_frame, corner_radius=5, height=30)
    client_frame.grid(row=i, column=0, padx=10,
                            pady=5, sticky="nsew")
    client_frame.grid_rowconfigure(0, weight=1)
    client_frame.grid_columnconfigure(0, weight=1, minsize=50)
    
    client_data = customtkinter.CTkLabel(
        client_frame, text=f"Cliente teste {i}", font=customtkinter.CTkFont(size=12))
    client_data.grid(row=0, column=0, padx=20, pady=(2, 0))

    return client_frame

def remove_client(app, name, mode):
    # Criar uma cópia do arquivo original como backup
    shutil.copy2(CLIENTS_CSV_FILE, BACKUP_CSV_FILE)
    
    # Atualizar o arquivo CSV apagando a linha
    lines_to_keep = []

    with open(CLIENTS_CSV_FILE, 'r', newline='', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        header = next(reader)
        lines_to_keep.append(header)

        for row in reader:
            if row[0] != name:
                lines_to_keep.append(row)

    with open(CLIENTS_CSV_FILE, 'w', newline='', encoding='utf-8') as new_csv_file:
        writer = csv.writer(new_csv_file)
        writer.writerows(lines_to_keep)

    # Atualize os widgets ScrollableRadiobuttonFrame
    updateScroll(app, name, '?', 'delete')

    CLIENTS.clean()
    fill_list()
    
    if(mode == 'delete'):
        mssg(title="Cliente removido!", text=name, dimension="300x100")
    elif(mode == 'edit'):
        mssg(title="Cliente editado!", text=name+'\n Reinicie o programa', dimension="300x100")
    
    print(f"A linha com o cliente '{name}' foi removida do arquivo.")

def mssg(title, text, dimension):
    popup = customtkinter.CTk()
    popup.geometry(dimension)
    popup.title("Informações do cliente")

    frame1 = customtkinter.CTkFrame(master=popup)
    frame1.pack(pady=10, padx=10, fill="both", expand=True)
    
    if title:
        title_label = customtkinter.CTkLabel(frame1, text=title, justify= 'left', font=customtkinter.CTkFont(size=20, weight="bold"))
        title_label.grid(row=0, column=0)
    if text:
        info_label = customtkinter.CTkLabel(frame1, text=text, justify= 'left', font=customtkinter.CTkFont(size=15, weight="normal"))
        info_label.grid(row=1, column=0)
    
    popup.mainloop()

def inactived_client(app, client_name):
    # Encontrar o cliente na lista de clientes ativos
    for client in CLIENTS.clients:
        if client.name == client_name:
            # Alterar o estado do cliente no arquivo CSV
            if client.is_active():
                with open(CLIENTS_CSV_FILE, 'r', newline='', encoding='utf-8') as csv_file:
                    reader = csv.reader(csv_file)
                    header = next(reader)
                    lines = [row for row in reader]
                    
                with open(CLIENTS_CSV_FILE, 'w', newline='', encoding='utf-8') as new_csv_file:
                    writer = csv.writer(new_csv_file)
                    writer.writerow(header)
                    for row in lines:
                        if row[0] == client_name:
                            row[-1] = "FALSE"  # Alterar o valor da coluna "Ativo"
                        writer.writerow(row)
                
                CLIENTS.clean()
                fill_list()

                # Atualizar os widgets ScrollableRadiobuttonFrame
                updateScroll(app, client_name, 'TRUE', 'swap')
                
                mssg(title="Cliente alterado para inativo", text=f"O cliente '{client_name}' foi alterado para inativo.", dimension="600x100")
                
                break
            else:
                print("Não está ativo")
                with open(CLIENTS_CSV_FILE, 'r', newline='', encoding='utf-8') as csv_file:
                    reader = csv.reader(csv_file)
                    header = next(reader)
                    lines = [row for row in reader]
                    
                with open(CLIENTS_CSV_FILE, 'w', newline='', encoding='utf-8') as new_csv_file:
                    writer = csv.writer(new_csv_file)
                    writer.writerow(header)
                    for row in lines:
                        if row[0] == client_name:
                            row[-1] = "TRUE"  # Alterar o valor da coluna "Ativo"
                        writer.writerow(row)
                # Atualizar os widgets ScrollableRadiobuttonFrame
                
                CLIENTS.clean()
                fill_list()
                
                updateScroll(app, client_name, 'FALSE', 'swap')
                
                mssg(title="Cliente alterado para ativo", text=f"O cliente '{client_name}' foi alterado para ativo.", dimension="600x100")
                
                
                break
            
            
    else:
        mssg(title="Cliente não encontrado", text=f"O cliente '{client_name}' não foi encontrado na lista de ativos.", dimension="400x100")

def updateScroll(app, client, satate, action):
    print('Atualizando updateScroll...')
    if action == 'new':
        print('Novo cliente')
        app.scrollable_radiobutton_frame_all.add_item(client)
        if satate == 'TRUE':
            app.scrollable_radiobutton_frame_actived.add_item(client)
        else:
            app.scrollable_radiobutton_frame_inactived.add_item(client)

    elif action == 'delete':
        print('deleting client')
        app.scrollable_radiobutton_frame_all.remove_item(client)
        app.scrollable_radiobutton_frame_actived.remove_item(client)
        app.scrollable_radiobutton_frame_inactived.remove_item(client)

    elif action == 'swap':
        print('swapping client')
        if satate == 'TRUE':
            app.scrollable_radiobutton_frame_actived.remove_item(client)
            app.scrollable_radiobutton_frame_inactived.add_item(client)
        else:
            app.scrollable_radiobutton_frame_inactived.remove_item(client)
            app.scrollable_radiobutton_frame_actived.add_item(client)

def add_client_csv(app, popup, name, subname_01, subname_02, subname_03, subname_04, cnpj, email, number, representative, state, mode,  
                   old_name):

    state_text='TRUE'
    
    popup.destroy()
    
    if(mode == 'edit'):
        print('mode = edit')
        remove_client(app, old_name, mode)

    if(name ==''):
        mssg(title="Cliente sem nome", text='Insira um nome no cliente para prosseguir', dimension="400x100")
    if(subname_01 ==''):
        subname_01='NA'
    if(subname_02 ==''):
        subname_02='NA'
    if(subname_03 ==''):
        subname_03='NA'
    if(subname_04 ==''):
        subname_04='NA'
    if(cnpj==''):
        cnpj='NA'
    if(email==''):
        email='NA'
    if(representative==''):
        representative='NA'
    if(state==1):
        state_text='TRUE'
    else:
        state_text='FALSE'
    
    name= name.upper()
    subname_01= subname_01.upper()
    subname_02= subname_02.upper()
    subname_03= subname_03.upper()
    subname_04= subname_04.upper()
    cnpj= cnpj.upper()
    email= email.upper()
    number= number.upper()
    representative = representative.upper()


    row = name+','+subname_01+','+subname_02+','+subname_03+','+subname_04+','+cnpj+','+email+','+number+','+representative+','+state_text
    print (row)

    with open(CLIENTS_CSV_FILE, 'a', newline='', encoding='utf-8') as csv_file:
        print("Escrevendo no csv...")
        writer = csv.writer(csv_file)
        writer.writerow([name,subname_01,subname_02,subname_03,subname_04,cnpj,email,number,representative,state_text])
    
    if state:
        print('ADICIONANDO ATIVO NOVO')
        updateScroll(app, name, 'TRUE', 'new')
    else:
        print('ADICIONANDO NÃO ATIVO NOVO')
        updateScroll(app, name, 'FALSE', 'new')


    CLIENTS.clean()
    csv_order_by_name()
    fill_list()

def add_client(app, mode):
    client_info = CLIENTS.get_client_info(app.select_client, type='class')

    SEND_FORM = False
    popup = customtkinter.CTk()
    popup.geometry('500x550')
    popup.title("Informações do cliente")

    frame1 = customtkinter.CTkFrame(master=popup)
    frame1.pack(pady=10, padx=10, fill="both", expand=True)

    title_label = customtkinter.CTkLabel(frame1, text='Dados Cliente', justify= 'center', font=customtkinter.CTkFont(size=20, weight="bold"))
    title_label.grid(row=0, column=0)

    name_label = customtkinter.CTkLabel(frame1, text='Cliente:', justify= 'left', font=customtkinter.CTkFont(size=15, weight="normal"))
    name_label.grid(row=1, column=0)
    entry_name = customtkinter.CTkTextbox(frame1, width=300, height=20)
    entry_name.grid(row=1, column=1, pady=5)

    subname_01_label = customtkinter.CTkLabel(frame1, text='Subcliente_01:', justify= 'left', font=customtkinter.CTkFont(size=15, weight="normal"))
    subname_01_label.grid(row=2, column=0)
    entry_subname_01 = customtkinter.CTkTextbox(frame1, width=300, height=20)
    entry_subname_01.grid(row=2, column=1, pady=5)

    subname_02_label = customtkinter.CTkLabel(frame1, text='Subcliente_02:', justify= 'left', font=customtkinter.CTkFont(size=15, weight="normal"))
    subname_02_label.grid(row=3, column=0)
    entry_subname_02 = customtkinter.CTkTextbox(frame1, width=300, height=20)
    entry_subname_02.grid(row=3, column=1, pady=5)

    subname_03_label = customtkinter.CTkLabel(frame1, text='Subcliente_03:', justify= 'left', font=customtkinter.CTkFont(size=15, weight="normal"))
    subname_03_label.grid(row=4, column=0)
    entry_subname_03 = customtkinter.CTkTextbox(frame1, width=300, height=20)
    entry_subname_03.grid(row=4, column=1, pady=5)
    
    subname_04_label = customtkinter.CTkLabel(frame1, text='Subcliente_04:', justify= 'left', font=customtkinter.CTkFont(size=15, weight="normal"))
    subname_04_label.grid(row=5, column=0)
    entry_subname_04 = customtkinter.CTkTextbox(frame1, width=300, height=20)
    entry_subname_04.grid(row=5, column=1, pady=5)

    cnpj_label = customtkinter.CTkLabel(frame1, text='CNPJ:', justify= 'left', font=customtkinter.CTkFont(size=15, weight="normal"))
    cnpj_label.grid(row=6, column=0)
    entry_cnpj = customtkinter.CTkTextbox(frame1, width=300, height=20)
    entry_cnpj.grid(row=6, column=1, pady=5)

    email_label = customtkinter.CTkLabel(frame1, text='Emails:', justify= 'left', font=customtkinter.CTkFont(size=15, weight="normal"))
    email_label.grid(row=7, column=0)
    entry_email = customtkinter.CTkTextbox(frame1, width=300, height=80)
    entry_email.grid(row=7, column=1, pady=5)

    number_label = customtkinter.CTkLabel(frame1, text='Telefone:', justify= 'left', font=customtkinter.CTkFont(size=15, weight="normal"))
    number_label.grid(row=8, column=0)
    entry_number = customtkinter.CTkTextbox(frame1, width=300, height=20)
    entry_number.grid(row=8, column=1, pady=5)

    representative_label = customtkinter.CTkLabel(frame1, text='Representante:', justify= 'left', font=customtkinter.CTkFont(size=15, weight="normal"))
    representative_label.grid(row=9, column=0)
    entry_representative = customtkinter.CTkTextbox(frame1, width=300, height=20)
    entry_representative.grid(row=9, column=1, pady=5)

    active_label = customtkinter.CTkLabel(frame1, text='Ativar cliente:', justify= 'left', font=customtkinter.CTkFont(size=15, weight="normal"))
    active_label.grid(row=10, column=0)
    switch_1 = customtkinter.CTkSwitch(master=frame1, width=300, height=20, text='')
    switch_1.grid(row=10, column=1, pady=5)
    
    if(mode == 'edit'):
        print('editar cliente')
        entry_name.insert('end', client_info.get_names(1))
        if client_info.get_names(2) != 'NA': entry_subname_01.insert('end', client_info.get_names(2))
        if client_info.get_names(3) != 'NA': entry_subname_02.insert('end', client_info.get_names(3))
        if client_info.get_names(4) != 'NA': entry_subname_03.insert('end', client_info.get_names(4))
        if client_info.get_names(5) != 'NA': entry_subname_04.insert('end', client_info.get_names(5))
        if client_info.get_cnpj() != 'NA': entry_cnpj.insert('end', client_info.get_cnpj())
        if client_info.get_email() != 'NA': entry_email.insert('end', client_info.get_email())
        if client_info.get_number() != 'NA': entry_number.insert('end', client_info.get_number())
        if client_info.get_representative() != 'NA': entry_representative.insert('end', client_info.get_representative())
        
        switch_1.select() if client_info.is_active() else switch_1.deselect()
        
        button_1 = customtkinter.CTkButton(master=frame1, command=lambda: add_client_csv(app, popup, 
                                                                                        entry_name.get('1.0', 'end').strip(), 
                                                                                        entry_subname_01.get('1.0', 'end').strip(),
                                                                                        entry_subname_02.get('1.0', 'end').strip(),
                                                                                        entry_subname_03.get('1.0', 'end').strip(), 
                                                                                        entry_subname_04.get('1.0', 'end').strip(),
                                                                                        entry_cnpj.get('1.0', 'end').strip(),
                                                                                        entry_email.get('1.0', 'end').strip(),
                                                                                        entry_number.get('1.0', 'end').strip(),
                                                                                        entry_representative.get('1.0', 'end').strip(),
                                                                                        switch_1.get(), 
                                                                                        mode, client_info.get_names(1)), text='Atualizar')


    else:
        button_1 = customtkinter.CTkButton(master=frame1, command=lambda: add_client_csv(app, popup, 
                                                                                        entry_name.get('1.0', 'end').strip(), 
                                                                                        entry_subname_01.get('1.0', 'end').strip(),
                                                                                        entry_subname_02.get('1.0', 'end').strip(),
                                                                                        entry_subname_03.get('1.0', 'end').strip(), 
                                                                                        entry_subname_04.get('1.0', 'end').strip(),
                                                                                        entry_cnpj.get('1.0', 'end').strip(),
                                                                                        entry_email.get('1.0', 'end').strip(),
                                                                                        entry_number.get('1.0', 'end').strip(),
                                                                                        entry_representative.get('1.0', 'end').strip(),
                                                                                        switch_1.get(), 
                                                                                        mode, entry_name.get('1.0', 'end').strip()), text='Adicionar')
        
    button_1.grid(row=11, column=1, pady=5)
    popup.mainloop()

def csv_order_by_name():
    # Função para obter a chave de ordenação (nome do Cliente)
    def get_sort_key(row):
        return row['Cliente']

    # Lê o arquivo CSV de entrada
    with open(CLIENTS_CSV_FILE, 'r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        rows = list(reader)

    # Ordena as linhas pelo nome do Cliente
    sorted_rows = sorted(rows, key=get_sort_key)

    # Escreve as linhas ordenadas no arquivo CSV de saída
    with open(CLIENTS_CSV_FILE, 'w', newline='', encoding='utf-8') as outfile:
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(sorted_rows)

    print("Linhas ordenadas e escritas com sucesso!")

def save_alert(app):
    def press_yes():
        csv_order_by_name()
        shutil.copy2(CLIENTS_CSV_FILE, BACKUP_CSV_FILE)
        app.destroy()
        popup.destroy()


    def press_no():
        csv_order_by_name()
        popup.destroy()
        app.destroy()
    
    def press_cancel():
        csv_order_by_name()
        popup.destroy()


    popup = customtkinter.CTk()
    popup.geometry('220x100')
    popup.title("Informações do cliente")
    
    frame1 = customtkinter.CTkFrame(master=popup)
    frame1.pack(pady=5, padx=10, fill="both", expand=True)

    info_label = customtkinter.CTkLabel(frame1, text='Deseja salvar antes de sair?', justify= 'center', font=customtkinter.CTkFont(size=15, weight="normal"))
    info_label.grid(row=0, column=0)

    
    frame2 = customtkinter.CTkFrame(master=popup)
    frame2.pack(pady=5, padx=10, fill="both", expand=True)

    
    button_yes = customtkinter.CTkButton(
            frame2, command=lambda: press_yes(), text='Sim', width=50, height=30, anchor='w')
    button_yes.grid(row=2, column=0, padx=5, pady=5)

    button_no = customtkinter.CTkButton(
            frame2, command=lambda: press_no(), text='Não', width=50, height=30, anchor='w')
    button_no.grid(row=2, column=1, padx=5, pady=5)

    button_cancel = customtkinter.CTkButton(
            frame2, command=lambda: press_cancel(), text='Cancelar', width=50, height=30, anchor='w')
    button_cancel.grid(row=2, column=2, padx=5, pady=5)

    popup.mainloop()

def backup():
    print("Backup started")
    csv_file = tkinter.filedialog.askopenfilename(filetypes=[('Arquivos CSV', '*.csv')])

    if csv_file:
        shutil.copy(csv_file, CLIENTS_CSV_FILE)
        print(f"Backup successful. File '{csv_file}' copied to '{CLIENTS_CSV_FILE}'")
        mssg(title='Sucesso!', text='Nova base de dados importada! \n REINICIE O PROGRAMA', dimension='400x100')
    else:
        mssg(title='ERROR', text='Erro ao importar CVS como base de dados', dimension='320x100')

### PADRÕES DEFAULT DA INTERFACE ##
# Modes: "System" (standard), "Dark", "Light"
customtkinter.set_appearance_mode("System")
# Themes: "blue", "green", "dark-blue"
customtkinter.set_default_color_theme("green")
