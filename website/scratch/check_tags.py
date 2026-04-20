import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Filter out comments
content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)

# Find all opening and closing div and section tags
tags = re.findall(r'<(div|section|/div|/section)[\s>]', content)

stack = []
for tag in tags:
    if tag.startswith('/'):
        if not stack:
            print(f"Error: Found extra closing tag </{tag[1:]}>")
        else:
            opening = stack.pop()
            if opening != tag[1:]:
                print(f"Error: Mismatched tags <{opening}> and </{tag[1:]}>")
    else:
        stack.append(tag)

if stack:
    print(f"Error: Unclosed tags: {stack}")
else:
    print("Tags are balanced.")
