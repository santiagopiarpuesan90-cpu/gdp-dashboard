import streamlit as st
from datetime import datetime, date, time, timedelta
import pandas as pd

st.set_page_config(page_title="Compañero de Escritorio", page_icon="🦉", layout="wide")

# ------------------ Estado de sesión y registro ------------------
if "page" not in st.session_state:
    st.session_state.page = "Panel"
if "events" not in st.session_state:
    now = datetime.now()
    st.session_state.events = [
        {"id": 1, "fecha": (now - timedelta(days=1)).replace(hour=16, minute=35, second=0, microsecond=0),
         "tipo": "Persona detectada", "estado": "Pendiente", "detalle": "Se detectó una persona frente al escritorio."},
        {"id": 2, "fecha": (now - timedelta(days=1)).replace(hour=14, minute=12, second=0, microsecond=0),
         "tipo": "Movimiento", "estado": "Revisado", "detalle": "Movimiento registrado en el área de trabajo."},
        {"id": 3, "fecha": (now - timedelta(days=2)).replace(hour=10, minute=5, second=0, microsecond=0),
         "tipo": "Persona detectada", "estado": "Falsa alarma", "detalle": "La detección fue clasificada como falsa alarma."},
    ]
if "actions" not in st.session_state:
    st.session_state.actions = []
if "device_name" not in st.session_state:
    st.session_state.device_name = "Compañero del escritorio"
if "connected" not in st.session_state:
    st.session_state.connected = True
if "tracking" not in st.session_state:
    st.session_state.tracking = False
if "flash" not in st.session_state:
    st.session_state.flash = False
if "alerts_enabled" not in st.session_state:
    st.session_state.alerts_enabled = True
if "start_hour" not in st.session_state:
    st.session_state.start_hour = time(8, 0)
if "end_hour" not in st.session_state:
    st.session_state.end_hour = time(18, 0)
if "setup_step" not in st.session_state:
    st.session_state.setup_step = 1
if "setup_done" not in st.session_state:
    st.session_state.setup_done = False
if "last_capture" not in st.session_state:
    st.session_state.last_capture = datetime.now().strftime("%H:%M")

def log_action(label):
    st.session_state.actions.append({
        "hora": datetime.now().strftime("%H:%M:%S"),
        "pantalla": st.session_state.page,
        "acción": label
    })

def go(page):
    st.session_state.page = page
    log_action(f"Navegó a {page}")

# ------------------ Estilos ------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html, body, [class*="css"] {font-family: Inter, sans-serif;}
.block-container {padding-top: 1.2rem; max-width: 1200px;}
.hero {background:#1E3A5F;color:white;padding:22px 24px;border-radius:16px;margin-bottom:16px;}
.hero h1 {color:white;margin:0;font-size:1.65rem;}
.hero p {color:#e8eef5;margin:6px 0 0 0;}
.card {background:#F7FAFC;border:1px solid #dce5ee;border-radius:14px;padding:16px;margin-bottom:10px;}
.small {color:#64748b;font-size:0.88rem;}
.pill {display:inline-block;padding:5px 10px;border-radius:20px;font-weight:600;font-size:0.82rem;}
.ok {background:#dcfce7;color:#166534;}
.warn {background:#fef3c7;color:#92400e;}
.bad {background:#fee2e2;color:#991b1b;}
div.stButton > button {min-height:44px;border-radius:9px;font-weight:600;}
</style>
""", unsafe_allow_html=True)

# ------------------ Navegación ------------------
with st.sidebar:
    st.markdown("## 🦉 Compañero")
    st.caption("Prototipo de evaluación · versión 1")
    pages = ["Panel", "Vincular dispositivo", "En vivo", "Alertas", "Historial", "Configuración"]
    for pg in pages:
        if st.button(pg, use_container_width=True, type="primary" if st.session_state.page == pg else "secondary"):
            go(pg)
            st.rerun()
    st.divider()
    st.caption("SIMULACIÓN: no existe conexión física con ESP32-CAM.")
    st.caption(f"Acciones registradas: {len(st.session_state.actions)}")

st.markdown("""
<div class="hero">
  <h1>Compañero de Escritorio</h1>
  <p>Dispositivo inteligente con cámara para supervisar tu espacio de estudio.</p>
</div>
""", unsafe_allow_html=True)

page = st.session_state.page

# ------------------ Panel ------------------
if page == "Panel":
    st.subheader("Tu espacio, siempre bajo control")
    st.write("Desde este panel puedes consultar el estado del dispositivo, observar la cámara, atender alertas y revisar detecciones anteriores.")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Estado del dispositivo", "En línea" if st.session_state.connected else "Fuera de línea")
    with c2:
        st.metric("Seguimiento facial", "Activo" if st.session_state.tracking else "Pausado")
    with c3:
        pendientes = sum(1 for e in st.session_state.events if e["estado"] == "Pendiente")
        st.metric("Alertas pendientes", pendientes)
    st.markdown("### Accesos principales")
    a,b,c = st.columns(3)
    with a:
        if st.button("📹 Ver cámara en vivo", use_container_width=True):
            go("En vivo"); st.rerun()
    with b:
        if st.button("🔔 Revisar alertas", use_container_width=True):
            go("Alertas"); st.rerun()
    with c:
        if st.button("🗂️ Abrir historial", use_container_width=True):
            go("Historial"); st.rerun()
    st.info("Este sistema utiliza una ESP32-CAM para detectar presencia y permitir el monitoreo remoto. El seguimiento facial puede pausarse desde la interfaz.")
    st.markdown("### Actividad reciente")
    recent = sorted(st.session_state.events, key=lambda x:x["fecha"], reverse=True)[:3]
    for ev in recent:
        st.markdown(f"**{ev['tipo']}** · {ev['fecha'].strftime('%d/%m/%Y %H:%M')}  —  {ev['estado']}")

# ------------------ Vinculación ------------------
elif page == "Vincular dispositivo":
    st.subheader("Vinculación del dispositivo")
    st.write("Sigue los pasos para preparar tu Compañero por primera vez.")
    st.progress(st.session_state.setup_step / 4)
    st.caption(f"Paso {st.session_state.setup_step} de 4")
    if st.session_state.setup_step == 1:
        st.markdown("### 1. Identifica tu dispositivo")
        st.markdown('<div class="card"><h3>🦉 Compañero ESP32-CAM</h3><p>Escanea el código QR de la tarjeta incluida con tu dispositivo o continúa con la conexión manual.</p><b>Código de vinculación:</b> COMP-2026-05</div>', unsafe_allow_html=True)
        if st.button("Continuar con conexión manual", type="primary"):
            log_action("Seleccionó conexión manual")
            st.session_state.setup_step = 2; st.rerun()
    elif st.session_state.setup_step == 2:
        st.markdown("### 2. Conecta a una red Wi-Fi")
        ssid = st.text_input("Nombre de la red Wi-Fi", value="Red_Estudio")
        password = st.text_input("Contraseña de red (simulada)", type="password", value="12345678")
        if st.button("Validar conexión", type="primary"):
            log_action("Validó datos Wi-Fi")
            if ssid.strip() and len(password) >= 8:
                st.session_state.connected = True
                st.success("Conexión simulada correctamente.")
                st.session_state.setup_step = 3; st.rerun()
            else:
                st.error("No se pudo conectar. Comprueba los datos e inténtalo nuevamente.")
    elif st.session_state.setup_step == 3:
        st.markdown("### 3. Personaliza tu dispositivo")
        name = st.text_input("Nombre del dispositivo", value=st.session_state.device_name)
        track = st.checkbox("Activar seguimiento facial", value=st.session_state.tracking)
        if st.button("Guardar configuración", type="primary"):
            st.session_state.device_name = name.strip() or "Mi Compañero"
            st.session_state.tracking = track
            log_action("Guardó nombre y seguimiento")
            st.session_state.setup_step = 4; st.rerun()
    else:
        st.success("¡Tu Compañero está listo!")
        st.write(f"Nombre: **{st.session_state.device_name}**")
        st.write("La configuración inicial se completó correctamente.")
        if st.button("Ir al panel principal", type="primary"):
            st.session_state.setup_done = True
            st.session_state.setup_step = 1
            go("Panel"); st.rerun()
    if st.session_state.setup_step > 1 and st.button("Volver al paso anterior"):
        st.session_state.setup_step -= 1; log_action("Retrocedió en vinculación"); st.rerun()

# ------------------ En vivo ------------------
elif page == "En vivo":
    st.subheader("Monitoreo en tiempo real")
    left, right = st.columns([1.7,1])
    with left:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#dbeafe,#eff6ff);border:1px solid #bfdbfe;border-radius:16px;height:310px;display:flex;align-items:center;justify-content:center;flex-direction:column;">
        <div style="font-size:90px;">🦉</div>
        <div style="font-size:18px;font-weight:700;color:#1e3a5f;">Vista simulada de la cámara</div>
        <div style="color:#475569;">ESP32-CAM · imagen de demostración</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("📸 Capturar imagen", use_container_width=True):
            st.session_state.last_capture = datetime.now().strftime("%H:%M")
            st.session_state.events.insert(0, {"id":len(st.session_state.events)+1,"fecha":datetime.now(),"tipo":"Captura manual","estado":"Revisado","detalle":"Imagen capturada desde la vista en vivo."})
            log_action("Capturó imagen")
            st.success("Imagen guardada en el historial (simulación).")
    with right:
        status = "En línea" if st.session_state.connected else "Fuera de línea"
        st.markdown(f"### Estado: {status}")
        st.write(f"**Última imagen:** {st.session_state.last_capture}")
        st.write(f"**Dispositivo:** {st.session_state.device_name}")
        st.write(f"**Seguimiento:** {'Activo' if st.session_state.tracking else 'Pausado'}")
        if st.button("Pausar seguimiento" if st.session_state.tracking else "Activar seguimiento", use_container_width=True):
            st.session_state.tracking = not st.session_state.tracking
            log_action("Cambió seguimiento facial")
            st.rerun()
        if st.button("Simular desconexión / reconexión", use_container_width=True):
            st.session_state.connected = not st.session_state.connected
            log_action("Cambió estado de conexión")
            st.rerun()
        if not st.session_state.connected:
            st.error("El dispositivo está fuera de línea. Comprueba la alimentación y vuelve a intentar.")
            if st.button("Reintentar conexión"):
                st.session_state.connected = True
                log_action("Reintentó conexión")
                st.rerun()

# ------------------ Alertas ------------------
elif page == "Alertas":
    st.subheader("Alertas de detección")
    st.write("Consulta las notificaciones generadas por el dispositivo.")
    pending = [e for e in st.session_state.events if e["estado"] == "Pendiente"]
    if not pending:
        st.success("No tienes alertas pendientes.")
    for ev in pending:
        with st.container(border=True):
            st.markdown(f"**{ev['tipo']}**")
            st.caption(ev["fecha"].strftime("%d/%m/%Y · %H:%M"))
            st.write(ev["detalle"])
            c1,c2 = st.columns(2)
            with c1:
                if st.button("Marcar como revisada", key=f"review{ev['id']}"):
                    ev["estado"] = "Revisado"; log_action("Marcó alerta revisada"); st.rerun()
            with c2:
                if st.button("Marcar falsa alarma", key=f"false{ev['id']}"):
                    ev["estado"] = "Falsa alarma"; log_action("Marcó falsa alarma"); st.rerun()
    st.divider()
    if st.button("Simular nueva alerta de persona"):
        st.session_state.events.insert(0, {"id":max([e["id"] for e in st.session_state.events],default=0)+1,"fecha":datetime.now(),"tipo":"Persona detectada","estado":"Pendiente","detalle":"Se detectó una persona frente al escritorio."})
        log_action("Generó alerta simulada"); st.rerun()

# ------------------ Historial ------------------
elif page == "Historial":
    st.subheader("Historial de detecciones")
    st.write("Filtra los registros y consulta el detalle de una actividad anterior.")
    col1,col2 = st.columns(2)
    with col1:
        desde = st.date_input("Desde", value=date.today()-timedelta(days=2))
    with col2:
        hasta = st.date_input("Hasta", value=date.today())
    estado = st.selectbox("Tipo de registro", ["Todos","Persona detectada","Movimiento","Captura manual"])
    rows=[]
    for ev in st.session_state.events:
        d=ev["fecha"].date()
        if desde <= d <= hasta and (estado=="Todos" or ev["tipo"]==estado):
            rows.append(ev)
    if rows:
        df=pd.DataFrame([{"Fecha":e["fecha"].strftime("%d/%m/%Y %H:%M"),"Tipo":e["tipo"],"Estado":e["estado"],"ID":e["id"]} for e in sorted(rows,key=lambda x:x["fecha"],reverse=True)])
        st.dataframe(df, use_container_width=True, hide_index=True)
        chosen=st.selectbox("Selecciona un registro para ver sus detalles", options=[e["id"] for e in rows], format_func=lambda x: next(e["fecha"].strftime("%d/%m %H:%M")+" · "+e["tipo"] for e in rows if e["id"]==x))
        selected=next(e for e in rows if e["id"]==chosen)
        with st.container(border=True):
            st.markdown(f"**{selected['tipo']}**")
            st.write(selected["detalle"])
            st.write(f"Fecha: {selected['fecha'].strftime('%d/%m/%Y %H:%M')}")
            st.write(f"Estado: {selected['estado']}")
        if st.button("Exportar historial CSV"):
            st.download_button("Descargar CSV", df.to_csv(index=False).encode("utf-8-sig"), "historial_companero.csv", "text/csv")
            log_action("Preparó exportación de historial")
    else:
        st.warning("No se encontraron registros para los filtros seleccionados.")
        if st.button("Quitar filtros"):
            log_action("Quitó filtros del historial")
            st.rerun()

# ------------------ Configuración ------------------
elif page == "Configuración":
    st.subheader("Configuración y privacidad")
    st.markdown("### Seguimiento facial")
    tracking = st.toggle("Permitir seguimiento facial", value=st.session_state.tracking)
    if tracking != st.session_state.tracking:
        st.session_state.tracking = tracking
        log_action("Modificó seguimiento desde configuración")
    st.markdown("### Alertas")
    enabled = st.toggle("Recibir alertas de detección", value=st.session_state.alerts_enabled)
    if enabled != st.session_state.alerts_enabled:
        st.session_state.alerts_enabled = enabled
        log_action("Modificó alertas")
    start = st.time_input("Hora de inicio", value=st.session_state.start_hour)
    end = st.time_input("Hora de finalización", value=st.session_state.end_hour)
    if st.button("Guardar cambios", type="primary"):
        st.session_state.start_hour = start
        st.session_state.end_hour = end
        log_action("Guardó horario de alertas")
        st.success("Tus preferencias se guardaron correctamente.")
    st.info("Si el dispositivo se desconecta durante el horario configurado, el sistema mostrará el estado y permitirá reintentar la conexión.")
    st.markdown("### Datos del dispositivo")
    st.write(f"**Nombre:** {st.session_state.device_name}")
    st.write(f"**Conexión:** {'En línea' if st.session_state.connected else 'Fuera de línea'}")

# ------------------ Panel de apoyo para el equipo (oculto en uso normal) ------------------
with st.expander("Registro técnico de acciones (solo equipo evaluador)"):
    st.caption("Este registro sirve para revisar acciones realizadas durante una sesión. No sustituye la observación manual ni el cronómetro.")
    if st.session_state.actions:
        st.dataframe(pd.DataFrame(st.session_state.actions), use_container_width=True, hide_index=True)
        if st.button("Descargar registro de acciones"):
            st.download_button("Descargar acciones CSV", pd.DataFrame(st.session_state.actions).to_csv(index=False).encode("utf-8-sig"), "acciones_sesion.csv", "text/csv")
    else:
        st.write("Todavía no hay acciones registradas.")

st.divider()
st.caption("Prototipo académico de interacción · Simulación de interfaz · Grupo 5 · Práctica 6 IHM")
