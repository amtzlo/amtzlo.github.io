import os
import markdown
import frontmatter

# 1. Define Directories
POSTS_DIR = "_posts"
TEMPLATES_DIR = "_templates"
OUTPUT_DIR = "posts"
BLOG_SRC_FILE = os.path.join(TEMPLATES_DIR, "_blog.html")
BLOG_OUTPUT_FILE = "blog.html"

# 2. Get the base template
with open(os.path.join(TEMPLATES_DIR, "base.html"), "r") as f:
    base_template = f.read()

# 3. Process each post
posts = []
for filename in os.listdir(POSTS_DIR):
    if filename.endswith(".md"):
        with open(os.path.join(POSTS_DIR, filename), "r") as f:
            post = frontmatter.load(f)

        html_content = markdown.markdown(post.content)

        # Create a dictionary for the post
        post_data = {
            "title": post["title"],
            "content": html_content,
            "filename": os.path.splitext(filename)[0] + ".html",
        }
        posts.append(post_data)

        # Render the post with the base template
        post_output = base_template.replace("{{title}}", post_data["title"])
        post_output = post_output.replace("{{content}}", post_data["content"])

        with open(os.path.join(OUTPUT_DIR, post_data["filename"]), "w") as f:
            f.write(post_output)

# 4. Generate the blog listing page
with open(BLOG_SRC_FILE, "r") as f:
    blog_page = frontmatter.load(f)

post_list_html = ""
for post in posts:
    post_list_html += f'''
        <div class="card fade-in">
            <h3>{post["title"]}</h3>
            <a href="posts/{post["filename"]}" class="card-link">Read more →</a>
        </div>
    '''

# Replace the placeholder in the content of the blog page
blog_content_with_list = blog_page.content.replace("{{post_list}}", post_list_html)

# Render the blog page with the base template
blog_output = base_template.replace("{{title}}", blog_page["title"])
blog_output = blog_output.replace("{{content}}", blog_content_with_list)

# Write the final blog page
with open(BLOG_OUTPUT_FILE, "w") as f:
    f.write(blog_output)

print("Build complete!")