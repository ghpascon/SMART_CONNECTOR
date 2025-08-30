---
description: Repository Information Overview
alwaysApply: true
---

# SMARTX RFID Middleware Information

## Summary
SMARTX RFID Middleware é uma solução desenvolvida para gestão de leitores RFID, oferecendo alta performance, escalabilidade e flexibilidade na integração com sistemas. Fornece funcionalidades para configurar e controlar leitores, gerenciar conexões e sessões de leitura, integrar com sistemas externos e simular comportamento de leitores.

## Structure
- **app/**: Código principal da aplicação
  - **async_func/**: Funções assíncronas para operações RFID
  - **core/**: Funcionalidades centrais incluindo configuração e gerenciamento de caminhos
  - **db/**: Conexão com banco de dados e gerenciamento de sessões
  - **models/**: Modelos de dados para a aplicação
  - **routers/**: Definições de rotas da API
  - **schemas/**: Esquemas de validação de dados
  - **static/**: Arquivos estáticos (JS, CSS, imagens)
  - **templates/**: Templates HTML
- **config/**: Arquivos de configuração
  - **devices/**: Configurações de dispositivos RFID
  - **examples/**: Configurações de exemplo
- **Logs/**: Logs da aplicação

## Language & Runtime
**Language**: Python
**Version**: 3.11 (exato)
**Build System**: Poetry
**Package Manager**: Poetry

## Dependencies
**Main Dependencies**:
- FastAPI (0.110.0)
- Uvicorn (0.29.0)
- SQLAlchemy (2.0.29)
- Jinja2 (3.1.3)
- PySerial/PySerial-AsyncIO (3.5/0.6)
- AIOHTTP (3.11.18)
- PyEPC (0.5.0)
- Database drivers (PyMySQL, AIOMySQL, AIOSQLite, AsyncPG)

**Development Dependencies**:
- Tomli (^2.2.1)

## Build & Installation
```bash
# Instalar dependências
poetry install

# Executar a aplicação
poetry run python main.py

# Construir executável
poetry run python build_exe.py
```

## Application Structure
**Entry Point**: main.py
**Web Framework**: FastAPI
**Template Engine**: Jinja2
**Database ORM**: SQLAlchemy
**Async Support**: Implementação totalmente assíncrona com asyncio

## Configuration
**Main Config**: config/config.json
**Device Definitions**: config/devices/*.json
**Actions Config**: config/actions.json
**Settings Management**: app/core/config.py

## Packaging
**Executable Builder**: PyInstaller (via build_exe.py)
**Build Configuration**: Executável único com recursos incorporados
**Included Resources**: Todos os diretórios e dependências da aplicação