#!/usr/bin/env python3
"""
Pequeña aplicación que demuestra el flujo básico del algoritmo Classic McEliece
utilizando la biblioteca liboqs-python.

Requisitos:
    pip install oqs pycryptodome

Uso:
    python mceliece_demo.py "Hola mundo"
    python mceliece_demo.py "Hola mundo" -p Classic_McEliece_460896f
"""

import argparse
import binascii
from hashlib import sha256

import oqs                                   # liboqs-python
from Crypto.Cipher import AES               # PyCryptodome
from Crypto.Util.Padding import pad, unpad


# ---------- utilidades ------------------------------------------------------ #
def pretty_size(n: int) -> str:
    """Convierte n bytes en una cadena legible (B/KB/MB)."""
    if n < 1024:
        return f"{n} B"
    if n < 1024**2:
        return f"{n/1024:.1f} KB"
    return f"{n/1024**2:.1f} MB"


# ---------- programa principal --------------------------------------------- #
def main() -> None:
    parser = argparse.ArgumentParser(
        prog="mceliece_demo",
        description="Demostración sencilla de Classic McEliece con liboqs-python",
        epilog=(
            "Ejemplo:\n"
            "  python mceliece_demo.py \"Hola mundo\" "
            "--params Classic_McEliece_348864"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "mensaje",
        help="Texto plano que se cifrará con AES-128 usando el secreto compartido",
    )
    parser.add_argument(
        "-p",
        "--params",
        default="Classic_McEliece_348864",
        help="Nombre exacto del esquema (consulte oqs.get_enabled_KEM_mechanisms())",
    )
    args = parser.parse_args()
    plaintext = args.mensaje.encode()

    print("\n=== Classic McEliece Demo ===\n")
    print(f"[*] Esquema KEM : {args.params}\n")

    # «with» libera los recursos nativos del wrapper
    with oqs.KeyEncapsulation(args.params) as kem:
        print("[1] Generando par de claves …")
        public_key = kem.generate_keypair()           # devuelve PK y guarda SK internamente
        secret_key = kem.export_secret_key()          # opcional: para mostrar tamaño
        print(f"    Clave pública : {pretty_size(len(public_key))}")
        print(f"    Clave secreta  : {pretty_size(len(secret_key))}\n")

        print("[2] Encapsulando secreto compartido …")
        ciphertext, ss_enc = kem.encap_secret(public_key)
        print(f"    Ciphertext     : {pretty_size(len(ciphertext))}")
        print(f"    Secreto (hex)  : {binascii.hexlify(ss_enc).decode()}\n")

        print("[3] Decapsulando secreto …")
        ss_dec = kem.decap_secret(ciphertext)         # SK ya está dentro del objeto
        if ss_enc == ss_dec:
            print("    ✓ Secreto verificado correctamente")
        else:
            print("    ✗ ¡Los secretos no coinciden!")
            return

    # ---------- ejemplo de uso práctico ------------------------------------ #
    print("\n[4] Cifrado simétrico con AES-128-CBC derivado del secreto")
    key = sha256(ss_enc).digest()[:16]                # 128 bits de la SHA-256
    iv = b"\0" * 16                                   # IV fijo SOLO para la demo
    ct = AES.new(key, AES.MODE_CBC, iv).encrypt(pad(plaintext, 16))
    print(f"    Texto cifrado (hex): {binascii.hexlify(ct).decode()}")

    recovered = unpad(AES.new(key, AES.MODE_CBC, iv).decrypt(ct), 16)
    print(f"    Texto descifrado    : {recovered.decode()}")

    print("\nDemostración completada ✔\n")


if __name__ == "__main__":
    main()
