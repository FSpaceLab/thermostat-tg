import os
from manager.os_manager import OS
from manager.db_manager.manager import update_bot_session
from manager import config
from .answers import IS_NOT_A_FILE


class ShellManager(OS):
    def show_files(self, user_id, path=""):
        return self.ls(user_id, path=path)

    def show_current_dir(self, user_id):
        return self.pwd(user_id)

    def change_dir(self, user_id, cmd):
        cmd = cmd.replace("$", "").replace("cd", '').strip()
        return self.cd(user_id=user_id, path=cmd)

    def path_to_file(self, user_id, name_file):
        name_file = name_file.split()[-1]
        path = f"{self.pwd(user_id)}/{name_file}"
        return path if os.path.isfile(path) else IS_NOT_A_FILE

    def command(self, user_id: int, cmd: str):
        is_sudo = False
        sudo_start = cmd.find("sudo")
        cmd = cmd[1:]
        pwd = self.pwd(user_id=user_id)
        cmd = cmd.replace("{P}", pwd+("/" if pwd[-1] != "/" else ""))\
                 .replace("{PATH}", pwd+("/" if pwd[-1] != "/" else ""))

        if sudo_start != -1:
            is_sudo = True
            cmd = cmd[5:]

        return self.runner(
            f"{self.sudo(config.os.sudo_password) if is_sudo else ''} {cmd}",
            return_result=True
        ).replace("\n", "\n\n")