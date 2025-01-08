 # 🚀 Are.na Channel Export Tool

Automated tool for exporting Are.na channels using Selenium and Python.

## ⚙️ Setup

```bash
# 1. Clone the repository and navigate to directory
git clone https://github.com/yourusername/arena-channel-export.git
cd arena-channel-export

# 2. Set up Python virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install project dependencies
pip install -r requirements.txt

# 4. Install ChromeDriver
# macOS
brew install chromedriver

# Linux
sudo apt install chromium-chromedriver

# Windows: Download from https://sites.google.com/chromium.org/driver/
```

Create a `.env` file in the project root:
```plaintext
ARENA_EMAIL=<your_email>
ARENA_PASSWORD=<your_password>
ARENA_USERNAME=<your_username>
CHROMEDRIVER_PATH=<path_to_chromedriver>
```

## 🎯 Usage

Export all channels:
```bash
python arena_export.py --all
```

Export specific channels:
```bash
python arena_export.py --count <number>    # Export first N channels
python arena_export.py --name "<name>"     # Export specific channel
```

Override environment variables:
```bash
python arena_export.py --email <your_email> --password <your_password>
```

## 🔧 Troubleshooting

- **ChromeDriver issues**: Ensure Chrome and ChromeDriver versions match
- **Login fails**: Check credentials in `.env` file
- **Debug mode**: Run with `--debug` flag for detailed logs

## 📋 Requirements

- Python 3.8+
- Google Chrome
- ChromeDriver
- Are.na account

## 📄 License

MIT License - See [LICENSE](LICENSE) file
