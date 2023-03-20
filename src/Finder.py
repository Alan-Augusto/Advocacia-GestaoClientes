import pdfplumber
import csv
import tkinter as tk
import tkinter.filedialog
import tkinter.scrolledtext
import re
import tkinter.messagebox
import customtkinter
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
                                                       compound="left", font=customtkinter.CTkFont( size=12, weight="bold"))
        self.logo_frame_label.grid(row=0, column=0, padx=20, pady=(10, 20))

        # DESCRIÇÃO
        self.sidebar_description_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="busca de clientes", font=customtkinter.CTkFont(size=15))
        self.sidebar_description_label.grid(row=1, column=0, padx=20, pady=(0, 10))

        

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

        #----------------------------------#
        ###### ====GESTÃO CLIENTES====######
        self.clients_frame = customtkinter.CTkFrame(
            self, corner_radius=5)
        #fg_color="transparent"
        self.clients_frame.grid(row=0, column=1, padx=10,
                                pady=10, rowspan=4, sticky="new")
        self.clients_frame.grid_rowconfigure(0, weight=1)
        self.clients_frame.grid_columnconfigure(0, weight=1, minsize=400)


        
        #TÍTULO DO FRAME
        self.find_title_label = customtkinter.CTkLabel(
            self.clients_frame, text="Gerenciamento de clientes", font=customtkinter.CTkFont( size=22, weight="bold"))
        self.find_title_label.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="new")

        #Frame com filtros
        # create tabview
        self.tabview = customtkinter.CTkTabview(self.clients_frame, width=600)
        self.tabview.grid(row=2, column=0, padx=15, pady=15, sticky="nsew")
        self.tabview.add("Ativos")
        self.tabview.add("Inativos")
        self.tabview.add("Todos")
        self.tabview.tab("Ativos").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Inativos").grid_columnconfigure(0, weight=1)

        # Geração de lista de todos os clientes
        self.scrollable_radiobutton_frame = ScrollableRadiobuttonFrame(master=self.tabview.tab("Todos"), 
                                                                       command=self.radiobutton_frame_event,
                                                                       item_list=[f"{i+1} - {CLIENTS.clients[i].name}" for i in range(len(CLIENTS.clients))])
        self.scrollable_radiobutton_frame.grid(row=0, column=0, padx=0, pady=5, sticky="n")
        self.scrollable_radiobutton_frame.configure(width = 600, height= 200, fg_color = "transparent")
        self.scrollable_radiobutton_frame.remove_item("item 3")

        # Geração de lista de clientes Ativos
        self.scrollable_radiobutton_frame = ScrollableRadiobuttonFrame(master=self.tabview.tab("Ativos"), 
                                                                       command=self.radiobutton_frame_event,
                                                                       item_list=[f"{i+1} - {CLIENTS.actived_clients[i].name}" for i in range(len(CLIENTS.actived_clients))])
        self.scrollable_radiobutton_frame.grid(row=0, column=0, padx=0, pady=5, sticky="n")
        self.scrollable_radiobutton_frame.configure(width = 600, height= 200, fg_color = "transparent")
        self.scrollable_radiobutton_frame.remove_item("item 3")

        # Geração de lista de clientes Inativos
        self.scrollable_radiobutton_frame = ScrollableRadiobuttonFrame(master=self.tabview.tab("Inativos"), 
                                                                       command=self.radiobutton_frame_event,
                                                                       item_list=[f"{i+1} - {CLIENTS.inactived_clients[i].name}" for i in range(len(CLIENTS.inactived_clients))])
        self.scrollable_radiobutton_frame.grid(row=0, column=0, padx=0, pady=5, sticky="n")
        self.scrollable_radiobutton_frame.configure(width = 600, height= 200, fg_color = "transparent")
        self.scrollable_radiobutton_frame.remove_item("item 3")


        #------------------------------------#
        ###### ====BUSCA DE CLIENTES====######
        self.results_frame = customtkinter.CTkFrame(
            self, corner_radius=5)
        self.results_frame.grid(row=0, column=2, padx=10,
                                pady=10, rowspan=4, sticky="nsew")
        self.results_frame.grid_rowconfigure(4, weight=1)


        #TÍTULO DO FRAME
        self.find_title_label = customtkinter.CTkLabel(
            self.results_frame, text="Busca em diário", font=customtkinter.CTkFont(size=22, weight="bold"))
        self.find_title_label.grid(row=0, column=0, padx=20, pady=(20, 0))

        # BOTÃO DE SELAÇÃO DO DIÁRIO
        self.button_pdf_find = customtkinter.CTkButton(
            self.results_frame, command=browse_pdf, text='Selecionar Diário')
        self.button_pdf_find.grid(row=1, column=0, padx=20, pady=10)

        # BOTÃO DE BUSCA
        if NUM_SEARCHES == 0:
            self.button_search = customtkinter.CTkButton(
                self.results_frame, command=lambda: seek_client(self), text='Buscar clientes')
            self.button_search.grid(row=2, column=0, padx=20, pady=10)

        #TÍTULO CAIXA DE TEXTO
        self.results_title_label = customtkinter.CTkLabel(
            self.results_frame, text="Resultados da busca:", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.results_title_label.grid(row=3, column=0, padx=20, pady=(20, 0))

        # CAIXA DE TEXTO
        self.textbox = customtkinter.CTkTextbox(
            self.results_frame, width=400, corner_radius=5)
        self.textbox.grid(row=4, column=0, padx=(
            20, 20), pady=(0, 0), sticky="nsew")

        # BARRA DE PROGRESSO
        self.progressbar = customtkinter.CTkProgressBar(
            self.results_frame)
        self.progressbar.grid(row=5, column=0, padx=(
            20, 20), pady=(10, 20), sticky="ew")
        
        # BOTÃO DE CONTATAR
        if NUM_SEARCHES == 0:
            self.contact_button = customtkinter.CTkButton(
                self.results_frame, text='Contatar Clientes')
            self.contact_button.grid(row=6, column=0, padx=20, pady=10)

        ################################
        
        
        # Valores Default
        self.appearance_mode_optionemenu.set("System")
        self.progressbar.set(0)

    # ==========FUNÇÕES==========

    # Definir o tema da janela
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    # ATualizar Barra de Progresso
    def update_progress_bar(self, value):
        self.progressbar.set(value)
        self.update()

    # Atualizar escrita do botão de busca
    def update_search_button(self):
        global NUM_SEARCHES
        if NUM_SEARCHES > 0:
            self.button_search.configure(text="Nova Busca")
        return

    def radiobutton_frame_event(self):
        print(f"radiobutton frame modified: {self.scrollable_radiobutton_frame.get_checked_item()}")
    # ===========================

### MAIN ###
if __name__ == "__main__":
    #LER OS ARQUIVOS DO CSV
    fill_list()
    CLIENTS.print()
    CLIENTS.get_searchable_list()
    
    app = App()
    app.mainloop()
