import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO


st.set_page_config(page_title="PLOTXY", page_icon="📊")

# Configuración de estilo
st.markdown("""
<style>
.neon-title {
    font-size: 36px !important;
    font-weight: bold !important;
    color: #FF00FF !important;
    text-shadow: 0 0 10px #FF00FF,
                 0 0 20px #FF00FF,
                 0 0 30px #FF00FF,
                 0 0 40px #FF00FF;
    margin: 0 !important;
    padding: 10px 0;
}
</style>
""", unsafe_allow_html=True)

def main():
    # Título e instrucciones
    col_title, col_inst = st.columns([1, 3])
    with col_title:
        st.markdown('<h1 class="neon-title">PLOTXY</h1>', unsafe_allow_html=True)
    
    with col_inst:
        with st.expander("📌 Instrucciones"):
            st.markdown("""
            1. Sube archivo .txt o ingresa datos
            2. Formato: 2 columnas numéricas
            3. Usa punto decimal
            4. Personaliza en la barra lateral
            """)

    # Sección de entrada de datos
    uploaded_file = st.file_uploader("Cargar archivo TXT", type=["txt"])
    datos = st.text_area("Ingreso manual:", 
                       height=200,
                       placeholder="Ejemplo:\n1 3\n2 5\n3 7\n4 6")

    # Procesar datos
    df = pd.DataFrame()
    if uploaded_file or datos:
        try:
            content = uploaded_file.getvalue().decode() if uploaded_file else datos
            lineas = [line.split() for line in content.split('\n') if line.strip()]
            df = pd.DataFrame(lineas, columns=['X', 'Y']).astype(float)
        except Exception as e:
            st.error(f"Error: {str(e)}")
            return

    # Barra lateral de configuración
    with st.sidebar:
        st.header("Personalización")
        titulo = st.text_input("Título", "Gráfico PLOTXY")
        eje_x = st.text_input("Eje X", "X")
        eje_y = st.text_input("Eje Y", "Y")
        color = st.color_picker("Color", "#FF00FF")
        st.checkbox("Mostrar puntos", True, key='puntos')
        st.checkbox("Comenzar en (0,0)", True, key='origen')
        
        # Incrementos ajustados
        st.number_input("Incremento X", 
                       min_value=0.1, 
                       max_value=100.0, 
                       value=10.0,  # Valor por defecto X=10
                       step=1.0,
                       key='inc_x')
        
        st.number_input("Incremento Y", 
                       min_value=0.1, 
                       max_value=100.0, 
                       value=50.0,  # Valor por defecto Y=50
                       step=5.0,
                       key='inc_y')

    if not df.empty:
        # Crear y configurar gráfico
        fig = px.line(df, x='X', y='Y', 
                    markers=st.session_state.puntos,
                    title=titulo,
                    labels={'X': eje_x, 'Y': eje_y})
        
        fig.update_traces(
            line=dict(color=color, width=3),
            marker=dict(size=10, color=color, line=dict(width=2, color='black'))
        )
        
        # Configuración de ejes
        if st.session_state.origen:
            x_max = max(df.X.max(), 10)  # Mínimo 10 para mejor visualización
            y_max = max(df.Y.max(), 50)  # Mínimo 50 para mejor visualización
            fig.update_xaxes(range=[0, x_max * 1.1])
            fig.update_yaxes(range=[0, y_max * 1.1])
        
        fig.update_xaxes(dtick=st.session_state.inc_x)
        fig.update_yaxes(dtick=st.session_state.inc_y)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Exportar
        buffer = BytesIO()
        fig.write_image(buffer, format="png")
        st.download_button(
            "Descargar PNG",
            buffer.getvalue(),
            "grafico.png",
            "image/png"
        )

if __name__ == "__main__":
    main()