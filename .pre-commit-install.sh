#!/bin/bash

# Script pentru instalarea pre-commit hooks

echo "🔧 Installing pre-commit hooks..."

# Verifică dacă pre-commit este instalat
if ! command -v pre-commit &> /dev/null; then
    echo "❌ pre-commit nu este instalat. Instalează-l cu: pip install pre-commit"
    exit 1
fi

# Instalează pre-commit hooks
pre-commit install

echo "✅ Pre-commit hooks installed successfully!"
echo ""
echo "Pentru a rula manual verificările:"
echo "  pre-commit run --all-files"
echo ""
echo "Pentru a actualiza hooks:"
echo "  pre-commit autoupdate"
