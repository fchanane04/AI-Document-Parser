from agents.extraction_agent import run_agent
import json

print("Testing: agent extracting from csv")
result = run_agent("Extract customers from sample_files/customers.csv and return the raw JSON data")
print(result)

print("\nTesting: agent extracting from pdf")
result = run_agent("Extract customers from sample_files/invoice.pdf and return the raw JSON data")


try:
    start = result.index('[')
    end = result.rindex(']') + 1
    json_str = result[start:end]
    data = json.loads(json_str)
    print(json.dumps(data, indent=2))
except Exception:
    print(result)