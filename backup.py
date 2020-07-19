import os
import time
import shutil
import sys
import git
from collections import namedtuple

BACKUP_FILES = ('/etc/vimrc',
                '/home/viet/.bashrc',
                )

BACKUP_DIR = ('/home/viet/backup_folder')

OptionsTuple = namedtuple('OptionsTuple', 'index func description')


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
                if os.path.isdir(file):
                    shutil.copytree(src=file, dst=BACKUP_DIR)
                else:
                    shutil.copy2(src=file, dst=BACKUP_DIR)
                print(f'[+] Copied file {file} to backup directory')
            except FileNotFoundError:
                print(f'[!!!] File {repr(file)} doesn\'t exist. Ignored.')

    print()
    _ = input('Press Enter to continue ...')


def main():
    while True:
        os.system('clear')
        options = main_menu()

        user_input = input('\nChoose an option: ')
        while not user_input.isdigit():
            print('Please specify a valid index !!!')
            time.sleep(1)
            os.system('clear')

            main_menu()
            user_input = input('\nChoose an option: ')

        user_choice = int(user_input)
        if user_choice in [option.index for option in options]:
            choosen_option = list(filter(lambda x: x.index == int(user_choice), options))[0]
            choosen_option.func()
        else:
            print('Wrong index')
            time.sleep(1)
            os.system('clear')


@decorate
def main_menu():
    options = list()

    options.append(OptionsTuple(index=1,
                                func=gather_backup_files,
                                description='Gather backup files into backup dir'))
    options.append(OptionsTuple(index=2,
                                func=push_to_repo,
                                description='Push to git repository'))
    options.append(OptionsTuple(index=3,
                                func=lambda: sys.exit(0),
                                description='Exit'))

    for option in options:
        print(f'{option.index}. {option.description}')

    return options


def post_action_menu():
    print('\n1. Back to main menu')


def git_add(repo):
    repo.git.add('--all')


def git_commit(repo, message=None, author=None):
    if not message:
        message = 'Update configuration files.'
    if not author:
        author = 'quangviet910@gmail.com'

    repo.git.commit('-m', message, author=author)


def git_push(repo):
    origin = repo.remote(name='origin')
    origin.push()


def push_to_repo(repo=None):
    if not repo:
        repo = git.Repo(path='/home/viet/backup_project/.git')
    git_add(repo)
    git_commit(repo)
    git_push(repo)


# TODO: implement git functionality
if __name__ == '__main__':
    main()
