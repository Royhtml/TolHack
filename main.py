#!/usr/bin/env python3
import os
import sys
import subprocess
import time
import random
import requests
from typing import List, Dict, Tuple
import threading
from datetime import datetime

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

class Animations:
    @staticmethod
    def loading_animation(duration=3, text="Loading"):
        frames = ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"]
        end_time = time.time() + duration
        i = 0
        while time.time() < end_time:
            print(f"\r{Colors.CYAN}{frames[i % len(frames)]} {text}...{Colors.END}", end="")
            i += 1
            time.sleep(0.1)
        print("\r" + " " * 50 + "\r", end="")

    @staticmethod
    def progress_bar(iteration, total, prefix='', suffix='', length=30, fill='█'):
        percent = ("{0:.1f}").format(100 * (iteration / float(total)))
        filled_length = int(length * iteration // total)
        bar = fill * filled_length + '-' * (length - filled_length)
        print(f'\r{Colors.GREEN}{prefix} |{bar}| {percent}% {suffix}{Colors.END}', end='')
        if iteration == total:
            print()

    @staticmethod
    def typewriter(text, delay=0.03):
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()

    @staticmethod
    def matrix_rain(duration=2):
        chars = "01"
        width = os.get_terminal_size().columns
        lines = [-1] * width
        end_time = time.time() + duration
        
        while time.time() < end_time:
            for i in range(width):
                if lines[i] < 0 or random.random() < 0.05:
                    lines[i] = 0
                print(f"{Colors.GREEN}\033[{lines[i]};{i}H{random.choice(chars)}{Colors.END}", end="")
                lines[i] += 1
                if lines[i] >= os.get_terminal_size().lines:
                    lines[i] = -1
            time.sleep(0.1)

    @staticmethod
    def bouncing_ball(duration=3):
        ball = "🔴"
        positions = ["▁", "▂", "▃", "▄", "▅", "▆", "▇", "█", "▇", "▆", "▅", "▄", "▃", "▂"]
        end_time = time.time() + duration
        i = 0
        
        while time.time() < end_time:
            pos = i % len(positions)
            spaces = " " * (pos * 2)
            print(f"\r{Colors.RED}{spaces}{ball}{Colors.END}", end="")
            i += 1
            time.sleep(0.1)
        print("\r" + " " * 50 + "\r", end="")

    @staticmethod
    def spinning_circle(duration=3, text="Processing"):
        frames = ["◐", "◓", "◑", "◒"]
        end_time = time.time() + duration
        i = 0
        
        while time.time() < end_time:
            print(f"\r{Colors.MAGENTA}{frames[i % len(frames)]} {text}...{Colors.END}", end="")
            i += 1
            time.sleep(0.2)
        print("\r" + " " * 50 + "\r", end="")

class TermuxInstaller:
    def __init__(self):
        self.ascii_art = f"""
{Colors.RED}{Colors.BOLD}
                                              ███  ██                                               
                                              ░                                                     
                                         █▒█▒      ░░▒▒                                             
                                             ░   ░░░    ░░░░░                                       
                                       ░░      ░░     ░░░ ░░░▒▒▒                                    
                             █   ░▒   ░░  ░░░░░░░░░░░░░░ ░░░ ▒  ░                                   
                               ░▒    ░░░      ░░░░░░ ░░░░░░░░░▒░                                    
                          ░  ░▓░ ░░░ ░░░ ░  ░  ░░ ░░░  ░░░░ ░░ ▒  ░░░                               
                            ░░  ░░░  ░░ ░ █ ▒░  ░ ░ ░░ ░░░░░░   █                                   
                           ▒▓░ ░░░    ░ ░ █▒ █░   ░░  ░ ░░▒░ ▒   █   ░                              
                          █▓  ░░░░    ░   █░ ░█▓   ░░░▒      ░░  ▒▓  ░░                             
                         █▒  ░░░░░░░░░░   █ ▓   █▓    ░▒      ░░  ▒░  ▒░   █                        
                        ▓▒  ░░░░░ ░ ░░░   █ ▒ ▒  ░█▒   ▓▒     ░▒  ░█  ░░                            
                     █ ▒▒░ ░░░░░░░░░░ ░░ ▒▒ ░       ██  █     ░░░  █▒  ▒░   █                       
                       ▓▒░░░░░ ░░░░░ ░░░ ▓   ▒▒▒███▒ ██ ▒▓ ░░░░░░  █▓  ▒░   ░                       
                    █ █ ░░░░░░░░░░░░░░░  █▓░░▓▒░      ▒█░█ ▒░░░░░▒ ▓█▒ ░▒░  ▒                       
                      █ ░░░░░▒░░░░░░░▒  ▒█░▒█▒           █  ░░░░ ▒ ░▒█  ▒░  ░                       
                     █▓ ░░░░░▒ ░░░░░ █  ░▓  █ ▒███████████▒ ░░░░ ░ ░▒ ▓ ░▒  ░                       
                    ▒░▒ ▒░░░░▒ ░░░░░ █  ▓▒   ██░   ████ █ ░ ░░░░ ░  █▓▒  ░                          
                    █ ▒ ░░░░▒▓ ░░░░░ █▒░█   ▒▒    ██░ █▒▒▒▒ ░░░░ ▒░ █ █  ░░                         
                   ░█ ▒ ░▒░ ░▒ ░░░▒  ██ ▓ ░         ██░  ▓▒ ░░░░ ░░ █ █  ▒ ▒▓                       
                   █  ▓  ░▒ ░▒░░░░░ ▒▒▓░  ░░░░░░░▒░      ▓░ ░░░  ░▒ ███  ▒  █ █                     
                     ░ ▒ ░▒░▒▒▒░ ▒ ░██▒█▓ ░░░░░░░░ ░   ░ █▒ ░░░  ░▒░█▒█ ░▒  █                       
                      ▒█░  ▒▓▒░░█▒▓█ ▒  ▒  ░░░ ░░░░░ ░ ░ ▓  ░░░░  ▒░ ▒▒  ▓  █▒                      
                           ░▓█ ░█▓▓ █░  ░░░░░░░░░░░░░░░  █  ░░░░ ░▓░ █▒  █  █                       
                        █    ▓  █    ▒░░░ ░░░░░░░░░░░░░  █  ░░░  ░█░░█   █ ▓█ █                     
                         █░  █ ▒█░  ░         ░░░░░░░░░  █ ░░░░░  █  █  ░▓ ██                       
                           ▓  ░█▒█▒    ░░▒██▓  ░░░░░░    █ ░░░░░ ▒█▒░█  ▓▒ ▒▒█ ▓                    
                           ▓█ █▒█░▒█▒      ░ ░░░░░     ▓█  ░░░░  █▓ ░▓ ░▓▒ ▓ █ █                    
                           ▒ █░▒   ░▒██    ░░░░░     ██▒█  ░░░░  ██ ░▒ ▒▒░ ▒░█ █                    
                         ░░▒   ██▒░░░ ▒███       ▓████  ▓ ░░ ░░ ▒█▒ ▓░ ▒░░ ▒▓▒▒▓                    
                         ░█▒░  ░  ░░░ █   ▓█▒░███░  █  █  ▒ ░░  █ ▓░▒ ░░░░ ▒▓██                     
                         ▓▒ ░ █ ░░░ ▒ █  ░░ ░░   ░▓  ▒░░ ▒  ░  █▓░█▒▒░░░░░ ▓ █ ░                    
                         ░▒ ░ █ ░░░ ▒░██▒ ▓ ░░░░  ▒▓  █ ░ ░   ██░▒█░░░░░░ ▒▓▓                       
                        ▒▒█   █ ░░░ ▓░   ░▒░ ▒▒░░  █  ██  ░ ██░  ███  ░░  ▒                         
                        ▒▓█  ▓▓ ░░░ ▓░     ▓ ░      ▒██  ░ █░▒ ▓█  ▒ █░  ░                          
                        ▒▒▒ ░ █ ░░░ ▓         ░░░   ▓▒▒▓▒█▓       ▒█░▒                              
                       ▒▓▓▓▒░       ▒         ▒█████▓███████░   ▓█▓ ████                            
                        █░  ░    ░  ▒▓     ▒ ░              ▒▓▓▓░                                   
                        ▒▒         ▒ ▒    ██▒▓███████▓███         ██░                               
                                            ▓█▒    ░░▒▒░▒█▓     ░    ▒██▓                           
                                         █ █▓          ░▓▓█▓  ░    ░░░                              
                                         ░█      ░░░░░    ▒██   ░     ░▒      █                     
                                         █    ░░░░░░░  ░   ░██░     ░  ░▒▓▓▒ ▒                      
                                         ▒ ░ ░░░░ ░░░░░░     ██           ▒░ ░                      
                                        █▓   ░░░░░░░░░░░░░ ░  █▒                                    
                                       █ █ ░ ░░░░░░░░░░░ ░ ░░ ▒█         ░  ▒                       
                                         █ ░ ░░░░ ░░░░░░  ░░░  █            ▒                       
                                         █ ░ ░░░░░░░░░░  ░░░░░  █                                   
                                  ▓      █ ░  ░░░░░ ░   ░░░░    █                                   
                                █    ░░  █ ▒░ ░░░░░░░░░░░░░  ▒░ ░█        ░                         
                                    ░░   █ ░░ ░░░░░░░ ░░░   ▓█░  █                                  
                                  ░░░░  ░█ ▒░ ░░░░░░░░░░   ██░ ░ █▓                                 
                             █  ░░░░░░░ ▒█ ▒ ░░░░░░  ░░░  ██ ░ ░ █░                                 
                                 ░░░░   █░ ░ ░░░░░░░░░ ░ ░█  ░ ██            ▒                                                                                                                  
                        ████████╗███████╗██████╗ ███╗   ███╗██╗   ██╗██╗  ██╗
                        ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║   ██║╚██╗██╔╝
                           ██║   █████╗  ██████╔╝██╔████╔██║██║   ██║ ╚███╔╝ 
                           ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║   ██║ ██╔██╗ 
                           ██║   ███████╗██║  ██║██║ ╚═╝ ██║╚██████╔╝██╔╝ ██╗
                           ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝                              
                            {Colors.CYAN}PROFESSIONAL INSTALLER{Colors.RED}
                            {Colors.YELLOW}By Dwi Bakti N Dev{Colors.END}
"""
        
        self.installation_history = []
        self.start_time = datetime.now()
        
        self.menu_options = {
            "DISTRO LINUX": {
                1: ("Ubuntu 20.04 LTS", self.install_ubuntu),
                2: ("Arch Linux", self.install_arch),
                3: ("Kali Linux", self.install_kali),
                4: ("Debian 11", self.install_debian),
                5: ("Fedora 38", self.install_fedora),
                6: ("Alpine Linux", self.install_alpine),
                7: ("Void Linux", self.install_void),
                8: ("Kali Nethunter", self.install_nethunter),
                9: ("OpenSUSE", self.install_opensuse)
            },
            "PENTESTING TOOLS": {
                10: ("Metasploit Framework", self.install_metasploit),
                11: ("SQLMap", self.install_sqlmap),
                12: ("Nmap", self.install_nmap),
                13: ("Hydra", self.install_hydra),
                14: ("Aircrack-ng", self.install_aircrack),
                15: ("John The Ripper", self.install_john),
                16: ("Wireshark/Tshark", self.install_wireshark),
                17: ("Beef Framework", self.install_beef),
                18: ("Burp Suite Community", self.install_burpsuite),
                19: ("Nikto Scanner", self.install_nikto)
            },
            "WEB HACKING": {
                20: ("SEToolkit", self.install_setoolkit),
                21: ("RouterSploit", self.install_routersploit),
                22: ("Recon-ng", self.install_reconng),
                23: ("TheHarvester", self.install_theharvester),
                24: ("OSINT Framework", self.install_osint),
                25: ("WhatWeb", self.install_whatweb),
                26: ("Dirb", self.install_dirb),
                27: ("Gobuster", self.install_gobuster)
            },
            "DEVELOPMENT TOOLS": {
                28: ("Programming Tools", self.install_programming_tools),
                29: ("Network Tools", self.install_network_tools),
                30: ("Git & Version Control", self.install_git_tools),
                31: ("Database Tools", self.install_database_tools),
                32: ("Web Development", self.install_web_tools)
            },
            "UTILITIES & GAMES": {
                33: ("Update Dependencies", self.install_dependencies),
                34: ("System Upgrade", self.system_upgrade),
                35: ("Install All Hacking Tools", self.install_all_hacking_tools),
                36: ("Clean System", self.clean_system),
                37: ("System Info", self.show_system_info),
                38: ("Termux Theme", self.install_termux_theme),
                39: ("Termux Games", self.install_games),
                40: ("Custom Commands", self.custom_commands_menu)
            }
        }

    def clear_screen(self):
        os.system('clear')

    def print_header(self):
        self.clear_screen()
        print(self.ascii_art)

    def log_installation(self, tool_name, status):
        """Log installation history"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.installation_history.append({
            'timestamp': timestamp,
            'tool': tool_name,
            'status': status
        })

    def run_command(self, command: str, description: str = "", show_output: bool = False) -> bool:
        """Run shell command with enhanced progress indicator"""
        if description:
            print(f"{Colors.YELLOW}[*] {description}...{Colors.END}")
        
        # Show random animation
        animations = [Animations.loading_animation, Animations.spinning_circle]
        random.choice(animations)(2, description)
        
        try:
            if show_output:
                # Show real-time output
                process = subprocess.Popen(
                    command,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    universal_newlines=True
                )
                
                # Read output in real-time
                for line in process.stdout:
                    print(f"{Colors.BLUE}{line.strip()}{Colors.END}")
                
                process.wait()
                return_code = process.returncode
            else:
                # Run silently with progress indicator
                process = subprocess.Popen(
                    command,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                return_code = process.wait()

            if return_code == 0:
                print(f"{Colors.GREEN}[✓] {description} completed successfully!{Colors.END}")
                self.log_installation(description, "Success")
                return True
            else:
                print(f"{Colors.RED}[✗] {description} failed!{Colors.END}")
                self.log_installation(description, "Failed")
                return False
                
        except Exception as e:
            print(f"{Colors.RED}[✗] Error: {str(e)}{Colors.END}")
            self.log_installation(description, f"Error: {str(e)}")
            return False

    def install_dependencies(self):
        """Install basic dependencies"""
        print(f"{Colors.CYAN}📦 Installing Dependencies...{Colors.END}")
        
        commands = [
            ("pkg update -y", "Updating package list", False),
            ("pkg upgrade -y", "Upgrading packages", True),
            ("pkg install -y wget curl git proot tar pulseaudio", "Installing core utilities", False),
            ("pkg install -y x11-repo unstable-repo root-repo", "Adding repositories", False),
            ("pkg install -y python python2 python3 nodejs golang", "Installing programming languages", False),
            ("pkg install -y ruby perl php clang make cmake", "Installing development tools", False),
            ("pkg install -y nano vim git zip unzip", "Installing text editors and utilities", False),
            ("termux-setup-storage", "Setting up storage permissions", False)
        ]
        
        for i, (cmd, desc, show_out) in enumerate(commands):
            Animations.progress_bar(i + 1, len(commands), f"Installing {desc}")
            if not self.run_command(cmd, desc, show_out):
                return False
            time.sleep(1)
        return True

    def install_ubuntu(self):
        return self.run_command("pkg install -y proot-distro && proot-distro install ubuntu", 
                               "Installing Ubuntu 20.04 LTS", True)

    def install_arch(self):
        return self.run_command("pkg install -y proot-distro && proot-distro install archlinux", 
                               "Installing Arch Linux", True)

    def install_kali(self):
        return self.run_command("pkg install -y proot-distro && proot-distro install kali", 
                               "Installing Kali Linux", True)

    def install_debian(self):
        return self.run_command("pkg install -y proot-distro && proot-distro install debian", 
                               "Installing Debian 11", True)

    def install_fedora(self):
        return self.run_command("pkg install -y proot-distro && proot-distro install fedora", 
                               "Installing Fedora 38", True)

    def install_alpine(self):
        return self.run_command("pkg install -y proot-distro && proot-distro install alpine", 
                               "Installing Alpine Linux", True)

    def install_void(self):
        return self.run_command("pkg install -y proot-distro && proot-distro install void", 
                               "Installing Void Linux", True)

    def install_opensuse(self):
        return self.run_command("pkg install -y proot-distro && proot-distro install opensuse", 
                               "Installing OpenSUSE", True)

    def install_nethunter(self):
        Animations.typewriter(f"{Colors.RED}🚀 Installing Kali Nethunter...{Colors.END}")
        commands = [
            ("git clone https://github.com/Hax4us/Nethunter-In-Termux.git", "Cloning Nethunter", False),
            ("cd Nethunter-In-Termux && chmod +x kalinethunter", "Setting up Nethunter", False),
            ("cd Nethunter-In-Termux && ./kalinethunter", "Installing Kali Nethunter", True)
        ]
        for cmd, desc, show_out in commands:
            if not self.run_command(cmd, desc, show_out):
                return False
        return True

    def install_metasploit(self):
        Animations.matrix_rain(2)
        return self.run_command("pkg install -y unstable-repo && pkg install -y metasploit", 
                               "Installing Metasploit Framework", True)

    def install_sqlmap(self):
        return self.run_command("git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git", 
                               "Installing SQLMap", False)

    def install_nmap(self):
        return self.run_command("pkg install -y nmap", "Installing Nmap", False)

    def install_hydra(self):
        return self.run_command("pkg install -y hydra", "Installing Hydra", False)

    def install_aircrack(self):
        return self.run_command("pkg install -y aircrack-ng", "Installing Aircrack-ng", False)

    def install_john(self):
        return self.run_command("pkg install -y john", "Installing John The Ripper", False)

    def install_wireshark(self):
        return self.run_command("pkg install -y tshark", "Installing Wireshark (tshark)", False)

    def install_beef(self):
        Animations.typewriter(f"{Colors.MAGENTA}🐮 Installing Beef Framework...{Colors.END}")
        commands = [
            ("pkg install -y ruby nodejs", "Installing dependencies for Beef", False),
            ("git clone https://github.com/beefproject/beef.git", "Cloning Beef Framework", False),
            ("cd beef && gem install bundler", "Installing Bundler", True),
            ("cd beef && bundle install", "Installing Beef dependencies", True)
        ]
        for cmd, desc, show_out in commands:
            if not self.run_command(cmd, desc, show_out):
                return False
        return True

    def install_burpsuite(self):
        return self.run_command("pkg install -y burpsuite", "Installing Burp Suite Community", True)

    def install_nikto(self):
        return self.run_command("pkg install -y nikto", "Installing Nikto Scanner", False)

    def install_setoolkit(self):
        commands = [
            ("git clone https://github.com/trustedsec/social-engineer-toolkit.git setoolkit/", "Cloning SEToolkit", False),
            ("cd setoolkit && pip install -r requirements.txt", "Installing SEToolkit dependencies", True)
        ]
        for cmd, desc, show_out in commands:
            if not self.run_command(cmd, desc, show_out):
                return False
        return True

    def install_routersploit(self):
        commands = [
            ("git clone https://github.com/threat9/routersploit.git", "Cloning RouterSploit", False),
            ("cd routersploit && pip install -r requirements.txt", "Installing RouterSploit dependencies", True)
        ]
        for cmd, desc, show_out in commands:
            if not self.run_command(cmd, desc, show_out):
                return False
        return True

    def install_reconng(self):
        commands = [
            ("git clone https://github.com/lanmaster53/recon-ng.git", "Cloning Recon-ng", False),
            ("cd recon-ng && pip install -r REQUIREMENTS", "Installing Recon-ng dependencies", True)
        ]
        for cmd, desc, show_out in commands:
            if not self.run_command(cmd, desc, show_out):
                return False
        return True

    def install_theharvester(self):
        commands = [
            ("git clone https://github.com/laramies/theHarvester.git", "Cloning TheHarvester", False),
            ("cd theHarvester && pip install -r requirements.txt", "Installing TheHarvester dependencies", True)
        ]
        for cmd, desc, show_out in commands:
            if not self.run_command(cmd, desc, show_out):
                return False
        return True

    def install_osint(self):
        return self.run_command("git clone https://github.com/lockfale/OSINT-Framework.git", 
                               "Installing OSINT Framework", False)

    def install_whatweb(self):
        return self.run_command("pkg install -y whatweb", "Installing WhatWeb", False)

    def install_dirb(self):
        return self.run_command("pkg install -y dirb", "Installing Dirb", False)

    def install_gobuster(self):
        return self.run_command("pkg install -y gobuster", "Installing Gobuster", False)

    def install_programming_tools(self):
        commands = [
            ("pkg install -y python python2 python3 nodejs golang", "Installing programming languages", False),
            ("pkg install -y ruby perl php clang make cmake", "Installing development tools", False),
            ("pip install --upgrade pip", "Upgrading pip", True),
            ("pkg install -y vim nano emacs", "Installing text editors", False)
        ]
        for cmd, desc, show_out in commands:
            if not self.run_command(cmd, desc, show_out):
                return False
        return True

    def install_network_tools(self):
        commands = [
            ("pkg install -y curl wget net-tools dnsutils", "Installing network utilities", False),
            ("pkg install -y tcpdump netcat-openbsd openssh", "Installing network tools", False),
            ("pkg install -y telnet ftp sslscan", "Installing security tools", False)
        ]
        for cmd, desc, show_out in commands:
            if not self.run_command(cmd, desc, show_out):
                return False
        return True

    def install_git_tools(self):
        return self.run_command("pkg install -y git git-lfs", "Installing Git tools", False)

    def install_database_tools(self):
        commands = [
            ("pkg install -y sqlite", "Installing SQLite", False),
            ("pkg install -y mariadb", "Installing MariaDB", True),
            ("pkg install -y postgresql", "Installing PostgreSQL", True)
        ]
        for cmd, desc, show_out in commands:
            if not self.run_command(cmd, desc, show_out):
                return False
        return True

    def install_web_tools(self):
        commands = [
            ("pkg install -y apache2", "Installing Apache", False),
            ("pkg install -y nginx", "Installing Nginx", False),
            ("pkg install -y php-apache", "Installing PHP for Apache", False)
        ]
        for cmd, desc, show_out in commands:
            if not self.run_command(cmd, desc, show_out):
                return False
        return True

    def system_upgrade(self):
        Animations.bouncing_ball(2)
        return self.run_command("pkg update -y && pkg upgrade -y", "System upgrade", True)

    def clean_system(self):
        return self.run_command("pkg clean && pkg autoclean", "Cleaning package cache", False)

    def show_system_info(self):
        """Display system information"""
        self.clear_screen()
        print(f"{Colors.CYAN}{Colors.BOLD}🖥️  SYSTEM INFORMATION{Colors.END}")
        print(f"{Colors.YELLOW}═" * 50 + Colors.END)
        
        info_commands = [
            ("uname -a", "System Info"),
            ("pkg list-installed | wc -l", "Installed Packages"),
            ("df -h", "Disk Usage"),
            ("free -h", "Memory Usage"),
            ("pkg version", "Package Versions")
        ]
        
        for cmd, desc in info_commands:
            print(f"\n{Colors.GREEN}📊 {desc}:{Colors.END}")
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                print(f"{Colors.WHITE}{result.stdout}{Colors.END}")
            except Exception as e:
                print(f"{Colors.RED}Error: {e}{Colors.END}")
        
        print(f"\n{Colors.MAGENTA}⏰ Session started: {self.start_time}{Colors.END}")
        print(f"{Colors.MAGENTA}📝 Installations attempted: {len(self.installation_history)}{Colors.END}")
        
        input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")

    def install_termux_theme(self):
        """Install Termux theme and customization"""
        Animations.typewriter(f"{Colors.CYAN}🎨 Installing Termux Theme...{Colors.END}")
        commands = [
            ("pkg install -y termux-styling", "Installing Termux Styling", False),
            ("git clone https://github.com/adi1090x/termux-style.git", "Cloning Termux Style", False),
            ("cd termux-style && chmod +x install && ./install", "Installing Termux Style", True)
        ]
        for cmd, desc, show_out in commands:
            if not self.run_command(cmd, desc, show_out):
                return False
        return True

    def install_games(self):
        """Install some fun games for Termux"""
        Animations.typewriter(f"{Colors.GREEN}🎮 Installing Games...{Colors.END}")
        games = [
            ("pkg install -y nethack", "NetHack"),
            ("pkg install -y moon-buggy", "Moon Buggy"),
            ("pkg install -y nudoku", "Sudoku"),
            ("pkg install -y pacman4console", "Pacman")
        ]
        
        for i, (cmd, game_name) in enumerate(games):
            Animations.progress_bar(i + 1, len(games), f"Installing {game_name}")
            self.run_command(cmd, f"Installing {game_name}", False)
            time.sleep(1)
        
        print(f"{Colors.GREEN}🎯 Games installed! Try 'moon-buggy' or 'nudoku' to play!{Colors.END}")
        return True

    def custom_commands_menu(self):
        """Menu for custom commands and utilities"""
        while True:
            self.clear_screen()
            print(f"{Colors.CYAN}{Colors.BOLD}🔧 CUSTOM COMMANDS MENU{Colors.END}")
            print(f"{Colors.YELLOW}═" * 50 + Colors.END)
            
            custom_options = {
                1: ("Speed Test", "pkg install -y speedtest-cli && speedtest-cli"),
                2: ("Weather Info", "curl wttr.in"),
                3: ("Random Quote", "curl https://api.quotable.io/random"),
                4: ("System Monitor", "pkg install -y htop && htop"),
                5: ("File Manager", "pkg install -y ranger && ranger"),
                6: ("Music Player", "pkg install -y mpv && echo 'Install complete. Use: mpv filename'"),
                7: ("Backup Termux", "tar -zcf /sdcard/termux-backup.tar.gz -C /data/data/com.termux/files ./"),
                8: ("Restore Termux", "tar -zxf /sdcard/termux-backup.tar.gz -C /data/data/com.termux/files --recursive-unlink --preserve-permissions"),
                9: ("Back to Main Menu", "")
            }
            
            for key, (name, cmd) in custom_options.items():
                color = Colors.GREEN if key <= 8 else Colors.RED
                print(f" {color}{key:2d}. {name}{Colors.END}")
            
            try:
                choice = int(input(f"\n{Colors.WHITE}Select option [1-9]: {Colors.END}"))
                
                if choice == 9:
                    break
                elif choice in custom_options:
                    name, command = custom_options[choice]
                    if command:
                        self.run_command(command, f"Running {name}", True)
                    input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")
                else:
                    print(f"{Colors.RED}Invalid option!{Colors.END}")
                    time.sleep(1)
            except ValueError:
                print(f"{Colors.RED}Please enter a valid number!{Colors.END}")
                time.sleep(1)

    def install_all_hacking_tools(self):
        """Install all hacking tools in sequence with progress"""
        tools = [
            ("Metasploit", self.install_metasploit),
            ("Nmap", self.install_nmap),
            ("SQLMap", self.install_sqlmap),
            ("Hydra", self.install_hydra),
            ("Aircrack-ng", self.install_aircrack),
            ("John The Ripper", self.install_john),
            ("Wireshark", self.install_wireshark),
            ("Beef Framework", self.install_beef),
            ("SEToolkit", self.install_setoolkit),
            ("RouterSploit", self.install_routersploit),
            ("Recon-ng", self.install_reconng),
            ("TheHarvester", self.install_theharvester),
            ("OSINT Framework", self.install_osint),
            ("Burp Suite", self.install_burpsuite),
            ("Nikto", self.install_nikto),
            ("WhatWeb", self.install_whatweb),
            ("Dirb", self.install_dirb),
            ("Gobuster", self.install_gobuster)
        ]
        
        print(f"{Colors.MAGENTA}🚀 Installing ALL hacking tools...{Colors.END}")
        print(f"{Colors.YELLOW}This may take a while. Please be patient...{Colors.END}")
        
        successful = 0
        for i, (name, tool_func) in enumerate(tools, 1):
            Animations.progress_bar(i, len(tools), f"Installing {name}")
            if tool_func():
                successful += 1
            time.sleep(2)  # Give time to see progress
        
        print(f"{Colors.GREEN}🎯 Installation complete! {successful}/{len(tools)} tools installed successfully.{Colors.END}")

    def display_menu(self):
        """Display the enhanced main menu"""
        self.print_header()
        
        # Show session info
        session_duration = datetime.now() - self.start_time
        print(f"{Colors.CYAN}⏰ Session: {session_duration} | 📦 Installations: {len(self.installation_history)}{Colors.END}")
        
        print(f"{Colors.BOLD}{Colors.CYAN}╔═══════════════════════════════════════════╗{Colors.END}")
        print(f"{Colors.BOLD}{Colors.CYAN}║           🚀 MAIN INSTALLATION MENU       ║{Colors.END}")
        print(f"{Colors.BOLD}{Colors.CYAN}╚═══════════════════════════════════════════╝{Colors.END}")
        print()
        
        for category, options in self.menu_options.items():
            print(f"{Colors.BOLD}{Colors.YELLOW}┌─ {category} ──────────────────────────────{Colors.END}")
            
            for key, (name, _) in options.items():
                if key <= 9:
                    color = Colors.GREEN
                elif key <= 19:
                    color = Colors.CYAN
                elif key <= 27:
                    color = Colors.MAGENTA
                elif key <= 32:
                    color = Colors.BLUE
                else:
                    color = Colors.WHITE
                print(f" {color}│ {key:2d}. {name}{Colors.END}")
            
            print(f"{Colors.YELLOW}└─────────────────────────────────────────────{Colors.END}")
            print()
        
        print(f"{Colors.BOLD}{Colors.RED}┌─ QUIT & UTILITIES ────────────────────────{Colors.END}")
        print(f" {Colors.RED}│  0. Exit Program{Colors.END}")
        print(f" {Colors.RED}│ 99. Show Installation History{Colors.END}")
        print(f"{Colors.RED}└─────────────────────────────────────────────{Colors.END}")
        print()

    def show_installation_history(self):
        """Display installation history"""
        self.clear_screen()
        print(f"{Colors.CYAN}{Colors.BOLD}📋 INSTALLATION HISTORY{Colors.END}")
        print(f"{Colors.YELLOW}═" * 60 + Colors.END)
        
        if not self.installation_history:
            print(f"{Colors.YELLOW}No installations recorded yet.{Colors.END}")
        else:
            for i, record in enumerate(self.installation_history, 1):
                status_color = Colors.GREEN if record['status'] == 'Success' else Colors.RED
                print(f"{Colors.WHITE}{i:2d}. {record['timestamp']} - {record['tool']} - {status_color}{record['status']}{Colors.END}")
        
        input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")

    def get_user_choice(self) -> int:
        """Get user menu choice"""
        try:
            choice = int(input(f"{Colors.BOLD}{Colors.WHITE}Select option [0-40, 99]: {Colors.END}"))
            return choice
        except ValueError:
            return -1

    def execute_choice(self, choice: int) -> bool:
        """Execute the chosen menu option"""
        for category, options in self.menu_options.items():
            if choice in options:
                _, function = options[choice]
                return function()
        
        return False

    def run(self):
        """Main program loop"""
        # Welcome animation
        Animations.typewriter(f"{Colors.GREEN}🚀 Welcome to Termux Professional Installer!{Colors.END}")
        Animations.loading_animation(2, "Initializing")
        
        while True:
            self.display_menu()
            choice = self.get_user_choice()
            
            if choice == 0:
                Animations.typewriter(f"{Colors.GREEN}👋 Thank you for using Termux Professional Installer!{Colors.END}")
                break
            elif choice == 99:
                self.show_installation_history()
            elif choice == -1:
                print(f"{Colors.RED}❌ Invalid input! Please enter a number.{Colors.END}")
                time.sleep(2)
            elif any(choice in options for options in self.menu_options.values()):
                print()
                self.execute_choice(choice)
                print(f"\n{Colors.YELLOW}⏳ Press Enter to continue...{Colors.END}")
                input()
            else:
                print(f"{Colors.RED}❌ Invalid option! Please choose between 0-40 or 99.{Colors.END}")
                time.sleep(2)

def main():
    """Main function"""
    try:
        # Check if running on Termux
        if not os.path.exists('/data/data/com.termux/files/usr'):
            print(f"{Colors.RED}❌ Error: This script is designed to run on Termux!{Colors.END}")
            print(f"{Colors.YELLOW}💡 Please run this on Termux app.{Colors.END}")
            sys.exit(1)
        
        # Check internet connection
        try:
            requests.get("https://google.com", timeout=5)
        except:
            print(f"{Colors.RED}❌ No internet connection! Please check your connection.{Colors.END}")
            sys.exit(1)
        
        installer = TermuxInstaller()
        installer.run()
        
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}👋 Program interrupted by user. Goodbye!{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}💥 Unexpected error: {str(e)}{Colors.END}")
        sys.exit(1)

if __name__ == "__main__":
    main()