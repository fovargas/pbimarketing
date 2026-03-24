import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor

# ── Configuración — leída desde .streamlit/secrets.toml ───────────────────────
TABLE_NAME = "marca_evento"

@st.cache_resource
def get_conn():
    return psycopg2.connect(
        host=st.secrets["db_host"],
        port=st.secrets["db_port"],
        dbname=st.secrets["db_name"],
        user=st.secrets["db_user"],
        password=st.secrets["db_password"],
        cursor_factory=RealDictCursor,
        sslmode="require",
    )

def insert_row(payload: dict):
    cols         = ", ".join(payload.keys())
    placeholders = ", ".join(["%s"] * len(payload))
    sql          = f"INSERT INTO {TABLE_NAME} ({cols}) VALUES ({placeholders})"
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute(sql, list(payload.values()))
    conn.commit()

# ── Estilos ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] { background-color: #f7f9fc; }

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
</style>
""", unsafe_allow_html=True)

# ── Encabezado ─────────────────────────────────────────────────────────────────
st.markdown('<div class="titulo-principal">🏷️ Radiografía de marca y posicionamiento</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitulo">Responde sobre tu empresa. En tiempo real veremos colectivamente cómo están posicionadas las marcas de la sala en el tablero de Power BI.</div>', unsafe_allow_html=True)

# ── Formulario ─────────────────────────────────────────────────────────────────
with st.form("form_marca", clear_on_submit=True):

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

    antiguedad_empresa = st.selectbox(
        "Años de la empresa en el mercado *",
        options=[
            "— Selecciona —",
            "Menos de 2 años",
            "2–5 años",
            "6–15 años",
            "Más de 15 años",
        ],
    )

    # ── Sección 2: Posicionamiento percibido ──────────────────────────────────
    st.markdown('<div class="seccion-header">SECCIÓN 2 — Posicionamiento percibido</div>', unsafe_allow_html=True)

    posicionamiento_actual = st.selectbox(
        "¿Cómo describirías el posicionamiento actual de tu marca? *",
        options=[
            "— Selecciona —",
            "Líder reconocido en mi sector",
            "Competidor sólido pero no el primero",
            "En construcción / poco conocida",
            "No tenemos posicionamiento definido",
        ],
    )

    atributo_competencia = st.selectbox(
        "¿En qué atributo compite principalmente tu marca? *",
        options=[
            "— Selecciona —",
            "Precio / accesibilidad",
            "Calidad / premium",
            "Innovación / tecnología",
            "Servicio / experiencia del cliente",
            "Tradición / confianza",
            "Especialización / nicho",
        ],
    )

    brecha_percepcion = st.select_slider(
        "¿Qué tan cerca está la percepción real de tus clientes de cómo quisieras ser percibido? *",
        options=[1, 2, 3, 4, 5],
        value=3,
        format_func=lambda x: {
            1: "1 — Muy lejos de lo que queremos",
            2: "2 — Bastante diferente",
            3: "3 — Más o menos alineado",
            4: "4 — Bastante cerca",
            5: "5 — Exactamente como queremos",
        }[x],
    )

    # Indicador de brecha en tiempo real
    if brecha_percepcion <= 2:
        b_color, b_emoji, b_estado = "#ef4444", "🔴", "Brecha alta — lo que comunicas no llega como esperas"
    elif brecha_percepcion == 3:
        b_color, b_emoji, b_estado = "#f59e0b", "🟡", "Brecha media — hay oportunidad de mejora"
    else:
        b_color, b_emoji, b_estado = "#10b981", "🟢", "Brecha baja — tu marca comunica lo que quiere comunicar"

    st.markdown(
        f"""<div style="background:{b_color}18; border-left: 4px solid {b_color};
        padding: 10px 16px; border-radius: 6px; margin: 8px 0 16px 0;
        font-size: 14px; color: {b_color}; font-weight: 600;">
        {b_emoji} {b_estado}
        </div>""",
        unsafe_allow_html=True,
    )

    col3, col4 = st.columns(2)
    with col3:
        num_competidores = st.selectbox(
            "¿Cuántos competidores directos identificas? *",
            options=[
                "— Selecciona —",
                "1–3",
                "4–10",
                "Más de 10",
                "No tenemos competencia directa clara",
            ],
        )
    with col4:
        tiene_propuesta_valor = st.selectbox(
            "¿Tu empresa tiene propuesta de valor escrita y comunicada? *",
            options=[
                "— Selecciona —",
                "Sí, todos la conocen y la usan",
                "Sí, existe pero poco usada",
                "Está en proceso",
                "No existe",
            ],
        )

    # ── Sección 3: Coherencia de marca ────────────────────────────────────────
    st.markdown('<div class="seccion-header">SECCIÓN 3 — Coherencia e identidad de marca</div>', unsafe_allow_html=True)

    consistencia_comunicacion = st.select_slider(
        "¿Qué tan consistente es tu comunicación entre canales? *",
        options=[1, 2, 3, 4, 5],
        value=3,
        format_func=lambda x: {
            1: "1 — Cada canal dice algo diferente",
            2: "2 — Poca consistencia",
            3: "3 — Más o menos alineado",
            4: "4 — Bastante consistente",
            5: "5 — Totalmente coherente",
        }[x],
    )

    col5, col6 = st.columns(2)
    with col5:
        identidad_formal = st.selectbox(
            "¿Tienes identidad de marca formal (manual, guía de estilo)? *",
            options=[
                "— Selecciona —",
                "Sí, completa y actualizada",
                "Sí, pero desactualizada",
                "Solo lo básico (logo y colores)",
                "No tenemos",
            ],
        )
    with col6:
        mide_percepcion = st.selectbox(
            "¿Con qué frecuencia mides la percepción de tu marca? *",
            options=[
                "— Selecciona —",
                "Regularmente (encuestas, NPS, focus groups)",
                "Ocasionalmente",
                "Casi nunca",
                "Nunca lo hemos medido",
            ],
        )

    col7, col8 = st.columns(2)
    with col7:
        amenaza_principal = st.selectbox(
            "Principal amenaza para tu marca hoy *",
            options=[
                "— Selecciona —",
                "Un competidor más barato",
                "Un competidor más innovador",
                "Pérdida de reputación / crisis",
                "Irrelevancia / no nos conocen",
                "Sustitutos tecnológicos",
            ],
        )
    with col8:
        inversion_marca = st.selectbox(
            "Nivel de inversión en construcción de marca *",
            options=[
                "— Selecciona —",
                "Alta — es prioridad estratégica",
                "Media — invertimos algo",
                "Baja — solo lo básico",
                "Ninguna — no lo vemos necesario",
            ],
        )

    st.markdown("---")
    submitted = st.form_submit_button("Enviar mi marca al tablero →")

# ── Procesamiento del envío ────────────────────────────────────────────────────
if submitted:
    campos_vacios = []
    selects = {
        "Sector":                   sector,
        "Tamaño empresa":           tamano_empresa,
        "Antigüedad":               antiguedad_empresa,
        "Posicionamiento actual":   posicionamiento_actual,
        "Atributo de competencia":  atributo_competencia,
        "Competidores":             num_competidores,
        "Propuesta de valor":       tiene_propuesta_valor,
        "Identidad formal":         identidad_formal,
        "Medición de percepción":   mide_percepcion,
        "Amenaza principal":        amenaza_principal,
        "Inversión en marca":       inversion_marca,
    }
    for label, val in selects.items():
        if val.startswith("— Selecciona"):
            campos_vacios.append(label)

    if campos_vacios:
        st.error(f"Por favor completa: {', '.join(campos_vacios)}")
    else:
        payload = {
            "sector":                    sector,
            "tamano_empresa":            tamano_empresa,
            "antiguedad_empresa":        antiguedad_empresa,
            "posicionamiento_actual":    posicionamiento_actual,
            "atributo_competencia":      atributo_competencia,
            "brecha_percepcion":         brecha_percepcion,
            "num_competidores":          num_competidores,
            "tiene_propuesta_valor":     tiene_propuesta_valor,
            "consistencia_comunicacion": consistencia_comunicacion,
            "identidad_formal":          identidad_formal,
            "mide_percepcion":           mide_percepcion,
            "amenaza_principal":         amenaza_principal,
            "inversion_marca":           inversion_marca,
            # score_marca es columna generada en Supabase, no se envía
        }

        try:
            insert_row(payload)
            st.success("✅ ¡Tu marca fue registrada! Ya aparece en el tablero de Power BI.")
            st.balloons()
            st.markdown(
                f"""<div style="background:#f0fdf4; border:1px solid #86efac;
                padding:16px; border-radius:8px; margin-top:12px;">
                <b>Resumen de tu marca:</b><br>
                🏢 <b>{sector}</b> · {tamano_empresa}<br>
                🎯 Posicionamiento: <b>{posicionamiento_actual}</b><br>
                ⚔️ Compite en: <b>{atributo_competencia}</b><br>
                📊 Percepción: <span style="color:{b_color}; font-weight:600;">{b_estado}</span>
                </div>""",
                unsafe_allow_html=True,
            )
        except psycopg2.OperationalError:
            st.cache_resource.clear()
            try:
                insert_row(payload)
                st.success("✅ ¡Tu marca fue registrada! Ya aparece en el tablero de Power BI.")
                st.balloons()
            except Exception as e2:
                st.error(f"No se pudo conectar a la base de datos: {e2}")
                st.info("Verifica db_host, db_user y db_password en secrets.toml.")
        except Exception as e:
            st.error(f"Error al guardar: {e}")
            st.info("Verifica la configuración de conexión al pooler de Supabase.")