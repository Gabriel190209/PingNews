# PingNews - Site de Notícias em Tempo Real

## Descrição

O **PingNews** é um site dinâmico de coleta e exibição de notícias de diversas fontes, como **G1**, **CNN Brasil**, **UOL** e **Globo**. O site utiliza uma combinação de **scraping**, **resumo automático de textos** (via modelo de **Transformers**), **banco de dados SQLite** e **comunicação em tempo real** com **Socket.IO** para exibir as notícias de forma interativa e rápida.

As notícias são constantemente atualizadas a partir de sites de notícias, resumidas automaticamente e exibidas na interface, permitindo uma navegação eficiente e personalizada.

---

## Tecnologias Utilizadas

- **Flask**: Framework web em Python para o backend, gerenciando rotas, requisições HTTP e a comunicação com o banco de dados.
- **Flask-SocketIO**: Para comunicação bidirecional e em tempo real entre o servidor e o frontend.
- **BeautifulSoup**: Para realizar **web scraping**, coletando as notícias a partir de sites como G1, CNN Brasil, UOL e Globo.
- **Transformers (BART)**: Modelo de **resumo de texto** da biblioteca Hugging Face para resumir automaticamente os artigos coletados.
- **SQLite**: Banco de dados simples para armazenar e recuperar as notícias coletadas, garantindo persistência e evitando a repetição de conteúdo.
- **JavaScript (Vanilla)**: Utilizado para manipulação da interface no frontend, exibindo as notícias em tempo real e aplicando filtros de pesquisa.
- **CSS**: Estilos personalizados para a interface, criando uma experiência de usuário limpa e organizada.
- **HTML**: A estrutura principal da página, com uma interface de usuário simples e eficiente.

---

## Funcionalidades

1. **Coleta Automática de Notícias**: O backend coleta notícias de quatro fontes principais: G1, CNN Brasil, UOL e Globo, a cada 5 minutos.
2. **Resumos Automáticos**: Utiliza o modelo BART da Hugging Face para resumir os textos longos e exibir apenas o conteúdo relevante.
3. **Exibição em Tempo Real**: As notícias são enviadas em tempo real para o frontend utilizando **Socket.IO**, sem a necessidade de recarregar a página.
4. **Armazenamento em Banco de Dados SQLite**: As notícias são armazenadas em um banco de dados local, garantindo que as notícias antigas permaneçam acessíveis.
5. **Interface de Busca**: Um campo de pesquisa permite que os usuários filtrem as notícias exibidas com base na fonte (G1, CNN Brasil, UOL e Globo).
6. **Persistência no Local Storage**: O histórico de notícias visualizadas é armazenado localmente no navegador, evitando que notícias duplicadas apareçam.

---

## Como Funciona

### Backend (`back.py`)

- O **backend** é construído com o framework Flask e realiza várias funções essenciais:
  - **Scraping**: O backend realiza o scraping das páginas de notícias usando a biblioteca **BeautifulSoup** para extrair os links e conteúdo relevante.
  - **Resumos**: O modelo de **Transformers (BART)** é utilizado para resumir o conteúdo extraído, tornando as notícias mais curtas e diretas.
  - **Armazenamento**: As notícias são armazenadas no banco de dados **SQLite** para persistência. O banco de dados é atualizado periodicamente com novas notícias.
  - **WebSocket**: As notícias são enviadas ao frontend em tempo real usando **Socket.IO**, permitindo uma atualização constante sem a necessidade de recarregar a página.

### Frontend (`index.html`, `style.css`, `script.js`)

- **HTML**: A estrutura da página é simples e funcional, contendo um campo de busca, uma área de exibição para as notícias e uma animação de carregamento.
- **CSS**: O design da página é baseado em um tema roxo/azul, com a "caixa branca" sendo o principal componente para exibição das notícias.
- **JavaScript**: Utilizado para manipular a interface de usuário, estabelecer a conexão com o backend via **Socket.IO** e atualizar a lista de notícias em tempo real. Também implementa o campo de busca para filtrar notícias por fonte.

---

