"""Mock LLM service for testing without valid OpenAI API key

This mock attempts to follow the incoming brief so local testing reflects
what a real LLM would do. It generates different apps for common briefs
such as markdown conversion, sum-of-sales, todo list, calculator, JSON viewer,
GitHub user lookup, and a generic fall-back page.
"""

from app.models import LLMResponse


def _mit_license() -> str:
    return (
        "MIT License\n\n"
        "Copyright (c) 2025 TDS Project\n\n"
        "Permission is hereby granted, free of charge, to any person obtaining a copy\n"
        "of this software and associated documentation files (the \"Software\"), to deal\n"
        "in the Software without restriction, including without limitation the rights\n"
        "to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n"
        "copies of the Software, and to permit persons to whom the Software is\n"
        "furnished to do so, subject to the following conditions:\n\n"
        "The above copyright notice and this permission notice shall be included in all\n"
        "copies or substantial portions of the Software.\n\n"
        "THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n"
        "IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n"
        "FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n"
        "AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n"
        "LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n"
        "OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n"
        "SOFTWARE."
    )


def _wrap_html(title: str, body_html: str, extra_head: str = "", extra_script: str = "") -> str:
    return f"""<!DOCTYPE html>
<html lang=\"en\">\n<head>\n  <meta charset=\"UTF-8\">\n  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n  <title>{title}</title>\n  <style>body{{font-family: system-ui, Arial, sans-serif; max-width: 900px; margin: 0 auto; padding: 20px}}</style>\n  {extra_head}\n</head>\n<body>\n{body_html}\n<script>document.addEventListener('DOMContentLoaded',()=>{{try{{hljs&&hljs.highlightAll&&hljs.highlightAll()}}catch(e){{}}}});</script>\n{extra_script}\n</body>\n</html>"""


def _markdown_app() -> tuple[str, str]:
    title = "Markdown to HTML Converter"
    extra_head = (
        "<script src=\"https://cdn.jsdelivr.net/npm/marked/marked.min.js\"></script>\n"
        "<script src=\"https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/highlight.min.js\"></script>\n"
        "<link rel=\"stylesheet\" href=\"https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/styles/default.min.css\">"
    )
    body = (
        "<h1>Markdown to HTML Converter</h1>\n"
        "<p>Loads input.md if present in this repository. You can also type below.</p>\n"
        "<textarea id=\"markdown-input\" placeholder=\"Enter your markdown here...\" style=\"width:100%;height:180px\"></textarea>\n"
        "<div><button id=\"convert\">Convert</button></div>\n"
        "<div id=\"markdown-output\" style=\"border:1px solid #ddd;padding:12px;margin-top:12px\"></div>\n"
    )
    script = (
        "<script>\n"
        "async function loadAttachment() {\n"
        "  try { const res = await fetch('input.md'); if(res.ok){ const t = await res.text(); document.getElementById('markdown-input').value = t; convert(); } } catch(e){}\n"
        "}\n"
        "function convert(){ const md=document.getElementById('markdown-input').value; document.getElementById('markdown-output').innerHTML = (window.marked? marked.parse(md): md); }\n"
        "document.getElementById('convert').addEventListener('click', convert);\n"
        "document.addEventListener('DOMContentLoaded', loadAttachment);\n"
        "</script>"
    )
    html = _wrap_html(title, body, extra_head, script)
    readme = (
        "# Markdown to HTML Converter\n\n"
        "Converts Markdown to HTML using marked.js and highlights code with highlight.js."
    )
    return html, readme


def _sum_sales_app() -> tuple[str, str]:
    title = "Sales Summary"
    body = (
        "<h1>Sales Summary</h1>\n"
        "<p>Loads sales.csv from this repository, sums the sales column (optionally filter category <= 11) and shows the total.</p>\n"
        "<label><input type=\"checkbox\" id=\"filter-cat\" checked> Only categories <= 11</label>\n"
        "<div id=\"total-sales\" style=\"margin-top:12px;font-weight:bold\">0.00</div>\n"
    )
    script = (
        "<script>\n"
        "async function sumSales(){\n"
        "  const res = await fetch('sales.csv'); const text = await res.text();\n"
        "  const lines = text.trim().split(/\n+/); const header = lines.shift().split(',');\n"
        "  const cIdx = header.findIndex(h=>h.trim().toLowerCase()==='category');\n"
        "  const sIdx = header.findIndex(h=>h.trim().toLowerCase()==='sales');\n"
        "  let total = 0; const filter = document.getElementById('filter-cat').checked;\n"
        "  for(const line of lines){ const cols=line.split(','); const cat=parseFloat(cols[cIdx]); const val=parseFloat(cols[sIdx]); if(!isNaN(val)){ if(!filter || (cat<=11)) total+=val; } }\n"
        "  document.getElementById('total-sales').textContent = total.toFixed(2);\n"
        "}\n"
        "document.addEventListener('DOMContentLoaded', ()=>{ sumSales(); document.getElementById('filter-cat').addEventListener('change', sumSales); });\n"
        "</script>"
    )
    html = _wrap_html(title, body, extra_script=script)
    readme = "# Sales Summary\n\nSums the `sales` column from `sales.csv` and displays the total."
    return html, readme


def _todo_app() -> tuple[str, str]:
    title = "To-Do List"
    body = (
        "<h1>To-Do List</h1>\n"
        "<input id=\"task-input\" placeholder=\"Add a task...\"> <button id=\"add-btn\">Add</button>\n"
        "<ul id=\"task-list\"></ul>\n"
    )
    script = (
        "<script>\n"
        "function add(){ const inp=document.getElementById('task-input'); const v=inp.value.trim(); if(!v)return; const li=document.createElement('li'); li.textContent=v+' '; const del=document.createElement('button'); del.textContent='Delete'; del.onclick=()=>li.remove(); li.appendChild(del); document.getElementById('task-list').appendChild(li); inp.value=''; }\n"
        "document.getElementById('add-btn').addEventListener('click', add);\n"
        "</script>"
    )
    html = _wrap_html(title, body, extra_script=script)
    readme = "# To-Do List\n\nSimple to-do app with add and delete features."
    return html, readme


def _calculator_app() -> tuple[str, str]:
    title = "Calculator"
    body = (
        "<h1>Calculator</h1>\n"
        "<input id=\"display\" readonly style=\"width:100%;margin-bottom:8px\">\n"
        "<div id=\"keys\"></div>\n"
    )
    script = (
        "<script>\n"
        "const keys='789/456*123-0.C+'.split(''); const cont=document.getElementById('keys'); const d=document.getElementById('display');\n"
        "keys.forEach(k=>{ const b=document.createElement('button'); b.textContent=k; b.style.margin='4px'; b.onclick=()=>press(k); cont.appendChild(b); });\n"
        "function press(k){ if(k==='C'){ d.value=''; return;} if(k==='='){ try{ d.value= String(Function('return '+d.value)()); }catch(e){ d.value='Err'; } return;} d.value += k; }\n"
        "</script>"
    )
    html = _wrap_html(title, body, extra_script=script)
    readme = "# Calculator\n\nBasic calculator supporting + - * /."
    return html, readme


def _json_viewer_app() -> tuple[str, str]:
    title = "JSON Viewer"
    body = (
        "<h1>JSON Viewer</h1>\n"
        "<input id=\"json-search\" placeholder=\"Search...\">\n"
        "<pre id=\"json-output\" style=\"border:1px solid #ddd;padding:12px\"></pre>\n"
    )
    script = (
        "<script>\n"
        "let data={}; function render(){ const q=document.getElementById('json-search').value.toLowerCase(); const txt=JSON.stringify(data, null, 2); document.getElementById('json-output').textContent = q? txt.split('\n').filter(l=>l.toLowerCase().includes(q)).join('\n') : txt; }\n"
        "async function load(){ try{ const r=await fetch('data.json'); if(r.ok){ data=await r.json(); render(); } }catch(e){} }\n"
        "document.getElementById('json-search').addEventListener('input', render); document.addEventListener('DOMContentLoaded', load);\n"
        "</script>"
    )
    html = _wrap_html(title, body, extra_script=script)
    readme = "# JSON Viewer\n\nLoads data.json and renders formatted JSON with simple search."
    return html, readme


def _github_user_app() -> tuple[str, str]:
    title = "GitHub User Lookup"
    body = (
        "<h1>GitHub User Lookup</h1>\n"
        "<form id=\"github-user-form\"><input id=\"username\" placeholder=\"octocat\"> <button>Lookup</button></form>\n"
        "<div id=\"github-status\" aria-live=\"polite\"></div>\n"
        "<div>Created at: <span id=\"github-created-at\"></span></div>\n"
    )
    script = (
        "<script>\n"
        "document.getElementById('github-user-form').addEventListener('submit', async (e)=>{ e.preventDefault(); const u=document.getElementById('username').value.trim(); const s=document.getElementById('github-status'); s.textContent='Starting lookup...'; try{ const r=await fetch('https://api.github.com/users/'+encodeURIComponent(u)); if(!r.ok) throw new Error('HTTP '+r.status); const j=await r.json(); s.textContent='Success'; const d=new Date(j.created_at); document.getElementById('github-created-at').textContent = d.toISOString().slice(0,10); } catch(err){ s.textContent='Failed'; } });\n"
        "</script>"
    )
    html = _wrap_html(title, body, extra_script=script)
    readme = "# GitHub User Lookup\n\nFetches user info and shows account creation date."
    return html, readme


def _generic_app(brief: str) -> tuple[str, str]:
    title = "Generated App"
    body = (
        f"<h1>{brief}</h1>\n"
        "<p>This page is generated by the mock LLM to mirror your brief. Implement specific logic here as needed.</p>\n"
    )
    html = _wrap_html(title, body)
    readme = f"# Generated App\n\nThis app reflects the brief: {brief}"
    return html, readme


def generate_app_mock(brief: str, checks: str) -> LLMResponse:
    """Generate a mock app response for testing purposes following the brief."""
    print("Using MOCK LLM service - generating response based on brief...")

    b = (brief or "").lower()
    if any(k in b for k in ["markdown", "md to html", "marked"]):
        html_content, readme_content = _markdown_app()
    elif any(k in b for k in ["sum", "sales", "csv"]):
        html_content, readme_content = _sum_sales_app()
    elif any(k in b for k in ["todo", "to-do", "to do"]):
        html_content, readme_content = _todo_app()
    elif any(k in b for k in ["calculator", "calc"]):
        html_content, readme_content = _calculator_app()
    elif any(k in b for k in ["json", "viewer"]):
        html_content, readme_content = _json_viewer_app()
    elif any(k in b for k in ["github", "user"]):
        html_content, readme_content = _github_user_app()
    else:
        html_content, readme_content = _generic_app(brief)

    license_content = _mit_license()

    return LLMResponse(**{
        "README.md": readme_content,
        "LICENSE": license_content,
        "index.html": html_content,
        "script.js": None,
        "main.py": None,
    })