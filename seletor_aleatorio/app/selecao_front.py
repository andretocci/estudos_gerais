import streamlit as st
import numpy as np
import time
import json


def weighted_random_selection(data):
    """
    Seleciona um nome de um dicionário de nomes e frequências.
    A probabilidade de um nome ser selecionado é inversamente proporcional à sua frequência.

    Args:
        data (dict): Um dicionário onde as chaves são nomes (str) e
                     os valores são suas frequências (int/float).

    Returns:
        tuple: (nome_selecionado, probabilidades_de_selecao)
               Retorna (None, None) se os dados de entrada estiverem vazios ou inválidos.
    """
    if not data:
        st.error("Os dados de entrada estão vazios.")
        return None, None

    names = list(data.keys())
    frequencies = np.array(list(data.values()), dtype=float)

    # A soma total das frequências não pode ser zero
    total_freq = frequencies.sum()
    if total_freq == 0:
        if len(frequencies) > 0:
            st.error(
                "A soma total das frequências é 0. Não é possível calcular as probabilidades."
            )
            return None, None
        else:
            st.error("Não há participantes no sorteio.")
            return None, None

    # Calcular probabilidades diretas (chance de ter sido sorteado no passado)
    probabilities = frequencies / total_freq

    # Calcular pesos inversos
    # Se a probabilidade é 0 (frequência 0), o peso inverso também deve ser 0.
    inverse_weights = np.zeros_like(probabilities)

    # Criar uma máscara para encontrar probabilidades maiores que zero
    non_zero_mask = probabilities > 0

    # Calcular o peso inverso apenas para quem tem probabilidade > 0
    inverse_weights[non_zero_mask] = 1.0 / probabilities[non_zero_mask]

    # Normalizar os pesos inversos para que somem 1 (tornando-os as probabilidades de seleção)
    total_inverse_weight = inverse_weights.sum()
    if total_inverse_weight == 0:
        # Isso pode acontecer se todos tiverem frequência 0 (que já foi tratado)
        # ou se houver um problema numérico.
        st.error(
            "Não foi possível calcular as probabilidades de seleção. Verifique as frequências."
        )
        return None, None

    selection_probabilities = inverse_weights / total_inverse_weight

    # Selecionar um nome com base nas probabilidades de seleção (pesos inversos normalizados)
    selected_name = np.random.choice(names, p=selection_probabilities)

    return selected_name, selection_probabilities


def display_probabilities(data, weights):
    """
    Exibe as probabilidades de seleção em um gráfico de barras.
    """
    st.subheader("Probabilidades de Seleção (Inversas)")
    st.markdown("Quem tem **frequência menor** tem **mais chance** de ser selecionado.")

    prob_data = {"Nomes": list(data.keys()), "Probabilidade": weights}

    # Configura o gráfico de barras
    st.bar_chart(prob_data, x="Nomes", y="Probabilidade", use_container_width=True)

    # Exibe os dados em texto formatado também
    with st.expander("Ver probabilidades exatas"):
        prob_dict = dict(zip(data.keys(), weights))
        st.json(prob_dict)


def suspense_selection_st(selected_name):
    """
    Cria um efeito de suspense no Streamlit antes de revelar o vencedor.
    """
    st.subheader("Preparando para o sorteio...")

    # Usa st.spinner para um efeito de espera "suspense"
    with st.spinner("Sorteando... 🥁"):
        time.sleep(3)  # Simula o suspense

    # Revela o vencedor
    st.subheader("E o selecionado é...")
    time.sleep(1)  # Pausa dramática

    # Exibe o vencedor com destaque
    st.header(f"🎉 !!! {selected_name} !!! 🎉")

    # Comemoração!
    st.balloons()


# --- Configuração Principal do App Streamlit ---

st.title("Sorteio Ponderado 🎲")
st.markdown(
    """
Esta aplicação realiza um sorteio ponderado. A probabilidade de um nome ser
selecionado é **inversamente proporcional** à sua frequência (quem apareceu
menos vezes tem mais chance de ser sorteado).
"""
)

# Dados padrão
default_name_frequencies = {
    "Aline": 2,
    "Deyvid": 2,
    "Passeto": 1,
    "Rayan": 2,
    "Claudio": 2,
    "Pina - o mestre da Yoga": 1,
    "Rabello - o marinheiro": 1,
    "Rafa Machado": 2,
    "Tocci": 2,
    "Thaina": 1,
}

# Inicializa o session state se não existir
if "participants_json" not in st.session_state:
    st.session_state.participants_json = json.dumps(
        default_name_frequencies, indent=4, ensure_ascii=False
    )

# Área de texto para o usuário editar os dados
st.subheader("Participantes e Frequências (Formato JSON)")
help_text = "Edite o JSON abaixo para mudar os participantes e suas frequências. As frequências devem ser números."
data_input = st.text_area(
    "Dados dos Participantes",
    key="participants_json",  # Usa o session state
    height=300,
    help=help_text,
)

# Botão para iniciar o sorteio
if st.button("Sortear! 🚀", type="primary", use_container_width=True):
    try:
        # Tenta carregar os dados do JSON a partir do session state
        name_frequencies = json.loads(st.session_state.participants_json)

        # Validações
        if not isinstance(name_frequencies, dict):
            st.error(
                "Erro: O formato dos dados deve ser um dicionário JSON (ex: {'Nome': 1})."
            )
        elif not all(isinstance(v, (int, float)) for v in name_frequencies.values()):
            st.error("Erro: Os valores (frequências) devem ser números.")
        elif any(v < 0 for v in name_frequencies.values()):
            st.error("Erro: As frequências não podem ser negativas.")
        else:
            # Se tudo estiver OK, executa o sorteio

            # Limpa resultados anteriores (se houver)
            results_placeholder = st.empty()

            with results_placeholder.container():
                # 1. Executa a seleção
                winner, inverse_probs = weighted_random_selection(name_frequencies)

                if winner:
                    # 2. Exibe as probabilidades
                    display_probabilities(name_frequencies, inverse_probs)

                    # 3. Exibe o resultado com suspense
                    suspense_selection_st(winner)

                    # 4. Prepara os dados atualizados e oferece opções para salvar
                    st.divider()
                    st.subheader("Salvar Resultado")

                    # Prepara os dados atualizados
                    updated_frequencies = name_frequencies.copy()
                    updated_frequencies[winner] += 1
                    updated_json_data = json.dumps(
                        updated_frequencies, indent=4, ensure_ascii=False
                    )

                    st.markdown(
                        f"O vencedor foi **{winner}**. A frequência dele/dela será atualizada de **{name_frequencies[winner]}** para **{updated_frequencies[winner]}**."
                    )

                    # Botão para baixar o JSON atualizado
                    st.download_button(
                        label=f"Baixar JSON atualizado (com {winner} +1)",
                        data=updated_json_data,
                        file_name="participantes_atualizados.json",
                        mime="application/json",
                        help="Baixa um novo arquivo .json com a frequência do vencedor incrementada.",
                    )

                    # Botão para atualizar a lista na própria tela
                    if st.button(
                        f"Atualizar lista na tela com {winner} +1",
                        help="Atualiza o JSON na caixa de texto acima para o próximo sorteio.",
                    ):
                        st.session_state.participants_json = updated_json_data
                        st.success(
                            "Lista de participantes na tela foi atualizada! Pode sortear novamente."
                        )
                        time.sleep(2)  # Pausa para o usuário ler a mensagem
                        st.rerun()

    except json.JSONDecodeError:
        st.error(
            "Erro ao ler os dados. Por favor, verifique se o formato JSON está correto."
        )
    except Exception as e:
        st.error(f"Ocorreu um erro inesperado: {e}")

# Informações na barra lateral
st.sidebar.header("Sobre")
st.sidebar.info(
    "Esta é uma aplicação Streamlit que implementa a lógica de sorteio ponderado do seu script, com seleção inversamente proporcional à frequência."
)
st.sidebar.markdown("Feito com Streamlit e `numpy`.")
