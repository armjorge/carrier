class CHROME_HELPER:
    @staticmethod
    def install_chromedriver():
        """Guide user to install Chrome and ChromeDriver for Testing into home directory."""

        import os
        import platform
        import zipfile
        import glob
        import subprocess
        import stat

        system = platform.system()
        home = os.path.expanduser("~")

        chrome_relative_parts = []

        if system == "Windows":
            target_dir = os.path.join(home, "Documents")
            chromedriver_prefix = "chromedriver-win64"
            chrome_prefix = "chrome-win64"
            chromedriver_exe = "chromedriver.exe"
            chrome_relative_parts = [chrome_prefix, "chrome.exe"]
        elif system == "Darwin":  # macOS
            target_dir = os.path.join(home, "chrome_testing")
            machine = platform.machine().lower()
            arch_suffix = "arm64" if "arm" in machine else "x64"
            chromedriver_prefix = f"chromedriver-mac-{arch_suffix}"
            chrome_prefix = f"chrome-mac-{arch_suffix}"
            chromedriver_exe = "chromedriver"
            chrome_relative_parts = [
                chrome_prefix,
                "Google Chrome for Testing.app",
                "Contents",
                "MacOS",
                "Google Chrome for Testing",
            ]
        else:
            print(f"❌ Unsupported OS: {system}")
            return None, None

        os.makedirs(target_dir, exist_ok=True)

        chrome_binary_path = os.path.join(target_dir, *chrome_relative_parts)
        chromedriver_path = os.path.join(target_dir, chromedriver_prefix, chromedriver_exe)

        if os.path.exists(chrome_binary_path) and os.path.exists(chromedriver_path):
            print("✅ Chrome for Testing ya está instalado. Reutilizando binarios existentes.")
            print(f"   Chrome: {chrome_binary_path}")
            print(f"   Chromedriver: {chromedriver_path}")
            return chrome_binary_path, chromedriver_path

        print("🌐 Open the following link to download the Chrome for Testing binaries:")
        print("👉 https://googlechromelabs.github.io/chrome-for-testing/\n")
        print(f"📂 Copia los zip en: {target_dir}")
        print("⬇️ Se requieren los archivos chromedriver y chrome del mismo release.")

        # Open folder for user convenience (macOS Finder / Windows Explorer)
        try:
            if system == "Darwin":
                subprocess.run(["open", target_dir], check=False)
            elif system == "Windows":
                subprocess.run(["explorer", target_dir], check=False)
        except Exception as e:
            print(f"(⚠️ No se pudo abrir la carpeta automáticamente: {e})")

        input("Presiona Enter cuando los zip estén en la carpeta...")

        chromedriver_zip = glob.glob(os.path.join(target_dir, f"{chromedriver_prefix}*.zip"))
        chrome_zip = glob.glob(os.path.join(target_dir, f"{chrome_prefix}*.zip"))

        # Recheck in case the user extracted manually before providing the zip
        if os.path.exists(chrome_binary_path) and os.path.exists(chromedriver_path):
            print("✅ Se detectó una instalación existente durante la verificación.")
            return chrome_binary_path, chromedriver_path

        if not chromedriver_zip or not chrome_zip:
            print("❌ No se encontraron los zip. Verifica los nombres descargados y vuelve a intentarlo.")
            return None, None

        chromedriver_zip = chromedriver_zip[0]
        chrome_zip = chrome_zip[0]

        def unzip_to_target(zip_path):
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(target_dir)
            print(f"✅ Se extrajo {os.path.basename(zip_path)}")

        unzip_to_target(chromedriver_zip)
        unzip_to_target(chrome_zip)

        if system == "Darwin":
            app_root = os.path.join(target_dir, chrome_prefix, "Google Chrome for Testing.app")
            quarantine_targets = [
                os.path.join(target_dir, chromedriver_prefix, chromedriver_exe),
                app_root,
            ]
            for target in quarantine_targets:
                try:
                    subprocess.run(
                        ["xattr", "-d", "com.apple.quarantine", target],
                        check=False,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
                except Exception as e:
                    print(f"(⚠️ No se pudo limpiar quarantine en {target}: {e})")

            def ensure_executable(path):
                if os.path.exists(path):
                    try:
                        mode = os.stat(path).st_mode
                        if not (mode & stat.S_IXUSR):
                            os.chmod(
                                path,
                                mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH,
                            )
                    except Exception as exec_err:
                        print(f"(⚠️ No se pudo ajustar permisos en {path}: {exec_err})")

            ensure_executable(chromedriver_path)
            ensure_executable(chrome_binary_path)

            helpers_glob = glob.glob(
                os.path.join(
                    app_root,
                    "Contents",
                    "Frameworks",
                    "Google Chrome for Testing Framework.framework",
                    "Versions",
                    "*",
                    "Helpers",
                )
            )

            for helpers_dir in helpers_glob:
                for root, _dirs, files in os.walk(helpers_dir):
                    for filename in files:
                        ensure_executable(os.path.join(root, filename))
        else:
            for executable_path in [chromedriver_path, chrome_binary_path]:
                if os.path.exists(executable_path):
                    try:
                        current_mode = os.stat(executable_path).st_mode
                        if not (current_mode & stat.S_IXUSR):
                            os.chmod(
                                executable_path,
                                current_mode
                                | stat.S_IXUSR
                                | stat.S_IXGRP
                                | stat.S_IXOTH,
                            )
                    except Exception as e:
                        print(f"(⚠️ No se pudo ajustar permisos en {executable_path}: {e})")

        for zip_path in [chromedriver_zip, chrome_zip]:
            try:
                os.remove(zip_path)
            except Exception as e:
                print(f"(⚠️ No se pudo borrar {zip_path}: {e})")

        if not os.path.exists(chromedriver_path) or not os.path.exists(chrome_binary_path):
            print("❌ Hubo un problema al preparar los binarios. Revisa los archivos extraídos.")
            return None, None

        print(f"✅ Chromedriver listo en: {chromedriver_path}")
        print(f"✅ Chrome for Testing listo en: {chrome_binary_path}")

        return chrome_binary_path, chromedriver_path

    @staticmethod
    def chrome_driver_load(directory):
        """Launch Chrome with OS-specific paths and consistent configuration."""

        import os
        import platform
        from selenium import webdriver
        from selenium.common.exceptions import SessionNotCreatedException, WebDriverException
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options

        os.makedirs(os.path.abspath(directory), exist_ok=True)

        chrome_binary_path, chromedriver_path = Helper.install_chromedriver()
        if not chrome_binary_path or not chromedriver_path:
            print("❌ No fue posible obtener los binarios de Chrome.")
            return None

        system = platform.system()

        chrome_options = Options()
        chrome_options.binary_location = chrome_binary_path

        prefs = {
            "download.default_directory": os.path.abspath(directory),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True,
        }
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--remote-allow-origins=*")

        if system == "Linux":
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--no-sandbox")
        elif system == "Windows":
            chrome_options.add_argument("--disable-gpu")

        try:
            service = Service(chromedriver_path)
            driver = webdriver.Chrome(service=service, options=chrome_options)
            print("🚀 ChromeDriver launched successfully.")
            return driver
        except SessionNotCreatedException as exc:
            print(f"❌ ChromeDriver no pudo crear la sesión: {exc}")
        except WebDriverException as exc:
            print(f"❌ Error al iniciar ChromeDriver: {exc}")
        except Exception as exc:
            print(f"❌ Error inesperado al iniciar ChromeDriver: {exc}")

        return None