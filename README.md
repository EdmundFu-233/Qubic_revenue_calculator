# Qubic Revenue Calculator / Qubic 收益计算器

一个中文本地化、免费开源的 Qubic 挖矿收益估算工具。项目通过 Qubic 网络数据、矿池数据、QUBIC 市场价格和用户算力，估算每日收益、每个 SOL 的价值、预期 SOL 产出、当前纪元进度和矿机运行概况。

Qubic Revenue Calculator is a Python-based open-source tool for estimating Qubic mining revenue. It combines live Qubic network statistics, market price data, pool performance data, and user-provided hashrate to produce practical revenue estimates for miners.

---

## 中文说明

### 项目简介

本项目是在开源 Qubic 收益估算 Notebook 基础上进行中文本地化和功能扩展的版本。它提供命令行和 Web 两种使用方式，适合个人矿工快速查看当前网络状态、预计收益、SOL 获取周期以及矿机汇总信息。

项目的目标不是提供金融承诺，而是把分散在 API、价格数据和矿池数据中的信息整理成更直观、可阅读的结果。

### 主要功能

- 根据用户算力估算每日收益和当前纪元收益。
- 从 Qubic-li API 获取当前纪元、网络算力、平均分和 SOL 产出速度。
- 从 CoinGecko 获取 QUBIC 市场价格。
- 将美元估算结果转换为人民币，便于中文用户查看。
- 支持离线模式，只需手动输入算力，不需要账号密码。
- 支持 Qubic-li 矿池账号模式，可查看矿机算力、SOL 数量、幸运值和最后活跃时间。
- Web 版本支持中文和英文输出。
- 命令行 Rich 版本使用表格展示结果。
- `without_rich` 目录提供更轻量的纯文本命令行版本。
- `web/test` 中的实验版包含 Qubic Solutions 矿池查询和短时间 JSON 缓存逻辑。

### 项目结构

```text
.
|-- README.md
|-- LICENSE
|-- requirements.txt
|-- qubic收益计算器.py
|-- without_rich/
|   |-- requirements.txt
|   `-- qubic收益计算器.py
`-- web/
    |-- qubic收益计算器web.py
    `-- test/
        `-- qubic收益计算器web.py
```

### 实现概览

核心脚本大致遵循同一套计算流程：

1. 获取用户算力。
   - 离线模式由用户手动输入算力。
   - Qubic-li 模式会登录 Qubic-li API，并汇总返回的矿机当前算力。
   - 实验 Web 版本还支持通过 token 或钱包 ID 查询 Qubic Solutions 矿池数据。

2. 获取网络状态。
   - 程序通过 Qubic-li score 接口获取当前纪元、估测网络算力、平均分和 SOL 产出速度。

3. 计算纪元进度。
   - 程序以 2024-02-21 12:00:00 UTC 作为第 97 纪元的开始时间。
   - 每个纪元按 7 天计算。
   - 根据当前时间推算当前纪元的开始时间、结束时间和进度百分比。

4. 获取价格和汇率数据。
   - CoinGecko 用于获取 QUBIC 的美元价格。
   - `CurrencyConverter` 用于将美元估算结果转换为人民币。

5. 计算收益。
   - 估算每 1 it/s 的每日收益。
   - 估算用户总算力对应的每日收益。
   - 估算每日预期 SOL 数量。
   - 估算每个 SOL 的当前价值和对应 QUBIC 数量。
   - 当预计获取一个 SOL 的周期超过一个纪元时输出风险提示。

6. 展示结果。
   - Rich 命令行版本用终端表格展示。
   - 无 Rich 版本用纯文本输出。
   - PyWebIO 版本在浏览器中展示表格。

### 安装

推荐使用 Python 3.9 或更高版本。

```bash
git clone https://github.com/EdmundFu-233/Qubic_revenue_calculator.git
cd Qubic_revenue_calculator
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

如果需要运行 Web 版本，还需要安装 PyWebIO：

```bash
pip install pywebio
```

运行无 Rich 版本时，可以使用 `without_rich` 目录下的依赖文件：

```bash
cd without_rich
pip install -r requirements.txt
```

### 使用方式

运行 Rich 命令行版本：

```bash
python3 qubic收益计算器.py
```

运行无 Rich 命令行版本：

```bash
cd without_rich
python3 qubic收益计算器.py
```

运行 Web 版本：

```bash
cd web
python3 qubic收益计算器web.py
```

Web 版本默认使用 80 端口。部分系统绑定 80 端口需要管理员权限；如果无法启动，可以将脚本中的 `port=80` 修改为 `8080` 等普通端口。

### 数据来源

- Qubic-li API：网络分数、纪元统计、Qubic-li 矿池矿机数据。
- Qubic Solutions pool endpoint：实验 Web 版本中的矿机数据。
- CoinGecko API：QUBIC 市场价格。
- CurrencyConverter：美元到人民币的汇率转换。

估算结果依赖外部 API。如果 Qubic 网络规则、矿池规则、价格接口或 API 返回格式发生变化，计算结果也可能需要调整。

### 隐私和安全说明

离线模式不需要输入矿池账号密码。

使用 Qubic-li 模式时，程序会把用户输入的用户名和密码发送到 Qubic-li 登录接口，以获取临时 API token。主命令行版本在用户选择保存时，会把账号密码保存到本地 `calculator_temp` 文件中。请不要在公共电脑或共享环境中保留该文件。

本项目是透明的开源工具。建议用户在输入任何凭据前先阅读源码。

### 局限性

- 收益结果是估算值，不是金融收益保证。
- 程序依赖第三方 API，网络错误或接口变更会影响结果。
- 开启 2FA 的 Qubic-li 账号目前可能无法通过登录模式使用，可改用离线模式。
- 矿机幸运值算法是近似计算，源码中也标注了该部分仍有改进空间。
- 原始计算公式来自公开的 Qubic 收益估算逻辑；如果 Qubic 奖励机制变化，公式需要同步更新。

### 技术要点

- 使用 Python、Requests、PyWebIO、Rich、PyCoinGecko、CurrencyConverter 和 pytz 构建。
- 实现 API 登录、JSON 解析、时间转换、收益估算和短时间缓存。
- 同时提供命令行和浏览器界面。
- Web 实验版本根据浏览器语言切换中文或英文显示。
- 提供轻量版本以适配不需要 Rich 表格的运行环境。

### 致谢

本项目基于以下开源 Qubic 收益估算 Notebook 进行本地化和扩展：

https://colab.research.google.com/github/dsglazyrin/qubic_utils/blob/main/Qubic_income_estimations.ipynb

### 许可证

本项目使用 GNU General Public License v3.0。详情请查看 `LICENSE`。

---

## English

### Overview

Qubic Revenue Calculator is a Python-based open-source tool for estimating Qubic mining revenue. It started as a Chinese-localized adaptation of an existing open-source Qubic income estimation notebook and grew into a multi-interface utility with command-line and web-based versions.

The project is designed to make Qubic mining economics easier to understand for individual miners by presenting epoch progress, network performance, expected SOL output, estimated daily income, and miner-level summaries in a readable format. It is an estimation tool, not a financial guarantee.

### Key Features

- Calculates estimated daily and epoch revenue from user hashrate.
- Retrieves live Qubic network statistics from the Qubic-li API.
- Retrieves QUBIC market price data through CoinGecko.
- Converts USD-based estimates into CNY for Chinese users.
- Supports offline mode for users who only want to enter hashrate manually.
- Supports Qubic-li pool login mode for miner-level hashrate, SOL count, luckiness, and activity summaries.
- Includes a PyWebIO web interface with Chinese and English output.
- Includes a terminal version using Rich tables for structured command-line output.
- Includes a simplified terminal version without Rich for lighter environments.
- Adds Qubic Solutions pool lookup and short-term JSON caching in the experimental web version.

### Project Structure

```text
.
|-- README.md
|-- LICENSE
|-- requirements.txt
|-- qubic收益计算器.py
|-- without_rich/
|   |-- requirements.txt
|   `-- qubic收益计算器.py
`-- web/
    |-- qubic收益计算器web.py
    `-- test/
        `-- qubic收益计算器web.py
```

### Implementation Overview

The main scripts share the same core calculation flow:

1. Collect hashrate information.
   - Offline mode asks the user to enter hashrate manually.
   - Qubic-li mode authenticates with the Qubic-li API and sums miner hashrate from the returned miner list.
   - The experimental web version also supports Qubic Solutions pool data through a token or wallet identifier.

2. Fetch current network information.
   - The project uses the Qubic-li score endpoint to retrieve the current epoch, estimated network hashrate, average score, and SOL production rate.

3. Estimate epoch timing.
   - Epoch 97 is treated as the reference epoch beginning on 2024-02-21 12:00:00 UTC.
   - Each epoch is modeled as a 7-day period.
   - The calculator derives the current epoch start time, end time, and progress percentage from this reference.

4. Fetch price and currency data.
   - CoinGecko is used to retrieve the current QUBIC price in USD.
   - `CurrencyConverter` is used to convert USD estimates into CNY where needed.

5. Calculate revenue estimates.
   - The calculator estimates income per 1 it/s per day.
   - It estimates total daily revenue from user hashrate.
   - It estimates expected SOL count per day.
   - It estimates current revenue per SOL and approximate QUBIC quantity per SOL.
   - It warns users when the expected time to obtain one SOL is longer than one epoch.

6. Present the results.
   - The Rich-based CLI version renders tables in the terminal.
   - The basic CLI version prints plain text output.
   - The PyWebIO version renders the same information in a browser-based interface.

### Installation

Python 3.9 or newer is recommended.

```bash
git clone https://github.com/EdmundFu-233/Qubic_revenue_calculator.git
cd Qubic_revenue_calculator
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The web version also requires PyWebIO:

```bash
pip install pywebio
```

For the simplified no-Rich version:

```bash
cd without_rich
pip install -r requirements.txt
```

### Usage

Run the Rich command-line version:

```bash
python3 qubic收益计算器.py
```

Run the simplified command-line version:

```bash
cd without_rich
python3 qubic收益计算器.py
```

Run the web version:

```bash
cd web
python3 qubic收益计算器web.py
```

The web script starts a PyWebIO server on port 80 by default. Depending on the operating system, binding to port 80 may require administrator privileges. If needed, change the `port=80` value in the script to another port such as `8080`.

### Data Sources

- Qubic-li API: network score data, epoch statistics, and Qubic-li pool miner performance.
- Qubic Solutions pool endpoint: miner data in the experimental web version.
- CoinGecko API: QUBIC market price.
- CurrencyConverter package: USD to CNY conversion.

The estimates depend on external API availability and may change as Qubic network conditions, price, pool reward rules, or endpoint behavior changes.

### Privacy and Security Notes

Offline mode does not require pool credentials.

When Qubic-li mode is used, the program sends the entered username and password to the Qubic-li authentication endpoint to obtain a temporary API token. The main command-line version can save credentials locally in a file named `calculator_temp` if the user chooses to reuse them. This file should be deleted on shared or public machines.

The project is intended as a transparency-first open-source calculator. Users should inspect the source code before entering any credentials.

### Limitations

- Revenue values are estimates, not financial guarantees.
- The calculator depends on third-party APIs, so network errors or API changes may affect results.
- Accounts with two-factor authentication may not work in the current Qubic-li login flow; offline mode can still be used.
- The miner luckiness calculation is an approximation and is marked in the source code as an area open to improvement.
- The original formulas are based on public Qubic mining estimation logic and may require updates if Qubic's reward mechanics change.

### Technical Highlights

- Built with Python, Requests, PyWebIO, Rich, PyCoinGecko, CurrencyConverter, and pytz.
- Implements API authentication, JSON parsing, timestamp conversion, revenue estimation, and short-term data caching.
- Provides both terminal and browser-based interfaces from the same estimation logic.
- Handles bilingual presentation in the experimental web interface by detecting browser language.
- Separates a dependency-light terminal variant for environments where Rich is unnecessary.

### Acknowledgement

This project is a localized and extended version of an open-source Qubic income estimation notebook:

https://colab.research.google.com/github/dsglazyrin/qubic_utils/blob/main/Qubic_income_estimations.ipynb

### License

This repository is licensed under the GNU General Public License v3.0. See `LICENSE` for details.
