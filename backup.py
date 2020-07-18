import os
import time
import shutil
import sys
from git import Repo


BACKUP_FILES = ('/etc/vimrc',
                '/home/viet/.bashrc')

BACKUP_DIR = ('/home/viet/backup_folder')


def decorate(func):
    def wrapper(*args, **kwargs):
        print()
        print(''.center(50, '-'))
        print('SysAdmin Tools'.center(50))
        print(''.center(50, '-'))
        print()
        return func(*args, **kwargs)

    return wrapper


def create_backup_dir(dir_name=BACKUP_DIR):
    print(f'Creating backup dir: {dir_name}')
    os.mkdir(path=BACKUP_DIR)


@decorate
def gather_backup_files():
    os.system('clear')
    print('Gathering backup files to backup dir ...\n')
    for file in BACKUP_FILES:
        if not os.path.exists(BACKUP_DIR):
            create_backup_dir()
        elif not os.path.isdir(BACKUP_DIR):
            print(f'{BACKUP_DIR} is not a directory')
            print('Exiting ...')
            sys.exit(-1)
        else:
            try:
                shutil.copy2(src=file, dst=BACKUP_DIR)
                print(f'[+] Copied file {file} to backup directory')
            except FileNotFoundError:
                print(f'[!!!] File {repr(file)} doesn\'t exist. Ignored.')

    print()
    _ = input('Press Enter to continue ...')


def main():
    while True:
        os.system('clear')
        main_menu()
        user_choice = input('Choose an option: ')

        while not user_choice.isdigit() or int(user_choice) < 0 or int(user_choice) > 5:
            print('Invalid index !!!')
            time.sleep(1)
            os.system('clear')

            main_menu()
            user_choice = input('Choose an option: ')

        if user_choice == '1':
            gather_backup_files()
        elif user_choice == '3':
            print('Exiting ...')
            sys.exit(0)


@decorate
def main_menu():
    options = {1: 'Gather backup files into backup dir',
               2: 'Push backup files to git repo',
               3: 'Exit\n'}

    for index, option in options.items():
        print(f'{str(index)}. {option}')

def post_action_menu():
    print('\n1. Back to main menu')


#TODO: implement git functionality
if __name__ == '__main__':
    main()
