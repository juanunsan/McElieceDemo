# 🌐 Classic McEliece Demo (TFG)

Demostración interactiva (Streamlit) y de consola (CLI) de un KEM pos-cuántico
**Classic McEliece** usando la librería `liboqs-python`.

## Instalar & ejecutar

```bash
git clone https://github.com/TU-USUARIO/classic-mceliece-demo.git
cd classic-mceliece-demo

python -m venv venv
venv\Scripts\activate         # Linux/macOS: source venv/bin/activate
pip install --no-binary :all: -r requirements.txt

# (solo Windows) añadir bin\ de liboqs al PATH de la sesión:
set "Path=%USERPROFILE%\_oqs\bin;%Path%"

# Aplicación web
streamlit run streamlit_mceliece_app.py

# Ejemplo en consola
python mceliece_demo.py "Hola mundo" -p Classic-McEliece-348864
