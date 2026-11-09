"""MOAI AI 講座のスライドのページ（index.html）を作る。

pdf/ の中にあるファイルを見て、あるものはリンクに、まだないものは「準備中」にする。
  pdf/lecture-01.pdf … 講座用（講座の当日に映す版）
  pdf/textbook-01.pdf … 教科書（あとで見返す、くわしい版）
使い方: python3 build.py
"""
from html import escape
from pathlib import Path

ROOT = Path(__file__).parent
LECTURES = [
    ('はじめに・準備・AI のしくみ', 'Claude を使える状態にして、AI のしくみと、まちがいの見分け方を学ぶ。'),
    ('調べる・書く', 'Deep Research・NotebookLM の使い分け、課題での書き方、モデルの選び方。'),
    ('GitHub と最初のゲーム', 'Claude Code を入れ、AI エージェントでゲームを作って GitHub に上げる。'),
    ('AI をつなぐ・動かすしくみ', 'API・MCP、スキルとフック、RAG。'),
    ('自分用のアプリ', '締切の一覧を作るツールを作り、セキュリティの監査までかける。'),
    ('セキュリティと業務のしくみ', '実際の事件、内部統制とリスク、監査、国ごとのルール。'),
    ('AI 時代の就活と、会社での AI', '個人と仕事のちがい、会社での管理、ローカル AI、権限の設定。'),
    ('発表・総復習', '自分で作ったものを発表し、全8回をふり返る。'),
]
KINDS = [('lecture', '講座用'), ('textbook', '教科書')]


def link(kind: str, label: str, number: int) -> str:
    name = f'pdf/{kind}-{number:02d}.pdf'
    if (ROOT / name).exists():
        return f'<a class="pdf" href="{name}">{label}（PDF）</a>'
    return f'<span class="pdf soon">{label}（準備中）</span>'


def card(number: int, title: str, about: str) -> str:
    links = ''.join(link(kind, label, number) for kind, label in KINDS)
    return f'''    <li class="card">
      <p class="num">第{number}回</p>
      <h2>{escape(title)}</h2>
      <p class="about">{escape(about)}</p>
      <div class="links">{links}</div>
    </li>
'''


PAGE = '''<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>MOAI AI 講座のスライド</title>
<meta name="description" content="MOAI AI 講座（全8回）のスライド。講座で映す版と、あとで見返す教科書の版。">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700;900&display=swap">
<style>
  :root {{ --ink: #0f1f3d; --soft: #4a5568; --accent: #1f6f8b; --paper: #f6f5f0; --card: #ffffff; --line: #c9d3e0; --tint: #e3eef2; }}
  @media (prefers-color-scheme: dark) {{
    :root {{ --ink: #f6f5f0; --soft: #c9d3e0; --accent: #8cc3d6; --paper: #0f1f3d; --card: #17294d; --line: #2c4170; --tint: #1f3a5c; }}
  }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; background: var(--paper); color: var(--ink); font-family: 'Noto Sans JP', system-ui, sans-serif; line-height: 1.7; word-break: auto-phrase; text-wrap: pretty; }}
  main {{ max-width: 1040px; margin: 0 auto; padding: 56px 16px 80px; }}
  .eyebrow {{ margin: 0; color: var(--accent); font-weight: 700; letter-spacing: .2em; font-size: 14px; }}
  h1 {{ margin: 8px 0 12px; font-size: clamp(28px, 5vw, 44px); font-weight: 900; line-height: 1.3; }}
  .lead {{ margin: 0 0 8px; color: var(--soft); }}
  ul {{ list-style: none; padding: 0; margin: 40px 0 0; display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 16px; }}
  .card {{ background: var(--card); border-top: 6px solid var(--accent); padding: 20px 22px 22px; display: flex; flex-direction: column; gap: 6px; }}
  .num {{ margin: 0; color: var(--accent); font-weight: 700; font-size: 14px; letter-spacing: .1em; }}
  h2 {{ margin: 0; font-size: 20px; line-height: 1.4; }}
  .about {{ margin: 0; color: var(--soft); font-size: 15px; flex: 1; }}
  .links {{ display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px; }}
  .pdf {{ display: inline-block; padding: 8px 14px; border: 2px solid var(--accent); color: var(--ink); text-decoration: none; font-weight: 700; font-size: 15px; }}
  a.pdf:hover, a.pdf:focus-visible {{ background: var(--tint); outline: none; }}
  .soon {{ border-color: var(--line); color: var(--soft); font-weight: 400; }}
  footer {{ margin-top: 48px; color: var(--soft); font-size: 14px; }}
</style>
</head>
<body>
<main>
  <p class="eyebrow">MOAI AI 講座</p>
  <h1>全8回のスライド</h1>
  <p class="lead">講座用は、講座の当日に映すスライドです。<br>教科書は、あとで見返すための、くわしい版です。</p>
  <ul>
{cards}  </ul>
  <footer>MOAI ｜ 講座の申し込みとお問い合わせは、<a href="https://unimatch-my.com" style="color: inherit">MOAI のサイト</a>から。</footer>
</main>
</body>
</html>
'''


def main() -> None:
    cards = ''.join(card(i + 1, title, about) for i, (title, about) in enumerate(LECTURES))
    (ROOT / 'index.html').write_text(PAGE.format(cards=cards), encoding='utf-8')
    found = sorted(p.name for p in (ROOT / 'pdf').glob('*.pdf')) if (ROOT / 'pdf').exists() else []
    print(f'index.html を作りました（PDF {len(found)}件）')


if __name__ == '__main__':
    main()
