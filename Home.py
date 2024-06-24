import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Home",
    page_icon=" ",
    layout="wide"
)

# image_path = '/home/emersds/repos_projetos/curry_company/capa_currycompany.png'
image = Image.open('capa_currycompany.png')
st.sidebar.image(image, use_column_width=True)

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## A entrega mais rápida do país')
st.sidebar.markdown("""___""")

st.write('# Curry Company Growth Dashboard')
st.markdown(
"""
   Growth dashboard foi construído para acompanhar as métricas de crescimento dos Entregadores e Restaurantes.
   ### Como utilizar esse Growth Dashboard?
   - Visão empresa:
     - Visão gerencial: métricas gerais de comportamento.
     - Visão tática: indicadores semanais de crescimento.
     - Visão geográfica: insights de geolocalização.

   - Visão entragadores:
     - Acompanhamento dos indicadores semanais de crescimento.

   - Visão restaurantes:
     - Indicadores semanais de crescimento dos restaurantes.

   ### Ask for Help (Contacts)
   - Time de Data Science
       - Discord: @emersoncoliveira
       - https://sites.google.com/view/emerson-oliveira-portfolio/
       - https://www.linkedin.com/in/emerson-carlos-oliveira
       - https://emerson-c-oliveira.github.io/portfolio_project_ds/#
""")