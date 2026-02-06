from utils import console

console.instructions()
console.show_current_data()

while True:
    option = console.main_menu()

    match option:
        
        # Definir ou alterar os dados necessários
        case 1:
            console.set_folders_paths()
            add_files = console.question_ignore_file()
            if add_files:
                console.add_files_to_ignore()
        
        # Transferir arquivos
        case 2:
            console.transfer_files()
        
        # Sair
        case 3:
            break

input('\nPressione Enter para sair...')
