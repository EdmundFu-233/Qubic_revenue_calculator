# Qubic Revenue Calculator

A free, open-source Qubic mining revenue estimation tool. Combines network data, pool data, market prices, and user hashrate to produce practical revenue estimates.

**[中文说明见 README.md](README.md)**

## Features

- Estimate daily/epoch revenue based on user hashrate
- Fetch current epoch, network hashrate, and SOL output from Qubic-li API
- Get QUBIC market price from CoinGecko
- Convert USD estimates to CNY
- Offline mode (manual hashrate input)
- Qubic-li pool account integration
- Web and CLI UIs
- Chinese and English output (web version)

## Quick Start

```bash
# CLI version
pip install -r requirements.txt
python qubic_revenue_calculator.py

# Web version
cd web
python qubic_revenue_calculator_web.py
```

## Project Structure

```
.
├── README.md           # 中文文档
├── README_EN.md        # English documentation
├── LICENSE
├── requirements.txt
├── qubic_revenue_calculator.py
├── without_rich/
│   └── qubic_revenue_calculator.py
└── web/
    ├── qubic_revenue_calculator_web.py
    └── test/
        └── qubic_revenue_calculator_web.py
```

## How It Works

1. **Get user hashrate** — manual input (offline) or Qubic-li API (pool mode)
2. **Fetch network status** — current epoch, estimated network hashrate, SOL output rate
3. **Calculate epoch progress** — each epoch lasts 7 days starting from 2024-02-21 12:00 UTC (epoch 97)
4. **Estimate revenue** — combine hashrate share, network hashrate, SOL output, and market price

## Requirements

- Python 3.8+
- See `requirements.txt` for dependencies

## Contributing

Pull requests and issues welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT License
