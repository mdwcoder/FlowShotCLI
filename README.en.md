[Español](README.es.md) | [English](README.en.md)

---

# FlowShotCLI

FlowShotCLI is a strict, elegant terminal workflow recorder. It captures your shell commands and converts them into clean, reusable, and safe shell scripts.

Unlike other tools that record session output (like asciinema), FlowShotCLI focuses purely on the **logic**—the commands you ran—transforming a chaotic interactive session into a polished automation script.

## Features

- **Non-intrusive Recording**: Reads directly from your shell history (`.zsh_history` / `.bash_history`). No shell hooks.
- **Clean Flows**: Automatically removes consecutive duplicates and allows you to edit the flow before export.
- **Smart Export**: Generates production-ready scripts with `set -euo pipefail`.
- **Steps & Sections**: Organize long workflows into named sections with `flowshot step`.
- **Variables Detection**: Automatically detects and extracts repeated paths or values into variables.
- **Security First**: 
  - **Validators**: Warns about destructive (`rm -rf`) or interactive commands before export.
  - **Sanitizers**: Masks secrets (`ghp_...`) and home paths.
- **Interactive Player**: Replay your captured flows step-by-step with `flowshot play`.
- **AI Powered (Optional)**: If you have [Ollama](https://ollama.com/) installed locally, generate explanations, summaries, and titles for your flows.

## Installation

FlowShotCLI requires Python 3.8+.

```bash
pip install flowshot-cli
```

## Quick Start

1. **Start Recording**
   ```bash
   flowshot start
   ```

2. **Capture Your Work**
   Run your commands as usual.
   ```bash
   mkdir project
   cd project
   touch README.md
   ```
   *Mark a new section:*
   ```bash
   flowshot step "Build Phase"
   ```

3. **Stop & Review**
   ```bash
   flowshot stop
   flowshot list
   ```

4. **Export**
   ```bash
   flowshot export --bash --output setup.sh --preset safe
   ```

## Advanced Usage

### Steps
Group commands logically. These appear as section headers in exported scripts.

```bash
flowshot step "Database Migration"
```

### Export Presets
Choose the right safety level for your script:

- **local** (Default): Standard strict mode.
- **safe**: Adds interactive confirmation prompts for every command.
- **ci**: Adds `set -x` for verbose logging, suitable for pipelines.

```bash
flowshot export --preset safe
```

### Variable Extraction
FlowShot can detect repeated paths or values.

```bash
flowshot export --with-vars
```
*It will ask to extract duplicates like `/var/www/html` into variables.*

### Interactive Player
Run a flow directly from the CLI.

```bash
flowshot play
```
*Prompts for confirmation before running each command. Use `--yes` to auto-approve safe commands.*

### AI Features (Local Only)
If `ollama` is detected on `localhost:11434`, additional commands become available:

- `flowshot explain`: Deep explanation of the workflow.
- `flowshot summarize`: One-sentence summary.
- `flowshot title`: Generates a filename suggestion.

*These features are strictly local. No data leaves your machine.*

### Artifacts (Share Flows)
Share flows with teammates as JSON files.

```bash
flowshot save my_workflow.flow.json --file
flowshot load my_workflow.flow.json --file
```

## Security & Privacy

- **Data**: All flows are stored locally in `~/.flowshot`.
- **Sanitization**: Secrets and `$HOME` paths are masked during export.
- **Validation**: You get warnings if you try to export `rm -rf` or `sudo` commands without review.

## License

MIT License. See [LICENSE](LICENSE) for details.
