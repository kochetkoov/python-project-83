#!/usr/bin/env bash
# скачиваем uv и запускаем команду установки зависимостей
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
source .venv/bin/activate
make install && psql -a -d $DATABASE_URL -f database.sql