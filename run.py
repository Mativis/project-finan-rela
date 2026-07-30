import subprocess
import sys
import os

try:
    from dotenv import load_dotenv
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-dotenv", "-q"])
    from dotenv import load_dotenv

def main():
    load_dotenv(override=True)
    url = os.environ.get("API_URL", "")

    if not url:
        print("=" * 50)
        print("💰  Financas do Casal - Setup")
        print("=" * 50)
        url = input("\nCole a URL do Web App (API_URL): ").strip()
        if not url:
            print("URL obrigatoria!")
            return
        with open(".env", "w") as f:
            f.write(f"API_URL={url}\n")
        print("✅ .env salvo com sucesso!\n")

    print("Iniciando o sistema...")
    print("   Local: http://localhost:8501\n")

    subprocess.run([
        sys.executable, "-m", "streamlit", "run", "app.py",
        "--server.headless", "true"
    ])

if __name__ == "__main__":
    main()
