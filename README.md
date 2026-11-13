# gemini-cli-dev-containers
Playground PoC utilizing VS Code Dev containers to run Gemini CLI

# Gemini CLI & Python Dev Container Playground 

VS Code + Dev Containers + Python (uv) + Gemini CLI によるAIプロトタイピングの最小構成テンプレートです。 

## クイックスタート手順 
1. `.env.example` をコピーして `.env` を作成し、APIキーを設定:
```bash 
cp .env.example .env

2. `uv sync`のビルド可否を確認する
```bash
uv sync

3. `uv run`でPythonスクリプトを実行する
```bash
uv run python main.py
