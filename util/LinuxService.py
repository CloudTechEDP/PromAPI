import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from util.ErrorMessages import error_message_box


exe_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
service_name = "promapi"
exec_start = f"{exe_dir}/PromAPI start"
description="promapi"
user="root"



def linux_service_setup():
    """
    Create and start a systemd service unit for the PromAPI executable.
    
    Writes a service unit file to /etc/systemd/system/{service_name}.service, reloads systemd, enables the service to start at boot, and starts the service immediately. Side effects include creating or overwriting the unit file and invoking systemctl commands.
    
    Raises:
        OSError: If writing the service file fails.
        subprocess.CalledProcessError: If any systemctl command returns a non-zero exit status.
    """
    import os
    import subprocess

    service_file_content = f"""[Unit]
    [Unit]
    Description={description}
    After=network.target
    [Service]
    Type=simple
    User={user}
    ExecStart={exec_start}
    Restart=on-failure
    [Install]
    WantedBy=multi-user.target  
    """

    service_file_path = f"/etc/systemd/system/{service_name}.service"
    with open(service_file_path, 'w') as service_file:
        service_file.write(service_file_content)
    subprocess.run(['systemctl', 'daemon-reload'], check=True)
    subprocess.run(['systemctl', 'enable', service_name], check=True)
    subprocess.run(['systemctl', 'start', service_name], check=True)
    print(f"Service {service_name} has been set up and started.")
    return 