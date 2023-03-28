from class_and_functions import *

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
        
        #Importação das imagens
        self.upload_icon = customtkinter.CTkImage(light_image=Image.open(r".\icons\upload_light.png"),
                                                  dark_image=Image.open(r".\icons\upload_dark.png"),
                                                  size=(20,20))
        self.find_icon = customtkinter.CTkImage(light_image=Image.open(r".\icons\find_light.png"),
                                                  dark_image=Image.open(r".\icons\find_dark.png"),
                                                  size=(20,20))
        self.add_icon = customtkinter.CTkImage(light_image=Image.open(r".\icons\add_light.png"),
                                                  dark_image=Image.open(r".\icons\add_dark.png"),
                                                  size=(20,20))
        self.hide_icon = customtkinter.CTkImage(light_image=Image.open(r".\icons\hide_light.png"),
                                                  dark_image=Image.open(r".\icons\hide_dark.png"),
                                                  size=(20,20))
        self.view_icon = customtkinter.CTkImage(light_image=Image.open(r".\icons\view_light.png"),
                                                  dark_image=Image.open(r".\icons\view_dark.png"),
                                                  size=(20,20))
        self.info_icon = customtkinter.CTkImage(light_image=Image.open(r".\icons\info_light.png"),
                                                  dark_image=Image.open(r".\icons\info_dark.png"),
                                                  size=(20,20))
        self.view_icon = customtkinter.CTkImage(light_image=Image.open(r".\icons\view_light.png"),
                                                  dark_image=Image.open(r".\icons\view_dark.png"),
                                                  size=(20,20))
        self.remove_icon = customtkinter.CTkImage(light_image=Image.open(r".\icons\remove_light.png"),
                                                  dark_image=Image.open(r".\icons\remove_dark.png"),
                                                  size=(20,20))
        self.edit_icon = customtkinter.CTkImage(light_image=Image.open(r".\icons\edit_light.png"),
                                                  dark_image=Image.open(r".\icons\edit_dark.png"),
                                                  size=(20,20))
        

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

        

        ###### ====GESTÃO CLIENTES====######
        self.clients_frame = customtkinter.CTkFrame(
            self, corner_radius=5)
        self.clients_frame.grid(row=0, column=1, padx=10,
                                pady=10, rowspan=4, sticky="nsew")
        self.clients_frame.grid_rowconfigure(1, weight=1)
        self.clients_frame.grid_columnconfigure(0, weight=1, minsize=400)


        
        #TÍTULO DO FRAME
        self.find_title_label = customtkinter.CTkLabel(
            self.clients_frame, text="Gerenciamento de clientes", font=customtkinter.CTkFont( size=22, weight="bold"))
        self.find_title_label.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="new")

        #FRame de tabela
        self.tableframe = customtkinter.CTkFrame(
            self.clients_frame, corner_radius=5, fg_color="transparent")
        self.tableframe.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.tableframe.grid_rowconfigure(1, weight=1)

        #Frame com filtros
        # create tabview
        self.tabview = customtkinter.CTkTabview(self.tableframe, height=600)
        self.tabview.grid(row=0, column=0, padx=15, pady=15)
        self.tabview.add("Ativos")
        self.tabview.add("Inativos")
        self.tabview.add("Todos")
        self.tabview.grid_rowconfigure(1, weight=1)


        

        # Geração de lista de todos os clientes
        self.scrollable_radiobutton_frame = ScrollableRadiobuttonFrame(master=self.tabview.tab("Todos"),height=490,
                                                                       command=self.radiobutton_frame_event,
                                                                       item_list=[f"{i+1} - {CLIENTS.clients[i].name}" for i in range(len(CLIENTS.clients))])
        self.scrollable_radiobutton_frame.grid(row=0, column=0, padx=0, pady=5, sticky="nsew")
        self.scrollable_radiobutton_frame.configure(width = 600, fg_color = "transparent")
        self.scrollable_radiobutton_frame.remove_item("item 3")

        # Geração de lista de clientes Ativos
        self.scrollable_radiobutton_frame = ScrollableRadiobuttonFrame(master=self.tabview.tab("Ativos"), height=490,
                                                                       command=self.radiobutton_frame_event,
                                                                       item_list=[f"{i+1} - {CLIENTS.actived_clients[i].name}" for i in range(len(CLIENTS.actived_clients))])
        self.scrollable_radiobutton_frame.grid(row=0, column=0, padx=0, pady=5, sticky="nsew")
        self.scrollable_radiobutton_frame.configure(width = 600, fg_color = "transparent")
        self.scrollable_radiobutton_frame.remove_item("item 3")

        # Geração de lista de clientes Inativos
        self.scrollable_radiobutton_frame = ScrollableRadiobuttonFrame(master=self.tabview.tab("Inativos"), height=490,
                                                                       command=self.radiobutton_frame_event,
                                                                       item_list=[f"{i+1} - {CLIENTS.inactived_clients[i].name}" for i in range(len(CLIENTS.inactived_clients))])
        self.scrollable_radiobutton_frame.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        self.scrollable_radiobutton_frame.configure(width = 600, fg_color = "transparent")
        self.scrollable_radiobutton_frame.remove_item("item 3")

        #FRAME-BOTÕES DE AÇÕES DE CLIENTES
        self.frame_actions_clients = customtkinter.CTkFrame(
            self.clients_frame, corner_radius=5, fg_color="transparent")
        #fg_color="transparent"
        self.frame_actions_clients.grid(row=3, column=0, padx=10,
                                pady=10, sticky="s")

        #Botão de inserir do Cliente
        self.button_insert_client = customtkinter.CTkButton(
            self.frame_actions_clients, command=self.insert_client, text='', image=self.add_icon, width=150, height=30)
        self.button_insert_client.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        #Botão de informações cliente
        self.button_info_client = customtkinter.CTkButton(
            self.frame_actions_clients, command=self.insert_client, text='', image=self.info_icon, width=150, height=30, state='disabled')
        self.button_info_client.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        #Botão de Desativar/Ativar Cliente
        self.button_hide_client = customtkinter.CTkButton(
            self.frame_actions_clients, command=self.insert_client, text='', image=self.hide_icon, width=150, height=30)
        self.button_hide_client.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")

        #Botão de Apagar Cliente
        self.button_remove_client = customtkinter.CTkButton(
            self.frame_actions_clients, command=self.insert_client, text='', image=self.remove_icon, width=150, height=30)
        self.button_remove_client.grid(row=0, column=3, padx=5, pady=5, sticky="nsew")

        # Redimensiona as colunas dos botões para ocupar o mínimo necessário
        for i in range(4):
            self.frame_actions_clients.grid_columnconfigure(i, minsize=120, weight=1)



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
            self.results_frame, command=self.browse_pdfs, text='', image=self.upload_icon, width=150, height=30)
        self.button_pdf_find.grid(row=1, column=0, padx=20, pady=10)

        # BOTÃO DE BUSCA
        if NUM_SEARCHES == 0:
            self.button_search = customtkinter.CTkButton(
                self.results_frame, command=lambda: seek_client(self), text='',image=self.find_icon, width=150, height=30)
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
                self.results_frame, text='',width=150, height=30 )
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

    def browse_pdfs(self):
        caminho = browse_pdf()
        nome_arquivo = os.path.splitext(os.path.basename(caminho))[0]
        #Selecionar Diário
        button_text=""
        if len(nome_arquivo) <= 17:
            button_text = nome_arquivo
        else:
            button_text = nome_arquivo[0:12]+"..."

        self.button_pdf_find.configure(text=f"{button_text}")

    def radiobutton_frame_event(self):
        print(f"radiobutton frame modified: {self.scrollable_radiobutton_frame.get_checked_item()}")
    
    def insert_client(self):
        self.button_info_client.configure(fg_collor= "blue", disabled='false')
    
    # ===========================

### MAIN ###
if __name__ == "__main__":
    #LER OS ARQUIVOS DO CSV
    fill_list()
    CLIENTS.print()
    CLIENTS.get_searchable_list()
    
    app = App()
    app.mainloop()
