from bd_zmic_metodos import *

import os
import random

# --------------------------
# Login y bienvenida
# --------------------------
def login():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("🎓 Bienvenido al Sistema de Estudio")
    nombre = input("📛 Ingresá tu nombre de usuario: ").strip()
    usuario_id = obtener_usuario(nombre)
    return usuario_id, nombre

# --------------------------
# Menú principal
# --------------------------
def menu_principal(usuario_id, nombre):
    while True:
        print(f"\n👤 Usuario: {nombre}")
        print("1. Modo Estudio")
        print("2. Modo Administrador (Agregar contenido)")
        print("0. Salir")

        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            menu_estudio(usuario_id)
        elif opcion == "2":
            menu_admin()
        elif opcion == "0":
            print("¡Hasta luego y éxitos en tu examen!")
            break
        else:
            print("Opción inválida.")

# --------------------------
# Menú administrador
# --------------------------
def menu_admin():
    while True:
        print("\n🛠️ MENÚ ADMINISTRADOR")
        print("1. Agregar tema")
        print("2. Agregar pregunta multiple choice a un tema")
        print("0. Volver")

        opcion = input("Opción: ")

        if opcion == "1":
            nombre = input("Nombre del nuevo tema: ").strip()
            agregar_tema(nombre)

        elif opcion == "2":
            temas = obtener_temas()
            if not temas:
                print("⚠️ No hay temas disponibles.")
                continue

            print("\nTemas disponibles:")
            for t in temas:
                print(f"{t[0]}. {t[1]}")

            tema_id = int(input("Seleccione el ID del tema: "))
            pregunta = input("Escriba la pregunta: ").strip()

            opciones = []
            correcta = input("Respuesta correcta: ").strip()
            opciones.append(correcta)

            for i in range(3):
                opciones.append(input(f"Opción incorrecta {i+1}: ").strip())

            dificultad = int(input("Nivel de dificultad (1 a 3): "))

            agregar_pregunta(pregunta, tema_id, dificultad, opciones, correcta)

        elif opcion == "0":
            break
        else:
            print("Opción inválida.")

# --------------------------
# Menú estudio
# --------------------------
def menu_estudio(usuario_id):
    while True:
        print("\n📚 MODO ESTUDIO")
        print("1. Repaso clásico por tema")
        print("0. Volver al menú principal")

        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            repaso_por_tema(usuario_id)
        elif opcion == "0":
            break
        else:
            print("Opción inválida.")

# --------------------------
# Repaso clásico por tema
# --------------------------
def repaso_por_tema(usuario_id):
    temas = obtener_temas()
    if not temas:
        print("⚠️ No hay temas disponibles.")
        return

    print("\nTemas disponibles:")
    for t in temas:
        print(f"{t[0]}. {t[1]}")

    try:
        tema_id = int(input("Seleccione el ID del tema para repasar: "))
    except:
        print("ID inválido.")
        return

    preguntas = obtener_preguntas_por_tema(tema_id)
    if not preguntas:
        print("⚠️ No hay preguntas en este tema.")
        return

    random.shuffle(preguntas)
    puntos = 0

    for pid, texto, dificultad in preguntas:
        print(f"\n📌 Pregunta: {texto} (Dificultad: {dificultad})")
        opciones = obtener_opciones(pid)
        random.shuffle(opciones)

        for i, (texto_op, _) in enumerate(opciones):
            print(f"{i+1}. {texto_op}")

        try:
            eleccion = int(input("Elegí una opción: ")) - 1
            _, es_correcta = opciones[eleccion]
            if es_correcta:
                print("✅ ¡Correcto!")
                puntos += 10 * dificultad
            else:
                print("❌ Incorrecto.")
        except:
            print("❌ Opción inválida.")

    actualizar_puntaje(usuario_id, tema_id, puntos)
    puntaje_total = obtener_puntaje(usuario_id, tema_id)
    print(f"\n🎯 Puntos ganados: {puntos}")
    print(f"🎓 Puntaje total en el tema: {puntaje_total}/100")

# --------------------------
# EJECUCIÓN PRINCIPAL
# --------------------------
if __name__ == "__main__":
    crear_tablas()
    usuario_id, nombre = login()
    menu_principal(usuario_id, nombre)
