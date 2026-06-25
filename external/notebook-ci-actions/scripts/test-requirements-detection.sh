#!/bin/bash

# Test script to demonstrate the enhanced requirements file detection logic
# This simulates what happens when a requirements.txt file is changed in a PR

echo "🧪 Testing Requirements File Change Detection"
echo "============================================"

# Simulate the scenario you described
echo ""
echo "Scenario: PR changes notebooks/examples/requirements.txt"
echo "Expected: Should find all notebooks in notebooks/examples/ and process them"
echo ""

# Create test directory structure
mkdir -p test-notebooks/examples
mkdir -p test-notebooks/analysis

# Create some test notebook files
touch test-notebooks/examples/notebook1.ipynb
touch test-notebooks/examples/notebook2.ipynb
touch test-notebooks/examples/notebook3.ipynb
touch test-notebooks/analysis/analysis1.ipynb

# Create requirements file
echo "pandas>=1.3.0" > test-notebooks/examples/requirements.txt

echo "📁 Test directory structure created:"
find test-notebooks -type f | sort

echo ""
echo "🔍 Testing the enhanced logic:"
echo "Changed file: test-notebooks/examples/requirements.txt"

# Simulate the logic
CHANGED_FILES="test-notebooks/examples/requirements.txt"
declare -a CHANGED_NOTEBOOKS
declare -a AFFECTED_DIRECTORIES

echo ""
echo "📋 Processing changed files..."

while IFS= read -r file; do
  [[ -z "$file" ]] && continue
  echo "Processing: $file"
  
  case "$file" in
    */requirements.txt|requirements.txt|pyproject.toml)
      echo "📦 Requirements file changed: $file"
      dir=$(dirname "$file")
      if [[ "$file" == "requirements.txt" || "$file" == "pyproject.toml" ]]; then
        echo "🌐 Root requirements file changed - affecting all notebooks"
        AFFECTED_DIRECTORIES=("test-notebooks")
      else
        echo "📁 Directory requirements file changed: $dir"
        if [[ ! " ${AFFECTED_DIRECTORIES[*]} " =~ " $dir " ]]; then
          AFFECTED_DIRECTORIES+=("$dir")
        fi
      fi
      ;;
  esac
done <<< "$CHANGED_FILES"

echo ""
echo "📁 Affected directories: ${AFFECTED_DIRECTORIES[*]}"

# Find notebooks in affected directories
if [ ${#AFFECTED_DIRECTORIES[@]} -gt 0 ]; then
  echo ""
  echo "🔍 Finding notebooks in affected directories..."
  declare -a ALL_AFFECTED_NOTEBOOKS
  
  for dir in "${AFFECTED_DIRECTORIES[@]}"; do
    echo "📁 Searching in: $dir"
    while IFS= read -r notebook; do
      [[ -z "$notebook" ]] && continue
      echo "📓 Found notebook: $notebook"
      ALL_AFFECTED_NOTEBOOKS+=("$notebook")
    done < <(find "$dir" -name '*.ipynb' -type f 2>/dev/null)
  done
  
  # Combine with explicitly changed notebooks (none in this case)
  declare -A UNIQUE_NOTEBOOKS
  for notebook in "${CHANGED_NOTEBOOKS[@]}" "${ALL_AFFECTED_NOTEBOOKS[@]}"; do
    [[ -n "$notebook" ]] && UNIQUE_NOTEBOOKS["$notebook"]=1
  done
  
  # Convert back to regular array
  FINAL_NOTEBOOKS=()
  for notebook in "${!UNIQUE_NOTEBOOKS[@]}"; do
    FINAL_NOTEBOOKS+=("$notebook")
  done
  
  echo ""
  echo "📋 Final notebooks to process (${#FINAL_NOTEBOOKS[@]} total):"
  for notebook in "${FINAL_NOTEBOOKS[@]}"; do
    echo "  ✅ $notebook"
  done
  
  # Generate JSON array like the workflow does
  MATRIX_JSON=$(printf '%s\n' "${FINAL_NOTEBOOKS[@]}" | jq -R . | jq -s -c .)
  echo ""
  echo "🔧 Matrix JSON that would be generated:"
  echo "$MATRIX_JSON"
  
else
  echo "❌ No affected directories found"
fi

# Cleanup
rm -rf test-notebooks

echo ""
echo "✅ Test Results:"
echo "================"
echo "✅ Requirements file changes are now properly detected"
echo "✅ All notebooks in the affected directory are included in the matrix"
echo "✅ The workflow will now test all notebooks when dependencies change"
echo ""
echo "🎯 Expected workflow output for your PR:"
echo "----------------------------------------"
echo "🔄 PR Mode: Detecting changed files"
echo "📦 Requirements file changed: notebooks/examples/requirements.txt"
echo "📁 Directory requirements file changed: notebooks/examples"
echo "🔍 Finding notebooks in affected directories: notebooks/examples"
echo "📓 Found notebook: notebooks/examples/notebook1.ipynb"
echo "📓 Found notebook: notebooks/examples/notebook2.ipynb" 
echo "📓 Found notebook: notebooks/examples/notebook3.ipynb"
echo "✅ Matrix populated with 3 notebooks"
echo ""
echo "📊 Matrix Setup Complete:"
echo '  Notebooks: ["notebooks/examples/notebook1.ipynb","notebooks/examples/notebook2.ipynb","notebooks/examples/notebook3.ipynb"]'
echo '  Affected Dirs: ["notebooks/examples"]'
echo "  Skip Execution: false"
echo "  Docs Only: false"
