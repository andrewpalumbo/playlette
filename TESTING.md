# Test Coverage Documentation

## Overview
This document describes the test coverage for the playlette project.

## Coverage Summary
- **Total Coverage**: 100%
- **App Coverage**: 100%
- **Models Coverage**: 100%

## Test Files

### tests/test_routes.py
Tests for the Flask API endpoints (`/predict` and `/feedback`):

**Test Coverage:**
- ✅ POST /predict endpoint functionality
- ✅ CORS headers on all endpoints
- ✅ POST /feedback endpoint functionality
- ✅ Feedback data storage
- ✅ Color format validation (hex colors)
- ✅ Edge cases (zero values, max values)
- ✅ Empty and None data handling
- ✅ Multiple feedback entries

### tests/test_color_model.py
Tests for the ColorModel neural network:

**Test Coverage:**
- ✅ Model initialization
- ✅ Forward pass
- ✅ Output range validation (0-1 from Sigmoid)
- ✅ Batch processing
- ✅ Different input values
- ✅ Gradient flow
- ✅ Train/eval mode switching

## Running Tests

### Run all tests:
```bash
python -m pytest tests/ -v
```

### Run tests with coverage report:
```bash
python -m pytest tests/ --cov --cov-report=term-missing
```

### Generate HTML coverage report:
```bash
python -m pytest tests/ --cov --cov-report=html
# Open htmlcov/index.html in a browser
```

## Coverage Configuration

The `.coveragerc` file configures coverage measurement:
- Measures coverage for `app` and `models` packages
- Excludes test files, training scripts, and data processing scripts
- Requires 100% coverage threshold

## Excluded from Coverage

The following files are excluded as they are standalone scripts:
- `models/train_model.py` - Model training script
- `scripts/data_collection.py` - Spotify data collection
- `scripts/data_cleaning.py` - Data cleaning utilities
- `scripts/data_preparation.py` - Data preparation for training

These scripts are meant to be run manually and are not part of the runtime application.

## Test Requirements

All tests are written using Python's `unittest` framework and include:
- Unit tests for individual functions
- Integration tests for API endpoints
- Edge case testing
- CORS verification tests
