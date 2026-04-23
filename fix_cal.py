import re

with open('calendario.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Remove everything between <main class="calendar-page"...> and <section class="calendar-section" id="calendario">
text = re.sub(
    r'(<main class="calendar-page"[^>]*>).*?(<section class="calendar-section" id="calendario">)',
    r'\1\n\2',
    text,
    flags=re.DOTALL
)

# 2. Remove the participate section. It starts at <section class="participate-section" id="participe">
# and ends right before <footer class="footer">. Wait, I replaced </section> of participate with </main> earlier!
# Let's just remove the participate section content.
text = re.sub(
    r'(</main>)\s*<div class="container participate-container.*?</section>',
    r'\1',
    text,
    flags=re.DOTALL
)

with open('calendario.html', 'w', encoding='utf-8') as f:
    f.write(text)

