# -*- coding: utf-8 -*-
"""
根据 API 接口说明实现：输入指数名称（或指数代码），获取该指数权重前 10 分布。
接口：THS_DR 专题报表 - 指数权重 p03563，参数 date、index_name。
"""
from __future__ import print_function

import sys
from pathlib import Path
from datetime import datetime

# 确保可导入 iFinDPy：优先使用项目侧接口包路径
_project_root = Path(__file__).resolve().parent.parent
_ifind_dir = _project_root / "THSDataInterface_Windows" / "bin" / "x86"
if _ifind_dir.is_dir() and str(_ifind_dir) not in sys.path:
    sys.path.insert(0, str(_ifind_dir))
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

# 若已通过 iFinDPy.pth 安装到 site-packages，则直接 import
try:
    from iFinDPy import THS_iFinDLogin, THS_iFinDLogout, THS_DR
except ImportError:
    print("无法导入 iFinDPy，请先运行项目根目录下的 setup_ifind_path.py 安装接口路径。")
    print("或确认 THSDataInterface_Windows 位于: {}".format(_ifind_dir))
    sys.exit(1)

# 使用项目配置的账号（可改为从环境变量读取）
try:
    from stratkit.config import IFIND_USERNAME, IFIND_PASSWORD
except ImportError:
    try:
        from config import IFIND_USERNAME, IFIND_PASSWORD
    except ImportError:
        IFIND_USERNAME = "接口账号"
        IFIND_PASSWORD = "接口密码"

# 指数权重报表 ID，输出列（按 API 文档）
INDEX_WEIGHT_REPORT = "p03563"
INDEX_WEIGHT_OUTPUT = "p03563_f001:Y,p03563_f002:Y,p03563_f003:Y,p03563_f004:Y"


# 登录错误码说明（SDK 接口）：0=成功，-201=重复登录，-2=用户名或密码错误，-9=设备数超限被锁
LOGIN_ERROR_MESSAGES = {
    0: "登录成功",
    -2: "用户名或密码错误",
    -9: "设备数超限被锁（登录累计可绑定 8 台设备，超过需联系客服解锁）",
    -201: "重复登录（已在其他处登录）",
}


def login():
    """登录 iFinD 数据接口（SDK 仅支持单设备同时登录，累计绑定不超过 8 台设备）"""
    ret = THS_iFinDLogin(IFIND_USERNAME, IFIND_PASSWORD)
    if ret in (0, -201):
        print("iFinD 登录成功")
        return True
    msg = LOGIN_ERROR_MESSAGES.get(ret, "未知错误，请查看接口文档或联系客服")
    print("iFinD 登录失败，errorcode: {} ({})".format(ret, msg))
    return False


def get_index_weight_top10(index_name, date=None):
    """
    获取指定指数的权重数据，并返回前 10 条。
    index_name: 指数名称或指数代码，如 000688USD08.SH、沪深300 等
    date: 日期，YYYYMMDD，默认当前交易日
    """
    if date is None:
        date = datetime.now().strftime("%Y%m%d")
    param = "date={};index_name={}".format(date, index_name)
    result = THS_DR(INDEX_WEIGHT_REPORT, param, INDEX_WEIGHT_OUTPUT, "format:json")
    if result.errorcode != 0:
        print("接口错误: {}".format(getattr(result, "errmsg", result.errorcode)))
        return None
    if not hasattr(result, "data") or result.data is None:
        print("无权重数据")
        return None
    df = result.data
    if hasattr(df, "head"):
        top10 = df.head(10)
    else:
        top10 = df[:10] if len(df) >= 10 else df
    return top10


def main():
    if not login():
        return
    try:
        index_input = input("请输入指数名称或指数代码（如 000688USD08.SH 或 沪深300）: ").strip()
        if not index_input:
            print("未输入指数")
            return
        top10 = get_index_weight_top10(index_input)
        if top10 is not None:
            print("\n指数 [{}] 权重前 10 分布:\n".format(index_input))
            print(top10.to_string() if hasattr(top10, "to_string") else top10)
    finally:
        THS_iFinDLogout()
        print("\n已登出 iFinD")


if __name__ == "__main__":
    main()
