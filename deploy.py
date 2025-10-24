import sys
import subprocess
from pathlib import Path

# -----------------------------
# 🔹 Colors
# -----------------------------
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

# -----------------------------
# 🔹 Helper Functions
# -----------------------------
def print_section(title):
    print(f"\n{Colors.HEADER}{'='*60}")
    print(f"🔹 {title}")
    print(f"{'='*60}{Colors.ENDC}\n")

def run(cmd, description=None, continue_on_error=False, color=None):
    if description:
        print_section(description)
    try:
        subprocess.check_call(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"{Colors.FAIL}❌ Error while running: {cmd}{Colors.ENDC}")
        if not continue_on_error:
            sys.exit(e.returncode)

# -----------------------------
# 🔹 Ensure pip
# -----------------------------
def ensure_pip(packages_dir: Path):
    try:
        import pip
        print(f"{Colors.OKGREEN}✅ pip is already installed.{Colors.ENDC}")
        return
    except ImportError:
        print(f"{Colors.WARNING}⚠️ pip not found. Bootstrapping pip...{Colors.ENDC}")
    try:
        import ensurepip
        ensurepip.bootstrap()
        print(f"{Colors.OKGREEN}✅ Pip bootstrapped successfully via ensurepip{Colors.ENDC}")
    except ImportError:
        print(f"{Colors.FAIL}❌ Cannot bootstrap pip. Ensure Python includes the ensurepip module.{Colors.ENDC}")
        sys.exit(1)

    pip_files = list(packages_dir.glob("pip*.*"))
    if pip_files:
        pip_file = pip_files[0]
        print(f"{Colors.OKBLUE}📦 Upgrading pip from offline package {pip_file.name} ...{Colors.ENDC}")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install",
            "--no-index",
            "--find-links", str(packages_dir),
            str(pip_file),
            "--upgrade"
        ])
        print(f"{Colors.OKGREEN}✅ Pip upgraded successfully from offline package{Colors.ENDC}")
    else:
        print(f"{Colors.WARNING}⚠️ No pip package found. Using pip installed via ensurepip.{Colors.ENDC}")

# -----------------------------
# 🔹 Prepare packages directory
# -----------------------------
def prepare_packages_dir(packages_dir: Path):
    packages_dir.mkdir(parents=True, exist_ok=True)
    print(f"{Colors.OKCYAN}✅ Packages directory ready at {packages_dir}{Colors.ENDC}")

# -----------------------------
# 🔹 Use existing requirements.txt
# -----------------------------
def get_requirements_file(project_path: Path) -> Path:
    req_file = project_path / "requirements.txt"
    if not req_file.exists():
        print(f"{Colors.WARNING}⚠️ requirements.txt not found. Generate it first with pipreqs.{Colors.ENDC}")
        sys.exit(1)
    print(f"{Colors.OKCYAN}📄 Using requirements.txt at {req_file}{Colors.ENDC}")
    return req_file

# -----------------------------
# 🔹 Extra packages 
# -----------------------------
EXTRA_PKGS = [
    "pip",
    "wfastcgi",
    "django-sslserver",
    "prettytable",
    "configparser",
    "setuptools",
    "wcwidth",
]

# -----------------------------
# 🔹 Install extra packages first (offline)
# -----------------------------
def install_extra_packages(packages_dir: Path):
    print_section("Installing extra packages required for deployment (offline)")
    for pkg in EXTRA_PKGS:
        found = False
        pkg_search_name = pkg.replace("-", "_")
        candidate_files = list(packages_dir.glob(f"{pkg_search_name}*.*"))

        if not candidate_files:
            print(f"{Colors.WARNING}⚠️ Extra package {pkg} not found in platform folder {packages_dir}!{Colors.ENDC}")
            continue

        for pkg_file in candidate_files:
            print(f"{Colors.OKGREEN}💾 Installing {pkg_file.name} (extra package){Colors.ENDC}")
            run(f'"{sys.executable}" -m pip install --no-index --find-links="{packages_dir}" "{pkg_file}" --no-deps')
            found = True

        if not found:
            print(f"{Colors.FAIL}⚠️ Could not install extra package {pkg}{Colors.ENDC}")

# -----------------------------
# 🔹 Display requirements table
# -----------------------------
def display_requirements_table(req_file: Path):
    try:
        from prettytable import PrettyTable
    except ImportError:
        pass
    table = PrettyTable()
    table.field_names = ["Package Name", "Version"]

    with open(req_file, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    print(f"{Colors.OKCYAN}\n📊 Total packages found: {len(lines)}\n{Colors.ENDC}")

    for line in lines:
        if "==" in line:
            name, version = line.split("==")
        else:
            name, version = line, "-"
        table.add_row([name, version])

    print(table)

# -----------------------------
# 🔹 Get web server settings
# -----------------------------
def get_web_settings():
    print_section("Web Server Settings")
    host = input("Enter host [default: 127.0.0.1]: ").strip() or "127.0.0.1"
    port = input("Enter port [default: 8000]: ").strip() or "8000"
    use_ssl_input = input("Use SSL? (yes/no) [default: no]: ").strip().lower() or "no"
    use_ssl = "true" if use_ssl_input in ["yes", "y"] else "false"
    return host, port, use_ssl

# -----------------------------
# 🔹 Install all packages from platform folder
# -----------------------------
def get_current_platform_tag():
    if sys.platform.startswith("win32") or sys.platform.startswith("cygwin"):
        return "win_amd64" if sys.maxsize > 2**32 else "win32"
    elif sys.platform.startswith("linux"):
        return "manylinux_2_28_x86_64"
    elif sys.platform.startswith("darwin"):
        return "macosx_13_0_x86_64"
    return "none"

def install_packages(packages_dir: Path):
    platform_tag = get_current_platform_tag()
    print_section(f"Installing packages for platform: {platform_tag}")

    installable_files = list(packages_dir.glob("*"))
    files_to_install = []

    for pkg_path in installable_files:
        # If universal (any) or matching current OS
        if pkg_path.suffix == ".whl":
            if "any" in pkg_path.name or platform_tag in pkg_path.name:
                files_to_install.append(pkg_path)
        else:
            # tar.gz and zip always install
            files_to_install.append(pkg_path)

    if not files_to_install:
        print(f"{Colors.WARNING}⚠️ No installable packages found for platform {platform_tag}. Continuing...{Colors.ENDC}")
        return

    for pkg_path in files_to_install:
        size_mb = pkg_path.stat().st_size / (1024*1024)
        print(f"{Colors.OKGREEN}💾 Installing {pkg_path.name} ({size_mb:.2f} MB){Colors.ENDC}")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install",
                "--no-index", "--find-links", str(packages_dir),
                str(pkg_path), "--no-deps"
            ])
        except subprocess.CalledProcessError as e:
            print(f"{Colors.WARNING}⚠️ Error installing {pkg_path.name}: {e}. Continuing...{Colors.ENDC}")

# -----------------------------
# 🔹 Create webconfig (INI + XML)
# -----------------------------
def create_webconfig(host, port, use_ssl):
    import sys
    import configparser
    from pathlib import Path
    import site

    project_root = Path(__file__).parent.resolve()
    env_python = Path(sys.executable)

    # پیدا کردن مسیر دقیق site-packages شامل wfastcgi.py
    site_packages = next(
        (Path(p) for p in site.getsitepackages() if (Path(p) / "wfastcgi.py").exists()),
        None
    )
    if not site_packages:
        site_packages = Path(env_python).parent / "Lib" / "site-packages"

    # PYTHONPATH کامل: ریشه پروژه + site-packages
    pythonpath = f"{project_root};{site_packages}"

    # -----------------------------
    # INI
    ini_file = project_root / "webconfig.ini"
    config = configparser.ConfigParser()
    config['server'] = {
        "host": host,
        "port": port,
        "use_ssl": use_ssl,
        "python_executable": str(env_python),
        "site_packages": str(site_packages)
    }
    with open(ini_file, "w", encoding="utf-8") as f:
        config.write(f)
    print(f"{Colors.OKGREEN}✅ webconfig.ini created at {ini_file}{Colors.ENDC}")

    # -----------------------------
    # XML
    # پیدا کردن پروژه Django (پوشه شامل wsgi.py)
    project_name = next((p.name for p in project_root.glob("*") if (p / "wsgi.py").exists()), None)
    if not project_name:
        project_name = "app"  # fallback

    xml_file = project_root / "web.config"
    xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <system.webServer>
        <handlers>
            <add name="Python FastCGI" path="*" verb="*" modules="FastCgiModule"
                scriptProcessor="{env_python}|{site_packages / 'wfastcgi.py'}"
                resourceType="Unspecified" requireAccess="Script" />
        </handlers>

        <rewrite>
            <rules>
                <!-- حذف trailing slash -->
                <rule name="RemoveTrailingSlash" stopProcessing="true">
                    <match url="(.*)/$" />
                    <action type="Redirect" url="{{R:1}}" redirectType="Permanent" />
                </rule>

                <!-- مستثنی کردن static و media -->
                <rule name="DjangoApp" stopProcessing="true">
                    <match url="^(?!static/|media/).*" />
                    <conditions>
                        <add input="{{REQUEST_FILENAME}}" matchType="IsFile" negate="true" />
                        <add input="{{REQUEST_FILENAME}}" matchType="IsDirectory" negate="true" />
                    </conditions>
                    <action type="Rewrite" url="wsgi.py/{{R:0}}" />
                </rule>
            </rules>
        </rewrite>

        <defaultDocument>
            <files>
                <add value="manage.py" />
            </files>
        </defaultDocument>
    </system.webServer>

    <appSettings>
        <add key="WSGI_HANDLER" value="{project_name}.wsgi.application" />
        <add key="PYTHONPATH" value="{pythonpath}" />
    </appSettings>
</configuration>
"""
    with open(xml_file, "w", encoding="utf-8") as f:
        f.write(xml_content)
    print(f"{Colors.OKGREEN}✅ web.config created at {xml_file}{Colors.ENDC}")

# -----------------------------
# 🔹 Main deploy logic
# -----------------------------
def deploy(target_os=None):
    project_path = Path(__file__).parent.resolve()
    packages_dir = project_path / "packages"
    req_file = get_requirements_file(project_path)

    ensure_pip(packages_dir)
    prepare_packages_dir(packages_dir)
    install_extra_packages(packages_dir)
    display_requirements_table(req_file)
    install_packages(packages_dir)
    print_section("Deployment completed!")
    print(f"🎉 Target OS: {target_os or 'auto-detect'}")

# -----------------------------
# 🔹 Command line interface
# -----------------------------
def main():
    import argparse
    parser = argparse.ArgumentParser(description="Deploy Python project with IIS configuration.")
    parser.add_argument("command", nargs="?", default="run", help="run / config / help")
    parser.add_argument("--os", type=str, default=None, help="Target OS: win64 / win32 / linux / macos")
    args = parser.parse_args()

    cmd = args.command.lower()

    if cmd == "help":
        print("""
Python Deploy Script

Commands:
  run           Run deployment (install packages, create packages and requirements)
  config        Create webconfig files (INI + XML)
  help          Show this help message

Options:
  --os=<os>     Specify target OS for deployment (win64, win32, linux, macos)
""")
        return

    if cmd == "run":
        deploy(target_os=args.os)
    elif cmd == "config":
        host = input("Enter host [127.0.0.1]: ").strip() or "127.0.0.1"
        port = input("Enter port [8000]: ").strip() or "8000"
        use_ssl_input = input("Use SSL? (yes/no) [no]: ").strip().lower() or "no"
        use_ssl = "true" if use_ssl_input in ["yes", "y"] else "false"
        create_webconfig(host, port, use_ssl)
        print_section("✅ Configuration completed!")
    else:
        print(f"{Colors.FAIL}❌ Unknown command: {args.command}{Colors.ENDC}")
        print("Use 'python deploy.py help' for instructions.")

if __name__ == "__main__":
    main()
