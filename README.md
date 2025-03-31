# ✨ Checkson

<div align="center">

![Checkson Logo](https://via.placeholder.com/150x150?text=Checkson)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![GitHub Stars](https://img.shields.io/github/stars/nipicoco/checkson?style=social)](https://github.com/nipicoco/checkson)

**A fast, user-friendly command-line tool for checking availability of GitHub usernames, repositories, and domain names.**

</div>

## 📋 Overview

Checkson is a modern, interactive terminal application designed to help you quickly check the availability of various online identifiers. Whether you're looking for a new GitHub username, repository name, or domain for your next project, Checkson provides a beautiful and efficient interface to search for available options.

## ✨ Features

- 🎨 **Beautiful Terminal UI**: Interactive menus, progress bars, and color-coded results
- ⚡ **Lightning Fast**: Concurrent processing with async I/O for checking multiple items simultaneously
- 🔄 **Multiple Check Types**: Support for GitHub usernames, GitHub repositories, and domain names
- 💻 **Dual Operation Modes**: 
  - Command-line parameters for scripting and automation
  - Interactive interface with keyboard navigation for casual use
- 📦 **Bulk Processing**: Check multiple items from files or command line arguments
- ⏱️ **Performance Optimized**: Fast responses with proper rate limiting to respect API constraints

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/nipicoco/checkson.git
cd checkson

# Install the package
pip install -e .
```

## 📖 Usage

### Interactive Mode

Simply run the application without arguments for an interactive terminal UI:

```bash
# Launch interactive mode
checkson
```

Or run the Python script directly:

```bash
python main.py
```

### Command Line Mode

#### GitHub Usernames

```bash
# Check specific usernames
checkson github username1 username2 username3

# Interactive mode for GitHub usernames
checkson github --interactive

# Check usernames from a file
checkson github --file usernames.txt

# Force synchronous mode (slower but more reliable for some APIs)
checkson github username1 username2 --sync
```

#### GitHub Repositories

```bash
# Check if repos exist under a specific owner
checkson repo --owner octocat repo1 repo2 repo3

# Interactive mode
checkson repo --owner octocat --interactive

# Check repo names from a file
checkson repo --owner octocat --file repos.txt
```

#### Domain Names

```bash
# Check domain availability
checkson domain example.com example.org

# Interactive mode
checkson domain --interactive

# Check domains from a file
checkson domain --file domains.txt
```

## ⚙️ Configuration

### Environment Variables

You can set the following environment variables in a `.env` file:

- `GITHUB_TOKEN`: GitHub personal access token (optional, increases rate limits)

Example `.env` file:
```
GITHUB_TOKEN=your_personal_access_token_here
```

## 💻 Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with increased verbosity
checkson github username --debug
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Nipicoco** - *Initial work*

## 🙏 Acknowledgments

- [Rich](https://github.com/Textualize/rich) - Beautiful terminal formatting
- [Typer](https://typer.tiangolo.com/) - CLI creation tool
- [httpx](https://www.python-httpx.org/) - Modern HTTP client for async requests 