import streamlit as st

st.set_page_config(page_title="Calculadora Reclame AQUI", layout="centered")
st.title("Calculadora de Avaliação - Reclame AQUI")

with st.form("formulario"):
    total_reclamacoes = st.number_input("Total de reclamações", min_value=0)
    total_respostas = st.number_input("Total de respostas", min_value=0)
    media_notas = st.number_input("Média das notas", min_value=0.0, max_value=10.0)
    indice_solucao = st.number_input("Índice de solução (%)", min_value=0.0, max_value=100.0)
    indice_novos_negocios = st.number_input("Índice de novos negócios (%)", min_value=0.0, max_value=100.0)
    total_avaliacoes = st.number_input("Total de avaliações", min_value=0)

    submitted = st.form_submit_button("Calcular Avaliação")

def calcular_ar(respostas, reclamacoes, notas, solucao, novos_negocios):
    ir = (respostas / reclamacoes) * 100 if reclamacoes > 0 else 0
    ar = ((ir * 2) + (notas * 10 * 3) + (solucao * 3) + (novos_negocios * 2)) / 100
    return ar, ir

def estimar_para_ra1000_site(ar_atual):
    delta_ar = 8.5 - ar_atual
    return int((2728 / 0.1) * delta_ar)

def estimar_para_bom_site(ar_atual):
    delta_ar = ar_atual - 7.0
    return int((533 / 1.4) * delta_ar)

if submitted:
    if total_reclamacoes == 0 or total_avaliacoes == 0:
        st.warning("Por favor, preencha todos os campos corretamente antes de calcular.")
    else:
        AR, indice_resposta = calcular_ar(total_respostas, total_reclamacoes, media_notas, indice_solucao, indice_novos_negocios)

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

        st.markdown(f"### Sua reputação é **{reputacao}** e o AR é **{AR:.2f}**.")

        faltam_positivas = estimar_para_ra1000_site(AR)
        faltam_negativas = estimar_para_bom_site(AR)
        faltam_respostas = max(0, int((0.9 * total_reclamacoes) - total_respostas))

        st.info(f"Para atingir a reputação **RA1000**, você precisa de mais **{faltam_positivas} avaliações positivas** e mais **{faltam_respostas} novas respostas públicas**.")
        st.warning(f"Por outro lado, se você obtiver mais **{faltam_negativas} avaliações negativas**, descerá para o selo **BOM**.")
