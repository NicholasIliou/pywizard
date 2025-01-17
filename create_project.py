import os
import subprocess
import sys

class Project:
    """
    A utility to automate Python project setup, including directory creation,
    virtual environment setup, library installation, and Git initialization.
    """
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.project_dir = self.select_directory()
        self.folder_name = input("Enter the project folder name: ").strip()
        self.folder_path = os.path.join(self.project_dir, self.folder_name)
        self.venv_path = os.path.join(self.folder_path, 'venv')

    def select_directory(self):
        """Prompts the user to select the directory for the project."""
        current_dir = self.base_dir
        while True:
            selected_dir = input(f"Enter the directory for the project (default is '{current_dir}'): ").strip()
            if not selected_dir:
                selected_dir = current_dir
            if os.path.exists(selected_dir):
                return selected_dir
            else:
                print(f"The folder '{selected_dir}' does not exist. Please choose a different directory.")

    def create_folder(self):
        """Creates the project folder."""
        os.makedirs(self.folder_path)
        print(f"Folder '{self.folder_name}' created successfully in {self.project_dir}.")

    def create_main_file(self):
        """Creates the main.py file."""
        main_py_path = os.path.join(self.folder_path, 'main.py')
        with open(main_py_path, 'w') as main_file:
            main_file.write("# This is the main.py file for your new project\n")
            main_file.write("print('Hello, world!')\n")
        print(f"Created 'main.py' in {self.folder_path}.")

    def create_virtual_environment(self):
        """Creates a virtual environment."""
        subprocess.run([sys.executable, "-m", "venv", self.venv_path])
        print(f"Virtual environment created at {self.venv_path}.")

    def install_libraries(self):
        """Prompts the user to enter library names and installs them."""
        pip_path = os.path.join(self.venv_path, 'Scripts', 'pip.exe')
        if not os.path.exists(pip_path):
            pip_path = os.path.join(self.venv_path, 'bin', 'pip')
        while True:
            library_name = input("Enter a library name to install (default is None): ").strip()
            if library_name.lower() == '':
                print("Skipping library installation.")
                break
            try:
                subprocess.run([pip_path, "install", library_name], check=True)
                print(f"Successfully installed {library_name}.")
            except subprocess.CalledProcessError:
                print(f"Failed to install {library_name}. Check the spelling or try a different package.")
                continue

    def create_run_script(self):
        """Creates a .bat file to activate the virtual environment and run main.py."""
        bat_script = os.path.join(self.folder_path, 'run_project.bat')
        with open(bat_script, 'w') as bat_file:
            bat_file.write(f'@echo off\n')
            bat_file.write(f'call {os.path.join(self.folder_path, "venv", "Scripts", "activate.bat")}\n')
            bat_file.write(f'python {os.path.join(self.folder_path, "main.py")}\n')
        print(f"Created 'run_project.bat' script to run the project.")

    def init_git_repo(self):
        """Initializes a git repository in the project folder."""
        subprocess.run(["git", "init"], cwd=self.folder_path)
        with open(os.path.join(self.folder_path, ".gitignore"), 'w') as gitignore:
            gitignore.write("__pycache__/\n")
            gitignore.write("venv/\n")
        subprocess.run(["git", "add", "."], cwd=self.folder_path)
        subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=self.folder_path)
        print(f"Initialized Git repository in {self.folder_path}.")

    def create_project(self):
        """Creates the entire project structure."""
        self.create_folder()
        self.create_main_file()
        self.create_virtual_environment()
        self.install_libraries()
        self.create_run_script()
        git_init = input("Do you want to initialize a Git repository? (y/n): ").strip().lower()
        if git_init == 'y':
            self.init_git_repo()

def main():
    base_dir = os.getcwd()
    while True:
        create_new = input("Press 'Enter' to create a new project. ")
        if create_new == "":
            project = Project(base_dir)
            project.create_project()
            print("Successfully created a new project.")

if __name__ == "__main__":
    main()