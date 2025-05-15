import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
from ttkbootstrap import Style

# Definir caminho do banco de dados na pasta do usuário
APP_DIR = os.path.expanduser("~/.controle_estoque")
DB_PATH = os.path.join(APP_DIR, "estoque.db")

if not os.path.exists(APP_DIR):
    os.makedirs(APP_DIR)

# Função para conectar ao banco de dados
def conectar():
    return sqlite3.connect(DB_PATH)

# Função para executar uma query no banco de dados com suporte a transações
def executar_query(query, params=(), fetch=False):
    try:
        conn = conectar()
        c = conn.cursor()
        c.execute(query, params)
        if fetch:
            result = c.fetchall()
        else:
            result = None
        conn.commit()
        return result
    except sqlite3.Error as e:
        messagebox.showerror("Erro no Banco de Dados", f"Ocorreu um erro: {e}")
    finally:
        conn.close()

# Criar tabela de estoque
executar_query('''
    CREATE TABLE IF NOT EXISTS estoque (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        tamanho TEXT NOT NULL,
        quantidade INTEGER NOT NULL
    )
''')

# Função para atualizar a lista de estoque
def atualizar_lista():
    tree.delete(*tree.get_children())  # Limpar a árvore de forma mais eficiente
    rows = executar_query("SELECT * FROM estoque ORDER BY nome, tamanho", fetch=True)
    for row in rows:
        tree.insert("", "end", values=row)

# Função para adicionar uma peça ao estoque
def adicionar_peca():
    nome = entry_nome.get().strip()
    tamanho = combo_tamanho.get().strip()
    quantidade = entry_quantidade.get().strip()
    
    if not nome or not tamanho or not quantidade.isdigit():
        messagebox.showerror("Erro", "Preencha todos os campos corretamente.")
        return
    
    quantidade = int(quantidade)
    resultado = executar_query(
        "SELECT id, quantidade FROM estoque WHERE nome = ? AND tamanho = ?",
        (nome, tamanho),
        fetch=True
    )
    
    if resultado:
        novo_total = resultado[0][1] + quantidade
        executar_query("UPDATE estoque SET quantidade = ? WHERE id = ?", (novo_total, resultado[0][0]))
    else:
        executar_query("INSERT INTO estoque (nome, tamanho, quantidade) VALUES (?, ?, ?)", (nome, tamanho, quantidade))
    
    messagebox.showinfo("Sucesso", "Estoque atualizado!")
    atualizar_lista()
    # Limpar campos após adicionar
    entry_nome.delete(0, tk.END)
    combo_tamanho.set('')
    entry_quantidade.delete(0, tk.END)

# Função para remover uma peça do estoque
def remover_peca():
    item_selecionado = tree.selection()
    if not item_selecionado:
        messagebox.showerror("Erro", "Selecione uma peça para remover.")
        return
    
    id_peca = tree.item(item_selecionado, "values")[0]
    executar_query("DELETE FROM estoque WHERE id = ?", (id_peca,))
    messagebox.showinfo("Sucesso", "Peça removida com sucesso!")
    atualizar_lista()

# Função para atualizar uma peça no estoque
def atualizar_peca():
    item_selecionado = tree.selection()
    if not item_selecionado:
        messagebox.showerror("Erro", "Selecione uma peça para atualizar.")
        return
    
    id_peca = tree.item(item_selecionado, "values")[0]
    nova_quantidade = entry_nova_quantidade.get().strip()
    
    if not nova_quantidade.isdigit():
        messagebox.showerror("Erro", "Digite uma quantidade válida.")
        return
    
    nova_quantidade = int(nova_quantidade)
    executar_query("UPDATE estoque SET quantidade = ? WHERE id = ?", (nova_quantidade, id_peca))
    messagebox.showinfo("Sucesso", "Quantidade atualizada com sucesso!")
    atualizar_lista()
    entry_nova_quantidade.delete(0, tk.END)

# Função para pesquisar peças no estoque
def pesquisar_peca():
    nome_pesquisa = entry_pesquisa_nome.get().strip()
    tamanho_pesquisa = entry_pesquisa_tamanho.get().strip()
    
    tree.delete(*tree.get_children())  # Limpar a árvore de forma mais eficiente
    
    rows = executar_query(
        "SELECT * FROM estoque WHERE nome LIKE ? AND tamanho LIKE ? ORDER BY nome, tamanho",
        (f"%{nome_pesquisa}%", f"%{tamanho_pesquisa}%"),
        fetch=True
    )
    for row in rows:
        tree.insert("", "end", values=row)

# Criando a interface com abas
style = Style(theme="cosmo")  # Escolha um tema moderno
tk_root = style.master
tk_root.title("Controle de Estoque")
tk_root.geometry("1000x800")
tk_root.resizable(True, True)

notebook = ttk.Notebook(tk_root)
notebook.pack(fill='both', expand=True, padx=20, pady=20)

# Aba de Cadastro
aba_cadastro = ttk.Frame(notebook)
notebook.add(aba_cadastro, text="Cadastro")

# Aba de Estoque
aba_estoque = ttk.Frame(notebook)
notebook.add(aba_estoque, text="Estoque")

# Cadastro de Peças
frame_cadastro = ttk.Frame(aba_cadastro)
frame_cadastro.pack(pady=30, padx=30)

ttk.Label(frame_cadastro, text="Nome da Peça:", font=("Helvetica", 14)).grid(row=0, column=0, padx=15, pady=15, sticky="w")
entry_nome = ttk.Entry(frame_cadastro, width=30, font=("Helvetica", 14))
entry_nome.grid(row=0, column=1, padx=15, pady=15)

ttk.Label(frame_cadastro, text="Tamanho:", font=("Helvetica", 14)).grid(row=1, column=0, padx=15, pady=15, sticky="w")
combo_tamanho = ttk.Combobox(
    frame_cadastro, 
    values=["PP","P", "M", "G", "GG", "UNICO"], 
    width=5, 
    font=("Helvetica", 14), 
    state="readonly"  # Desativa a edição manual
)
combo_tamanho.grid(row=1, column=1, padx=15, pady=15)

ttk.Label(frame_cadastro, text="Quantidade:", font=("Helvetica", 14)).grid(row=2, column=0, padx=15, pady=15, sticky="w")
entry_quantidade = ttk.Entry(frame_cadastro, width=10, font=("Helvetica", 14))
entry_quantidade.grid(row=2, column=1, padx=15, pady=15)

# Centralizar o botão de cadastrar
btn_add = ttk.Button(frame_cadastro, text="Adicionar", command=adicionar_peca, style="success.TButton", width=20)
btn_add.grid(row=3, column=0, columnspan=2, pady=25)

# Frame para pesquisa na aba de estoque
frame_pesquisa = ttk.Frame(aba_estoque)
frame_pesquisa.pack(pady=20, padx=20, fill="x")

ttk.Label(frame_pesquisa, text="Pesquisar por Nome:", font=("Helvetica", 14)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
entry_pesquisa_nome = ttk.Entry(frame_pesquisa, width=20, font=("Helvetica", 14))
entry_pesquisa_nome.grid(row=0, column=1, padx=10, pady=10)

ttk.Label(frame_pesquisa, text="Tamanho:", font=("Helvetica", 14)).grid(row=0, column=2, padx=10, pady=10, sticky="w")
entry_pesquisa_tamanho = ttk.Entry(frame_pesquisa, width=10, font=("Helvetica", 14))
entry_pesquisa_tamanho.grid(row=0, column=3, padx=10, pady=10)

btn_pesquisar = ttk.Button(frame_pesquisa, text="Pesquisar", command=pesquisar_peca, style="primary.TButton", width=15)
btn_pesquisar.grid(row=0, column=4, padx=10, pady=10)

# Criando a árvore de exibição do estoque
tree = ttk.Treeview(aba_estoque, columns=("ID", "Nome", "Tamanho", "Quantidade"), show="headings")
tree.heading("ID", text="ID", anchor="center")
tree.heading("Nome", text="Nome", anchor="center")
tree.heading("Tamanho", text="Tamanho", anchor="center")
tree.heading("Quantidade", text="Quantidade", anchor="center")
tree.column("ID", width=50, anchor="center")
tree.column("Nome", width=400, anchor="w")
tree.column("Tamanho", width=150, anchor="center")
tree.column("Quantidade", width=150, anchor="center")
tree.pack(fill="both", expand=True, padx=20, pady=20)

scrollbar = ttk.Scrollbar(aba_estoque, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right", fill="y")

# Frame para os botões de remover e atualizar
frame_botoes = ttk.Frame(aba_estoque)
frame_botoes.pack(pady=20, padx=20, fill="x")

btn_remover = ttk.Button(frame_botoes, text="Remover Peça", command=remover_peca, style="danger.TButton", width=20)
btn_remover.grid(row=0, column=0, padx=10)

ttk.Label(frame_botoes, text="Nova Quantidade:", font=("Helvetica", 14)).grid(row=0, column=1, padx=10)
entry_nova_quantidade = ttk.Entry(frame_botoes, width=10, font=("Helvetica", 14))
entry_nova_quantidade.grid(row=0, column=2, padx=10)

btn_atualizar = ttk.Button(frame_botoes, text="Atualizar Quantidade", command=atualizar_peca, style="info.TButton", width=20)
btn_atualizar.grid(row=0, column=3, padx=10)

atualizar_lista()

# Configurar o fechamento correto da janela
tk_root.protocol("WM_DELETE_WINDOW", lambda: (tk_root.destroy(), sys.exit(0)))  # Fechamento seguro

tk_root.mainloop()