import os
import sys
import platform
import subprocess
import shutil
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def check_git_pull():
    """Check for updates from git repository"""
    print(f"{Fore.CYAN}🔍 Checking for updates...")
    
    # Check if .git directory exists
    if not os.path.exists(".git"):
        print(f"{Fore.YELLOW}⚠ Not a git repository, skipping update check")
        return True
    
    try:
        # Fetch latest changes
        result = subprocess.run(["git", "fetch"], 
                              capture_output=True, 
                              text=True)
        
        # Check if there are updates
        result = subprocess.run(["git", "status", "-uno"],
                              capture_output=True,
                              text=True)
        
        if "Your branch is behind" in result.stdout:
            print(f"{Fore.YELLOW}🔄 Updates available! Pulling latest changes...")
            result = subprocess.run(["git", "pull"],
                                  capture_output=True,
                                  text=True)
            if result.returncode == 0:
                print(f"{Fore.GREEN}✅ Successfully updated!")
                return True
            else:
                print(f"{Fore.RED}❌ Failed to update: {result.stderr}")
                return False
        else:
            print(f"{Fore.GREEN}✅ Already up to date!")
            return True
            
    except FileNotFoundError:
        print(f"{Fore.YELLOW}⚠ Git not installed, skipping update check")
        return True
    except Exception as e:
        print(f"{Fore.RED}❌ Error checking updates: {e}")
        return True

def check_architecture():
    """Check if device is 64-bit"""
    print(f"{Fore.CYAN}🔍 Checking device architecture...")
    
    # Method 1: Check platform module
    arch = platform.machine().lower()
    print(f"{Fore.YELLOW}Device architecture: {Fore.WHITE}{arch}")
    
    # List of 64-bit architecture identifiers
    x64_archs = ['x86_64', 'amd64', 'x64', 'arm64', 'aarch64', 'armv8']
    
    # Check if architecture is 64-bit
    is_64bit = any(x64_arch in arch for x64_arch in x64_archs)
    
    # Method 2: Check python build
    if hasattr(sys, 'maxsize'):
        is_64bit_python = sys.maxsize > 2**32
        print(f"{Fore.YELLOW}Python is 64-bit: {Fore.WHITE}{is_64bit_python}")
        is_64bit = is_64bit and is_64bit_python
    
    # Method 3: Check using os module
    if hasattr(os, 'uname'):
        uname_info = os.uname()
        print(f"{Fore.YELLOW}System: {Fore.WHITE}{uname_info.sysname}")
        print(f"{Fore.YELLOW}Machine: {Fore.WHITE}{uname_info.machine}")
    
    return is_64bit

def check_requirements():
    """Check if required files exist"""
    print(f"{Fore.CYAN}🔍 Checking required files...")
    
    required_files = ["main.cpython-312.so", "checker.txt"]
    all_exist = True
    
    for file in required_files:
        if os.path.exists(file):
            print(f"{Fore.GREEN}✅ Found: {file}")
        else:
            print(f"{Fore.RED}❌ Missing: {file}")
            all_exist = False
    
    return all_exist

def install_requirements():
    """Install required Python packages"""
    print(f"{Fore.CYAN}📦 Installing requirements...")
    
    requirements = [
        "yt-dlp",
        "instaloader",
        "colorama"
    ]
    
    for package in requirements:
        try:
            print(f"{Fore.YELLOW}Installing {package}...", end=" ")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package, "-q"])
            print(f"{Fore.GREEN}✅")
        except subprocess.CalledProcessError:
            print(f"{Fore.RED}❌ Failed to install {package}")
            return False
    
    return True

def create_checker_file():
    """Create checker.txt if it doesn't exist"""
    if not os.path.exists("checker.txt"):
        print(f"{Fore.YELLOW}📄 Creating checker.txt...")
        try:
            with open("checker.txt", "w") as f:
                f.write("")
            print(f"{Fore.GREEN}✅ Created checker.txt")
        except Exception as e:
            print(f"{Fore.RED}❌ Failed to create checker.txt: {e}")

def run_main_module():
    """Run the main Cython module"""
    print(f"{Fore.CYAN}🚀 Starting Instagram Tool...")
    print(f"{Fore.CYAN}{'='*60}")
    
    try:
        # Import the compiled module
        import main
        
        # Check if main module has main() function
        if hasattr(main, 'main'):
            main.main()
        else:
            print(f"{Fore.RED}❌ Error: main module doesn't have main() function")
            return False
            
    except ImportError as e:
        print(f"{Fore.RED}❌ Error importing main module: {e}")
        print(f"{Fore.YELLOW}Make sure 'main.cpython-312.so' exists in current directory")
        return False
    except Exception as e:
        print(f"{Fore.RED}❌ Error running main module: {e}")
        return False
    
    return True

def show_banner():
    """Show the tool banner"""
    banner = f"""
{Fore.CYAN}{'='*60}
{Fore.CYAN}🔐 INSTAGRAM TOOL - PREMIUM VERSION
{Fore.CYAN}📺 Created by YUNICK_XWD
{Fore.CYAN}🔗 Channel: @xwd_org
{Fore.CYAN}{'='*60}
    """
    print(banner)

def main():
    """Main entry point"""
    try:
        # Show banner
        show_banner()
        
        # Check git for updates
        if not check_git_pull():
            print(f"{Fore.YELLOW}⚠ Continuing with current version...")
        
        # Check device architecture
        if not check_architecture():
            print(f"\n{Fore.RED}{'='*60}")
            print(f"{Fore.RED}❌ UNSUPPORTED DEVICE")
            print(f"{Fore.RED}{'='*60}")
            print(f"{Fore.RED}This tool requires a 64-bit device.")
            print(f"{Fore.RED}Your device appears to be 32-bit.")
            print(f"{Fore.RED}Please use a 64-bit Android device.")
            print(f"{Fore.RED}{'='*60}")
            input(f"\n{Fore.YELLOW}Press Enter to exit...")
            return
        
        print(f"\n{Fore.GREEN}✅ Device is 64-bit, continuing...")
        
        # Check required files
        if not check_requirements():
            print(f"\n{Fore.YELLOW}⚠ Some files are missing, but we can continue...")
        
        # Create checker.txt if needed
        create_checker_file()
        
        # Check and install requirements
        print(f"\n{Fore.CYAN}🔧 Setting up environment...")
        if not install_requirements():
            print(f"{Fore.YELLOW}⚠ Some packages failed to install, but we can try to continue...")
        
        # Run the main module
        print(f"\n{Fore.CYAN}{'='*60}")
        success = run_main_module()
        
        if not success:
            print(f"\n{Fore.RED}{'='*60}")
            print(f"{Fore.RED}❌ TOOL FAILED TO START")
            print(f"{Fore.RED}{'='*60}")
            print(f"{Fore.YELLOW}Troubleshooting steps:")
            print(f"{Fore.YELLOW}1. Make sure you have Python 3.12 installed")
            print(f"{Fore.YELLOW}2. Check if 'main.cpython-312.so' exists")
            print(f"{Fore.YELLOW}3. Try: pip install yt-dlp instaloader colorama")
            print(f"{Fore.RED}{'='*60}")
        
        # Wait before exit
        input(f"\n{Fore.YELLOW}Press Enter to exit...")
        
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}⚠ Tool interrupted by user")
    except Exception as e:
        print(f"\n{Fore.RED}❌ Unexpected error: {e}")
        input(f"\n{Fore.YELLOW}Press Enter to exit...")

if __name__ == "__main__":
    main()
