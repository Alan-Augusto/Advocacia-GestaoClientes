from class_and_functions import *

### APLICAÇÃO ###
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        #Variáveis Globais
        self.state_buttons_client = 'disable'
        self.type_clients_select = ''
        self.select_client =''


        #Configuração da janela
        self.title("Gestão e Busca de Clientes - Campello Castro")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        
        #Importação das imagens
        self.folder_icon = customtkinter.CTkImage(light_image=Image.open(r".\icons\folder_light.png"),
                                                  dark_image=Image.open(r".\icons\folder_dark.png"),
                                                  size=(20,20))
        self.upload_icon = customtkinter.CTkImage(light_image=Image.open(r".\icons\upload_light.png"),
                                                  dark_image=Image.open(r".\icons\upload_dark.png"),
                                                  size=(20,20))
        self.find_icon = customtkinter.CTkImage(light_image=Image.open(r".\icons\find_light.png"),
                                                  dark_image=Image.open(r".\icons\find_dark.png"),
                                                  size=(20,20))
        
        self.add_icon = customtkinter.CTkImage(light_image=Image.open(r".\icons\add_light.png"),
                                                  dark_image=Image.open(r".\icons\add_dark.png"),
                                                  size=(20,20))
        self.edit_Icon = customtkinter.CTkImage(light_image=Image.open(r".\icons\edit_light.png"),
                                                  dark_image=Image.open(r".\icons\edit_dark.png"),
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

        #Botão de Backup dados
        self.button_insert_client = customtkinter.CTkButton(
            self.sidebar_frame, command=lambda: backup(), text='Nova base de dados', image=self.folder_icon, width=150, height=30, anchor='w')
        self.button_insert_client.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")


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
        self.tabview = customtkinter.CTkTabview(self.tableframe, height=800)
        self.tabview.grid(row=0, column=0, padx=15, pady=15)
        self.tabview.add("Ativos")
        self.tabview.add("Inativos")
        self.tabview.add("Todos")
        self.tabview.grid_rowconfigure(1, weight=1)


        

        # Geração de lista de todos os clientes
        self.scrollable_radiobutton_frame_all = ScrollableRadiobuttonFrame( master=self.tabview.tab("Todos"), height=490,
                                                                           command=lambda: self.defClient_select('all'),
                                                                           item_list=[f"{CLIENTS.clients[i].name}" for i in range(len(CLIENTS.clients))])
        self.scrollable_radiobutton_frame_all.grid(row=0, column=0, padx=0, pady=5, sticky="nsew")
        self.scrollable_radiobutton_frame_all.configure(width = 600, fg_color = "transparent")
        self.scrollable_radiobutton_frame_all.remove_item("item 3")

        # Geração de lista de clientes Ativos
        self.scrollable_radiobutton_frame_actived = ScrollableRadiobuttonFrame( master=self.tabview.tab("Ativos"), height=490,
                                                                               command=lambda: self.defClient_select('actived'),
                                                                               item_list=[f"{CLIENTS.actived_clients[i].name}" for i in range(len(CLIENTS.actived_clients))])
        self.scrollable_radiobutton_frame_actived.grid(row=0, column=0, padx=0, pady=5, sticky="nsew")
        self.scrollable_radiobutton_frame_actived.configure(width = 600, fg_color = "transparent")
        self.scrollable_radiobutton_frame_actived.remove_item("item 3")

        # Geração de lista de clientes Inativos
        self.scrollable_radiobutton_frame_inactived = ScrollableRadiobuttonFrame( master=self.tabview.tab("Inativos"), height=490,
                                                                                 command=lambda: self.defClient_select('inactived'),
                                                                                 item_list=[f"{CLIENTS.inactived_clients[i].name}" for i in range(len(CLIENTS.inactived_clients))])
        self.scrollable_radiobutton_frame_inactived.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        self.scrollable_radiobutton_frame_inactived.configure(width = 600, fg_color = "transparent")
        self.scrollable_radiobutton_frame_inactived.remove_item("item 3")

        #FRAME-BOTÕES DE AÇÕES DE CLIENTES
        self.frame_actions_clients = customtkinter.CTkFrame(
            self.clients_frame, corner_radius=5, fg_color="transparent")
        #fg_color="transparent"
        self.frame_actions_clients.grid(row=3, column=0, padx=10,
                                pady=10, sticky="s")

        #Botão de inserir do Cliente
        self.button_insert_client = customtkinter.CTkButton(
            self.frame_actions_clients, command=lambda: add_client(self,'add'), text='', image=self.add_icon, width=150, height=30)
        self.button_insert_client.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        #Botão de editar do Cliente
        self.button_insert_client = customtkinter.CTkButton(
            self.frame_actions_clients, command=lambda: add_client(self, 'edit'), text='', image=self.edit_Icon, width=150, height=30)
        self.button_insert_client.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        #Botão de informações cliente
        self.button_info_client = customtkinter.CTkButton(
            self.frame_actions_clients, command=self.open_dialog_event, text='', image=self.info_icon, width=150, height=30)
        self.button_info_client.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")

        #Botão de Desativar/Ativar Cliente
        self.button_hide_client = customtkinter.CTkButton(
            self.frame_actions_clients, command=lambda: inactived_client(self, self.select_client), text='', image=self.hide_icon, width=150, height=30)
        self.button_hide_client.grid(row=0, column=3, padx=5, pady=5, sticky="nsew")

        #Botão de Apagar Cliente
        self.button_remove_client = customtkinter.CTkButton(
            self.frame_actions_clients, command=lambda: remove_client(self, self.select_client, mode='delete'), text='', image=self.remove_icon, width=150, height=30)
        self.button_remove_client.grid(row=0, column=4, padx=5, pady=5, sticky="nsew")

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
            self.results_frame,width=400, corner_radius=5)  
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
        
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
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

    #Abrir vizualização de clientes
    def open_dialog_event(self):
        if self.select_client:
            client_info = CLIENTS.get_client_info(self.select_client, type='text')
            self.show_client_info_popup(client_info)
        else:
            # Caso nenhum cliente esteja selecionado, exiba uma mensagem de aviso
            mssg(title='Opa!', text='Nenhum cliente seleiconado :(\n Selecione algum cliente para ver as informações', dimension='360x100')
    
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

    def defClient_select(self, value):
        self.type_clients_select = value
        self.state_buttons_client = 'enable'
        
        if(self.type_clients_select == 'all'):
            self.select_client = self.scrollable_radiobutton_frame_all.get_checked_item()
        
        if(self.type_clients_select == 'actived'):
            self.select_client = self.scrollable_radiobutton_frame_actived.get_checked_item()

        if(self.type_clients_select == 'inactived'):
            self.select_client = self.scrollable_radiobutton_frame_inactived.get_checked_item()

        print('Cliente selecionado: '+ self.select_client)
    
    def insert_client(self):
        self.button_info_client.configure(fg_collor= "blue", disabled='false')
    
    def show_client_info_popup(self, client_info):
        print(client_info)
        mssg(title=self.select_client, text=client_info, dimension='550x300')

    def on_close(self):
        result = save_alert(self)
        
        if result is None:  # Clicou em "Cancelar"
            return
        elif result:  # Clicou em "Sim"
            self.save_changes()
            
        self.root.destroy()
    # ===========================

### MAIN ###
if __name__ == "__main__":
    #LER OS ARQUIVOS DO CSV
    csv_order_by_name()
    fill_list()
    CLIENTS.print()
    CLIENTS.get_searchable_list()
    
    app = App()
    app.mainloop()
