# Contributing to EV Charging Platform

Thank you for your interest in contributing to the EV Charging Platform! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and encourage diverse perspectives
- Focus on constructive feedback
- Maintain professional communication

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in Issues
2. If not, create a new issue with:
   - Clear, descriptive title
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - Environment details (OS, versions, etc.)

### Suggesting Features

1. Check existing feature requests
2. Create a new issue with:
   - Clear description of the feature
   - Use cases and benefits
   - Potential implementation approach

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make your changes**
   - Follow the code style guidelines
   - Add tests for new features
   - Update documentation

4. **Commit your changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```
   
   Commit message format:
   - `feat:` New feature
   - `fix:` Bug fix
   - `docs:` Documentation changes
   - `style:` Code style changes
   - `refactor:` Code refactoring
   - `test:` Test additions/changes
   - `chore:` Build/config changes

5. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```

6. **Open a Pull Request**
   - Provide clear description
   - Reference related issues
   - Include screenshots for UI changes

## Development Guidelines

### Code Style

#### Python (Backend)
- Follow PEP 8 style guide
- Use type hints
- Maximum line length: 100 characters
- Use meaningful variable names
- Add docstrings to functions

```python
def calculate_distance(
    origin: Tuple[float, float],
    destination: Tuple[float, float]
) -> float:
    """
    Calculate distance between two coordinates.
    
    Args:
        origin: (latitude, longitude) tuple
        destination: (latitude, longitude) tuple
        
    Returns:
        Distance in kilometers
    """
    # Implementation
    pass
```

#### JavaScript/React Native (Mobile)
- Use ESLint configuration
- Prefer functional components with hooks
- Use meaningful component names
- Add PropTypes or TypeScript types

```javascript
// Good
const StationCard = ({ station, onPress }) => {
  // Component logic
};

// Better with PropTypes
StationCard.propTypes = {
  station: PropTypes.object.isRequired,
  onPress: PropTypes.func.isRequired,
};
```

### Testing

#### Backend Tests
```bash
cd backend
pytest tests/
```

#### Mobile Tests
```bash
cd mobile
npm test
```

### Documentation

- Update README for significant changes
- Add API documentation for new endpoints
- Include inline comments for complex logic
- Update SETUP.md for new dependencies

## Project Structure

```
ev-charging-platform/
├── backend/          # FastAPI backend
├── mobile/           # React Native app
├── web/             # Web dashboard (future)
├── docs/            # Documentation
└── scripts/         # Utility scripts
```

## Getting Help

- Check documentation in `/docs`
- Search existing issues
- Ask questions in discussions
- Join our community chat (link)

## Recognition

Contributors will be:
- Listed in README
- Mentioned in release notes
- Invited to contributor discussions

Thank you for contributing! 🎉
