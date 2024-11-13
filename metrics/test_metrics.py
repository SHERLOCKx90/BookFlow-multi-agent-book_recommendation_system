# test_metrics.py

# test_metrics.py
import sys
import os

# Dynamically add the project root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from metrics.adaptability_metrics import test_adaptability
from metrics.relevance_metrics import test_relevance

def main():
    print("Testing Adaptability Metrics...")
    adaptability_results = test_adaptability()
    for metric, value in adaptability_results.items():
        print(f"{metric}: {value}")

    print("\nTesting Relevance Metrics...")
    relevance_results = test_relevance()
    for metric, value in relevance_results.items():
        print(f"{metric}: {value}")

if __name__ == "__main__":
    main()


from adaptability_metrics import test_adaptability
from relevance_metrics import test_relevance


def main():
    print("Testing Adaptability Metrics...")
    adaptability_results = test_adaptability()
    for metric, value in adaptability_results.items():
        print(f"{metric}: {value}")

    print("\nTesting Relevance Metrics...")
    relevance_results = test_relevance()
    for metric, value in relevance_results.items():
        print(f"{metric}: {value}")

if __name__ == "__main__":
    main()
