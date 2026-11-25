# gemini-cli-dev-containers
Playground PoC utilizing VS Code Dev containers to run Gemini CLI

# Gemini CLI & Python Dev Container Playground 

VS Code + Dev Containers + Python (uv) + Gemini CLI によるAIプロトタイピングの最小構成テンプレートです。 

> 📖 **解説記事（Zenn）**: [Dev Containers×UV×Gemini CLIで作る最小AIプロトタイプ](https://zenn.dev/atsupi/articles/fff382504df18c)  
> （このテンプレートの設計意図や技術選定のトレードオフについて詳しく解説しています）

## クイックスタート手順 
1. `.env.example` をコピーして `.env` を作成し、APIキーを設定:
```bash 
cp .env.example .env
```

2. `uv sync`のビルド可否を確認する:
```bash
uv sync
```

3. `uv run`でPythonスクリプトを実行する:
```bash
uv run python main.py
```

## テスト手順 
- `uv run pytest`でpytestを実行する:

```bash
uv run pytest test_main.py
```

---

## License
This project is licensed under the MIT License - see the LICENSE file for details.
