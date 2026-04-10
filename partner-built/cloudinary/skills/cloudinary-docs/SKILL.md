---
name: cloudinary-docs
description: This skill is used to look up how to do something in Cloudinary using the Cloudinary LLMs.txt and the sanitized markdown files.
---

# My Skill

Helps developers to integrate Cloudinary into their applications by providing documentation and code examples retrieved directly from the optimized .md files in the Cloudinary documentation rather than having parse the HTML pages.


## When to Use

- Use this skill when a user asks a question about Cloudinary.
- Use this skill when an agent is trying to integrate Cloudinary into their application.

## Instructions

When answering questions about Cloudinary:

1. **First, get the documentation index using **llms.txt** with the llms.txt URL - https://cloudinary.com/documentation/llms.txt
2. **Analyze the llms.txt content** to understand what documentation pages are available
3. **Reflect on the user's question** and identify which specific documentation URLs would be most relevant
4. **Navigate** to the specific relevant documentation URLs from the llms.txt index (you can make multiple calls).
5. **Use the fetched documentation** to provide a comprehensive, accurate answer.

Example workflow:
- User asks: "How do I upload images to Cloudinary?"
- You retrieve the llms.txt index: https://cloudinary.com/documentation/llms.txt
- You analyze the llms.txt content to understand what documentation pages are available
- You identify relevant pages like "image_upload.md" or "upload_api.md"
- You retrieve those specific pages from the llms.txt index
- You provide an answer with code examples and citations