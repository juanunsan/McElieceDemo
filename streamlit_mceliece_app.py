import binascii, textwrap, sys
from hashlib import sha256

import streamlit as st
import oqs                                # liboqs-python wrapper
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# ------------------------------------------------------------------------------
st.set_page_config(page_title="Demo Classic McEliece", page_icon="🔐", layout="centered")
st.title("🔐 Demostración interactiva — Classic McEliece KEM")

st.markdown(
    """
    Esta aplicación muestra cómo **Classic McEliece** establece un secreto compartido  
    y cómo de él se deriva una clave simétrica para cifrar un mensaje.

    > ⚠️ *Demo educativa*. No usar tal cual en producción.
    """,
    unsafe_allow_html=True,
)

# ------------ parámetros disponibles sólo Classic-McEliece-* -------------------
MCELIECE_PARAMS = [
    p for p in oqs.get_enabled_kem_mechanisms() if p.startswith("Classic-McEliece")
]
DEFAULT_PARAM = "Classic-McEliece-348864"
default_idx   = MCELIECE_PARAMS.index(DEFAULT_PARAM) if DEFAULT_PARAM in MCELIECE_PARAMS else 0

with st.sidebar:
    st.header("⚙️ Configuración")
    param_choice = st.selectbox("Conjunto de parámetros", MCELIECE_PARAMS, index=default_idx)
    texto_plano  = st.text_area("Mensaje a cifrar", "Hola TFG 📚", max_chars=4096)
    ejecutar     = st.button("Cifrar", use_container_width=True)

# ------------------------------------------------------------------------------
if not ejecutar:
    st.stop()

plaintext_bytes = texto_plano.encode()

st.subheader("1️⃣ Generación de claves")
with oqs.KeyEncapsulation(param_choice) as kem:

    # --- compatibilidad versión vieja / nueva ---------------------------------
    if hasattr(kem, "generate_keypair"):            # API ≤ 0.10
        public_key = kem.generate_keypair()         # devuelve la PK
        try:                                        # SK sólo si existe export*
            secret_key = kem.export_secret_key()
            sk_len = f"{len(secret_key)/1024:.1f} KB"
        except AttributeError:
            secret_key = None
            sk_len = "- (interna)"
    else:                                           # API ≥ 0.11
        public_key = kem.export_public_key()
        secret_key = kem.export_secret_key()
        sk_len     = f"{len(secret_key)/1024:.1f} KB"

    col1, col2 = st.columns(2)
    col1.metric("Clave pública", f"{len(public_key)/1024:.1f} KB")
    col2.metric("Clave secreta", sk_len)

    # ---------------- encapsular y decapsular ----------------------------------
    st.subheader("2️⃣ Encapsulación del secreto")
    ciphertext, shared_secret_enc = kem.encap_secret(public_key)
    st.write("Ciphertext (tamaño):", f"{len(ciphertext)/1024:.1f} KB")
    st.code(binascii.hexlify(ciphertext).decode(), language="text")

    st.subheader("3️⃣ Decapsulación y verificación")
    try:                                            # API ≥ 0.11
        shared_secret_dec = kem.decap_secret(ciphertext, secret_key)
    except TypeError:                               # API ≤ 0.10 (no pasa la SK)
        shared_secret_dec = kem.decap_secret(ciphertext)

    if shared_secret_dec == shared_secret_enc:
        st.success("Secreto verificado correctamente ✨")
    else:
        st.error("¡Los secretos no coinciden!")
        sys.exit()

# ---------- derivar AES-128-CBC y cifrar ---------------------------------------
st.subheader("4️⃣ Cifrado simétrico del mensaje (AES-128-CBC)")
key = sha256(shared_secret_enc).digest()[:16]          # 128-bit
iv  = b"\0"*16                                         # IV fijo (demo)
ct  = AES.new(key, AES.MODE_CBC, iv=iv).encrypt(pad(plaintext_bytes, 16))

st.code(textwrap.dedent(f"""
    Clave derivada (hex): {binascii.hexlify(key).decode()}
    Texto cifrado (hex):  {binascii.hexlify(ct).decode()}
"""), language="text")

# ---------- descifrar para mostrar round-trip -----------------------------------
recovered = unpad(AES.new(key, AES.MODE_CBC, iv=iv).decrypt(ct), 16)

with st.expander("Ver texto descifrado ⬇️"):
    st.write(recovered.decode())

st.success("Demo completada ✔️")

st.markdown(
    """
    ---
    ### ℹ️ Glosario rápido
    * **KEM** (*Key Encapsulation Mechanism*): algoritmo que establece un secreto compartido con clave pública.
    * **Classic McEliece**: esquema KEM resistente a ordenadores cuánticos (basado en códigos correctores).
    * **AES-128-CBC**: cifrado simétrico por bloques; aquí se usa sólo como ejemplo.
    """
)
