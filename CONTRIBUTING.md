# Contributing to docx2navTree

Contributions to the template tooling are welcome. This guide covers contributing back to the **template repository**, not working with content in your private fork.

## Getting Started

1. **Fork the repository**
   ```bash
   git clone https://github.com/PlateauPerspectives/docx2navTree.git
   cd docx2navTree
   ```

2. **Install dependencies**
   ```bash
   make install-deps
   make check-deps
   ```

3. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## What to Contribute

- **Bug fixes** in the build system or parsers
- **New features** for document processing
- **Better image handling** (WMF conversion, format support)
- **Documentation** improvements
- **Tests** for build_book.py and related scripts

## Coding Standards

- Follow PEP 8 for Python code
- Use `Path` objects for file paths
- Specify `encoding="utf-8"` when opening files
- Use clear commit messages: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`

## Testing

```bash
make clean
make build
make verify
```

Test with the included `example/sample-book.docx` before submitting.

## Pull Request Process

1. Update your fork: `git fetch upstream && git rebase upstream/main`
2. Run `make verify`
3. Push and create a PR with a clear description of the change

**Do not commit:**
- Content files (DOCX, per-language configs)
- Generated output (`export/`, `export_md/`)
- IDE or OS files

## License

By contributing, you agree that your contributions will be licensed under the GPL-3.0 License.
