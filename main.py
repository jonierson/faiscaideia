import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv


# Carregar variáveis do arquivo .env
load_dotenv()

# Função para obter as respostas do Groq
def get_groq_completions(user_content):
    client = Groq(
        api_key=os.getenv('API_KEY')
    )

    completion = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[
            {
                "role": "system",
                "content": "You are a YouTube expert creator who likes to write engaging titles for a keyword. \nYou will provide 10 attention-grabbing YouTube titles on keywords specified by the user."
            },
            {
                "role": "user",
                "content": user_content
            }
        ],
        temperature=0.5,
        max_tokens=5640,
        top_p=1,
        stream=True,
        stop=None,
    )

    result = ""
    for chunk in completion:
        result += chunk.choices[0].delta.content or ""

    return result

# Função para gerar ideias de projetos de feira de ciências
def gerar_ideias(dados_usuario):
    prompt = criar_prompt(dados_usuario)

    try:
        response = get_groq_completions(prompt)
        return response.strip() if response else None
    except Exception as e:
        st.error(f"Erro ao tentar gerar ideias: {e}")
        return None


# Função para criar o prompt com base nos dados do usuário
def criar_prompt(dados_usuario):
    metodologia = dados_usuario.get('metodologia')
    prompt_template = """
    Como estudante do ensino {ano_serie}, estou empolgado em criar um projeto {preferencia_projeto} para participar de uma feira de ciência. 
    Meu objetivo é desenvolver um projeto utilizando a metodologia {metodologia}, que envolve {detalhes_metodologia}. 
    Gostaria de abordar um problema ou investigação da subárea {especialidade} que faz parte da grande área {area_conhecimento}, com preferência por temas relacionados à {tema_especifico}, pois tenho interesse no {motivacao}. 
    Sobre o conhecimento prévio sobre esse tema minha resposta é {conhecimento_previo}. 
    Para desenvolver esse projeto pretendo fazer uso das minhas habilidades de {habilidades} e dos seguintes recursos {recursos}. 
    Espero que ao final do projeto possa {impacto}. 
    Gostaria ainda de acrescentar que {informacao_adicional}. 
    Poderia me ajudar a criar uma lista contendo 5 ideias de projetos de feira de ciência que se encaixem na metodologia escolhida? As sugestões devem conter um título, objetivo e materiais e devem ser organizadas da seguinte forma:\n
    1. Título:\n
    2. Objetivo:\n
    3. Materiais:\n
    Cada ideia deve ser clara, concisa e adequada ao {ano_serie} e {tema_especifico} escolhidos. Ao final ofereça recursos adicionais, como links para artigos científicos ou vídeos explicativos.
    """

    detalhes_metodologia = "o teste de uma hipótese, coleta e processamento de dados para chegar a uma conclusão" if metodologia == "Científica" else "a criação ou aperfeiçoamento de um dispositivo, procedimento, programa de computador ou algoritmo"

    return prompt_template.format(
        ano_serie=dados_usuario['ano_serie'],
        preferencia_projeto=dados_usuario['preferencia_projeto'],
        metodologia=dados_usuario['metodologia'],
        detalhes_metodologia=detalhes_metodologia,
        especialidade=dados_usuario['especialidade'],
        area_conhecimento=dados_usuario['area_conhecimento'],
        tema_especifico=dados_usuario['tema_especifico'],
        motivacao=dados_usuario['motivacao'],
        conhecimento_previo=dados_usuario['conhecimento_previo'],
        habilidades=dados_usuario['habilidades'],
        recursos=dados_usuario['recursos'],
        impacto=dados_usuario['impacto'],
        informacao_adicional=dados_usuario['informacao_adicional']
    )


# Configuração da aplicação Streamlit
st.title("Tenha ideias incríveis de projetos com o Faísca, seu assistente virtual!")

# Centralizando a imagem usando colunas
col1, col2, col3 = st.columns(3)

with col1:
    st.write("")

with col2:
    st.image("https://github.com/jonierson/faiscaideia/blob/main/faisca.png", use_column_width=True)

with col3:
    st.write("")

st.write("""
Faísca é um chatbot de inteligência artificial feito sob medida para alunos da educação básica como você. Ele não é apenas um assistente; é uma fonte de inspiração que irá acender sua criatividade e ajudá-lo a gerar ideias para seus projetos.
""")

st.write("""
Para que o Faísca possa te oferecer as melhores sugestões, é fundamental que você responda a todas as perguntas.
""")

# Coletando informações do usuário
ano_serie = st.selectbox("Qual ano/série você está cursando?", [
    "", "6º Ano do Ensino Fundamental", "7º Ano do Ensino Fundamental",
    "8º Ano do Ensino Fundamental", "9º Ano do Ensino Fundamental", "1º Ano do Ensino Médio",
    "2º Ano do Ensino Médio", "3º Ano do Ensino Médio"], key="ano_serie")

preferencia_projeto = st.radio("Prefere realizar o projeto sozinho ou em equipe?", ["Sozinho", "Em equipe"],
                               key="preferencia_projeto")

metodologia = st.selectbox("Qual metodologia você pretende utilizar para o seu projeto?",
                           ["", "Científica", "Engenharia"], key="metodologia")

area_conhecimento = st.selectbox("Em qual área do conhecimento você tem mais interesse?", [
    "", "Ciências Agrárias", "Ciências Biológicas", "Ciências da Saúde",
    "Ciências Exatas e da Terra", "Engenharias", "Ciências Humanas",
    "Ciências Sociais Aplicadas", "Lingüística, Letras e Artes"], key="area_conhecimento")

# Condicional para exibir a especialidade com base na área de conhecimento
especialidade = ""
if area_conhecimento == "Ciências Agrárias":
    especialidade = st.selectbox("Dentro da área de conhecimento escolhido, qual especialidade te interessa mais:", [
        "", "Agronomia", "Ciência e Tecnologia de Alimentos", "Medicina Veterinária",
        "Recursos Florestais e Engenharia Florestal", "Zootecnia"])
elif area_conhecimento == "Ciências Biológicas":
    especialidade = st.selectbox("Dentro da área de conhecimento escolhido, qual especialidade te interessa mais:", [
        "", "Biotecnologia", "Genética", "Microbiologia", "Imunologia"])
elif area_conhecimento == "Ciências da Saúde":
    especialidade = st.selectbox("Dentro da área de conhecimento escolhido, qual especialidade te interessa mais:", [
        "", "Farmácia", "Enfermagem", "Medicina", "Nutrição", "Odontologia"])
elif area_conhecimento == "Ciências Exatas e da Terra":
    especialidade = st.selectbox("Dentro da área de conhecimento escolhido, qual especialidade te interessa mais:", [
        "", "Astronomia", "Computação", "Geociências", "Matemática", "Oceanografia", "Química", "Estatística"])
elif area_conhecimento == "Engenharias":
    especialidade = st.selectbox("Dentro da área de conhecimento escolhido, qual especialidade te interessa mais:", [
        "", "Engenharia Aeroespacial", "Engenharia Ambiental", "Engenharia Biomédica", "Engenharia Civil",
        "Engenharia Elétrica",
        "Engenharia de Controle e Automação", "Engenharia de Materiais e Metalúrgica", "Engenharia de Produção",
        "Engenharia de Minas", "Engenharia Mecânica", "Engenharia Química"])
elif area_conhecimento == "Ciências Humanas":
    especialidade = st.selectbox("Dentro da área de conhecimento escolhido, qual especialidade te interessa mais:", [
        "", "Antropologia", "Arqueologia", "Ciência Política", "Educação", "Filosofia", "Geografia", "História",
        "Psicologia", "Sociologia", "Teologia"])
elif area_conhecimento == "Ciências Sociais Aplicadas":
    especialidade = st.selectbox("Dentro da área de conhecimento escolhido, qual especialidade te interessa mais:", [
        "", "Administração", "Arquitetura e Urbanismo", "Ciências Contábeis", "Comunicação", "Direito", "Economia",
        "Museologia", "Planejamento Urbano e Regional", "Serviço Social", "Turismo"])
elif area_conhecimento == "Lingüística, Letras e Artes":
    especialidade = st.selectbox("Dentro da área de conhecimento escolhido, qual especialidade te interessa mais:", [
        "", "Artes", "Letras", "Lingüística", "Música"])

tema_especifico = st.text_input("Informe o tema específico que você deseja explorar no seu projeto:",
                                key="tema_especifico")

motivacao = st.text_input("O que te motivou a escolher esse tema? (Ex.: 1. Sempre fui fascinado(a) por...; 2. Quero contribuir para encontrar soluções para...; 3. Sempre tive curiosidade sobre...)", key="motivacao")

conhecimento_previo = st.radio("Você já tem algum conhecimento prévio sobre esse tema?", ["Sim", "Não"],
                               key="conhecimento_previo")

habilidades = st.text_area("Quais habilidades você tem que podem ajudar no desenvolvimento do projeto? (Ex.: 1. Sou muito bom em...; 2. Tenho facilidade em...; 3. Possuo conhecimento em...)",
                           key="habilidades")

recursos = st.text_area("Quais recursos você tem disponível para realizar o projeto? (Ex.: 1.Tenho acesso a [instituição, laboratório, biblioteca] que me permite...; 2. Conheço pessoas que podem me auxiliar com...; 3. Tenho à disposição equipamentos como [lista de equipamentos] que podem facilitar...)", key="recursos")

impacto = st.text_area("Qual impacto você espera alcançar com o projeto? (Ex.: 1. Minha pesquisa tem o potencial de...; 2. Meu objetivo é transformar a vida de... ; 3. Acredito que minha pesquisa terá um impacto significativo em...)", key="impacto")

informacao_adicional = st.text_area("Deseja adicionar alguma informação adicional?", key="informacao_adicional")

# Dados do usuário para o prompt
dados_usuario = {
    'ano_serie': ano_serie,
    'preferencia_projeto': preferencia_projeto,
    'metodologia': metodologia,
    'area_conhecimento': area_conhecimento,
    'especialidade': especialidade,
    'tema_especifico': tema_especifico,
    'motivacao': motivacao,
    'conhecimento_previo': conhecimento_previo,
    'habilidades': habilidades,
    'recursos': recursos,
    'impacto': impacto,
    'informacao_adicional': informacao_adicional
}

# Gerar ideias de projetos
if st.button("Gerar Ideias de Projetos"):
    if not ano_serie or not preferencia_projeto or not metodologia or not area_conhecimento or not tema_especifico:
        st.error("Por favor, preencha todos os campos.")
    else:
        st.write("Aqui estão algumas ideias de projetos para você:")
        response = gerar_ideias(dados_usuario)
        if response:
            st.write(response)
