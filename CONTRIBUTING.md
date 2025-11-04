# Contributing to VENOM

Thank you for your interest in contributing to VENOM Ω-AIOS + Λ-Genesis! 🌌

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/VENOM-Omega-Lambda.git
   ```
3. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Setup

### Android Development

**Prerequisites:**
- Android Studio Arctic Fox or later
- JDK 17
- Android SDK 26+ (minimum), 34 (target)
- NDK for native bridge

**Setup:**
```bash
./gradlew build
```

### Python Development

**Prerequisites:**
- Python 3.8+
- pip and virtualenv

**Setup:**
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -e .

# Run tests
cd venom_lambda
pytest -v
```

## Code Style

### Kotlin
- Follow [Kotlin Coding Conventions](https://kotlinlang.org/docs/coding-conventions.html)
- Use meaningful variable names
- Add KDoc comments for public APIs
- Keep functions focused and small

### Python
- Follow [PEP 8](https://pep8.org/)
- Use type hints where applicable
- Add docstrings for all public functions/classes
- Maximum line length: 100 characters

Example:
```python
def time_wrap(k: float, p: float, u: float, t1: float) -> float:
    """
    Apply time wrapping transformation.
    
    Args:
        k: Kernel multiplier
        p: Parallel fraction
        u: Utilization factor
        t1: Original time
        
    Returns:
        Wrapped time value
    """
    # Implementation
```

## Testing

### Android Tests
```bash
# Unit tests
./gradlew test

# Instrumented tests (requires device/emulator)
./gradlew connectedAndroidTest
```

### Python Tests
```bash
cd venom_lambda
pytest -v --cov=. --cov-report=html
```

**Test Requirements:**
- All new features must include tests
- Maintain or improve code coverage
- Tests should be fast and focused
- Use descriptive test names

## Pull Request Process

1. **Update Documentation**: Ensure README.md and relevant docs are updated
2. **Add Tests**: Include tests for new features
3. **Run Tests**: Ensure all tests pass locally
4. **Lint Code**: Fix any linting errors
5. **Update CHANGELOG**: Add your changes to CHANGELOG.md
6. **Create PR**: Submit with clear description of changes

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Python tests pass
- [ ] Kotlin tests pass (if applicable)
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests passing
- [ ] No breaking changes (or documented)
```

## Areas for Contribution

### High Priority
- Full TensorFlow Lite model integration
- Voice I/O implementation
- Vision processing module
- Multi-device mesh testing
- Performance benchmarking

### Medium Priority
- Additional organ implementations
- Enhanced RAG with FAISS
- gRPC implementation completion
- iOS port planning
- Cloud synchronization (optional)

### Documentation
- Additional examples
- Video tutorials
- API usage guides
- Architecture deep-dives

### Testing
- Integration tests
- Performance tests
- Stress testing
- Device compatibility testing

## Commit Messages

Use conventional commits format:

```
type(scope): brief description

Detailed explanation if needed

Fixes #issue_number
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Formatting changes
- `refactor`: Code restructuring
- `test`: Test additions/changes
- `chore`: Build/tooling changes

**Examples:**
```
feat(omega): add GPU acceleration for LLM inference
fix(lambda): resolve mesh discovery timeout issue
docs(readme): add quick start guide
test(arbiter): add tests for decision fusion
```

## Code Review

All submissions require review. We use GitHub pull requests for this purpose.

**Review Criteria:**
- Code quality and style
- Test coverage
- Documentation completeness
- Performance impact
- Security considerations
- Breaking changes

## Security

If you discover a security vulnerability, please email the maintainers directly rather than opening a public issue.

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (see LICENSE file).

## Questions?

- Open an issue for bugs or feature requests
- Use Discussions for questions and ideas
- Check existing issues before opening new ones

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for making VENOM better! 🚀
