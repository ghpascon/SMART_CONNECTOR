import sys
from pathlib import Path


def get_path(relative_path: str) -> Path:
    """
    Retorna o caminho absoluto do arquivo ou diretório, levando em consideração se o
    aplicativo está sendo executado como um script normal ou como um executável.

    :param relative_path: Caminho relativo do arquivo ou diretório.
    :return: Caminho absoluto correto.
    """
    if getattr(sys, "frozen", False):
        # Quando o aplicativo é executado como executável (PyInstaller)
        base_path = Path(
            sys._MEIPASS
        )  # O diretório temporário onde o executável é descompactado
    else:
        # Quando o aplicativo está sendo executado do código-fonte
        base_path = (
            Path(sys.argv[0]).resolve().parent
        )  # O diretório onde o script foi executado

    return base_path / relative_path


def get_prefix_from_path(current_file: str, base_dir: str = "routers") -> str:
    """
    Gera automaticamente o prefixo para o APIRouter com base na estrutura de pastas a partir de 'routers'.

    :param current_file: Geralmente use __file__
    :param base_dir: Nome da pasta raiz dos routers (ex: "routers")
    :return: Prefixo do router, ex: "/rfid/get"
    """
    path = Path(current_file).resolve()
    parts = path.parts

    if base_dir not in parts:
        raise ValueError(f"'{base_dir}' not found in path: {path}")

    # Pega os subcaminhos após 'routers'
    base_index = parts.index(base_dir)
    prefix_parts = parts[base_index + 1 :]  # Ignora a pasta base e o nome do arquivo
    prefix_string = "/" + "/".join(prefix_parts)
    prefix_string = prefix_string.replace(".py", "")
    return prefix_string
