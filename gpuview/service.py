import getpass
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import textwrap

SERVICE_NAME = "gpuview.service"
SERVICE_FILE_PATH = f"/etc/systemd/system/{SERVICE_NAME}"


def _run_sudo(command: list[str]):
    """Helper function to run a command with sudo and handle errors."""
    try:
        print(f"Running: sudo {' '.join(command)}")
        subprocess.run(["sudo"] + command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: Command failed: 'sudo {' '.join(command)}'", file=sys.stderr)
        print(f"Return code: {e.returncode}", file=sys.stderr)
        print("Please check permissions and systemd logs.", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("Error: 'sudo' command not found. Cannot manage system service.", file=sys.stderr)
        sys.exit(1)


def _check_systemd():
    """Check if we are on Linux with systemd."""
    if platform.system() != "Linux":
        print("Error: Service installation is only supported on Linux.", file=sys.stderr)
        sys.exit(1)

    if not shutil.which("systemctl"):
        print("Error: Service installation only supports systemd. 'systemctl' not found.", file=sys.stderr)
        print("Your 'service.sh' (supervisor) script is no longer supported.", file=sys.stderr)
        sys.exit(1)

    # Check if root, if not, we need sudo
    if os.geteuid() != 0 and not shutil.which("sudo"):
        print("Error: This command requires 'sudo' to manage system services.", file=sys.stderr)
        sys.exit(1)


def _is_installed() -> bool:
    """Checks if the service file already exists."""
    return os.path.exists(SERVICE_FILE_PATH)


def _is_active() -> bool:
    """Checks if the service is currently active."""
    # systemctl is-active returns exit code 0 if active, non-zero otherwise
    result = subprocess.run(["systemctl", "is-active", "--quiet", SERVICE_NAME])
    return result.returncode == 0


def _install(args):
    """Internal function to create, install, and enable the service file."""
    print(f"Installing {SERVICE_NAME}...")

    gpuview_path = shutil.which("gpuview")
    if not gpuview_path:
        print("Error: 'gpuview' executable not found in PATH.", file=sys.stderr)
        print("Please ensure gpuview is installed and your PATH is correct.", file=sys.stderr)
        sys.exit(1)

    username = getpass.getuser()
    arg_list = ["run"]  # The 'run' command for gpuview
    if args.host:
        arg_list.append(f"--host {args.host}")
    if args.port:
        arg_list.append(f"--port {args.port}")
    if args.safe_zone:
        arg_list.append("--safe-zone")
    if args.exclude_self:
        arg_list.append("--exclude-self")

    run_command_args = " ".join(arg_list)
    service_content = textwrap.dedent(f"""
    [Unit]
    Description=GPUView Dashboard Server
    After=network.target

    [Service]
    User={username}
    ExecStart={gpuview_path} {run_command_args}
    Restart=always
    RestartSec=3

    [Install]
    WantedBy=multi-user.target
    """)

    print("--- Service File Content ---")
    print(service_content)
    print("----------------------------")

    try:
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write(service_content)
            temp_path = f.name

        print("Sudo privileges are required to install the system service.")
        _run_sudo(["cp", temp_path, SERVICE_FILE_PATH])
        _run_sudo(["systemctl", "daemon-reload"])
        _run_sudo(["systemctl", "enable", SERVICE_NAME])

        print(f"Service '{SERVICE_NAME}' has been installed and enabled.")
        print("To check the status, run: gpuview service status")
    finally:
        if "temp_path" in locals():
            os.remove(temp_path)


def status(args):
    """Checks the status of the systemd service."""
    _check_systemd()
    if not _is_installed():
        print(f"Service '{SERVICE_NAME}' is not installed.")
        return

    print(f"Checking status for {SERVICE_NAME}...")
    # Don't use _run_sudo, as status can return non-0 exit codes
    subprocess.run(["systemctl", "status", SERVICE_NAME])


def start(args):
    """Starts the systemd service. Installs it if not already installed."""
    _check_systemd()

    if _is_active():
        print(f"Service '{SERVICE_NAME}' is already running.")
        status(args)
        return

    if not _is_installed():
        print("Service not found. Running first-time installation...")
        _install(args)

    print(f"Starting {SERVICE_NAME}...")
    _run_sudo(["systemctl", "start", SERVICE_NAME])
    print("Service started.")
    status(args)


def stop(args):
    """Stops the systemd service."""
    _check_systemd()
    if not _is_installed():
        print(f"Service '{SERVICE_NAME}' is not installed.")
        return
    if not _is_active():
        print(f"Service '{SERVICE_NAME}' is already stopped.")
        return

    print(f"Stopping {SERVICE_NAME}...")
    _run_sudo(["systemctl", "stop", SERVICE_NAME])
    print("Service stopped.")


def logs(args):
    """Shows systemd service logs using journalctl."""
    _check_systemd()
    if not _is_installed():
        print(f"Service '{SERVICE_NAME}' is not installed.")
        return

    print(f"Showing logs for {SERVICE_NAME}...")
    print("Press Ctrl+C to exit log viewing.")
    try:
        subprocess.run(["journalctl", "-u", SERVICE_NAME, "-f"], check=True)
    except KeyboardInterrupt:
        print("Stopped viewing logs.")
    except subprocess.CalledProcessError as e:
        print(f"Error viewing logs: {e}", file=sys.stderr)
        print("Try running: sudo journalctl -u gpuview.service", file=sys.stderr)


def delete(args):
    """Stops and deletes the systemd service."""
    _check_systemd()
    if not _is_installed():
        print(f"Service '{SERVICE_NAME}' is not installed.")
        return

    print(f"Deleting {SERVICE_NAME}...")
    try:
        if _is_active():
            _run_sudo(["systemctl", "stop", SERVICE_NAME])
    except Exception:
        print("Service was running, continuing with deletion.")

    _run_sudo(["systemctl", "disable", SERVICE_NAME])
    _run_sudo(["rm", SERVICE_FILE_PATH])
    _run_sudo(["systemctl", "daemon-reload"])

    print(f"Service '{SERVICE_NAME}' has been stopped and deleted.")
