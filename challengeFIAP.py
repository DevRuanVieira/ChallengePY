import pandas as pd
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import random


try:
    banco_dados = pd.read_csv('pilotos_formula_e.csv', index_col='ID')
    proximo_id = banco_dados.index.max() + 1
except FileNotFoundError:
    banco_dados = pd.DataFrame(columns=['nome', 'equipe', 'data_nascimento', 'local_nascimento', 'classificacao', 'vitorias', 'podios'])
    proximo_id = 1


def salvar_banco_dados():
    banco_dados.to_csv('pilotos_formula_e.csv')


def insere_piloto(nome, equipe, data_nascimento, local_nascimento, classificacao, vitorias, podios):
    global proximo_id, banco_dados
    novo_piloto = {
        'nome': nome,
        'equipe': equipe,
        'data_nascimento': data_nascimento,
        'local_nascimento': local_nascimento,
        'classificacao': classificacao,
        'vitorias': vitorias,
        'podios': podios
    }
    banco_dados.loc[proximo_id] = novo_piloto
    proximo_id += 1
    salvar_banco_dados()
    messagebox.showinfo("Sucesso", "Piloto inserido com sucesso!")


def adicionar_piloto():
    def salvar_dados():
        nome = entry_nome.get()
        equipe = entry_equipe.get()
        data_nascimento = entry_data_nascimento.get()
        local_nascimento = entry_local_nascimento.get()
        classificacao = entry_classificacao.get()
        vitorias = entry_vitorias.get()
        podios = entry_podios.get()
        
        if nome and equipe and data_nascimento and local_nascimento and classificacao.isdigit():
            classificacao = int(classificacao)
            vitorias = int(vitorias) if vitorias.isdigit() else 0
            podios = int(podios) if podios.isdigit() else 0
            insere_piloto(nome, equipe, data_nascimento, local_nascimento, classificacao, vitorias, podios)
            janela_adicionar.destroy()  
        else:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos obrigatórios corretamente.")

    
    janela_adicionar = tk.Toplevel()
    janela_adicionar.title("Adicionar Piloto")

 
    tk.Label(janela_adicionar, text="Nome").grid(row=0, column=0, padx=10, pady=5)
    entry_nome = tk.Entry(janela_adicionar)
    entry_nome.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(janela_adicionar, text="Equipe").grid(row=1, column=0, padx=10, pady=5)
    entry_equipe = tk.Entry(janela_adicionar)
    entry_equipe.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(janela_adicionar, text="Data de Nascimento").grid(row=2, column=0, padx=10, pady=5)
    entry_data_nascimento = tk.Entry(janela_adicionar)
    entry_data_nascimento.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(janela_adicionar, text="Local de Nascimento").grid(row=3, column=0, padx=10, pady=5)
    entry_local_nascimento = tk.Entry(janela_adicionar)
    entry_local_nascimento.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(janela_adicionar, text="Classificação").grid(row=4, column=0, padx=10, pady=5)
    entry_classificacao = tk.Entry(janela_adicionar)
    entry_classificacao.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(janela_adicionar, text="Vitórias").grid(row=5, column=0, padx=10, pady=5)
    entry_vitorias = tk.Entry(janela_adicionar)
    entry_vitorias.grid(row=5, column=1, padx=10, pady=5)

    tk.Label(janela_adicionar, text="Pódios").grid(row=6, column=0, padx=10, pady=5)
    entry_podios = tk.Entry(janela_adicionar)
    entry_podios.grid(row=6, column=1, padx=10, pady=5)


    tk.Button(janela_adicionar, text="Salvar", command=salvar_dados).grid(row=7, column=0, columnspan=2, pady=10)


def exibir_dados_piloto(piloto):
    janela_detalhes = tk.Toplevel()
    janela_detalhes.title(f"Dados do Piloto - {piloto['nome']}")

  
    info_piloto = f"""
    Nome: {piloto['nome']}
    Equipe: {piloto['equipe']}
    Data de Nascimento: {piloto['data_nascimento']}
    Local de Nascimento: {piloto['local_nascimento']}
    Classificação: {piloto['classificacao']}
    Vitórias: {piloto['vitorias']}
    Pódios: {piloto['podios']}
    """
    label = tk.Label(janela_detalhes, text=info_piloto, justify="left", font=("Arial", 12))
    label.pack(padx=10, pady=10)


def consulta_piloto():
    if banco_dados.empty:
        messagebox.showinfo("Informação", "Não há pilotos cadastrados.")
        return

    
    janela_consulta = tk.Toplevel()
    janela_consulta.title("Consultar Piloto")

  
    label = tk.Label(janela_consulta, text="Clique em um piloto para ver seus dados:", font=("Arial", 12))
    label.pack(pady=10)

  
    for idx, piloto in banco_dados.iterrows():
        nome_piloto = f"{piloto['nome']} (ID: {idx})"
        botao = ttk.Button(janela_consulta, text=nome_piloto, command=lambda p=piloto: exibir_dados_piloto(p))
        botao.pack(pady=5)


def exibir_todos_pilotos():
    if banco_dados.empty:
        messagebox.showinfo("Informação", "Não há pilotos cadastrados.")
        return
    
    
    janela_tabela = tk.Toplevel()
    janela_tabela.title("Todos os Pilotos")

   
    colunas = ["ID", "Nome", "Equipe", "Data de Nascimento", "Local de Nascimento", "Classificação", "Vitórias", "Pódios"]
    tree = ttk.Treeview(janela_tabela, columns=colunas, show="headings")
    tree.pack(fill=tk.BOTH, expand=True)


    for coluna in colunas:
        tree.heading(coluna, text=coluna)
        tree.column(coluna, anchor='center')

 
    for idx, piloto in banco_dados.iterrows():
        tree.insert("", "end", values=(idx, piloto['nome'], piloto['equipe'], piloto['data_nascimento'],
                                       piloto['local_nascimento'], piloto['classificacao'], piloto['vitorias'], piloto['podios']))

  
    scrollbar = ttk.Scrollbar(janela_tabela, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")


def listar_pilotos_por_equipe(equipe):
    pilotos = banco_dados[banco_dados['equipe'] == equipe]
    if pilotos.empty:
        messagebox.showinfo("Informação", f"Não há pilotos na equipe {equipe}.")
        return
    
  
    janela_equipes = tk.Toplevel()
    janela_equipes.title(f"Pilotos da Equipe {equipe}")

  
    colunas = ["ID", "Nome", "Equipe", "Data de Nascimento", "Local de Nascimento", "Classificação", "Vitórias", "Pódios"]
    tree = ttk.Treeview(janela_equipes, columns=colunas, show="headings")
    tree.pack(fill=tk.BOTH, expand=True)

   
    for coluna in colunas:
        tree.heading(coluna, text=coluna)
        tree.column(coluna, anchor='center')


    for idx, piloto in pilotos.iterrows():
        tree.insert("", "end", values=(idx, piloto['nome'], piloto['equipe'], piloto['data_nascimento'],
                                       piloto['local_nascimento'], piloto['classificacao'], piloto['vitorias'], piloto['podios']))

    scrollbar = ttk.Scrollbar(janela_equipes, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")


def menu_equipes():
    equipes = banco_dados['equipe'].unique()
    if equipes.size > 0:
       
        janela_equipes = tk.Toplevel()
        janela_equipes.title("Seleção de Equipe")
        
     
        label = tk.Label(janela_equipes, text="Selecione uma equipe para visualizar os pilotos:")
        label.pack(pady=10)

        for equipe in equipes:
            ttk.Button(janela_equipes, text=equipe, command=lambda e=equipe: listar_pilotos_por_equipe(e)).pack(pady=5)
    else:
        messagebox.showerror("Erro", "Nenhuma equipe encontrada.")


def curiosidades():
    curiosidades_lista = [
        "A Fórmula E é o primeiro campeonato internacional de monopostos totalmente elétricos.",
        "Os carros da Fórmula E podem ir de 0 a 100 km/h em apenas 2.8 segundos.",
        "A Fórmula E foi fundada em 2014 pela FIA para promover a mobilidade elétrica.",
        "A energia usada nas corridas de Fórmula E vem de fontes 100% renováveis.",
        "As corridas da Fórmula E são realizadas em circuitos de rua em algumas das maiores cidades do mundo.",
        "As baterias dos carros da Fórmula E têm uma capacidade de 54 kWh, suficiente para alimentar uma casa por dois dias.",
        "A Fórmula E utiliza o sistema 'FanBoost', onde os fãs podem votar e dar potência extra a seus pilotos favoritos.",
        "A categoria conta com montadoras de renome como Porsche, BMW, Mercedes-Benz, Nissan e Audi.",
    ]

    curiosidade_aleatoria = random.choice(curiosidades_lista)
    
    messagebox.showinfo("Curiosidade sobre a Fórmula E", curiosidade_aleatoria)


def menu():
    janela = tk.Tk()
    janela.title("Sistema de Gerenciamento de Pilotos de Fórmula E")
    
    ttk.Button(janela, text="Adicionar Piloto", command=adicionar_piloto).pack(pady=10)
    ttk.Button(janela, text="Consultar um Piloto", command=consulta_piloto).pack(pady=10)
    ttk.Button(janela, text="Exibir Todos os Pilotos", command=exibir_todos_pilotos).pack(pady=10)
    ttk.Button(janela, text="Listar Equipes", command=menu_equipes).pack(pady=10)
    ttk.Button(janela, text="Curiosidades", command=curiosidades).pack(pady=10)
    ttk.Button(janela, text="Sair", command=janela.quit).pack(pady=10)
    
    janela.mainloop()


menu()
