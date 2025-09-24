# Desafio de Estágio em IA e Dados - Jacto

Este repositório contém as soluções desenvolvidas para o processo seletivo de estágio na área de Inteligência Artificial e Dados, promovido pela **Jacto**.

Os três desafios propostos foram resolvidos utilizando Python e um conjunto de ferramentas selecionadas para otimizar cada tarefa, demonstrando habilidades em análise de dados, desenvolvimento de backend e machine learning.

## Tecnologias Utilizadas

* **Linguagem:** Python
* **Análise de Dados:** Pandas, Matplotlib, Seaborn
* **API Backend:** FastAPI, SQLAlchemy, Uvicorn
* **Inteligência Artificial:** TensorFlow, Keras
* **Ambientes:** Google Colab e Visual Studio Code

## Estrutura do Repositório

* **/ (Raiz)**
    * `desafio1_jacto.ipynb`: Notebook com a análise exploratória.
    * `desafio3_jacto.ipynb`: Notebook com o modelo de IA.
    * `cars_data.csv`: Dataset para o Desafio 1.
    * `dataset.zip`: Dataset para o Desafio 3.
    * `README.md`: Este arquivo.
* **/desafio2_api_rest/**
    * `main.py`: Código-fonte da API REST.

## Desafios e Como Executar

Aqui estão a descrição e o guia de execução para cada desafio.

### **Desafio 1: Análise de Dados e Visualização**

**Descrição:** Análise de um dataset de carros para identificar os 10 fabricantes com mais modelos e a proporção de seus veículos por tipo de combustível. O notebook é autossuficiente e busca os dados diretamente do repositório.

**Como Executar:**

1.  Abra o notebook **`desafio1_jacto.ipynb`** diretamente no Google Colab.
2.  Execute a primeira célula de código. Ela irá clonar este repositório do GitHub para o ambiente do Colab, dando acesso ao `cars_data.csv`.
3.  Execute as células seguintes em sequência para gerar a análise e o gráfico.

   ### **Desafio 2: API REST com Banco de Dados Relacional e Não-Relacional**

**Descrição:** Foi desenvolvida uma API REST completa com operações CRUD (Create, Read, Update, Delete). A API gerencia:
* **Carros:** Usando um banco de dados **relacional (SQLite)**.
* **Revisões dos Carros:** Usando um banco de dados **não-relacional (arquivo JSON)**.

**Como Executar:**

1.  Clone **este** repositório e navegue até a pasta do desafio:
    ```bash
    git clone [https://github.com/AlisonCarv/desafiosJacto.git](https://github.com/AlisonCarv/desafiosJacto.git)
    cd desafiosJacto/desafio2_api_rest
    ```

2.  Crie e ative um ambiente virtual. Este passo é crucial para isolar as dependências do projeto.
    ```bash
    # Criar o ambiente
    python -m venv venv

    # Ativar no Windows
    .\venv\Scripts\activate

    # Ativar no macOS/Linux
    source venv/bin/activate
    ```

3.  Instale as bibliotecas necessárias:
    ```bash
    pip install fastapi "uvicorn[standard]" sqlalchemy
    ```

4.  Inicie o servidor da API:
    ```bash
    uvicorn main:app --reload
    ```

5.  Teste a API:
    * Abra seu navegador e acesse **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**.
    * Use a interface interativa do Swagger para testar todos os endpoints.

### **Desafio 3: Implementação de Ferramenta de IA (Agricultura Digital)**

**Descrição:** O desafio foi implementar uma ferramenta de IA para um caso de uso em agricultura digital. Foi criado um modelo de visão computacional, usando *Transfer Learning*, para classificar imagens de folhas de plantas como "saudáveis" ou "doentes".

**Como Executar:**

1.  Certifique-se de que o arquivo **`dataset.zip`** está na raiz do repositório no GitHub.
2.  Abra o notebook **`desafio3_jacto.ipynb`** diretamente no Google Colab.
3.  **Importante:** Ative o ambiente de GPU para acelerar o treinamento (`Ambiente de execução` > `Alterar o tipo de ambiente de execução` > `GPU`).
4.  Execute as células do notebook em sequência. A primeira célula irá clonar este repositório para o ambiente do Colab, dando acesso ao `dataset.zip`, e as seguintes irão treinar e testar o modelo.

---

## Autor

Desenvolvido por **Álison Christian Rebouças Vidal de Carvalho**.
