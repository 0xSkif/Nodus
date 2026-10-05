![Nodus Logo](<Nodus Logo - PT-BR.jpg>)

**English Version:** [README in English](../README.md)
## 1. Sobre

O Nodus é uma ferramenta de linha de comando (CLI) interativa e leve, desenvolvida em Python para automatizar a criação, navegação e gerenciamento em massa de diretórios e arquivos.

Com suporte nativo a **Windows, Linux e macOS**, o Nodus foi projetado para acelerar a montagem de ambientes de desenvolvimento, estruturas de estudo e organização de projetos com poucos comandos.

### 1.1 Recursos

- **Navegação Interativa:** Exibição dinâmica da estrutura de diretórios em formato de árvore.
- **Manipulação em Massa:** Criação de múltiplos arquivos e pastas com nomenclatura padrão ou personalizada em uma única sessão.
- **Multiplataforma:** Suporte nativo e automático para Windows, Linux e macOS sem necessidade de ajustes de sistema.
- **Portátil e Eficiente:** Execução leve com consumo mínimo de recursos.

## 2. Funcionamento

O Nodus foi projetado utilizando uma arquitetura modular, baseando-se no **Princípio da Responsabilidade Única (SRP)**, divididindo-se em três pilares principais: interface do usuário (CLI), navegação recursiva e gerenciamento de entrada e saída (I/O) do sistema de arquivos.

### 2.1 Tecnologias Utilizadas

- **[Python 3.10+](https://www.python.org/):** Linguagem base do projeto.
- **[Rich](https://github.com/Textualize/rich):** Renderização de texto formatado, painéis e visualização de estruturas em árvore no terminal.
- **`InquirerPy`:** Interface de linha de comando (CLI) interativa para seleções e navegação nos menus.
- **Módulos Nativos:** 
   - **`pathlib`:** Manipulação cross-platform de caminhos.
   - **`platform`:** Detecção do sistema operacional.
   - **`typing`:** Tipagem estática.

## 3. Instalação e Execução

O **Nodus** pode ser excutado de duas formas:

- Instalando o **executável portátil** (não requer Python).
- Excutando o **código-fonte** manualmente (requer instalação do Python).

### 3.1 Executável Portátil

1. Acesse a aba [Releases](https://github.com/0xSkif/nodus/releases) do repositório.
2. Baixe o arquivo `nodus.exe` ou o binário correspondente ao sistema.
3. Abra o terminal no diretório onde baixou o arquivo e execute:

   ```powershell
   .\nodus.exe
   ```

### 3.2 Código-Fonte

1. Clone o repositório:
   ```bash
   git clone [https://github.com/0xSkif/nodus.git](https://github.com/0xSkif/nodus.git)
   cd nodus
   ```
2. Instale as dependências e o pacote executável:
   ```bash
   pip install -e .
   ```
3. Execute o comando global:
   ```bash
   nodus
   ```
