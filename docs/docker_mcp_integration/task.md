# Task List: Dockerize Deep Searcher & Add MCP Support

- [ ] リポジトリの調査
    - [ ] `README.md` の確認
    - [ ] 既存 `Dockerfile` の確認
    - [ ] `main.py` および主要機能のインターフェース確認
- [ ] 実装計画の作成 (Implementation Plan)
    - [ ] `implementation_plan.md` の作成
- [ ] Docker環境の整備
    - [ ] `Dockerfile` の修正 (必要に応じて)
    - [ ] `docker-compose.yml` の作成
    - [ ] Volumeマウント設定
- [ ] MCPサーバーの実装
    - [ ] MCPサーバースクリプトの作成 (`mcp_server.py` 等)
    - [ ] Deep Searcher機能のMCPツール化
- [ ] 検証
    - [ ] Dockerビルドと起動確認
    - [ ] MCP経由での動作確認
