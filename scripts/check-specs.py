#!/usr/bin/env python3
"""Specification Checker

Validates that implementations follow exact specifications from research.

Usage:
    python scripts/check-specs.py
"""

import json
from pathlib import Path
import sys


def load_validation_rules():
    """Load validation rules from specs/validation-rules.json."""
    rules_path = Path("specs/validation-rules.json")
    if not rules_path.exists():
        print("Error: specs/validation-rules.json not found")
        return None
    
    with open(rules_path) as f:
        return json.load(f)


def check_parameters():
    """Check that specs/parameters.json has all required values."""
    params_path = Path("specs/parameters.json")
    if not params_path.exists():
        print("❌ specs/parameters.json not found")
        return False
    
    with open(params_path) as f:
        params = json.load(f)
    
    print("\nChecking parameters.json...")
    
    checks = [
        ("nlp.ngrams.pass_1.weight", 3, "Pass 1 bigram weight must be 3"),
        ("nlp.ngrams.pass_2.distance_1_weight", 2, "Pass 2 distance-1 weight must be 2"),
        ("nlp.ngrams.pass_2.distance_2_weight", 1, "Pass 2 distance-2 weight must be 1"),
        ("graph.edge_weights.normalization", False, "Edge weights must NOT be normalized"),
        ("algorithms.louvain.resolution", 1.0, "Louvain resolution must be 1.0"),
        ("algorithms.betweenness.normalized", True, "Betweenness must be normalized"),
        ("visualization.node_sizing.min_pixels", 5, "Min node size must be 5 pixels"),
        ("visualization.node_sizing.max_pixels", 40, "Max node size must be 40 pixels"),
        ("gaps.min_community_size", 3, "Min community size must be 3"),
        ("gaps.max_path_length", 6, "Max path length must be 6"),
        ("gaps.density_threshold", 0.1, "Density threshold must be 0.1"),
        ("gaps.max_gaps_returned", 3, "Must return max 3 gaps"),
    ]
    
    all_passed = True
    for path, expected, description in checks:
        keys = path.split(".")
        value = params
        try:
            for key in keys:
                value = value[key]
            
            if value == expected:
                print(f"  ✅ {description}")
            else:
                print(f"  ❌ {description} - Got {value}, expected {expected}")
                all_passed = False
        except (KeyError, TypeError):
            print(f"  ❌ {description} - Path not found: {path}")
            all_passed = False
    
    return all_passed


def check_stopwords():
    """Check that stopwords.json has correct count."""
    stopwords_path = Path("specs/stopwords.json")
    if not stopwords_path.exists():
        print("❌ specs/stopwords.json not found")
        return False
    
    with open(stopwords_path) as f:
        stopwords = json.load(f)
    
    count = len(stopwords.get("stopwords", []))
    
    print("\nChecking stopwords.json...")
    if count >= 180:
        print(f"  ✅ Stopwords count: {count} (>= 180 required)")
        return True
    else:
        print(f"  ❌ Stopwords count: {count} (180+ required)")
        return False


def check_critical_constants():
    """Check critical constants in source code."""
    print("\nChecking critical constants in source code...")
    
    checks = []
    
    # Check GapDetector constants
    gap_detector_path = Path("src/gaps/gap_detector.py")
    if gap_detector_path.exists():
        content = gap_detector_path.read_text()
        if "MIN_COMMUNITY_SIZE = 3" in content:
            checks.append(("✅", "GapDetector.MIN_COMMUNITY_SIZE = 3"))
        else:
            checks.append(("❌", "GapDetector.MIN_COMMUNITY_SIZE must be 3"))
        
        if "MAX_GAPS_RETURNED = 3" in content:
            checks.append(("✅", "GapDetector.MAX_GAPS_RETURNED = 3"))
        else:
            checks.append(("❌", "GapDetector.MAX_GAPS_RETURNED must be 3"))
    
    for status, message in checks:
        print(f"  {status} {message}")
    
    return all(status == "✅" for status, _ in checks)


def main():
    """Run all specification checks."""
    print("=" * 50)
    print("Synthesis Specification Checker")
    print("=" * 50)
    
    results = []
    
    # Load validation rules
    rules = load_validation_rules()
    if rules:
        print("✅ Loaded validation rules")
    else:
        print("❌ Failed to load validation rules")
        sys.exit(1)
    
    # Run checks
    results.append(("Parameters", check_parameters()))
    results.append(("Stopwords", check_stopwords()))
    results.append(("Constants", check_critical_constants()))
    
    # Summary
    print("\n" + "=" * 50)
    print("Summary:")
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status}: {name}")
    
    all_passed = all(passed for _, passed in results)
    
    if all_passed:
        print("\n✅ All specification checks passed!")
        sys.exit(0)
    else:
        print("\n❌ Some specification checks failed. Please review.")
        sys.exit(1)


if __name__ == "__main__":
    main()
