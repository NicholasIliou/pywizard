import os, subprocess, sys

from main_wizard import Project


if __name__ == "__main__":
    base_dir = os.getcwd()
    while True:
        create_new = input("Press 'Enter' to create a new project. ")
        if create_new == "":
            project = Project(base_dir)
            project.create_virtual_environment()
            project.install_libraries()
            print("Successfully created venv.")