import subprocess
import os
import sys

class VirtualEnv:
    """This Class is useful to install the packages used in code
       to the user's system while executing the script. (No need to create the env manually though commands)."""
    
    def __init__(_self, **kwargs):
        """Initialize the virtual environment parameters."""
        _self.pip_path = None
        _self.activate_script = None
        _self.env = dict(kwargs)
        _self.requirements_file = _self.env.get("requirements_file")
        
        if not _self.requirements_file:
            raise ValueError("Both 'env_name' and 'requirements_file' must be provided.")
        
    @staticmethod
    def install_java():
        """Installing the latest version of Java."""
        try:
            result = subprocess.run(["java", "-version"], capture_output=True, text=True)
            # prin(result)
            if result.returncode == 0:
                print("Java is already installed.")
                return False
            else:
                print("Installing the latest version of Java (OpenJDK)...")
                subprocess.check_call(["winget", "install", "OpenJDK"])
                return True
        except subprocess.CalledProcessError as e:
            print(f"Error during Java installation: {e}")
            sys.exit(1)
        except FileNotFoundError:
            print("Error: winget is not available. Please install Java manually.")
            sys.exit(1)

    @staticmethod
    def upgrade_pip():
        """Upgrades pip to the latest version globally."""
        print("Upgrading pip to the latest version...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        print("pip has been upgraded successfully.")



    def install_requirements(_self):
        """Create the virtual environment and install the requirements."""
        try:
            VirtualEnv.upgrade_pip()
            print(f"Installing dependencies from {_self.requirements_file}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", _self.requirements_file])
            print("Dependencies installed successfully.")

            # Optionally install Java
            download_java = VirtualEnv.install_java()
            if download_java:
                print("Java has been installed successfully!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error during subprocess execution: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
