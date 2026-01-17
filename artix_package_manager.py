#!/usr/bin/env python3
"""
Artix Linux Uygulama Mağazası
Resmi depolardan uygulama yükleme aracı
"""

import subprocess
import sys
import os

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

# Kategorilere göre uygulamalar
APPLICATIONS = {
    "Tarayıcılar": {
        "firefox": "Mozilla Firefox - Popüler açık kaynak tarayıcı",
        "librewolf": "LibreWolf - Gizlilik odaklı Firefox fork'u",
        "chromium": "Chromium - Google Chrome'un açık kaynak versiyonu",
        "brave-bin": "Brave - Gizlilik odaklı tarayıcı",
        "vivaldi": "Vivaldi - Özelleştirilebilir tarayıcı",
        "falkon": "Falkon - Hafif Qt tabanlı tarayıcı",
        "qutebrowser": "Qutebrowser - Klavye odaklı tarayıcı",
        "epiphany": "GNOME Web (Epiphany) - Basit GNOME tarayıcısı"
    },
    "Ofis Uygulamaları": {
        "libreoffice-fresh": "LibreOffice - Tam özellikli ofis paketi",
        "onlyoffice-bin": "OnlyOffice - Modern ofis paketi",
        "abiword": "AbiWord - Hafif kelime işlemci",
        "gnumeric": "Gnumeric - Hafif hesap tablosu",
        "calligra": "Calligra Suite - KDE ofis paketi"
    },
    "Medya Oynatıcılar": {
        "vlc": "VLC Media Player - Güçlü medya oynatıcı",
        "mpv": "MPV - Minimalist medya oynatıcı",
        "celluloid": "Celluloid - MPV için GTK arayüzü",
        "audacious": "Audacious - Hafif müzik çalar",
        "clementine": "Clementine - Modern müzik çalar",
        "rhythmbox": "Rhythmbox - GNOME müzik çalar",
        "strawberry": "Strawberry - Gelişmiş müzik çalar"
    },
    "Grafik ve Tasarım": {
        "gimp": "GIMP - Güçlü resim düzenleyici",
        "inkscape": "Inkscape - Vektör grafik editörü",
        "krita": "Krita - Dijital çizim uygulaması",
        "blender": "Blender - 3D modelleme ve animasyon",
        "darktable": "Darktable - Fotoğraf işleme",
        "kdenlive": "Kdenlive - Video düzenleyici",
        "shotcut": "Shotcut - Basit video düzenleyici"
    },
    "Geliştirme Araçları": {
        "code": "Visual Studio Code - Modern kod editörü",
        "vim": "Vim - Gelişmiş metin editörü",
        "neovim": "Neovim - Modern Vim",
        "emacs": "Emacs - Güçlü metin editörü",
        "geany": "Geany - Hafif IDE",
        "qtcreator": "Qt Creator - Qt geliştirme IDE'si",
        "git": "Git - Versiyon kontrol sistemi",
        "docker": "Docker - Konteyner platformu"
    },
    "İletişim": {
        "telegram-desktop": "Telegram - Hızlı mesajlaşma",
        "discord": "Discord - Sesli/yazılı sohbet",
        "thunderbird": "Thunderbird - E-posta istemcisi",
        "hexchat": "HexChat - IRC istemcisi",
        "pidgin": "Pidgin - Çoklu protokol mesajlaşma"
    },
    "Sistem Araçları": {
        "htop": "htop - İnteraktif sistem monitörü",
        "btop": "btop - Modern sistem monitörü",
        "gparted": "GParted - Disk bölümleme aracı",
        "timeshift": "Timeshift - Sistem yedekleme",
        "bleachbit": "BleachBit - Sistem temizleme",
        "baobab": "Baobab - Disk kullanım analizi",
        "gnome-disk-utility": "GNOME Diskler - Disk yönetimi"
    },
    "İnternet Araçları": {
        "filezilla": "FileZilla - FTP istemcisi",
        "transmission-gtk": "Transmission - Torrent istemcisi",
        "qbittorrent": "qBittorrent - Gelişmiş torrent istemcisi",
        "remmina": "Remmina - Uzak masaüstü istemcisi",
        "wget": "wget - Dosya indirme aracı",
        "curl": "curl - Veri transfer aracı"
    }
}

def clear_screen():
    os.system('clear')

def print_header():
    clear_screen()
    print(f"{Colors.CYAN}{Colors.BOLD}")
    print("╔════════════════════════════════════════════════╗")
    print("║     Artix Linux Uygulama Mağazası              ║")
    print("╚════════════════════════════════════════════════╝")
    print(f"{Colors.END}")

def is_installed(package):
    """Paketin kurulu olup olmadığını kontrol et"""
    result = subprocess.run(['pacman', '-Q', package], 
                          capture_output=True, text=True)
    return result.returncode == 0

def install_package(package):
    """Paket yükle"""
    print(f"\n{Colors.YELLOW}'{package}' yükleniyor...{Colors.END}\n")
    result = subprocess.run(['sudo', 'pacman', '-S', package, '--needed'])
    return result.returncode == 0

def remove_package(package):
    """Paket kaldır"""
    print(f"\n{Colors.YELLOW}'{package}' kaldırılıyor...{Colors.END}\n")
    result = subprocess.run(['sudo', 'pacman', '-R', package])
    return result.returncode == 0

def show_category(category_name, apps):
    """Kategori uygulamalarını göster ve işlem yap"""
    while True:
        print_header()
        print(f"{Colors.BOLD}{Colors.BLUE}Kategori: {category_name}{Colors.END}\n")
        
        app_list = list(apps.items())
        
        for i, (pkg, desc) in enumerate(app_list, 1):
            installed = is_installed(pkg)
            status = f"{Colors.GREEN}[Kurulu]{Colors.END}" if installed else f"{Colors.RED}[Kurulu değil]{Colors.END}"
            print(f"{Colors.CYAN}{i}.{Colors.END} {status} {pkg}")
            print(f"   {Colors.YELLOW}{desc}{Colors.END}")
            print()
        
        print(f"{Colors.CYAN}0.{Colors.END} Geri Dön")
        print()
        
        choice = input(f"{Colors.BOLD}Uygulama numarası (yüklemek/kaldırmak için): {Colors.END}").strip()
        
        if choice == '0':
            break
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(app_list):
                pkg_name = app_list[idx][0]
                
                if is_installed(pkg_name):
                    confirm = input(f"\n{Colors.YELLOW}'{pkg_name}' kaldırılsın mı? (e/h): {Colors.END}").strip().lower()
                    if confirm == 'e':
                        remove_package(pkg_name)
                        input(f"\n{Colors.GREEN}Devam etmek için Enter'a basın...{Colors.END}")
                else:
                    confirm = input(f"\n{Colors.YELLOW}'{pkg_name}' yüklensin mi? (e/h): {Colors.END}").strip().lower()
                    if confirm == 'e':
                        install_package(pkg_name)
                        input(f"\n{Colors.GREEN}Devam etmek için Enter'a basın...{Colors.END}")
            else:
                print(f"\n{Colors.RED}Geçersiz numara!{Colors.END}")
                input(f"{Colors.GREEN}Devam etmek için Enter'a basın...{Colors.END}")
        except ValueError:
            print(f"\n{Colors.RED}Geçersiz giriş!{Colors.END}")
            input(f"{Colors.GREEN}Devam etmek için Enter'a basın...{Colors.END}")

def update_system():
    """Sistemi güncelle"""
    print_header()
    print(f"\n{Colors.YELLOW}Sistem güncelleniyor...{Colors.END}\n")
    subprocess.run(['sudo', 'pacman', '-Syu'])
    input(f"\n{Colors.GREEN}Devam etmek için Enter'a basın...{Colors.END}")

def show_installed():
    """Yüklü uygulamaları göster"""
    print_header()
    print(f"{Colors.BOLD}{Colors.BLUE}Mağazadan Yüklü Uygulamalar:{Colors.END}\n")
    
    installed_count = 0
    for category, apps in APPLICATIONS.items():
        category_apps = []
        for pkg, desc in apps.items():
            if is_installed(pkg):
                category_apps.append((pkg, desc))
        
        if category_apps:
            print(f"\n{Colors.CYAN}{Colors.BOLD}{category}:{Colors.END}")
            for pkg, desc in category_apps:
                print(f"  {Colors.GREEN}✓{Colors.END} {pkg} - {desc}")
                installed_count += 1
    
    if installed_count == 0:
        print(f"{Colors.YELLOW}Henüz hiç uygulama yüklenmemiş.{Colors.END}")
    else:
        print(f"\n{Colors.BOLD}Toplam: {installed_count} uygulama{Colors.END}")
    
    input(f"\n{Colors.GREEN}Devam etmek için Enter'a basın...{Colors.END}")

def show_main_menu():
    """Ana menü"""
    while True:
        print_header()
        print(f"{Colors.BOLD}Kategoriler:{Colors.END}\n")
        
        categories = list(APPLICATIONS.keys())
        for i, category in enumerate(categories, 1):
            print(f"{Colors.CYAN}{i}.{Colors.END} {category}")
        
        print()
        print(f"{Colors.CYAN}u.{Colors.END} Sistemi Güncelle")
        print(f"{Colors.CYAN}y.{Colors.END} Yüklü Uygulamalar")
        print(f"{Colors.CYAN}0.{Colors.END} Çıkış")
        print()
        
        choice = input(f"{Colors.BOLD}Seçiminiz: {Colors.END}").strip().lower()
        
        if choice == '0':
            print(f"\n{Colors.GREEN}Çıkış yapılıyor...{Colors.END}")
            sys.exit(0)
        elif choice == 'u':
            update_system()
        elif choice == 'y':
            show_installed()
        else:
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(categories):
                    category_name = categories[idx]
                    show_category(category_name, APPLICATIONS[category_name])
                else:
                    print(f"\n{Colors.RED}Geçersiz seçim!{Colors.END}")
                    input(f"{Colors.GREEN}Devam etmek için Enter'a basın...{Colors.END}")
            except ValueError:
                print(f"\n{Colors.RED}Geçersiz giriş!{Colors.END}")
                input(f"{Colors.GREEN}Devam etmek için Enter'a basın...{Colors.END}")

def main():
    """Ana program"""
    try:
        show_main_menu()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Program sonlandırıldı.{Colors.END}")
        sys.exit(0)

if __name__ == "__main__":
    main()