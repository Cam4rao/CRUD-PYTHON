import streamlit as st # type: ignore
import pandas as pd # type: ignore
import os
from datetime import datetime

# Arquivos de dados
ARQ_LIVROS = "livros.csv"
ARQ_USUARIOS = "usuarios.csv"
ARQ_EMPRESTIMOS = "emprestimos.csv"

# Tipos imutáveis
TIPOS_USUARIO = ("Aluno", "Professor", "Visitante")


# Funções para carregar e salvar dados
def carregar_dados():
    if os.path.exists(ARQ_LIVROS):
        st.session_state.livros = pd.read_csv(ARQ_LIVROS)
    else:
        st.session_state.livros = pd.DataFrame(columns=["titulo", "autor", "ano", "isbn", "categoria"])

    if os.path.exists(ARQ_USUARIOS):
        st.session_state.usuarios = pd.read_csv(ARQ_USUARIOS)
    else:
        st.session_state.usuarios = pd.DataFrame(columns=["id", "nome", "email", "tipo"])

    if os.path.exists(ARQ_EMPRESTIMOS):
        st.session_state.emprestimos = pd.read_csv(ARQ_EMPRESTIMOS)
    else:
        st.session_state.emprestimos = pd.DataFrame(columns=["isbn", "id_usuario", "data_emprestimo"])


def salvar_dados():
    st.session_state.livros.to_csv(ARQ_LIVROS, index=False)
    st.session_state.usuarios.to_csv(ARQ_USUARIOS, index=False)
    st.session_state.emprestimos.to_csv(ARQ_EMPRESTIMOS, index=False)


# Interface principal
def menu_principal():
    st.title("Biblioteca Digital")

    menu = st.sidebar.selectbox(
        "Escolha uma opção",
        [
            "Cadastrar Livro",
            "Cadastrar Usuário",
            "Listar Livros",
            "Buscar Livro",
            "Realizar Empréstimo",
            "Ver Empréstimos Ativos"
        ]
    )

    if menu == "Cadastrar Livro":
        cadastrar_livro()
    elif menu == "Cadastrar Usuário":
        cadastrar_usuario()
    elif menu == "Listar Livros":
        listar_livros()
    elif menu == "Buscar Livro":
        buscar_livro()
    elif menu == "Realizar Empréstimo":
        emprestar_livro()
    elif menu == "Ver Empréstimos Ativos":
        listar_emprestimos()


# Funcionalidades
def cadastrar_livro():
    st.header("Cadastro de Livro")
    with st.form("form_livro"):
        titulo = st.text_input("Título")
        autor = st.text_input("Autor")
        ano = st.text_input("Ano de Publicação")
        isbn = st.text_input("ISBN")
        categoria = st.text_input("Categoria")
        submitted = st.form_submit_button("Cadastrar")

        if submitted:
            if isbn in st.session_state.livros["isbn"].values:
                st.error("Este ISBN já está cadastrado.")
            else:
                novo = pd.DataFrame([{
                    "titulo": titulo,
                    "autor": autor,
                    "ano": ano,
                    "isbn": isbn,
                    "categoria": categoria
                }])
                st.session_state.livros = pd.concat([st.session_state.livros, novo], ignore_index=True)
                salvar_dados()
                st.success("Livro cadastrado com sucesso.")


def cadastrar_usuario():
    st.header("Cadastro de Usuário")
    with st.form("form_usuario"):
        nome = st.text_input("Nome")
        email = st.text_input("E-mail")
        tipo = st.selectbox("Tipo", TIPOS_USUARIO)
        submitted = st.form_submit_button("Cadastrar")

        if submitted:
            if email in st.session_state.usuarios["email"].values:
                st.error("E-mail já cadastrado.")
            else:
                novo_id = str(len(st.session_state.usuarios) + 1)
                novo = pd.DataFrame([{
                    "id": novo_id,
                    "nome": nome,
                    "email": email,
                    "tipo": tipo
                }])
                st.session_state.usuarios = pd.concat([st.session_state.usuarios, novo], ignore_index=True)
                salvar_dados()
                st.success("Usuário cadastrado com sucesso.")


def listar_livros():
    st.header("Lista de Livros")
    if st.session_state.livros.empty:
        st.info("Nenhum livro cadastrado.")
    else:
        st.dataframe(st.session_state.livros)


def buscar_livro():
    st.header("Buscar Livro")

    criterio = st.radio("Buscar por", ["Titulo", "Autor", "Categoria"])
    termo = st.text_input(f"Digite o {criterio.lower()}")

    if termo:
        filtro = criterio.lower()
        resultado = st.session_state.livros[
            st.session_state.livros[filtro].str.lower().str.contains(termo.lower())
        ]
        if resultado.empty:
            st.warning("Nenhum livro encontrado.")
        else:
            st.dataframe(resultado)


def emprestar_livro():
    st.header("Realizar Empréstimo")

    isbn = st.text_input("ISBN do livro")
    id_usuario = st.text_input("ID do usuário")

    if st.button("Emprestar"):
        if isbn not in st.session_state.livros["isbn"].values:
            st.error("Livro não encontrado.")
            return

        if id_usuario not in st.session_state.usuarios["id"].values:
            st.error("Usuário não encontrado.")
            return

        if isbn in st.session_state.emprestimos["isbn"].values:
            st.warning("Este livro já está emprestado.")
            return

        novo = pd.DataFrame([{
            "isbn": isbn,
            "id_usuario": id_usuario,
            "data_emprestimo": datetime.today().strftime('%Y-%m-%d')
        }])
        st.session_state.emprestimos = pd.concat([st.session_state.emprestimos, novo], ignore_index=True)
        salvar_dados()
        st.success("Empréstimo realizado com sucesso.")


def listar_emprestimos():
    st.header("Empréstimos Ativos")
    if st.session_state.emprestimos.empty:
        st.info("Nenhum empréstimo registrado.")
    else:
        st.dataframe(st.session_state.emprestimos)


def exportar_emprestimos():
    base1 = pd.read_csv("emprestimos.csv")
    base2 = pd.read_csv("livros.csv")
    base3 = pd.read_csv("usuarios.csv")
    
    base_merge = base1.merge(base2, on="isbn", how='left')
    base_exportar = base_merge.merge(base3, left_on="id_usuario", right_on="id", how='left')

    csv = base_exportar.to_csv(index=False).encode('utf-8')
    
    st.download_button(
        label = "Exportar dados",
        data = csv,
        file_name="base_biblioteca.csv",
        mime="text/csv"
    )


if __name__ == "__main__":
    if "livros" not in st.session_state:
        carregar_dados()
    menu_principal()
    exportar_emprestimos()
