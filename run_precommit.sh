#!/usr/bin/env sh
# Dockerイメージをビルド
docker-compose build app

# Dockerコンテナ内でRuffを実行
docker-compose run -it app ruff check ./src