# **Stract Challenge** 

Este repositório contém uma API desenvolvida para consumir dados de plataformas de anúncios e gerar relatórios em formato CSV. A aplicação foi construída utilizando **Flask** e **Docker**. O desafio propõe a criação de endpoints que recuperam insights de anúncios, fornecendo tabelas dinâmicas e agregadas com base nas informações obtidas.

## **Passos para Rodar a Aplicação**

### 1. **Clonar o Repositório**

Clone o projeto utilizando o comando:

```bash
git clone https://github.com/natalia-armstrong/scract-challenge.git
```

### 2. Criar e Ativar o Ambiente Virtual
#### 2.1 Criar o Ambiente Virtual
No terminal, na raiz do projeto, execute o comando para criar um ambiente virtual:

Windows:
```bash
python -m venv venv
```
Linux:
```bash
python3 -m venv venv
```
#### 2.2 Ativar o Ambiente Virtual
Execute o seguinte comando no terminal:

Windows:
```bash
venv\Scripts\activate
```
Linux:
```bash
source venv/bin/activate
```
Após a ativação, o nome do ambiente virtual aparecerá no terminal.

### 3. Instalar Dependências
Com o ambiente virtual ativo, instale as dependências do projeto com o comando:

```bash
pip install -r requirements.txt
```

### 4. Rodar a Aplicação
Agora que as dependências estão instaladas, você pode rodar a aplicação de duas formas: utilizando Docker ou diretamente no terminal.

#### 4.1 Rodar a Aplicação com Docker

Abra o [Docker Desktop](https://www.docker.com/products/docker-desktop/) e certifique-se de que o Docker esteja rodando.

No terminal, navegue até a raiz do projeto e execute os seguintes passos:

Crie a imagem Docker:
```bash
docker build -t nome-imagem .
```
Rode o container com a aplicação:
```bash
docker run -p 5000:5000 nome-imagem
```
(Caso queira usar portas diferentes, basta ajustar o número da porta conforme necessário.)

Abra o navegador e acesse a aplicação através do endereço http://127.0.0.1:5000.

#### 4.2 Rodar a Aplicação Localmente (sem Docker)
Caso prefira rodar a aplicação diretamente no terminal, execute o seguinte comando:

Windows
```bash
python app.py
```
Linux
```bash
python3 app.py
```

Isso irá iniciar a aplicação localmente. Em seguida, abra o navegador e acesse a URL http://127.0.0.1:5000.

### 5. Endpoints Disponíveis
#### 5.1 Raiz da API
GET /

Este endpoint retorna informações pessoais.

Resposta:

```json
{
    "name": "Natalia Armstrong",
    "email": "natalia.armstronggg@gmail.com",
    "linkedin": "https://www.linkedin.com/in/nataliaarmstrong23/"
}
```
#### 5.2 Anúncios de uma Plataforma Específica
GET /{{plataforma}}

Este endpoint retorna uma tabela com os anúncios de uma plataforma específica, incluindo todos os campos de insights relacionados ao anúncio, bem como o nome da conta que está veiculando o anúncio.

Exemplo de resposta:

```csv
Platform,Ad Name,Clicks,Impressions,Spend,...
Facebook,Some Ad,10,1000,200,...
Facebook,Other Ad,20,1500,300,...
YouTube,One More Ad,5,500,100,...
```
#### 5.3 Resumo de Anúncios por Conta em uma Plataforma
GET /{{plataforma}}/resumo

Este endpoint retorna uma tabela similar à do endpoint anterior, mas colapsando os dados por conta. As colunas numéricas são somadas, e as colunas de texto podem ficam vazias (exceto para o nome da conta).

Exemplo de resposta:

```csv
Platform,Ad Name,Clicks,Impressions,Spend,...
Facebook,,30,2500,500,...
YouTube,,5,500,100,...
```

#### 5.4 Todos os Anúncios de Todas as Plataformas
GET /geral

Este endpoint retorna todos os anúncios de todas as plataformas, incluindo colunas para identificar o nome da plataforma e o nome da conta que veicula o anúncio. Para as plataformas que não possuem um determinado campo, o valor ficará vazio.

Exemplo de resposta:

```csv
Platform,Ad Name,Clicks,Impressions,Spend,...
Facebook,Some Ad,10,1000,200,...
Facebook,Other Ad,20,1500,300,...
YouTube,One More Ad,5,500,100,...
```

#### 5.5 :bar_chart: Resumo de Todos os Anúncios
GET /geral/resumo

Este endpoint retorna uma tabela semelhante ao endpoint anterior, mas com a soma dos valores numéricos para cada plataforma. As colunas de texto ficam vazias (exceto para o nome da plataforma).

Exemplo de resposta:

```csv
Copiar
Platform,Ad Name,Clicks,Impressions,Spend,...
Facebook,,30,2500,500,...
YouTube,,5,500,100,...
```
### Conclusão
Agora você pode acessar os relatórios dinâmicos das plataformas de anúncios, seja localmente ou por meio de um container Docker. Utilize os endpoints da API para visualizar os dados e gerar os relatórios necessários.

Se houver dúvidas ou problemas, fique à vontade para abrir uma issue no repositório ou entrar em contato diretamente pelo email: natalia.armstronggg@gmail.com
