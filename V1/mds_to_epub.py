#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mds_to_epub.py - 更稳健的版本
修复点：
 - 自动处理 UTF-8 BOM / 常见编码
 - 自动剥离 YAML front-matter（以防只有 front-matter 导致空文档）
 - 自动解码 URL 编码（%20 -> space）来寻找图片
 - 强制将章节内容写成合格的 XHTML bytes
 - 写前用正则检查 <body>，若为空导出 raw 以便调试并临时替换占位

# 激活虚拟环境
.\venv\Scripts\activate
# 执行命令
python .\mds_to_epub.py -i . -o "美少女的数据结构漫话V1.epub" -t "美少女的数据结构漫话V1" -a "Carrie - 泠"

"""
import argparse
import re
from pathlib import Path
import mimetypes
import markdown
from ebooklib import epub
import ebooklib
import urllib.parse
from typing import List

NUM_RE = re.compile(r'\d+')
IMAGE_MD_RE = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')
FRONT_MATTER_RE = re.compile(r'^\s*---\s*.*?---\s*', flags=re.DOTALL)

# 封面图片绝对路径或相对路径
COVER_IMAGE = r"I:\B-1 笔记\DS & Algorithm\0. 故事集\V1\assets\images\cover.jpg"

DEFAULT_CSS = """
body {
  font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
  line-height: 1.6;
  margin: 1em;
  color: #222;
}
h1, h2, h3, h4, h5 { color: #10b981; margin-top: 1.2em; }
pre { background: #f6f6f6; padding: 0.8em; overflow: auto; }
code { font-family: monospace; font-size: 0.9em; }
img { max-width: 100%; height: auto; }
table { border-collapse: collapse; width: 100%; }
table, th, td { border: 1px solid #ccc; padding: 6px; }
"""

def _numeric_key_from_name(name: str):
    # 提取所有数字并转成整数序列： "1.9 abc 10" -> [1,9,10]
    nums = [int(x) for x in NUM_RE.findall(name)]
    if nums:
        return (0, nums)   # 前缀 0 表示有数字，优先按数字排序
    else:
        return (1, name)   # 没数字的放后，按名字排序

def find_md_files(input_dir: str) -> List[Path]:
    p = Path(input_dir)
    if not p.exists():
        raise SystemExit(f'输入目录不存在：{p.resolve()}')
    files = [f for f in p.iterdir() if f.is_file() and f.suffix.lower() == '.md']
    files_sorted = sorted(files, key=lambda f: _numeric_key_from_name(f.stem))
    return files_sorted

def read_md_safely(path: Path) -> str:
    b = path.read_bytes()
    # 首先尝试 utf-8-sig（会去 BOM），然后 utf-8，再回退到 gbk
    for enc in ('utf-8-sig', 'utf-8', 'gbk'):
        try:
            text = b.decode(enc)
            return text
        except Exception:
            continue
    # 最后强制忽略错误解码
    return b.decode('utf-8', errors='ignore')

def strip_front_matter(md_text: str) -> str:
    return FRONT_MATTER_RE.sub('', md_text, count=1)

def convert_md_to_html(md_text: str) -> str:
    return markdown.markdown(md_text, extensions=['extra', 'toc', 'fenced_code', 'codehilite', 'tables'])

def ensure_book_internal_struct(book):
    if not hasattr(book, '_added_images'):
        book._added_images = {}

def add_image_to_book(book, img_path: Path):
    img_key = str(img_path.resolve())
    if img_key in book._added_images:
        return book._added_images[img_key]
    data = img_path.read_bytes()
    mime, _ = mimetypes.guess_type(str(img_path))
    if mime is None:
        mime = 'image/png'
    file_name = f'images/{img_path.name}'
    item = epub.EpubItem(uid=None, file_name=file_name, media_type=mime, content=data)
    book.add_item(item)
    book._added_images[img_key] = file_name
    return file_name

def collect_and_pack_images(book, md_text: str, md_parent_dir: Path):
    def repl(match):
        alt, src = match.group(1), match.group(2).strip()
        if src.startswith('http://') or src.startswith('https://') or src.startswith('data:'):
            return match.group(0)
        # 尝试 url 解码
        src_unq = urllib.parse.unquote(src)
        candidates = [
            md_parent_dir / src,
            md_parent_dir / src_unq,
            Path(src),
            Path(src_unq)
        ]
        found = None
        for c in candidates:
            try:
                if c.exists():
                    found = c.resolve()
                    break
            except Exception:
                continue
        if not found:
            print(f'  ⚠️ 找不到图片：{src}（在 {md_parent_dir} 下尝试了 { [str(x) for x in candidates] } ） —— 保留原引用')
            return match.group(0)
        epub_path = add_image_to_book(book, found)
        return f'![{alt}]({epub_path})'
    return IMAGE_MD_RE.sub(repl, md_text)

def make_xhtml_fragment(html_body: str, title: str, lang='zh-CN') -> bytes:
    # 确保 body 非空（如果 html_body 为空，调用者应先处理）
    x = f'''<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="{lang}">
  <head><meta charset="utf-8"/><title>{title}</title><link rel="stylesheet" type="text/css" href="styles/style.css"/></head>
  <body>
    {html_body}
  </body>
</html>'''
    return x.encode('utf-8')

def build_epub(input_dir, output_file, title, author, language='zh-CN', css_file=None):
    files = find_md_files(input_dir)
    if not files:
        raise SystemExit(f'没有在 {Path(input_dir).resolve()} 目录下找到任何 .md 文件。')

    book = epub.EpubBook()
    ensure_book_internal_struct(book)

    book.set_identifier('id-' + title.replace(' ', '_'))
    book.set_title(title)
    book.set_language(language)
    book.add_author(author)

    if COVER_IMAGE:
        cover_path = Path(COVER_IMAGE)
        if cover_path.exists():
            book.set_cover(cover_path.name, cover_path.read_bytes())
            print(f"已添加封面: {cover_path}")
        else:
            print(f"⚠️ 指定的封面文件 {COVER_IMAGE} 不存在，跳过。")

    # css
    if css_file:
        css_path = Path(css_file)
        if css_path.exists():
            css_data = css_path.read_text(encoding='utf-8')
        else:
            print(f'警告: 指定的 CSS 文件 {css_file} 未找到，使用默认样式。')
            css_data = DEFAULT_CSS
    else:
        css_data = DEFAULT_CSS
    style_item = epub.EpubItem(uid="style_nav", file_name="styles/style.css", media_type="text/css", content=css_data.encode('utf-8'))
    book.add_item(style_item)

    spine = ['nav']
    toc = []
    chapters = []

    print(f'找到 {len(files)} 个 md 文件，开始逐个处理...')
    for idx, md_path in enumerate(files, start=1):
        print(f'  [{idx}/{len(files)}] 处理: {md_path.name}')
        raw_md = read_md_safely(md_path)
        md_clean = strip_front_matter(raw_md)
        md_packed = collect_and_pack_images(book, md_clean, md_path.parent)
        html = convert_md_to_html(md_packed).strip()
        if not html:
            print(f'    ⚠️ 注意: {md_path.name} 转换后 HTML 为空，已用文件名作为占位内容。')
            html = f'<h1>{md_path.stem}</h1><p>（原始 Markdown 转换结果为空）</p>'

        xhtml_bytes = make_xhtml_fragment(html, md_path.stem, lang=language)
        chapter = epub.EpubHtml(title=md_path.stem, file_name=f'chap_{idx}.xhtml', lang=language)
        # 强制以 bytes 形式存放内容
        chapter.content = xhtml_bytes
        book.add_item(chapter)
        chapters.append(chapter)
        spine.append(chapter)
        toc.append(epub.Link(chapter.file_name, md_path.stem, chapter.file_name))

    # 手动构建 nav.xhtml，避免自动生成时出现不可控问题
    nav_entries = []
    for ch in chapters:
        nav_entries.append(f'<li><a href="{ch.file_name}">{ch.title}</a></li>')
    nav_html = f'''<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml">
  <head><meta charset="utf-8"/><title>Navigation</title></head>
  <body>
    <nav epub:type="toc" id="toc">
      <h1>目录</h1>
      <ol>
        {''.join(nav_entries)}
      </ol>
    </nav>
  </body>
</html>
'''.encode('utf-8')
    nav_item = epub.EpubItem(uid="nav", file_name="nav.xhtml", media_type="application/xhtml+xml", content=nav_html)
    # 移除已有的 nav（如果存在）
    for it in list(book.get_items()):
        if getattr(it, 'file_name', '') == 'nav.xhtml':
            try:
                book.remove_item(it)
            except Exception:
                pass
    book.add_item(nav_item)

    book.toc = tuple(toc)
    book.spine = spine
    # 添加 NCX
    book.add_item(epub.EpubNcx())

    # ----- 写前检查：确保每个 document 都有 <body> 内容 -----
    debug_dir = Path('debug_html')
    debug_dir.mkdir(exist_ok=True)

    docs = [it for it in book.get_items_of_type(ebooklib.ITEM_DOCUMENT)]
    print(f'准备写入 EPUB，检测 {len(docs)} 个 document 条目...')
    any_empty = False
    body_re = re.compile(br'<body[^>]*>(.*?)</body>', flags=re.DOTALL | re.IGNORECASE)
    for i, it in enumerate(docs, start=1):
        try:
            raw = it.get_content() if hasattr(it, 'get_content') else (it.content if hasattr(it, 'content') else None)
            raw_bytes = raw if isinstance(raw, (bytes, bytearray)) else (str(raw).encode('utf-8') if raw is not None else b'')
            m = body_re.search(raw_bytes)
            size = len(m.group(1)) if (m and m.group(1)) else 0
        except Exception as e:
            raw_bytes = b''
            size = 0
            print(f'  ⚠️ 在检查 {it.file_name} 时发生异常：{e}')

        print(f'  doc[{i}/{len(docs)}] {it.file_name} - body length = {size}')
        if size == 0:
            any_empty = True
            debug_path = debug_dir / (it.file_name.replace('/', '_') + '.raw.xhtml')
            try:
                debug_path.write_bytes(raw_bytes)
                print(f'    -> 导出为 {debug_path} 以便调试')
            except Exception as ee:
                print(f'    -> 导出失败: {ee}')
            # 替换为安全占位 XHTML（bytes）
            placeholder = f'<?xml version="1.0" encoding="utf-8"?><html xmlns="http://www.w3.org/1999/xhtml"><head><meta charset="utf-8"/></head><body><h1>占位章节：{it.file_name}</h1><p>原始章节 body 为空或无法解析，已用占位符替换以继续生成 EPUB。</p></body></html>'.encode('utf-8')
            try:
                # 有些 item 需要直接设置 .content（bytes）
                it.content = placeholder
                print(f'    -> 已用占位内容替换 {it.file_name}')
            except Exception as ee:
                print(f'    -> 无法替换内容：{ee}')

    if any_empty:
        print('已检测到一个或多个空文档，已导出 raw 内容到 debug_html/ 并用占位内容替换它们，继续写入 EPUB。（请检查 debug_html 中的文件以定位原因）')

    print('正在写出 EPUB 文件...')
    epub.write_epub(output_file, book, {})
    print('完成：', output_file)

def main():
    parser = argparse.ArgumentParser(description='将一个目录内的 Markdown 文件合并成 EPUB（更稳健版本）。')
    parser.add_argument('--input-dir', '-i', required=True, help='输入目录，包含 .md 文件')
    parser.add_argument('--output', '-o', default='output.epub', help='输出 epub 文件名 (默认 output.epub)')
    parser.add_argument('--title', '-t', default='Combined Book', help='书名')
    parser.add_argument('--author', '-a', default='Anonymous', help='作者名')
    parser.add_argument('--language', '-l', default='zh-CN', help='语言代码 (例如 zh-CN)')
    parser.add_argument('--css', help='可选：自定义 CSS 文件路径')
    args = parser.parse_args()

    print(f'输入目录: {args.input_dir}')
    print(f'输出文件: {args.output}')
    print('开始打包...')
    build_epub(args.input_dir, args.output, args.title, args.author, args.language, args.css)

if __name__ == '__main__':
    main()
