import os
import sys

sys.path.append(os.getcwd())

from logging.config import fileConfig
from multiprocessing import pool
from sqlalchemy import engine_from_config
from alembic import context
from models import Base  # Исправляем инструкцию импорта
from sqlalchemy.pool import NullPool

# Это объект Alembic Config, который предоставляет
# доступ к значениям в используемом файле .ini.
config = context.config
fileConfig(config.config_file_name)

# Интерпретация файла конфигурации для логирования Python.
# Эта строка, в основном, настраивает логгеры.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Используйте Base.metadata для target_metadata
target_metadata = Base.metadata

# Другие значения из конфигурации, определенные потребностями env.py,
# могут быть получены:
# my_important_option = config.get_main_option("my_important_option")
# ... и так далее.


def run_migrations_offline() -> None:
    """Выполняет миграции в режиме 'offline'.

    Это настраивает контекст только с URL
    и без Engine, хотя Engine также допустим
    здесь. Пропуская создание Engine
    нам даже не нужен DBAPI.

    Вызовы context.execute() здесь отправляют данный текст в
    вывод сценария.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Выполняет миграции в режиме 'online'.

    В этом сценарии нам нужно создать Engine
    и связать соединение с контекстом.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
