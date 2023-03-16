import pdfplumber
import csv
import tkinter as tk
import tkinter.filedialog
import tkinter.scrolledtext
import re
import tkinter.messagebox
import customtkinter
from PIL import Image

### VARIÁBVEIS GLOBAIS ###
CLIENTS_CSV_FILE = './data/Clientes.csv'
NUM_SEARCHES = 0

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

    def add_client(self, client):
        #Define o ID na ordem de inserção
        client.set_ID(len(self.clients)+1)
        #Adiciona o cliente na lista
        self.clients.append(client)

    def remove_client(self, clientID):
        #Remove o clente baseado no seu ID
        self.pop(clientID)

    def print(self):
        for client in self.clients:
            client.print()

    def searched_names(self):
        #Lista de nomes a serem pesquisados
        names = []

        for client in self.clients:
            #Realiza a pesquisa somente se o cliente for ativo
            if client.actived:
                names.append(client.name)
                if client.subname_01 != "NA":
                    names.append(client.subname_01)
                if client.subname_02 != "NA":
                    names.append(client.subname_02)
                if client.subname_03 != "NA":
                    names.append(client.subname_03)
                if client.subname_04 != "NA":
                    names.append(client.subname_04)
        return names

### FUNÇÕES GLOBAIS ###

#Preenche a lista de clientes na memória
def fill_list():
    clients = ClientsList()

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
            clients.add_client(client)

    return clients

#Obtem o caminho do arquivo pdf
def browse_pdf():
    global pdf_file
    pdf_file = tkinter.filedialog.askopenfilename(
        filetypes=[('Arquivos PDF', '*.pdf')])

#Busca os clientes no arquivo PDF
def buscar_palavras(app):

    app.textbox.delete(1.0, tk.END)

    global NUM_SEARCHES
    NUM_SEARCHES += 1
    app.update_search_button()

    clients = fill_list()
    client_names = clients.searched_names()

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
            for client in client_names:
                # Utilizar expressão regular para buscar pela palavra completa no texto da página
                matches = re.findall(r'\b{}\b'.format(
                    client), text, re.IGNORECASE)
                if matches:
                    for match in matches:
                        finded_number += 1
                        app.textbox.insert(
                            tk.END, f'O cliente "{match}" foi encontrada na página {page_num+1}.\n')

            if (page_num+1) == num_paginas:
                if finded_number > 1:
                    app.textbox.insert(
                        tk.END, f'_____________________________\n{finded_number} correspondências encontrados\n_____________________________\n')
                if finded_number == 1:
                    app.textbox.insert(
                        tk.END, f'_____________________________\nSomente uma correspondência encontrada\n_____________________________\n')
                if finded_number == 0:
                    app.textbox.insert(
                        tk.END, f'_____________________________\nNenhum cliente encontrado\n_____________________________\n')

                app.textbox.insert(
                    tk.END, f'Busca finalizada!\n')


### PADRÕES DEFAULT DA INTERFACE ##
# Modes: "System" (standard), "Dark", "Light"
customtkinter.set_appearance_mode("System")
# Themes: "blue", "green", "dark-blue"
customtkinter.set_default_color_theme("green")

### APLICAÇÃO ###
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        #Configuração da janela
        self.title("Gestão e Busca de Clientes - Campello Castro")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        
        #---------------------------------#
        ###### ====BARRA LATERAL====######
        self.sidebar_frame = customtkinter.CTkFrame(
            self, width=140, corner_radius=5)
        self.sidebar_frame.grid(row=0, column=0, padx=10,
                                pady=10, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=50)

        # LOGOMARCA
        self.logo_image = customtkinter.CTkImage(light_image=Image.open("./icons/Logo.png"),
                                                 dark_image=Image.open("./icons/Logo.png"),
                                                 size=(60, 40))

        self.logo_frame_label = customtkinter.CTkLabel(self.sidebar_frame, text="campello\ncastro", image=self.logo_image,
                                                       compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.logo_frame_label.grid(row=0, column=0, padx=20, pady=(10, 20))

        # DESCRIÇÃO
        self.sidebar_description_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="busca de clientes", font=customtkinter.CTkFont(size=15))
        self.sidebar_description_label.grid(row=1, column=0, padx=20, pady=(0, 10))

        # BOTÃO DE SELAÇÃO DO DIÁRIO
        self.button_pdf_find = customtkinter.CTkButton(
            self.sidebar_frame, command=browse_pdf, text='Selecionar Diário')
        self.button_pdf_find.grid(row=2, column=0, padx=20, pady=10)

        # BOTÃO DE BUSCA
        if NUM_SEARCHES == 0:
            self.button_search = customtkinter.CTkButton(
                self.sidebar_frame, command=lambda: buscar_palavras(self), text='Buscar clientes')
            self.button_search.grid(row=3, column=0, padx=20, pady=10)

        # MENU DE TEMA
        self.appearance_mode_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="Tema da janela:", anchor="w")
        self.appearance_mode_label.grid(
            row=5, column=0, padx=20, pady=(100, 10))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(
            self.sidebar_frame, values=["Light", "Dark", "System"],
            command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(
            row=6, column=0, padx=20, pady=(0, 20))

        #-----------------------------#
        ###### ====RESULTADOS====######
        self.results_frame = customtkinter.CTkFrame(
            self, corner_radius=5)
        self.results_frame.grid(row=0, column=1, padx=10,
                                pady=10, rowspan=4, sticky="nsew")
        self.results_frame.grid_rowconfigure(4, weight=1)

        # TÍTULO
        self.logo_label = customtkinter.CTkLabel(
            self.results_frame, text="Resultado da busca:", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 0))

        # CAIXA DE TEXTO
        self.textbox = customtkinter.CTkTextbox(
            self.results_frame, width=500, corner_radius=5)
        self.textbox.grid(row=1, column=0, padx=(
            20, 20), pady=(0, 0), sticky="nsew")

        # BARRA DE PROGRESSO
        self.progressbar = customtkinter.CTkProgressBar(
            self.results_frame)
        self.progressbar.grid(row=2, column=0, padx=(
            20, 20), pady=(10, 10), sticky="ew")

        ################################
        # Valores Default
        self.appearance_mode_optionemenu.set("System")
        self.progressbar.set(0)

    # ==========FUNÇÕES==========

    # Definir o tema da janela

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def update_progress_bar(self, value):
        self.progressbar.set(value)
        self.update()

    def update_search_button(self):
        global NUM_SEARCHES
        if NUM_SEARCHES > 0:
            self.button_search.configure(text="Nova Busca")
        return

    # ===========================
        # Valores Default

### MAIN ###
if __name__ == "__main__":
    app = App()
    app.mainloop()
