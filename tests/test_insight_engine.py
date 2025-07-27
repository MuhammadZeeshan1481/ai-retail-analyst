from backend.insight_engine import InsightEngine

engine = InsightEngine()

query = "Which region had the highest total revenue?"
result = engine.generate_answer(query)

print("\n Answer:")
print(result["answer"])

print("\n Sources:")
for src in result["sources"]:
    print("-", src)
