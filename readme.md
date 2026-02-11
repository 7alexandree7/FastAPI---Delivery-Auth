 uvicorn main:app --reload = run the server

 ## Configuração Inicial

 1.  Instalar as dependencias
 2.  Instanciar o fastAPI
 3.  Criar o arquivo das rotas (rota de auth / rota de order)
 4.  Importar nossas rotas no main.py
 5.  Criar um roteador para cada rota com o APIRouter / definir o prefix para as rotas / definir tags para deixar aparecendo na documentação
 6.  Dizer ao main para ele usar os roteadores (minhas rotas)



 ## Criação de Rota De Criação de conta

 1.  Usar um decorator mais o seu roteador, passando o status HTTP e o endpoint
 2.  Criar uma função assincrona para a rota 
 3. Passar os parametros / tipados 
 4. Verificar se ja existe um usuário com esse email (trazer a tabela de usuarios para ter acesso e fazer essa busca + trazer a variavel do banco)
 4. Criar uma session com o *sqlalchemy.orm import sessionmarker* para evitar ficar com conexões abertas no nosso banco. Cria uma sessão faz oq tem que fazer depois deleta a sessão 
 5. Chamar a session *session =  sessionmaker(bind=db)* Criar uma instancia da session *session = session()*
 6. umar a session Fazer uma query na minha tabela usser e filtrar um email do usuario do banco se é igual ao email passado no parametro, utilizar metodo first()
 7. Se ja existir um usuario (já existe um usuario com esse email, return uma msg), se não cria ele
 8. utilizar a nossa session.add(new_user), para armazenar no nosso banco de dados dentro da session
 9. Utilizar o session.commit()
 10. retornar um JSON com uma message do usuario criado
 11. Refatorar a parte de session para utlizar a dependencia
 12. Encriptografar a senha
 13. import o HTTPException para definir o status http da nossa request, passando o status_code / detail
 14. Sempre quando o usuario for fazer algo que não deve, não devemos usar o return e sim o raise, quando se trata de devolver o status_http


## Criação de Rota De Login da conta

1. Na rota de login, vamos passar nosso email e senha, nossa API vai devolver um token, aonde com esse token eu vou usar em todas as rotas que pede que tenha um usuario logado
2. Iremos utilizar o formato token via (JWT)
3. Criar um Schema para o login recebendo como parametro do schema o email e a senha
4. tipando a Session e usando o Depends junto com nosso method Depends(get_session)
5. Fazer uma consulta no banco, para chekar se existe de fato esse usuario com o respesctivo email
6. Se não existir o usuario, retornar => raise HTTPException(status_code=404, detail="user not found")
7. Caso exista um usuario no bloco else. Criar um usuario
8. Criar um token JWT


## Criação de Rota De Pedido

1. Na rota de login, vamos passar nosso email e senha, nossa API vai devolver um token, aonde com esse token eu vou usar em todas as rotas que pede que tenha um usuario logado
2. Iremos utilizar o formato token via (JWT)
3. Retornar um dicionario informando return { "access_token": nomeDaVariavel, "token_type": "Bearer}


## Gerenciamento de Sessão

 1. Se eu tiver varias rotas que edita meu banco de dados, significa que eu vou ter que repetir esse codigo em cada rota, em cada parte do codigo
 2. Todas as rotas que formos criar dependem de uma sessão
 3. O session close, que encerra a sessão, não podemos apenas colocar por fim de cada rota, pois se existir um erro no meio da rota, ela nunca é executada, não finalizando a sessão
 4. Criar uma dependencia python = E uma função que vai me retornar um parametro ou algo que precisamos, vindo de um arquivo externo dentro do nosso codigo, simplificando nosso codigo e deixando limpo
 5. Importar nossa dependencia get_session, que é uma função, onde lida com as sesion, atribuir como parametro e importar do fastAPI o Depends() para informar que esse parametro não vem do usuario
 6. No lugar de retornar a session, usamos o yield, ele retorna um valor, mas n encerra a execução da função
 7. Fechar a sessão - session.close()
 8. envolver todo nosso sesseion dentro de um try: pra tentar executar aquele pedaço e no finally executar o session.close()



## Criptografia de Senha

1. Instalar a ferramenta bcrypt para a emcripitação
2. Definir uma SECRET_KEY no meu .env
3. atraves da lib dotenv from load_dotenv pegamos a nossa variavel
4. SECRET_KEY = os.getenv("SECRET_KEY")
5. Em nenhum lugar devemos armazenar a senha do usuario descriptografada
6. Criar no main nosso bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
7. Realizar o hash da senha que o usuario esta enviando no nosso site, para armazenar ja a senha encriptada password_encrypted = bcrypt_context.hash(password)
8. Passar a senha encriptada no lugar da senha padrão


## Criação de Schemas

1. Criar um arquivo schemas.py
2. Forçar a tipagem dos dados com o python usando o Pydantic
3. Criar uma classe com o nome de Schema no final
4. Importar o from pydantic import BaseModel e usar o BaseModel como parametro da função
5. Criar um objeto model_config passando como valor "from_attributes": True
6. Ele vai ser interpretado como uma classe que vai ser transformada num SQL diretamente no banco de dados, ele ta conectando no nosso modelo
7. Importar esse nosso schema, no parametro das nossas rotas
8. Remove isso async def create_user(name: str, email: str, password: str) e chama nosso schema no lugar desses valores


## Banco de dados / ORM + Criação de Tabelas

 1.  Criação + conexão com o banco de dados
 2.  Criar uma pasta / arquivo que se chama models, aonde usaremos nossa *ORM sqlalchemy*, com o banco *sqlLite*
 3.  utilizar uma const db e atribuir a função *create_engine* do nosso sqlalchemy, passando como parametro a URL do banco  => db = create_engine("sqlite:///database.db")
 4.  Criar nossa Base para o banco de dado, com o *declarative_base*
 5.  Criar as classes / tabela no nosso banco de dados
    - Usar um parametro para a classe __tablename__ setar manualmente o nome da tabela
    - Definir os valores para cada tabela
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
    - criando uma tupla *STATUS_CHOICE = (("pendente", "pendente"), ("cancelado", "cancelado"), ("finalizado", "finalizado"))*
    - Adicionando na coluna *status = Column("status", ChoiceType(choices=STATUS_CHOICE))*


## Config + Migrations (Alembic)

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



 ## Anotações Derivadas

 1. Node/Express + Mongoose/Prisma → ORM/ODM cuida da sessão/conexão. Você só chama métodos.
 2. Python + FastAPI + SQLAlchemy → você precisa criar e gerenciar a session por rota.


# Diferença do Models para Schemas

1. Model representa a estrutura da tabela no banco de dados
2. Schema representa o formato dos dados que entram e saem da API
3. Model utiliza SQLAlchemy (ORM).
4. Schema utiliza Pydantic.
5. Model é responsável por mapear dados para o banco (CRUD).
6. Schema é responsável por validar e serializar dados da requisição e resposta.
7. Model se comunica com o banco de dados.
8. Schema se comunica com o cliente (JSON da API).
9. Model = estrutura do banco.
0. Schema = estrutura da API.