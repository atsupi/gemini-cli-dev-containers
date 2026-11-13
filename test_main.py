import os
import subprocess
from unittest.mock import MagicMock, patch
import pytest
import main

# ==========================================
# 1. SDKのテスト (test_sdk)
# ==========================================

@patch("main.genai.Client")
def test_test_sdk_success(mock_client_cls):
    """GEMINI_API_KEYが設定されており、SDKが正常に応答する場合のテスト"""
    # 擬似的なレスポンスオブジェクトを作成
    mock_response = MagicMock()
    mock_response.text = "Dev ContainersとGemini CLIの組み合わせは、一貫した開発環境と高速なAIアシスタントの統合を提供します。"
    
    # client.models.generate_content() が上の擬似レスポンスを返すように設定
    mock_client_instance = mock_client_cls.return_value
    mock_client_instance.models.generate_content.return_value = mock_response

    # 環境変数にダミーのAPIキーを注入して実行
    with patch.dict(os.environ, {"GEMINI_API_KEY": "dummy_api_key"}):
        # main.py の test_sdk を呼び出す
        main.test_sdk()

    # 正しくClientが初期化され、意図した引数でAPIが呼ばれたかを検証
    mock_client_cls.assert_called_once_with(api_key="dummy_api_key")
    mock_client_instance.models.generate_content.assert_called_once_with(
        model="gemini-3.6-flash",
        contents="Gemini CLI と Dev Containers を組み合わせた開発環境のメリットを1文で教えて。"
    )

@patch("main.genai.Client")
def test_test_sdk_missing_api_key(mock_client_cls):
    """GEMINI_API_KEYが未設定の場合に、警告を出して早期リターンするかを検証するテスト"""
    # 環境変数から GEMINI_API_KEY を完全に削除した状態を作る
    with patch.dict(os.environ, {}, clear=True):
        main.test_sdk()
    
    # キーがないため、Clientは一度も初期化（呼び出し）されないことを検証
    mock_client_cls.assert_not_called()


# ==========================================
# 2. CLIのテスト (test_cli)
# ==========================================

@patch("main.subprocess.run")
def test_test_cli_success(mock_run):
    """gemini コマンドが正常に実行され、標準出力が返ってくる場合のテスト"""
    # subprocess.run の擬似戻り値を設定
    mock_process = MagicMock()
    mock_process.stdout = "CLIからの正常な動作確認応答です。"
    mock_run.return_value = mock_process

    main.test_cli()

    # 正しい引数と、信頼ワークスペースの環境変数が渡されて実行されたか検証
    mock_run.assert_called_once()
    args, kwargs = mock_run.call_args
    assert args[0] == ["gemini", "-p", "Dev Containers環境からの動作テストです"]
    assert kwargs["env"]["GEMINI_CLI_TRUST_WORKSPACE"] == "true"
    assert kwargs["capture_output"] is True
    assert kwargs["text"] is True

@patch("main.subprocess.run")
def test_test_cli_command_error(mock_run):
    """gemini コマンド実行時にエラー（CalledProcessError）が発生した場合の例外ハンドリングのテスト"""
    # CalledProcessErrorを発生させるようにモックを設定
    mock_run.side_effect = subprocess.CalledProcessError(
        returncode=1, 
        cmd=["gemini"], 
        stderr="Error: Workspace not trusted"
    )

    # 例外が内部でキャッチ（try-except）されるため、テスト自体はクラッシュせずに正常終了する
    main.test_cli()
    mock_run.assert_called_once()

@patch("main.subprocess.run")
def test_test_cli_not_found(mock_run):
    """そもそもシステムに gemini コマンドが存在しない（FileNotFoundError）場合のテスト"""
    # FileNotFoundErrorを発生させるようにモックを設定
    mock_run.side_effect = FileNotFoundError("[Errno 2] No such file or directory: 'gemini'")

    # 同様に内部でキャッチされることを検証
    main.test_cli()
    mock_run.assert_called_once()
