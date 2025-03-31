# Checkson

A fast, user-friendly command-line tool for checking availability of GitHub usernames, repositories, and domain names, this was made because i was bored and couldnt find a perfect name for my github and my domain.

## Features

- **Modern Terminal UI**: Beautiful, user-friendly terminal interface with colors, tables, and progress bars
- **Concurrent Checking**: Efficient async processing to check multiple items in parallel
- **Multiple Check Types**: Support for GitHub usernames, GitHub repositories, and domain names
- **Interactive Mode**: Prompt for items to check with a friendly interactive interface
- **Bulk Processing**: Check items from arguments or from a file
- **Performance Optimized**: Fast response times with proper rate limiting

## Installation

```bash
# Clone the repository
git clone https://github.com/Nipicoco/checkson.git
cd checkson

# Install the package
pip install -e .
```

## Usage

### Check GitHub Usernames

```bash
# Check specific usernames
checkson github username1 username2 username3

# Interactive mode
checkson github --interactive

# Check usernames from a file
checkson github --file usernames.txt

# Force synchronous mode (slower but more reliable for some APIs)
checkson github username1 username2 --sync
```

### Check GitHub Repositories

```bash
# Check if repos exist under a specific owner
checkson repo --owner octocat repo1 repo2 repo3

# Interactive mode
checkson repo --owner octocat --interactive

# Check repo names from a file
checkson repo --owner octocat --file repos.txt
```

### Check Domain Names

```bash
# Check domain availability
checkson domain example.com example.org

# Interactive mode
checkson domain --interactive

# Check domains from a file
checkson domain --file domains.txt
```

## Environment Variables

You can set the following environment variables:

- `GITHUB_TOKEN`: GitHub personal access token (optional, increases rate limits)

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with increased verbosity
checkson github username --debug
```

## License

MIT 