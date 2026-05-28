import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Configuración del Dashboard
st.set_page_config(page_title="Análisis de Vigas", layout="wide")
st.title("📊 Dashboard Predictivo: Deflexión en Vigas Hiperestáticas")
st.markdown("### Método: Condiciones de Compatibilidad y Doble Integración")
st.markdown("Simulación predictiva de una viga empotrada-apoyada con carga distribuida.")

# Controles Dinámicos en la barra lateral
st.sidebar.header("🛠️ Parámetros Variables")
L = st.sidebar.slider("Longitud de la viga (L) en metros", 2.0, 15.0, 6.0, step=0.5)
w = st.sidebar.slider("Carga distribuida (w) en kN/m", 0.0, 80.0, 20.0, step=2.0)

st.sidebar.subheader("Propiedades del Material")
E_gpa = st.sidebar.number_input("Módulo de Elasticidad (E) en GPa", value=200) # Acero
I_cm4 = st.sidebar.number_input("Momento de Inercia (I) en cm⁴", value=8500)

# Conversión interna de unidades al Sistema Internacional (N y metros)
E = E_gpa * 1e9  
I = I_cm4 * 1e-8 
EI = E * I

# Motor de Cálculo (Doble Integración + Compatibilidad)
Rb = (3 / 8) * w * 1000 * L  # Reacción apoyo simple
Ra = (w * 1000 * L) - Rb     # Reacción apoyo empotrado
Ma = (1 / 8) * w * 1000 * (L ** 2) # Momento en empotramiento

# Puntos para la curva del gráfico
x = np.linspace(0, L, 500)

# Ecuaciones resultantes
M = Ra * x - Ma - (w * 1000 * x ** 2) / 2
y = (1 / EI) * ((Ra * x ** 3) / 6 - (Ma * x ** 2) / 2 - (w * 1000 * x ** 4) / 24)
y_mm = y * 1000 # Convertir a milímetros para leer mejor

# Panel de Indicadores (KPIs)
ymax_predicha = abs(np.min(y_mm))
L_flecha_adm = (L * 1000) / 360 # Límite reglamentario común

col1, col2, col3 = st.columns(3)
col1.metric("Reacción Izquierda (Ra)", f"{Ra/1000:.2f} kN")
col2.metric("Momento en Empotramiento (Ma)", f"{Ma/1000:.2f} kN·m")
with col3:
    if ymax_predicha <= L_flecha_adm:
        st.metric("Deflexión Máxima", f"{ymax_predicha:.2f} mm", "✅ CUMPLE NORMA")
    else:
        st.metric("Deflexión Máxima", f"{ymax_predicha:.2f} mm", "-❌ EXCEDE LÍMITE", delta_color="inverse")

# Gráfico interactivo
st.subheader("📉 Predicción de la Deformación (Curva Elástica)")
fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y_mm, mode='lines', name='Curva Elástica (Predicción)', line=dict(color='blue', width=3)))
fig.add_trace(go.Scatter(x=[0, L], y=[0, 0], mode='lines', name='Viga Original (Sin carga)', line=dict(color='gray', dash='dash')))

fig.update_layout(xaxis_title="Posición en la viga (x) [m]", yaxis_title="Deflexión [mm]", height=400)
st.plotly_chart(fig, use_container_width=True)