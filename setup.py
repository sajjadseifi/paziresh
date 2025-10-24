import sys
import subprocess
from pathlib import Path

# -----------------------------
# 🔹 Helper Functions
# -----------------------------
def print_section(title):
    print("\n" + "="*60)
    print(f"🔹 {title}")
    print("="*60 + "\n")

def run(cmd, description=None, continue_on_error=False):
    if description:
        print_section(description)
    try:
        subprocess.check_call(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error while running: {cmd}")
        if not continue_on_error:
            sys.exit(e.returncode)

def ensure_pip():
    print_section("Checking pip in virtual environment")
    try:
        import pip
        print("✅ pip is available in this environment")
    except ImportError:
        print("⚠️ pip not found, bootstrapping pip ...")
        from ensurepip import bootstrap
        bootstrap()
        run(f'"{sys.executable}" -m pip install --upgrade pip', "Upgrading pip")

# -----------------------------
# 🔹 Platform Targets
# -----------------------------
PLATFORMS = [
    "win_amd64", "win32",
    "manylinux_2_28_x86_64", "manylinux_2_28_i686",
    "macosx_13_0_x86_64", "macosx_13_0_i386"
]

# -----------------------------
# 🔹 Extra packages 
# -----------------------------
EXTRA_PKGS = [
    "pip",
    "wfastcgi",
    "prettytable",
    "configparser",
    "setuptools",
    "wcwidth",
    "django-sslserver",
]

# -----------------------------
# 🔹 Requirements file
# -----------------------------
def get_requirements_file(project_path: Path):
    req_file = project_path / "requirements.txt"
    if not req_file.exists():
        print("⚠️ requirements.txt not found. Please create it first.")
        sys.exit(1)
    print_section(f"Using requirements.txt: {req_file.name}")
    return req_file

# -----------------------------
# 🔹 Update requirements with extras
# -----------------------------
def update_requirements(req_file: Path):
    if not req_file.exists():
        existing_packages = []
    else:
        with open(req_file, "r", encoding="utf-8") as f:
            existing_packages = [line.strip() for line in f if line.strip()]
    updated_packages = list(dict.fromkeys(existing_packages + EXTRA_PKGS))
    with open(req_file, "w", encoding="utf-8") as f:
        f.write("\n".join(updated_packages))
    print(f"✅ requirements.txt updated with {len(EXTRA_PKGS)} extra packages")
    return updated_packages

# -----------------------------
# 🔹 Install only extra packages (locally)
# -----------------------------
def install_extra_packages_locally(extra_packages):
    print_section("Installing extra packages required for setup.py (only locally)")
    for pkg in extra_packages:
        run(f'"{sys.executable}" -m pip install {pkg}', f"Installing {pkg}", continue_on_error=True)

# -----------------------------
# 🔹 Download package for all platforms
# -----------------------------
def download_package_for_all_platforms(pkg, packages_dir):
    """
    Download a package for all target platforms.
    Will download:
      1. Universal / source (sdist) .tar.gz
      2. Wheels for each platform if available
    """
    # 1️⃣ دانلود source/universal (sdist)
    run(f'"{sys.executable}" -m pip download "{pkg}" -d "{packages_dir}" --no-deps --no-binary=:all:',
        f"Downloading {pkg} (source/universal)")

    # 2️⃣ دانلود wheel مخصوص هر پلتفرم
    for plat in PLATFORMS:
        cmd = (
            f'"{sys.executable}" -m pip download "{pkg}" '
            f'-d "{packages_dir}" '
            f'--platform {plat} '
            f'--python-version {sys.version_info[0]}{sys.version_info[1]} '
            f'--implementation cp '
            f'--abi cp{sys.version_info[0]}{sys.version_info[1]} '
            f'--only-binary=:all: '
            f'--no-deps'
        )
        run(cmd, f"Downloading {pkg} for platform {plat}", continue_on_error=True)

# -----------------------------
# 🔹 Download all requirements
# -----------------------------
def download_requirements(req_file: Path, packages_dir: Path):
    print_section("Downloading all requirements for all platforms (no installation)")
    packages_dir.mkdir(exist_ok=True, parents=True)

    packages = update_requirements(req_file)

    for pkg in packages:
        print(f"\n📦 Downloading {pkg} for all platforms ...")
        download_package_for_all_platforms(pkg, packages_dir)

    print("\n✅ All required packages downloaded for all platforms successfully!")

# -----------------------------
# 🔹 Main
# -----------------------------
def main():
    print_section("Starting setup.py script")
    project_path = Path(__file__).parent.resolve()
    packages_dir = project_path / "packages"
    packages_dir.mkdir(exist_ok=True, parents=True)

    ensure_pip()

    # Install only extra packages locally for setup execution
    install_extra_packages_locally(EXTRA_PKGS)

    # Download everything else (no installation)
    req_file = get_requirements_file(project_path)
    download_requirements(req_file, packages_dir)

    print_section("Setup complete!")
    print("🎉 All packages downloaded for offline use (no installation done).")
    print(f"📂 Packages stored in: {packages_dir}")
    print("💡 To install offline later, use:")
    print("   pip install --no-index --find-links=packages -r requirements.txt")

if __name__ == "__main__":
    main()
