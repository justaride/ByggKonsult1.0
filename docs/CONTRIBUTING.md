# 🤝 Contributing to Oslo Planning Documents - Premium

Thank you for your interest in contributing to the Oslo Planning Documents Premium project! This guide will help you get started.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contributing Guidelines](#contributing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)
- [Documentation](#documentation)
- [Testing](#testing)

## 📜 Code of Conduct

This project follows a professional code of conduct:

### Our Standards
- **Respectful**: Be respectful and inclusive
- **Professional**: Maintain professional communication
- **Collaborative**: Work together constructively
- **Quality**: Strive for high-quality contributions

### Unacceptable Behavior
- Personal attacks or harassment
- Discrimination of any kind
- Spam or off-topic discussions
- Sharing private information without permission

## 🚀 Getting Started

### Prerequisites
- Python 3.7+ (Recommended: 3.9+)
- Git
- Code editor (VS Code, PyCharm, etc.)
- Basic knowledge of Streamlit and Plotly

### Fork and Clone
1. **Fork** the repository on GitHub
2. **Clone** your fork:
   ```bash
   git clone https://github.com/yourusername/oslo-planning-premium.git
   cd oslo-planning-premium
   ```

## 🛠️ Development Setup

### 1. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
# Production dependencies
pip install -r requirements.txt

# Development dependencies
pip install pytest black flake8 mypy jupyter
```

### 3. Run Application
```bash
# Start in development mode
streamlit run oslo_planning_premium.py --server.runOnSave true
```

### 4. Verify Setup
```bash
# Run tests
python -m pytest tests/

# Check code quality
black --check .
flake8 .
mypy oslo_planning_premium.py
```

## 🎯 Contributing Guidelines

### Types of Contributions

#### 🐛 Bug Fixes
- Fix functionality issues
- Improve error handling
- Resolve performance problems

#### ✨ New Features
- Add new visualization capabilities
- Enhance user interface
- Implement additional analytics

#### 📚 Documentation
- Improve README files
- Add code comments
- Create user guides

#### 🧪 Testing
- Add unit tests
- Create integration tests
- Improve test coverage

#### 🎨 UI/UX Improvements
- Enhance visual design
- Improve user experience
- Add responsive features

### Contribution Areas

#### High Priority
- **Data Quality**: Improve document verification
- **Performance**: Optimize loading and queries
- **Mobile UX**: Enhance mobile experience
- **Accessibility**: Improve accessibility features

#### Medium Priority
- **Visualizations**: Add new chart types
- **Export Features**: Enhance data export options
- **Search**: Improve search functionality
- **Documentation**: Expand user guides

#### Nice to Have
- **Themes**: Add customizable themes
- **Localization**: Add language support
- **API**: Create REST API endpoints
- **Caching**: Implement advanced caching

## 🔄 Pull Request Process

### Before You Start
1. **Check existing issues** and PRs
2. **Create an issue** to discuss major changes
3. **Assign yourself** to the issue

### Development Process
1. **Create feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make changes** following coding standards
3. **Write tests** for new functionality
4. **Update documentation** as needed
5. **Test thoroughly** before submitting

### Code Quality Standards
```bash
# Format code
black oslo_planning_premium.py oslo_premium_enhancements.py

# Check style
flake8 .

# Type checking
mypy oslo_planning_premium.py

# Run tests
python -m pytest tests/ -v
```

### Commit Message Format
```
type(scope): description

- feat: new feature
- fix: bug fix
- docs: documentation
- style: formatting
- refactor: code restructuring
- test: adding tests
- chore: maintenance

Examples:
feat(ui): add interactive document cards
fix(database): resolve duplicate detection issue
docs(readme): update installation instructions
```

### Pull Request Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
- [ ] Tests pass locally
- [ ] New tests added (if applicable)
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or clearly documented)

## Screenshots (if applicable)
Add screenshots for UI changes
```

### Review Process
1. **Automated checks** must pass
2. **Code review** by maintainers
3. **Testing** on different environments
4. **Documentation** review
5. **Approval and merge**

## 🐛 Issue Reporting

### Bug Reports
Use the bug report template:
```markdown
**Bug Description**
Clear description of the bug

**Steps to Reproduce**
1. Go to '...'
2. Click on '...'
3. See error

**Expected Behavior**
What should happen

**Screenshots**
If applicable, add screenshots

**Environment**
- OS: [e.g. Windows 10]
- Python: [e.g. 3.9.0]
- Browser: [e.g. Chrome 91]

**Additional Context**
Any other relevant information
```

### Feature Requests
Use the feature request template:
```markdown
**Feature Description**
Clear description of the feature

**Problem Statement**
What problem does this solve?

**Proposed Solution**
How should this be implemented?

**Alternatives Considered**
Other solutions you considered

**Additional Context**
Mockups, examples, etc.
```

## 📚 Documentation

### Documentation Standards
- **Clear and concise** writing
- **Code examples** for technical docs
- **Screenshots** for UI features
- **Step-by-step** instructions

### Documentation Types
- **User guides**: How to use features
- **API docs**: Function/class documentation
- **Developer docs**: How to contribute
- **Deployment guides**: How to deploy

### Writing Guidelines
```markdown
# Use clear headings
## Organize with subheadings
### Use appropriate hierarchy

- Use bullet points for lists
- `Code blocks` for commands
- **Bold** for emphasis
- *Italic* for field names

```python
# Code examples with syntax highlighting
def example_function():
    return "Clear, commented code"
```
```

## 🧪 Testing

### Test Structure
```
tests/
├── test_database.py          # Database functionality
├── test_ui_components.py     # UI component testing
├── test_verification.py      # Verification system
├── test_search.py           # Search functionality
└── fixtures/                # Test data
```

### Writing Tests
```python
import pytest
from oslo_planning_premium import OsloPlanningPremium

def test_database_initialization():
    """Test database initializes correctly."""
    system = OsloPlanningPremium(":memory:")
    docs = system.get_all_documents()
    assert len(docs) > 0
    assert docs['title'].duplicated().sum() == 0

def test_search_functionality():
    """Test search returns relevant results."""
    system = OsloPlanningPremium(":memory:")
    results = system.search_documents("kommuneplan")
    assert len(results) > 0
    assert "kommuneplan" in results.iloc[0]['title'].lower()
```

### Test Coverage
- **Aim for 80%+ coverage**
- **Test critical paths** first
- **Include edge cases**
- **Test error handling**

### Running Tests
```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=oslo_planning_premium

# Run specific test
python -m pytest tests/test_database.py::test_database_initialization

# Run with verbose output
python -m pytest tests/ -v
```

## 🎨 UI/UX Guidelines

### Design Principles
- **Oslo Kommune Branding**: Use official colors and styling
- **Professional Appearance**: Clean, modern design
- **Responsive Design**: Works on all screen sizes
- **Accessibility**: WCAG compliance
- **Performance**: Fast loading and interaction

### Color Palette
```python
OSLO_COLORS = {
    'primary': '#1B4F72',      # Oslo blue
    'secondary': '#2E86AB',    # Light blue
    'accent': '#A23B72',       # Purple accent
    'success': '#148F77',      # Green
    'warning': '#F39C12',      # Orange
    'danger': '#E74C3C',       # Red
}
```

### Component Standards
- **Consistent spacing** using 0.5rem increments
- **Hover effects** for interactive elements
- **Loading states** for data operations
- **Error handling** with user-friendly messages

## 📞 Getting Help

### Resources
- **Documentation**: Check docs/ directory
- **Examples**: Look at existing code
- **Issues**: Search existing issues
- **Community**: Streamlit community

### Communication Channels
- **GitHub Issues**: For bugs and features
- **GitHub Discussions**: For questions and ideas
- **Pull Requests**: For code review

### Maintainer Response Time
- **Issues**: Within 48 hours
- **Pull Requests**: Within 72 hours
- **Security Issues**: Within 24 hours

## 🏆 Recognition

### Contributors
All contributors will be:
- **Listed** in CONTRIBUTORS.md
- **Credited** in release notes
- **Acknowledged** in documentation

### Contribution Types
We recognize all types of contributions:
- Code contributions
- Documentation improvements
- Bug reports and testing
- Feature suggestions
- Community support

---

**Thank you for contributing to Oslo Planning Documents - Premium!**

Your contributions help make municipal planning more accessible and efficient for everyone.

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.