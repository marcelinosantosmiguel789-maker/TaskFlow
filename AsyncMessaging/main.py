
import os
import subprocess
import sys
from pathlib import Path


# Caminho da pasta AsyncMessaging
DIRETORIO_PROJETO = Path(__file__).resolve().parent

# Caminho da pasta src
DIRETORIO_SRC = DIRETORIO_PROJETO / "src"


def exibir_menu():
    print("\n" + "=" * 32)
    print("ASYNC MESSAGING")
    print("=" * 32)
    print("1. Enviar mensagem")
    print("2. Receber mensagens")
    print("0. Sair")
    print("=" * 32)


def executar_modulo(modulo):
    ambiente = os.environ.copy()

    pythonpath_atual = ambiente.get("PYTHONPATH", "")
    caminhos = [str(DIRETORIO_SRC)]

    if pythonpath_atual:
        caminhos.append(pythonpath_atual)

    ambiente["PYTHONPATH"] = os.pathsep.join(caminhos)

    subprocess.run(
        [sys.executable, "-m", modulo],
        cwd=DIRETORIO_PROJETO,
        env=ambiente,
        check=False,
    )


def main():
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            executar_modulo("mensageria.producer")

        elif opcao == "2":
            try:
                executar_modulo("mensageria.consumer")
            except KeyboardInterrupt:
                print("\nConsumidor interrompido.")

        elif opcao == "0":
            print("Encerrando o AsyncMessaging...")
            break

        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nPrograma encerrado.")
