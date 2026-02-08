# stratkit — 指数权重示例

基于同花顺 iFinD 数据接口（见项目根目录 `API` 文档），实现：**输入指数名称或指数代码，获取该指数权重前 10 分布**。

## 依赖准备

1. **接口包路径**  
   将 iFinD 接口包路径加入 Python：
   - 在项目根目录执行一次：`python setup_ifind_path.py`  
   - 或把根目录下的 `iFinDPy.pth` 复制到当前 Python 的 `Lib\site-packages`，并把其中路径改为你本机的 `THSDataInterface_Windows\bin\x86` 绝对路径。

2. **账号**  
   在 `stratkit/config.py` 中配置 iFinD 接口账号与密码（与 `API/APILIST` 一致）。

## 运行

在项目根目录执行：

```bash
python -m stratkit.index_weight
```

或进入 `stratkit` 目录后：

```bash
python index_weight.py
```

按提示输入指数名称或指数代码（如 `000688USD08.SH` 或 `沪深300`），即可看到该指数权重前 10 的分布。

## 接口说明

- 使用专题报表 **THS_DR**，报表 ID：`p03563`（指数权重）。
- 参数：`date`（YYYYMMDD）、`index_name`（指数名称或代码）。
- 输出列：`p03563_f001`～`p03563_f004`，取前 10 条。

详见项目根目录 `API/Ofiicial_Api_word` 与 `API/APILIST`。
