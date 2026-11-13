import os
import subprocess
from dotenv import load_dotenv
from google import genai

# .env ファイルから環境変数をロード
load_dotenv()

def test_sdk():
    print("=== Testing google-genai SDK ===")
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Warning: GEMINI_API_KEY is not set in .env")
        return

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents="Gemini CLI と Dev Containers を組み合わせた開発環境のメリットを1文で教えて。",
    )
    print(f"SDK Response:\n{response.text}\n")

def test_cli():
    print("=== Testing Gemini CLI Subprocess ===")
    try:
        env = os.environ.copy()
        # サブプロセス実行時のみ、このワークスペースを信頼する環境変数をインジェクション
        env["GEMINI_CLI_TRUST_WORKSPACE"] = "true"

        result = subprocess.run(
            ["gemini", "-p", "Dev Containers環境からの動作テストです"],
            capture_output=True,
            text=True,
            check=True,
            env=env,
        )
        print(f"CLI Response:\n{result.stdout.strip()}\n")
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"CLI test omitted or failed: {e}\n")
        if isinstance(e, subprocess.CalledProcessError):
            print(f"Error output:\n{e.stderr}")
        print()

if __name__ == "__main__":
    test_sdk()
    test_cli()
