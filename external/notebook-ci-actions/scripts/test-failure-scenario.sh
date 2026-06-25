#!/bin/bash

# Test scenario: 3 notebooks, 1 fails execution
# This simulates the enhanced workflow summary output

echo "🧪 Testing Workflow Summary: 3 Notebooks, 1 Failure Scenario"
echo "============================================================="

# Mock values for this test scenario
NOTEBOOKS='["notebooks/examples/test1.ipynb", "notebooks/examples/test2.ipynb", "notebooks/examples/test3.ipynb"]'
NOTEBOOK_COUNT=3
PROCESS_RESULT="failure"  # One or more notebooks failed
TRIGGER_EVENT="execute"
AFFECTED_DIRS='["notebooks/examples"]'

echo ""
echo "📊 Simulated Workflow Summary Output"
echo "===================================="
echo ""

# Generate the summary as it would appear
echo "## 📊 Unified Notebook CI/CD Summary"
echo "*Generated: $(date -u +'%Y-%m-%d %H:%M:%S UTC')*"
echo ""

echo "### 🔧 Configuration"
echo "- **Execution Mode**: on-demand"
echo "- **Trigger Event**: $TRIGGER_EVENT"
echo "- **Python Version**: 3.11"
echo ""

echo "### 📊 Job Results"
echo "| Job | Status | Duration |"
echo "|-----|--------|----------|"
echo "| Matrix Setup | success | - |"
echo "| Notebook Processing | $PROCESS_RESULT | - |"
echo "| Documentation Build | skipped | - |"
echo "| Deprecation Management | skipped | - |"
echo ""

echo "### 📝 Execution Details"

# Show affected directories
echo "**📁 Affected Directories:**"
echo "$AFFECTED_DIRS" | jq -r '.[]' | while read -r dir; do
    echo "- \`$dir\`"
done
echo ""

# Show processing results
echo "**🚀 Notebook Processing Results**"
echo "- **Total Notebooks**: $NOTEBOOK_COUNT"

case "$TRIGGER_EVENT" in
    "execute")
        echo "- **Operation**: Notebook execution"
        ;;
    "validate")
        echo "- **Operation**: Notebook validation"
        ;;
    "all")
        echo "- **Operation**: Full pipeline (validation, execution, security)"
        ;;
esac

if [ "$PROCESS_RESULT" = "success" ]; then
    echo "- **Status**: ✅ SUCCESS - All operations completed without errors"
elif [ "$PROCESS_RESULT" = "failure" ]; then
    echo "- **Status**: ❌ FAILURE - One or more notebooks failed processing"
    echo "- **Action Required**: Check the 'Notebook Processing' job logs for specific error details"
    echo "- **Common Causes**: Execution errors, missing dependencies, security issues, or environment problems"
fi

echo ""
echo "**📄 Processed Notebooks:**"
echo "$NOTEBOOKS" | jq -r '.[]' | while read -r notebook; do
    echo "- \`$notebook\`"
done

echo ""
echo "### 🚨 Error Information"
echo "One or more jobs failed. Check the following:"
echo "1. **Job Logs**: Click on the failed job(s) above to see detailed error messages"
echo "2. **Common Issues**:"
echo "   - Missing dependencies in requirements.txt"
echo "   - Notebook execution errors (infinite loops, missing data, etc.)"
echo "   - Environment setup issues"
echo "   - Security vulnerabilities detected"
echo "3. **Debugging**: Use on-demand mode to test specific notebooks individually"

echo ""
echo "## ⚠️ Workflow completed with partial success"
echo "*Some jobs succeeded but 1 job(s) failed - see error details above*"

echo ""
echo ""
echo "🔍 Additional Context for Failed Execution Scenario:"
echo "=================================================="
echo ""
echo "In the actual GitHub Actions logs, you would see matrix job results like:"
echo ""
echo "Matrix Job Results:"
echo "- notebooks/examples/test1.ipynb: ✅ SUCCESS"
echo "- notebooks/examples/test2.ipynb: ❌ FAILURE (execution error)"  
echo "- notebooks/examples/test3.ipynb: ✅ SUCCESS"
echo ""
echo "The failed notebook (test2.ipynb) would have detailed error logs showing:"
echo "- The specific cell that failed"
echo "- The error message (e.g., ImportError, RuntimeError, etc.)"
echo "- Stack trace for debugging"
echo ""
echo "Users can then:"
echo "1. Click on the failed matrix job to see detailed logs"
echo "2. Run 'execute-single' on just the failed notebook to debug"
echo "3. Fix the issue and re-run the workflow"
