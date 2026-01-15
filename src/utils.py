import sys
import os

def get_base_path() -> str:
    '''Gets the base path of the application.
    
    @returns Path to the project root or to the PyInstaller temp folder.
    
    '''
    
    if getattr(sys, "frozen", False):
        return sys._MEIPASS
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_resource_path(relative_path: str) -> str:
    '''Gets the absolute path to a resource, given its relative path.

    @param relative_path: Path relative to the project root or to the PyInstaller temp folder.
    @returns Absolute path to the resource.
    
    '''
    
    return os.path.join(get_base_path(), relative_path)

