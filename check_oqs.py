import importlib, importlib.metadata as md, sys, ctypes
import oqs

# versión del wrapper (pyoqs) o atributo __version__
try:
    wrapper = md.version("pyoqs")
except md.PackageNotFoundError:
    wrapper = getattr(oqs, "__version__", "n/a")

print("Wrapper  :", wrapper)
print("KeyEncap?:", hasattr(oqs, "KeyEncapsulation"))

# versión de la DLL liboqs (si está en PATH)
try:
    print("liboqs C :", ctypes.cdll.LoadLibrary("oqs").OQS_VERSION_STRING.decode())
except OSError as e:
    print("liboqs C : <no DLL>", e)

print("Python   :", sys.version.split()[0])

