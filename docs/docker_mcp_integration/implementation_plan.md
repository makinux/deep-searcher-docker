# Deep Searcher Docker & MCP Integration Plan

## Goal Description
Deep Searcher をDockerコンテナ化し、外部のMCP (Model Context Protocol) クライアントから操作可能にします。
また、ホスト側のディレクトリをDocker Volumeとしてマウントし、コンテナ内部からローカルファイルとして参照・ロードできるようにします。

## User Review Required
> [!IMPORTANT]
> - MCPサーバーの接続方式として、Dockerを使用する場合は `stdio` (標準入出力) 方式が一般的です。クライアント設定(`claude_desktop_config.json` 等) には `docker run -i ...` コマンドを設定することになります。
> - 依存関係に `mcp` パッケージを追加します。

## Proposed Changes

### Configuration
#### [MODIFY] [pyproject.toml](file:///wsl.localhost/Ubuntu/opt/workspace/deep-searcher-docker/pyproject.toml)
- `mcp` ライブラリを依存関係に追加します。

### Source Code
#### [NEW] [mcp_server.py](file:///wsl.localhost/Ubuntu/opt/workspace/deep-searcher-docker/mcp_server.py)
- `mcp` ライブラリを使用し、Deep Searcherの機能をラップしたサーバーを実装します。
- **実装するTool:**
    - `query`: 質問を行い、回答を取得します。
    - `load_from_local_files`: マウントされたパスを指定してファイルをロードします。
    - `load_from_website`: URLを指定してWebページをロードします。

### Docker configuration
#### [MODIFY] [Dockerfile](file:///wsl.localhost/Ubuntu/opt/workspace/deep-searcher-docker/Dockerfile)
- `mcp_server.py` がコンテナに含まれるようにします（現在の `COPY . .` でカバーされていますが、必要に応じて確認します）。
- 必要であればエントリポイントを調整しやすくします。

#### [NEW] [docker-compose.yml](file:///wsl.localhost/Ubuntu/opt/workspace/deep-searcher-docker/docker-compose.yml)
- テストおよび開発用に作成します。
- `data` ボリュームのマウント例を含めます。
- 環境変数の設定例を含めます。

## Verification Plan

### Automated Tests
- MCPサーバーの動作確認用の簡単なスクリプトを作成するか、ローカルでコマンドを実行してJSON-RPCメッセージのやり取りを確認します。
- `docker build` が成功することを確認します。

### Manual Verification
- Dockerコンテナを起動し、ホスト側のファイルをマウントして `load_from_local_files` ツールが成功することを確認します。
- `query` ツールで回答が返ってくることを確認します。
