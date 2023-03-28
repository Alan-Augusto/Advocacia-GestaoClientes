
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

    def make_cited(self):
        self.cited = True

    def select(self):
        self.selected = True

    ##--OTHERS--##
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
CLIENTS_CSV_FILE = './data/Clientes.csv'
NUM_SEARCHES = 0
CLIENTS = ClientsList()
SEARCHABLE_LIST = []


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

### PADRÕES DEFAULT DA INTERFACE ##
# Modes: "System" (standard), "Dark", "Light"
customtkinter.set_appearance_mode("System")
# Themes: "blue", "green", "dark-blue"
customtkinter.set_default_color_theme("green")
