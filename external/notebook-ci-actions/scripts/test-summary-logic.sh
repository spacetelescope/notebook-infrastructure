#!/bin/bash

# Quick test to simulate workflow summary output
# This helps verify the logic improvements

echo "🧪 Testing Enhanced Workflow Summary Logic"
echo "=========================================="

# Simulate different scenarios
echo ""
echo "Test 1: Successful notebook processing"
echo "-------------------------------------"

# Mock values for testing
NOTEBOOKS='["notebooks/examples/test.ipynb"]'
NOTEBOOK_COUNT=1
PROCESS_RESULT="success"
TRIGGER_EVENT="validate"

echo "Input: NOTEBOOKS='$NOTEBOOKS'"
echo "Parsed count: $NOTEBOOK_COUNT"
echo "Process result: $PROCESS_RESULT"
echo "Trigger event: $TRIGGER_EVENT"

# Test the logic
if [ "$NOTEBOOKS" = "null" ] || [ "$NOTEBOOKS" = "" ] || [ "$NOTEBOOKS" = "[]" ]; then
    NOTEBOOK_COUNT=0
else
    # Try to get count, fallback to 0 if parsing fails
    NOTEBOOK_COUNT=$(echo "$NOTEBOOKS" | jq -r 'length' 2>/dev/null)
    if [ "$NOTEBOOK_COUNT" = "null" ] || [ -z "$NOTEBOOK_COUNT" ]; then
        NOTEBOOK_COUNT=0
    fi
fi

echo ""
echo "Expected Summary Output:"
echo "========================"

if [ "$PROCESS_RESULT" = "success" ] || [ "$PROCESS_RESULT" = "failure" ]; then
    echo "**🚀 Notebook Processing Results**"
    
    if [ "$NOTEBOOK_COUNT" -gt 0 ]; then
        echo "- **Total Notebooks**: $NOTEBOOK_COUNT"
    else
        echo "- **Notebooks Processed**: Job completed (count unavailable)"
    fi
    
    case "$TRIGGER_EVENT" in
        "validate")
            echo "- **Operation**: Notebook validation"
            ;;
        "execute")
            echo "- **Operation**: Notebook execution"
            ;;
        "all")
            echo "- **Operation**: Full pipeline (validation, execution, security)"
            ;;
    esac
    
    if [ "$PROCESS_RESULT" = "success" ]; then
        echo "- **Status**: ✅ SUCCESS - All operations completed without errors"
    else
        echo "- **Status**: ❌ FAILURE - Check job logs for error details"
    fi
    
    if [ "$NOTEBOOK_COUNT" -gt 0 ] && [ "$NOTEBOOKS" != "[]" ]; then
        echo ""
        echo "**📄 Processed Notebooks:**"
        if [ "$NOTEBOOK_COUNT" = "1" ]; then
            SINGLE_NOTEBOOK=$(echo "$NOTEBOOKS" | jq -r '.[0]' 2>/dev/null)
            if [ "$SINGLE_NOTEBOOK" != "null" ] && [ -n "$SINGLE_NOTEBOOK" ]; then
                echo "- \`$SINGLE_NOTEBOOK\`"
            fi
        fi
    fi
else
    echo "**📋 No Processing Performed**"
fi

echo ""
echo "✅ Test completed - this should now show accurate results!"
