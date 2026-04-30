"""
Evaluation Script for Billing Analysis Assistant
Runs all evaluation questions against uploaded documents and measures:
- Keyword hit rate (accuracy proxy)
- Response time per query
- Average response time
- Total cost estimate (Groq free tier)
"""
import sys
import os
import json
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))

from document_loader import load_document
from text_processor import process_documents
from vector_store import create_vector_store
from rag_chain import get_qa_chain, ask_question


def load_eval_questions():
    """Load evaluation Q&A dataset."""
    eval_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "eval_questions.json")
    with open(eval_path, "r") as f:
        return json.loads(f.read())


def calculate_keyword_score(answer, expected_keywords):
    """
    Score answer based on expected keyword presence.
    Returns: (score 0.0-1.0, matched_keywords, missed_keywords)
    """
    answer_lower = answer.lower()
    matched = [kw for kw in expected_keywords if kw.lower() in answer_lower]
    missed = [kw for kw in expected_keywords if kw.lower() not in answer_lower]
    score = len(matched) / len(expected_keywords) if expected_keywords else 0
    return score, matched, missed


def run_evaluation(test_file_path):
    """
    Run full evaluation pipeline:
    1. Load and process a test document
    2. Run all eval questions
    3. Measure accuracy and response times
    """
    print("=" * 60)
    print("BILLING ANALYSIS ASSISTANT — EVALUATION")
    print("=" * 60)

    # Step 1: Load test document
    print(f"\n📄 Loading test document: {test_file_path}")
    start = time.time()

    # Create a simple file-like object for local files
    class LocalFile:
        def __init__(self, path):
            self.name = os.path.basename(path)
            self._file = open(path, "rb")

        def read(self):
            return self._file.read()

        def seek(self, pos, whence=0):
            return self._file.seek(pos, whence)

        def tell(self):
            return self._file.tell()

        def close(self):
            self._file.close()

    file_obj = LocalFile(test_file_path)
    raw_text = load_document(file_obj)
    file_obj.close()

    if raw_text.startswith("Error"):
        print(f"❌ Failed to load document: {raw_text}")
        return

    load_time = time.time() - start
    print(f"   ✅ Extracted {len(raw_text)} chars in {load_time:.2f}s")

    # Step 2: Process and index
    print("\n✂️ Chunking and embedding...")
    start = time.time()
    chunks = process_documents(raw_text)
    vector_store = create_vector_store(chunks)
    index_time = time.time() - start
    print(f"   ✅ Created {len(chunks)} chunks, indexed in {index_time:.2f}s")

    # Step 3: Create QA chain
    print("\n🔗 Building QA chain...")
    qa_chain = get_qa_chain(vector_store)

    # Step 4: Run evaluation questions
    questions = load_eval_questions()
    print(f"\n🧪 Running {len(questions)} evaluation questions...\n")
    print("-" * 60)

    results = []
    total_time = 0

    for q in questions:
        question = q["question"]
        expected = q["expected_keywords"]
        category = q["category"]

        # Time the query
        start = time.time()
        try:
            response = ask_question(qa_chain, question)
            answer = response["result"]
            elapsed = time.time() - start
            error = None
        except Exception as e:
            answer = ""
            elapsed = time.time() - start
            error = str(e)

        total_time += elapsed

        # Score
        score, matched, missed = calculate_keyword_score(answer, expected)

        results.append({
            "id": q["id"],
            "question": question,
            "category": category,
            "score": score,
            "response_time": elapsed,
            "matched_keywords": matched,
            "missed_keywords": missed,
            "answer_preview": answer[:150] if answer else "ERROR",
            "error": error,
        })

        # Print result
        status = "✅" if score >= 0.5 else "⚠️" if score > 0 else "❌"
        print(f"  {status} Q{q['id']}: {question}")
        print(f"     Score: {score:.0%} | Time: {elapsed:.2f}s | Keywords: {len(matched)}/{len(expected)}")
        if error:
            print(f"     ERROR: {error}")
        print()

    # Step 5: Summary
    print("=" * 60)
    print("EVALUATION SUMMARY")
    print("=" * 60)

    avg_score = sum(r["score"] for r in results) / len(results)
    avg_time = total_time / len(results)
    pass_count = sum(1 for r in results if r["score"] >= 0.5)

    print(f"\n  📊 Overall Accuracy:    {avg_score:.0%}")
    print(f"  ✅ Questions Passed:    {pass_count}/{len(results)} (≥50% keyword match)")
    print(f"  ⏱️  Avg Response Time:  {avg_time:.2f}s")
    print(f"  ⏱️  Total Time:         {total_time:.2f}s")
    print(f"  📄 Document Load Time:  {load_time:.2f}s")
    print(f"  🧮 Index Build Time:    {index_time:.2f}s")
    print(f"  💰 Estimated Cost:      $0.00 (Groq free tier)")

    # Category breakdown
    print(f"\n  📋 Category Breakdown:")
    categories = {}
    for r in results:
        cat = r["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(r["score"])

    for cat, scores in sorted(categories.items()):
        cat_avg = sum(scores) / len(scores)
        print(f"     {cat}: {cat_avg:.0%} ({len(scores)} questions)")

    # Save results
    results_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "eval_results.json")
    with open(results_path, "w") as f:
        json.dump({
            "summary": {
                "overall_accuracy": round(avg_score, 3),
                "pass_rate": f"{pass_count}/{len(results)}",
                "avg_response_time_sec": round(avg_time, 3),
                "total_time_sec": round(total_time, 3),
                "document_load_time_sec": round(load_time, 3),
                "index_build_time_sec": round(index_time, 3),
                "cost": "$0.00",
            },
            "category_scores": {cat: round(sum(s)/len(s), 3) for cat, s in categories.items()},
            "results": results,
        }, f, indent=2)

    print(f"\n  💾 Results saved to: {results_path}")
    print("=" * 60)


if __name__ == "__main__":
    # Default: use sample bill
    import argparse
    parser = argparse.ArgumentParser(description="Evaluate Billing Analysis Assistant")
    parser.add_argument("--file", type=str,
                        default=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                             "..", "data", "sample_bills", "batch1-0001.jpg"),
                        help="Path to test billing document")
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"❌ File not found: {args.file}")
        print("Usage: python run_evaluation.py --file path/to/bill.pdf")
        sys.exit(1)

    # Need streamlit secrets for API key
    import streamlit as st
    run_evaluation(args.file)
