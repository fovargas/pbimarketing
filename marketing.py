import streamlit as st
from supabase import create_client
import os

# ── Configuración ──────────────────────────────────────────────────────────────
SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://TU_PROJECT.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "TU_ANON_KEY")
TABLE_NAME   = "proyectos_evento"

@st.cache_resource
def get_client():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = get_client()

# ── Estilos ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Fondo y fuente general */
    [data-testid="stAppViewContainer"] {
        background-color: #f7f9fc;
    }
    /* Header de secciones */
    .seccion-header {
        background-color: #0B416D;
        color: white;
        padding: 8px 16px;
        border-radius: 6px;
        font-size: 14px;
        font-weight: 600;
        margin: 24px 0 12px 0;
        letter-spacing: 0.5px;
    }
    /* Card del formulario */
    .form-card {
        background: white;
        border-radius: 12px;
        padding: 28px 32px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.07);
        margin-bottom: 16px;
    }
    /* Título principal */
    .titulo-principal {
        color: #0B416D;
        font-size: 26px;
        font-weight: 700;
        margin-bottom: 4px;
    }
    .subtitulo {
        color: #5a7fa8;
        font-size: 14px;
        margin-bottom: 24px;
    }
    /* Botón submit */
    div[data-testid="stFormSubmitButton"] > button {
        background-color: #0B416D;
        color: white;
        border: none;
        padding: 12px 36px;
        border-radius: 8px;
        font-size: 16px;
        font-weight: 600;
        width: 100%;
        transition: background 0.2s;
    }
    div[data-testid="stFormSubmitButton"] > button:hover {
        background-color: #0d5490;
    }
    /* Slider labels */
    .slider-label {
        font-size: 13px;
        color: #666;
        display: flex;
        justify-content: space-between;
        margin-top: -12px;
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ── Encabezado ─────────────────────────────────────────────────────────────────
st.markdown('<div class="titulo-principal">📊 Radiografía del portafolio organizacional</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitulo">Completa los datos de un proyecto real o representativo de tu organización. La información se visualiza en tiempo real en el tablero de Power BI.</div>', unsafe_allow_html=True)

# ── Formulario ─────────────────────────────────────────────────────────────────
with st.form("form_proyectos", clear_on_submit=True):

    # ── Sección 1: Contexto ───────────────────────────────────────────────────
    st.markdown('<div class="seccion-header">SECCIÓN 1 — Contexto de tu organización</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        sector = st.selectbox(
            "Sector de tu empresa *",
            options=[
                "— Selecciona —",
                "Retail / Comercio",
                "Servicios profesionales",
                "Manufactura",
                "Educación",
                "Salud",
                "Tecnología",
                "Construcción / Infraestructura",
                "Gobierno / Público",
                "Otro",
            ],
        )

    with col2:
        tamano_empresa = st.selectbox(
            "Tamaño de la empresa *",
            options=[
                "— Selecciona —",
                "1–10 personas",
                "11–50 personas",
                "51–200 personas",
                "201–500 personas",
                "+500 personas",
            ],
        )

    # ── Sección 2: Datos del proyecto ─────────────────────────────────────────
    st.markdown('<div class="seccion-header">SECCIÓN 2 — Datos del proyecto</div>', unsafe_allow_html=True)

    col3, col4 = st.columns(2)

    with col3:
        tipo_proyecto = st.selectbox(
            "Tipo de proyecto *",
            options=[
                "— Selecciona —",
                "Tecnología / Sistemas",
                "Comercial / Ventas",
                "Operativo / Procesos",
                "Recursos Humanos",
                "Infraestructura / Obra",
                "Marketing / Comunicación",
            ],
        )

    with col4:
        duracion_plan = st.selectbox(
            "Duración total planificada *",
            options=[
                "— Selecciona —",
                "Menos de 1 mes",
                "1 a 3 meses",
                "3 a 6 meses",
                "6 a 12 meses",
                "Más de 12 meses",
            ],
        )

    fase_actual = st.selectbox(
        "Fase actual del proyecto *",
        options=[
            "— Selecciona —",
            "Inicio",
            "Planificación",
            "Ejecución",
            "Seguimiento y control",
            "Cierre",
        ],
    )

    col5, col6 = st.columns(2)

    with col5:
        avance_real = st.slider(
            "¿Cuál es el avance REAL del proyecto hoy? (%)",
            min_value=0, max_value=100, value=50, step=5,
            help="Sé honesto — nadie te está evaluando aquí 😊"
        )
        st.markdown('<div class="slider-label"><span>0%</span><span>50%</span><span>100%</span></div>', unsafe_allow_html=True)

    with col6:
        avance_esperado = st.slider(
            "¿Cuál DEBERÍA ser el avance a esta fecha? (%)",
            min_value=0, max_value=100, value=50, step=5,
            help="Según el cronograma original planificado"
        )
        st.markdown('<div class="slider-label"><span>0%</span><span>50%</span><span>100%</span></div>', unsafe_allow_html=True)

    # Indicador de desviación en tiempo real
    desviacion = avance_esperado - avance_real
    if desviacion > 20:
        color, emoji, estado = "#ef4444", "🔴", f"Proyecto en estado CRÍTICO (+{desviacion} pts de retraso)"
    elif desviacion > 5:
        color, emoji, estado = "#f59e0b", "🟡", f"Proyecto con retraso leve (+{desviacion} pts)"
    elif desviacion < 0:
        color, emoji, estado = "#10b981", "🟢", f"Proyecto adelantado ({abs(desviacion)} pts)"
    else:
        color, emoji, estado = "#10b981", "🟢", f"Proyecto al día ({desviacion} pts de desviación)"

    st.markdown(
        f"""<div style="background:{color}18; border-left: 4px solid {color};
        padding: 10px 16px; border-radius: 6px; margin: 8px 0 16px 0;
        font-size: 14px; color: {color}; font-weight: 600;">
        {emoji} {estado}
        </div>""",
        unsafe_allow_html=True,
    )

    tamano_equipo = st.selectbox(
        "Tamaño del equipo del proyecto *",
        options=[
            "— Selecciona —",
            "1–3 personas",
            "4–8 personas",
            "9–15 personas",
            "Más de 15 personas",
        ],
    )

    # ── Sección 3: Salud del proyecto ─────────────────────────────────────────
    st.markdown('<div class="seccion-header">SECCIÓN 3 — Salud del proyecto</div>', unsafe_allow_html=True)

    estado_presupuesto = st.selectbox(
        "Estado del presupuesto *",
        options=[
            "— Selecciona —",
            "Dentro del rango",
            "Sobreejecutado (gastamos más de lo planeado)",
            "Subejecutado (gastamos menos, hay retraso de actividades)",
            "No tenemos presupuesto formalmente definido",
        ],
    )

    claridad_objetivo = st.select_slider(
        "¿Qué tan claro tiene el equipo el objetivo del proyecto? *",
        options=[1, 2, 3, 4, 5],
        value=3,
        format_func=lambda x: {
            1: "1 — Nadie lo tiene claro",
            2: "2 — Muy confuso",
            3: "3 — Más o menos alineados",
            4: "4 — Bastante claro",
            5: "5 — Todos 100% alineados",
        }[x],
    )

    riesgo_principal = st.selectbox(
        "Principal riesgo activo en este momento *",
        options=[
            "— Selecciona —",
            "Falta de recursos humanos",
            "Desviación de alcance (scope creep)",
            "Problemas de tiempo / cronograma",
            "Presupuesto insuficiente",
            "Falta de apoyo directivo",
            "Dependencias externas",
            "Sin riesgos identificados formalmente",
        ],
    )

    tiene_reporte_formal = st.selectbox(
        "¿Existe un reporte de estado formal y periódico? *",
        options=[
            "— Selecciona —",
            "Sí, se reporta semanalmente",
            "Sí, pero de forma irregular",
            "No existe reporte formal",
            "Estamos construyéndolo",
        ],
    )

    satisfaccion_equipo = st.select_slider(
        "Nivel de satisfacción del equipo con la gestión del proyecto *",
        options=[1, 2, 3, 4, 5],
        value=3,
        format_func=lambda x: {
            1: "1 — Muy insatisfecho",
            2: "2 — Insatisfecho",
            3: "3 — Neutral",
            4: "4 — Satisfecho",
            5: "5 — Muy satisfecho",
        }[x],
    )

    st.markdown("---")
    submitted = st.form_submit_button("Enviar mi proyecto al tablero →")

# ── Procesamiento del envío ────────────────────────────────────────────────────
if submitted:
    # Validación de campos obligatorios
    campos_vacios = []
    selects = {
        "Sector": sector,
        "Tamaño empresa": tamano_empresa,
        "Tipo de proyecto": tipo_proyecto,
        "Duración planificada": duracion_plan,
        "Fase actual": fase_actual,
        "Tamaño del equipo": tamano_equipo,
        "Estado del presupuesto": estado_presupuesto,
        "Riesgo principal": riesgo_principal,
        "Reporte formal": tiene_reporte_formal,
    }
    for label, val in selects.items():
        if val.startswith("— Selecciona"):
            campos_vacios.append(label)

    if campos_vacios:
        st.error(f"Por favor completa: {', '.join(campos_vacios)}")
    else:
        payload = {
            "sector":               sector,
            "tamano_empresa":       tamano_empresa,
            "tipo_proyecto":        tipo_proyecto,
            "duracion_plan":        duracion_plan,
            "fase_actual":          fase_actual,
            "avance_real":          avance_real,
            "avance_esperado":      avance_esperado,
            "tamano_equipo":        tamano_equipo,
            "estado_presupuesto":   estado_presupuesto,
            "claridad_objetivo":    claridad_objetivo,
            "riesgo_principal":     riesgo_principal,
            "tiene_reporte_formal": tiene_reporte_formal,
            "satisfaccion_equipo":  satisfaccion_equipo,
            # desviacion_pct es columna generada en Supabase, no se envía
        }

        try:
            supabase.table(TABLE_NAME).insert(payload).execute()
            st.success("✅ ¡Tu proyecto fue registrado! Ya aparece en el tablero de Power BI.")
            st.balloons()
            st.markdown(
                f"""<div style="background:#f0fdf4; border:1px solid #86efac;
                padding:16px; border-radius:8px; margin-top:12px;">
                <b>Resumen de tu proyecto:</b><br>
                🏢 <b>{sector}</b> · {tipo_proyecto}<br>
                📅 Fase: <b>{fase_actual}</b> · Equipo: <b>{tamano_equipo}</b><br>
                📊 Avance real <b>{avance_real}%</b> vs esperado <b>{avance_esperado}%</b>
                → <span style="color:{color}; font-weight:600;">{estado}</span>
                </div>""",
                unsafe_allow_html=True,
            )
        except Exception as e:
            st.error(f"Error al guardar: {e}")
            st.info("Verifica que SUPABASE_URL y SUPABASE_KEY estén configurados correctamente.")