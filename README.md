# 📦 Controle de Estoque com Interface Gráfica (Tkinter + SQLite + ttkbootstrap)

Este é um sistema simples de **controle de estoque** desenvolvido com **Python**, utilizando **Tkinter** para a interface gráfica e **SQLite** para o armazenamento dos dados. O visual é melhorado com o uso da biblioteca `ttkbootstrap`, proporcionando uma aparência moderna e responsiva.

## 🚀 Funcionalidades

- ✅ Adicionar peças ao estoque com nome, tamanho e quantidade
- 🔍 Pesquisar peças por nome e/ou tamanho
- 📋 Visualizar estoque completo em uma tabela interativa
- 📝 Atualizar a quantidade de uma peça existente
- ❌ Remover peças do estoque
- 💾 Armazenamento local em banco de dados SQLite (pasta do usuário)

## 🖥️ Interface

A interface é dividida em duas abas:

- **Cadastro**: onde você adiciona novas peças ao estoque.
- **Estoque**: exibe a lista atual de itens cadastrados, com opções de busca, atualização e remoção.

## 🛠️ Requisitos

Antes de executar o sistema, certifique-se de ter instalado os seguintes pacotes:

```bash
pip install ttkbootstrap
