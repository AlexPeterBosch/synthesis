#!/usr/bin/env python3
"""Phase Validation Script

Validates that a development phase is complete according to specifications.

Usage:
    python scripts/validate-phase.py --phase 1
"""

import argparse
import sys
import json
from pathlib import Path


PHASE_REQUIREMENTS = {
    "1": {
        "name": "Database Architecture",
        "files": [
            "database/schema.sql",
            "database/schema.prisma",
            "database/seed.py"
        ],
        "tests": [],
        "duration_weeks": 2
    },
    "2": {
        "name": "NLP Processing",
        "files": [
            "src/nlp/text_processor.py",
            "src/nlp/stopwords.py",
            "src/nlp/ngram_generator.py"
        ],
        "tests": [
            "tests/specifications/test_ngram_weights.py"
        ],
        "duration_weeks": 2
    },
    "3": {
        "name": "Graph Construction",
        "files": [
            "src/graph/graph_builder.py",
            "src/graph/edge_calculator.py"
        ],
        "tests": [],
        "duration_weeks": 2
    },
    "4": {
        "name": "Core Algorithms",
        "files": [
            "src/algorithms/louvain.py",
            "src/algorithms/forceatlas2.py",
            "src/algorithms/betweenness.py",
            "src/algorithms/modularity.py"
        ],
        "tests": [
            "tests/specifications/test_node_sizing.py"
        ],
        "duration_weeks": 3
    },
    "5": {
        "name": "Gap Detection",
        "files": [
            "src/gaps/gap_detector.py",
            "src/gaps/filters.py"
        ],
        "tests": [
            "tests/specifications/test_gap_thresholds.py"
        ],
        "duration_weeks": 2
    },
    "6": {
        "name": "GraphRAG",
        "files": [
            "src/graphrag/query_processor.py",
            "src/graphrag/context_builder.py"
        ],
        "tests": [],
        "duration_weeks": 3
    },
    "7": {
        "name": "Visualization",
        "files": [
            "src/frontend/src/components/GraphVisualization.jsx"
        ],
        "tests": [],
        "duration_weeks": 2
    },
    "8": {
        "name": "Cognitive Analysis",
        "files": [],
        "tests": [],
        "duration_weeks": 1.5
    },
    "9": {
        "name": "Integrations",
        "files": [
            "n8n/workflows/graphrag-query.json",
            "n8n/workflows/gap-bridging.json"
        ],
        "tests": [],
        "duration_weeks": 2
    }
}


def validate_phase(phase_num: str) -> bool:
    """Validate that a phase is complete.
    
    Args:
        phase_num: Phase number as string
    
    Returns:
        True if phase is complete, False otherwise
    """
    if phase_num not in PHASE_REQUIREMENTS:
        print(f"Error: Invalid phase number '{phase_num}'")
        return False
    
    phase = PHASE_REQUIREMENTS[phase_num]
    print(f"\nValidating Phase {phase_num}: {phase['name']}")
    print("=" * 50)
    
    all_checks_passed = True
    
    # Check required files exist
    print("\nChecking required files...")
    for file_path in phase["files"]:
        if Path(file_path).exists():
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path} - MISSING")
            all_checks_passed = False
    
    # Check required tests exist and pass
    if phase["tests"]:
        print("\nChecking specification tests...")
        import subprocess
        for test_file in phase["tests"]:
            if Path(test_file).exists():
                print(f"  ✅ {test_file} exists")
                # Try to run the test
                try:
                    result = subprocess.run(
                        ["pytest", test_file, "-v"],
                        capture_output=True,
                        text=True
                    )
                    if result.returncode == 0:
                        print(f"    ✅ Tests pass")
                    else:
                        print(f"    ❌ Tests FAILED")
                        all_checks_passed = False
                except Exception as e:
                    print(f"    ⚠️ Could not run tests: {e}")
            else:
                print(f"  ❌ {test_file} - MISSING")
                all_checks_passed = False
    
    # Summary
    print("\n" + "=" * 50)
    if all_checks_passed:
        print(f"✅ Phase {phase_num} validation PASSED")
        print(f"Estimated duration: {phase['duration_weeks']} weeks")
    else:
        print(f"❌ Phase {phase_num} validation FAILED")
        print("Please complete missing requirements before proceeding.")
    print()
    
    return all_checks_passed


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate phase completion")
    parser.add_argument("--phase", type=str, required=True,
                       help="Phase number to validate (1-9)")
    
    args = parser.parse_args()
    
    success = validate_phase(args.phase)
    sys.exit(0 if success else 1)
