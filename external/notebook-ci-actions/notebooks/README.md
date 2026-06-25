# Test Notebooks for CI/CD Pipeline

This directory contains test notebooks for validating the unified notebook CI/CD system.

## 📁 Directory Structure

```
notebooks/
├── examples/
│   └── basic-validation-test.ipynb    # Basic functionality test
├── testing/
│   ├── performance-test.ipynb         # Performance benchmarking
│   └── security-test.ipynb           # Security validation
├── requirements.txt                   # Dependencies for all notebooks
└── README.md                         # This file
```

## 🎯 Test Notebooks Description

### examples/basic-validation-test.ipynb
- **Purpose**: Basic functionality validation
- **Features**: 
  - Library imports (numpy, pandas, matplotlib)
  - Data creation and manipulation
  - Simple plotting
  - Should execute without errors

### testing/performance-test.ipynb
- **Purpose**: Performance benchmarking and resource testing
- **Features**:
  - Large array operations
  - DataFrame operations
  - Memory usage monitoring
  - Execution time measurement
  - Performance optimization insights

### testing/security-test.ipynb
- **Purpose**: Security validation and safe coding practices
- **Features**:
  - Safe file operations
  - Secure random generation
  - Cryptographic hashing
  - Input validation
  - Environment variable handling
  - Should pass bandit security scanning

## 🧪 Local Testing Commands

You can test these notebooks locally using the provided testing script:

### Test All Notebooks
```bash
# Validate all notebooks
./scripts/test-on-demand-modes.sh validate-all

# Execute all notebooks
./scripts/test-on-demand-modes.sh execute-all

# Run security scan
./scripts/test-on-demand-modes.sh security-scan-all

# Full pipeline test
./scripts/test-on-demand-modes.sh full-pipeline-all
```

### Test Individual Notebooks
```bash
# Test basic validation notebook
./scripts/test-on-demand-modes.sh validate-single notebooks/examples/basic-validation-test.ipynb
./scripts/test-on-demand-modes.sh execute-single notebooks/examples/basic-validation-test.ipynb

# Test performance notebook
./scripts/test-on-demand-modes.sh execute-single notebooks/testing/performance-test.ipynb

# Test security notebook
./scripts/test-on-demand-modes.sh validate-single notebooks/testing/security-test.ipynb
```

### Performance Testing
```bash
# Run performance benchmark
./scripts/test-on-demand-modes.sh performance-test

# With debug logging
ENABLE_DEBUG=true ./scripts/test-on-demand-modes.sh performance-test
```

### HTML Documentation Build
```bash
# Test documentation building
./scripts/test-on-demand-modes.sh build-html-only
```

## 🔧 Environment Setup

### Install Dependencies
```bash
# Install notebook dependencies
pip install -r notebooks/requirements.txt

# Install testing dependencies
pip install pytest nbval jupyter bandit
```

### Conda Environment (Optional)
```bash
# Create test environment
conda create -n notebook-test python=3.11
conda activate notebook-test
pip install -r notebooks/requirements.txt
```

## 📊 Expected Results

### Validation Tests
- All notebooks should pass syntax validation
- No JSON parsing errors
- Valid notebook structure

### Execution Tests
- All code cells should execute successfully
- No runtime errors
- Proper output generation

### Security Tests
- Should pass bandit security scanning
- No hardcoded secrets or credentials
- Safe coding practices demonstrated

### Performance Tests
- Execution time benchmarks
- Memory usage monitoring
- Optimization recommendations

## 🎭 Testing with Act (GitHub Actions Simulation)

```bash
# Install Act (if not already installed)
brew install act  # macOS
# or see: https://github.com/nektos/act

# Test with Act
TEST_METHOD=act ./scripts/test-on-demand-modes.sh validate-all
TEST_METHOD=act ./scripts/test-on-demand-modes.sh execute-single notebooks/examples/basic-validation-test.ipynb
```

## 🐛 Troubleshooting

### Missing Dependencies
```bash
pip install numpy pandas matplotlib psutil
```

### Notebook Execution Issues
```bash
# Clear notebook outputs
jupyter nbconvert --clear-output notebooks/**/*.ipynb

# Test individual notebook
jupyter nbconvert --to notebook --execute notebooks/examples/basic-validation-test.ipynb
```

### Security Scan Issues
```bash
# Run bandit manually
bandit -r notebooks/
```

## 🚀 Integration with CI/CD

These notebooks are designed to work with the unified notebook CI/CD system:

1. **PR Validation**: Use `validate-all` mode
2. **Performance Testing**: Use `performance-test` mode  
3. **Security Scanning**: Use `security-scan-all` mode
4. **Full Pipeline**: Use `full-pipeline-all` mode

The notebooks demonstrate real-world scenarios and can be used as templates for other repositories.
