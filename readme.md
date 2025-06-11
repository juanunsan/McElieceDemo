# 🌐 Classic McEliece Demo (TFG)

Demostración educativa —CLI y Streamlit— de un **KEM post-cuántico Classic McEliece** usando  
[`liboqs-python`](https://github.com/open-quantum-safe/liboqs-python).

> ⚠️ **Solo para fines docentes**. No usar tal cual en producción.

---

## 📋 Funcionalidades
| Modo | Archivo | Descripción |
|------|---------|-------------|
| **CLI** | `mceliece_demo.py` | Genera par de claves, encapsula secreto y cifra un mensaje con AES-128-CBC. |
| **Web** | `streamlit_mceliece_app.py` | Interfaz interactiva que muestra cada paso y tamaños de clave/ciphertext. |

---


## 🚀 Instalación rápida 
# 0. Si tu Windows no tiene Build Tools instalados
```bash
winget install -e --id Microsoft.VisualStudio.2022.BuildTools `
  --source winget --override "--add Microsoft.VisualStudio.Component.VC.Tools.x86.x64 --quiet --wait --norestart"

  call "%ProgramFiles(x86)%\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat" #En cada nueva sesión carga las variables de entorno
```


# 1. Clona el proyecto
```bash
git clone https://github.com/juanunsan/McElieceDemo.git
cd McElieceDemo
```
# 2. **Native Tools** 
```bash
     Abre el "x64 Native Tools Command Prompt for VS 2022" # Linux/macOS: Asegúrate de tener un compilador C/C++ y CMake ≥ 3.20.
```
# 3. Crea un entorno virtual con Python 3.11  (3.9-3.11 funcionan; 3.12 aún no)
```bash
py -3.11 -m venv venv               # Linux/macOS: python3.11 -m venv venv
venv\Scripts\activate               # Linux/macOS: source venv/bin/activate
```
# 4. Instala dependencias **compilando liboqs** (tarda unos minutos)
```bash
python -m pip install -U pip wheel cmake
python -m pip install --no-binary :all: ^
       "liboqs-python @ git+https://github.com/open-quantum-safe/liboqs-python@0.10.0"
python -m pip install streamlit==1.45.0 pycryptodome==3.20.0
```
# 5. (solo Windows) añade las DLL de liboqs a la sesión
```bash
set "Path=%USERPROFILE%\_oqs\bin;%Path%"
```
# 6. ¡Listo!
```bash
streamlit run streamlit_mceliece_app.py          # interfaz web
python mceliece_demo.py "Hola" -p Classic-McEliece-348864   # CLI
```
## 📜 Licencias y créditos
* **liboqs / liboqs-python** © Open Quantum Safe (Apache 2.0)  
* Esta demo forma parte del **Trabajo Fin de Grado** de *Juan Nuñez Sanchez* (2025).

> Pull requests con mejoras de documentación o CI son bienvenidos.
