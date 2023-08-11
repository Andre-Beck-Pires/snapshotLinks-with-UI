import re

url = "https://www3.pagefreezer.com/admin/content.html?profile=706&snapshot=12174824"

# Define the regular expression pattern
pattern = r"snapshot=(\d+)"

# Use re.search to find the match
match = re.search(pattern, url)

if match:
    captured_text = match.group(1)
    print("Captured text:", captured_text)
else:
    print("Pattern not found")
