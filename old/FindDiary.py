import pdfplumber
import pandas as pd
import tkinter as tk
import tkinter.filedialog
import tkinter.scrolledtext
import re

clientes_csv_file = 'Clientes.csv'

# Função para selecionar o caminho do arquivo PDF de forma global


def browse_pdf():
    global pdf_file
    pdf_file = tkinter.filedialog.askopenfilename(
        filetypes=[('Arquivos PDF', '*.pdf')])

# Função para buscar os clientes no arquivo PDF


def buscar_palavras():
    # Abrir o arquivo CSV padrão com os clientes a serem buscadas
    df = pd.read_csv(clientes_csv_file)
    # Converter os clientes em uma lista
    clientes = list(df['Clientes'])

    # Abrir o arquivo PDF selecionado pelo usuário e criar um objeto PDFReader
    with pdfplumber.open(pdf_file) as pdf:
        # Obter o número total de páginas do PDF
        num_paginas = len(pdf.pages)
        # Iterar pelas páginas do arquivo PDF
        for page_num, page in enumerate(pdf.pages):
            text = page.extract_text()

            # Exibir o número da página atual do PDF na interface gráfica
            lbl_progresso.config(text=f'Página {page_num+1}/{num_paginas}')
            # Atualizar a interface gráfica
            janela.update_idletasks()

            # Verificar se cada palavra do arquivo CSV está na página atual do PDF
            for cliente in clientes:
                # Utilizar expressão regular para buscar pela palavra completa no texto da página
                matches = re.findall(r'\b{}\b'.format(
                    cliente), text, re.IGNORECASE)
                if matches:
                    for match in matches:
                        resultado.insert(
                            tk.END, f'O cliente "{match}" foi encontrada na página {page_num+1}.\n')


# Criar a janela principal
janela = tk.Tk()
janela.title('Buscar clientes em um diário PDF')

# Criar botão para selecionar o arquivo PDF
botao_pdf = tk.Button(janela, text='Selecionar diário PDF', command=browse_pdf)
botao_pdf.pack(padx=15, pady=10)

# Criar botão para buscar as palavras no arquivo PDF
botao_buscar = tk.Button(
    janela, text='Buscar clientes', command=buscar_palavras)
botao_buscar.pack(padx=15, pady=10)

# Criar área de texto para exibir os resultados da busca
resultado = tkinter.scrolledtext.ScrolledText(janela, height=10, width=70)
resultado.pack(padx=10, pady=10)

# Criar label para exibir o progresso da busca
lbl_progresso = tk.Label(janela, text='')
lbl_progresso.pack(padx=30, pady=10)

# Iniciar a janela principal
janela.mainloop()
