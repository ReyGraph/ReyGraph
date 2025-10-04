import json
import os

# Paths
books_file = "books.json"
readme_file = "README.md"

# Read books
with open(books_file, "r", encoding="utf-8") as f:
    books = json.load(f)

# Securely set added_by to PR author
pr_author = os.environ.get("GITHUB_ACTOR", "unknown")
for book in books:
    book["added_by"] = pr_author

# Generate Markdown for README
books_md = "<details>\n<summary>Expand to see books</summary>\n\n"
for book in books:
    books_md += f"- **{book['title']}** — {book['author']}  _(added by @{book['added_by']})_\n"
books_md += "\n</details>"

# Read README
with open(readme_file, "r", encoding="utf-8") as f:
    readme = f.read()

# Replace between markers
start_marker = "<!-- BOOKS-START -->"
end_marker = "<!-- BOOKS-END -->"

if start_marker not in readme or end_marker not in readme:
    raise ValueError("README missing book markers")

start_idx = readme.index(start_marker) + len(start_marker)
end_idx = readme.index(end_marker)

new_readme = readme[:start_idx] + "\n\n" + books_md + "\n\n" + readme[end_idx:]

# Write README
with open(readme_file, "w", encoding="utf-8") as f:
    f.write(new_readme)

print("✅ Books section updated successfully!")
