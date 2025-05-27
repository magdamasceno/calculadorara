
import streamlit as st

st.set_page_config(page_title="Calculadora Reclame AQUI", layout="centered")

st.title("Calculadora de Avaliação - Reclame AQUI")

with st.form("formulario"):
    total_reclamacoes = st.number_input("Total de reclamações", min_value=0, step=1)
    total_respostas = st.number_input("Total de respostas", min_value=0, step=1)
    media_notas = st.number_input("Média das notas", min_value=0.0, max_value=10.0, step=0.01)
    indice_solucao = st.number_input("Índice de solução (%)", min_value=0.0, max_value=100.0, step=0.01)
    indice_novos_negocios = st.number_input("Índice de novos negócios (%)", min_value=0.0, max_value=100.0, step=0.01)
    total_avaliacoes = st.number_input("Total de avaliações", min_value=0, step=1)

    submitted = st.form_submit_button("Calcular Avaliação")

if submitted:
    if total_reclamacoes == 0 or total_avaliacoes == 0:
        st.warning("Preencha todos os campos para calcular a avaliação.")
    else:
        indice_resposta = (total_respostas / total_reclamacoes) * 100 if total_reclamacoes > 0 else 0

        AR = ((indice_resposta * 2) + (media_notas * 10 * 3) + (indice_solucao * 3) + (indice_novos_negocios * 2)) / 100
        AR = round(AR, 2)

        if AR >= 8:
            reputacao = "ÓTIMO"
        elif AR >= 7:
            reputacao = "BOM"
        elif AR >= 6:
            reputacao = "REGULAR"
        elif AR >= 5:
            reputacao = "RUIM"
        else:
            reputacao = "NÃO RECOMENDADA"

        st.markdown(f"### Sua confirmação é: **{reputacao}** com AR de **{AR}**")

        faltam_para_RA1000 = max(0, int(((1000 * 0.8) - (total_avaliacoes * media_notas)) / (10 - media_notas))) if media_notas < 10 else 0
        cair_para_bom = int(((AR - 7) * 100 - (indice_resposta * 2 + media_notas * 10 * 3 + indice_solucao * 3 + indice_novos_negocios * 2)) / (0 - 10 * 3)) if AR > 7 else 0

        st.info(f"Faltam {faltam_para_RA1000} avaliações com nota 10 para alcançar o RA1000.")
        if AR > 7:
            st.info(f"Se receber {cair_para_bom} avaliações com nota 0, cairá para BOM.")
