# -*- coding: utf-8 -*-
"""
将 iFinD 接口包路径写入 iFinDPy.pth，并安装到当前 Python 的 Lib\\site-packages。
因 THSDataInterface_Windows 不提交到 git，在新电脑上需先配置接口路径，再运行本脚本。

路径优先级：命令行参数 > 环境变量 IFINDPY_PATH > 项目下 .ifind_path 文件 > 项目内 THSDataInterface_Windows（若存在）
"""
import os
import sys
import site
from pathlib import Path

ENV_PATH = "IFINDPY_PATH"
PATH_FILE = ".ifind_path"
DEFAULT_RELATIVE = ["THSDataInterface_Windows", "bin", "x86"]
PTH_NAME = "iFinDPy.pth"


def get_ifind_path(project_root, cli_path=None):
    """按优先级解析出 iFinD 接口包目录（含 iFinDPy.py 的目录）。"""
    # 1) 命令行参数
    if cli_path:
        p = Path(cli_path).resolve()
        if p.is_dir():
            return p
        print("命令行路径不存在或不是目录: {}".format(p))
    # 2) 环境变量
    env = os.environ.get(ENV_PATH, "").strip()
    if env:
        p = Path(env).expanduser().resolve()
        if p.is_dir():
            return p
        print("环境变量 {} 指向的路径不存在: {}".format(ENV_PATH, p))
    # 3) 项目下的 .ifind_path（一行，绝对或相对项目根）
    path_file = project_root / PATH_FILE
    if path_file.is_file():
        line = path_file.read_text(encoding="utf-8").strip().splitlines()
        line = (line[0].strip() if line else "").strip()
        if line and not line.startswith("#"):
            p = (project_root / line).resolve() if not Path(line).is_absolute() else Path(line).resolve()
            if p.is_dir():
                return p
            print(".ifind_path 中的路径不存在: {}".format(p))
    # 4) 项目内默认相对路径（克隆后自己拷了接口包时）
    default = project_root.joinpath(*DEFAULT_RELATIVE)
    if default.is_dir():
        return default
    return None


def main():
    project_root = Path(__file__).resolve().parent
    cli_path = sys.argv[1] if len(sys.argv) > 1 else None
    ifind_path = get_ifind_path(project_root, cli_path)

    if not ifind_path:
        print("未找到 iFinD 接口目录，无法生成 .pth。")
        print("")
        print("请任选一种方式配置路径（指向含 iFinDPy.py 的目录，一般为 .../THSDataInterface_Windows/bin/x86）：")
        print("  1) 设置环境变量: set {}=<接口包路径>  （再运行本脚本）".format(ENV_PATH))
        print("  2) 在项目根目录创建 {}，内容写一行路径。可参考 .ifind_path.example".format(PATH_FILE))
        print("  3) 将 THSDataInterface_Windows 放到项目根目录后直接运行本脚本")
        print("  4) 运行: python setup_ifind_path.py <接口包路径>")
        sys.exit(1)

    # 可选：简单校验是否像接口目录
    if not (ifind_path / "iFinDPy.py").exists() and not (ifind_path / "iFinDPy.pyd").exists():
        print("警告: 未在 {} 下发现 iFinDPy.py/iFinDPy.pyd，请确认路径是否正确。".format(ifind_path))

    pth_content = str(ifind_path).strip()

    # 1) 项目下保存 iFinDPy.pth（便于复制到 site-packages 或查看）
    pth_in_project = project_root / PTH_NAME
    pth_in_project.write_text(pth_content, encoding="utf-8")
    print("已写入: {}".format(pth_in_project))

    # 2) 写入当前 Python 的 site-packages
    try:
        site_packages = site.getsitepackages()
        if not site_packages:
            site_packages = [site.getusersitepackages()]
        for sp in site_packages:
            sp_path = Path(sp)
            if sp_path.is_dir():
                pth_dest = sp_path / PTH_NAME
                pth_dest.write_text(pth_content, encoding="utf-8")
                print("已安装到 site-packages: {}".format(pth_dest))
                break
        else:
            print("未找到 site-packages，请手动将 iFinDPy.pth 复制到 Python 的 Lib\\site-packages。")
    except Exception as e:
        print("写入 site-packages 失败: {}".format(e))
        print("请手动将项目下的 iFinDPy.pth 复制到 Python 的 Lib\\site-packages。")

    print("完成。可运行: python -c \"from iFinDPy import *; print('iFinDPy 可用')\" 验证。")


if __name__ == "__main__":
    main()
