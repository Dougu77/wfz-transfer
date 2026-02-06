from simpleValidatorForConsoleApp import validator
from .json_data import JsonData
from colorama import init, Fore
from time import sleep
import shutil
import os

init(autoreset=True)
json_data = JsonData()

def print_line() -> None:
    print()
    print(Fore.CYAN + '-' * 99)
    print()

def instructions() -> None:
    print_line()
    print(f'{Fore.CYAN}{"-" * 39} {Fore.YELLOW}Transferidor de WFZ {Fore.CYAN}{"-" * 39}')
    print_line()
    print(f'\n{Fore.GREEN}-> O programa transfere arquivos WFZ da pasta do PC para a pasta do relógio.')
    print(f'{Fore.GREEN}-> Digite a pasta de origem, a pasta de destino, e os arquivos que devem ser ignorados (se houver).')

def show_current_data() -> None:
    print_line()
    if json_data.source_folder == '' and json_data.destination_folder == '':
        print(f'Nenhum dado salvo ainda.')
        return
    print('Dados atuais:\n')
    print(f'Pasta de origem: {json_data.source_folder}')
    print(f'Pasta de destino: {json_data.destination_folder}')
    print(f'Arquivos ignorados: {", ".join(json_data.ignored_files)}')

def main_menu() -> int:
    print_line()

    menu_title = 'Selecione uma opção:'
    if json_data.source_folder == '' and json_data.destination_folder == '':
        first_option = 'Definir dados necessários'
    else:
        first_option = 'Alterar dados existentes'
    options = [
        first_option,
        'Transferir arquivos',
        'Sair'
    ]
    question = 'Opção: '
    error_message = 'Selecione uma opção válida.'
    return validator.validate_option(menu_title, options, question, error_message)

def set_folders_paths() -> None:
    print()

    json_data.source_folder = validator.validate_string(
        'Digite o caminho da pasta de origem: ',
        'Caminho inválido. Tente novamente.'
    )

    json_data.destination_folder = validator.validate_string(
        'Digite o caminho da pasta de destino: ',
        'Caminho inválido. Tente novamente.'
    )

    json_data.save()

def question_ignore_file() -> bool:
    question = 'Deseja adicionar algum arquivo à lista de ignorados? (S/N): '
    error_message = 'Resposta inválida. Digite "S" para sim ou "N" para não.'
    while True:
        answer = validator.validate_string(question, error_message)
        if answer.lower() == 's':
            return True
        elif answer.lower() == 'n':
            return False

def add_files_to_ignore() -> None:
    files = validator.validate_string(
        'Digite os nomes dos arquivos a serem ignorados, separados por ; : ',
        'Resposta inválida. Tente novamente.'
    )
    json_data.ignored_files = files.split(';')
    json_data.save()

def transfer_files() -> None:
    print()

    source = json_data.source_folder
    destination = json_data.destination_folder
    ignored = json_data.ignored_files

    if not os.path.exists(source):
        print('Erro: A pasta de origem não foi encontrada.')
        return

    files_to_transfer = []
    for root, _, files in os.walk(source):
        for file in files:
            if file.endswith('.wfz'):
                file_without_ext = os.path.splitext(file)[0]
                if file not in ignored and file_without_ext not in ignored:
                    files_to_transfer.append(os.path.join(root, file))

    if not files_to_transfer:
        print('Nenhum arquivo .wfz para transferir.')
        return

    for src_file in files_to_transfer:
        file_name = os.path.basename(src_file)
        dest_file = os.path.join(destination, file_name)
        try:
            shutil.copy(src_file, dest_file)
            print(f'Arquivo copiado: {file_name}')
            sleep(0.3)  # Pequena pausa para melhor visualização
        except Exception as e:
            print(f'Erro ao copiar {file_name}: {e}')

    print('\nTransferência concluída.')
