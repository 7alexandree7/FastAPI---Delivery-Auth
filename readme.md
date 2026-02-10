 uvicorn main:app --reload = run the server

 ## *Configuração Inicial*

 1.  Instalar as dependencias
 2.  Instanciar o fastAPI
 3.  Criar o arquivo das rotas (rota de auth / rota de order)
 4.  Importar nossas rotas no main.py
 5.  Criar um roteador para cada rota com o APIRouter / definir o prefix para as rotas / definir tags para deixar aparecendo na documentação
 6.  Dizer ao main para ele usar os roteadores (minhas rotas)


## *Criação de Rotas*

 1.  Usar um decorator mais o seu roteador, passando o status HTTP e o endpoint
 2.  Criar uma função assincrona para a rota 



## *Banco de dados / ORM + Criação de Tabelas*

 1.  Criação + conexão com o banco de dados
 2.  Criar uma pasta / arquivo que se chama models, aonde usaremos nossa *ORM sqlalchemy*, com o banco *sqlLite*
 3.  utilizar uma const db e atribuir a função *create_engine* do nosso sqlalchemy, passando como parametro a URL do banco  => db = create_engine("sqlite:///database.db")
 4.  Criar nossa Base para o banco de dado, com o *declarative_base*
 5.  Criar as classes / tabela no nosso banco de dados
    Usar um parametro para a classe __tablename__ setar manualmente o nome da tabela
    Definir os valores para cada tabela
 6.  Importar da nossa orm sqlalchemy o *Column*, para tipar nossos valores
 7.  Depois de importar o *Column*, importamos tambem os tipos de dados que usaremos nas nossas tabelas, como String | Integer | Boolean | Float | ForeignKey ex: id = Column("id", Integer)
   - Parametros importantes para a criação de cada coluna na nossa classe
      - *nullable=False* = Nunca um usario ou outra coisa pode ser criado sem um ID, ou outro campo em especifico, ele torna o elemento da coluna como obrigatorio passar um valor
      - *Primary_Key=True* = Toda tabela no nosso banco de dados tem que ter uma Primary_Key, tem que ser um valor unico para cada item armazenado dentro da tabela
      - *autoincrement=True* = Indentificador para a coluna, exemplo, cada novo usuario cadastrado o ID dele vira, 1, o proximo vira 2, e por ai em diante
      - *default=False* = Quando eu crio um usuario e não passo o parametro, usamos esse atributo *exemplo: is_active = Column("is_active", Boolean, default=True)*
      - *autoincrement=True* = Indentificador para a coluna, exemplo, cada novo usuario cadastrado o ID dele vira, 1, o proximo vira 2, e por ai em diante
      - *ForeignKey()* = Chave estrangeira, quando queremos atribuir a um valor da nossa tabela, um valor de outra tabela ex *user = Column("user", ForeignKey("users.id"))*
 8.  Criar a função __init__, responsável por inicializar os dados do objeto ao criar um novo registro, atribuindo valores aos atributos da classe. Essa função não cria tabelas nem colunas.
 9.  Tipar como um ENUM do ts, baixando a lib *sqlalchemy_utils* importando *from sqlalchemy_utils.types import ChoiceType*
    criando uma tupla *STATUS_CHOICE = (("pendente", "pendente"), ("cancelado", "cancelado"), ("finalizado", "finalizado"))*
    Adicionando na coluna *status = Column("status", ChoiceType(choices=STATUS_CHOICE))*


## *Config + Migrations (Alembic)*

 1.  Baixar a biblioteca alembic
 2.  No arquivo *alembic.ini* mudar o valor da variavel *sqlalchemy.url* para a URL do nosso banco
 3.  No arquivo env.py importar as bibliotecas *sys* e *os* e utilizar um comando
   - *sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))*
   - from models import Base
   - target_metadata = Base.metadata
 4.  Rodar no terminal *alembic revision --autogenerate -m "intial migration"*
   - Lê seus models
   - Compara com o estado do banco
   - Gera um arquivo de migration
   - Não cria tabelas / Não aplica nada no banco
   - Pode criar o arquivo .db vazio só por abrir a conexão (SQLite) 👉 Ele só escreve o plano, não executa.
 5.  Executar a migração *alembic upgrade head* - *usar a extensão SQLite Viewr, para visualizar as tabelas do seu banco*
 6.  A cada alteração, sendo remoção adição, deve-se criar uma nova migration no banco de dados