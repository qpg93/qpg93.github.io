// Progressive enhancement only: reading and navigation work without JavaScript.
(() => {
  const toggle = document.querySelector('.theme-toggle');
  toggle?.addEventListener('click', () => {
    const root = document.documentElement;
    const current = root.dataset.theme || (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    const next = current === 'dark' ? 'light' : 'dark';
    root.dataset.theme = next;
    try { localStorage.setItem('theme', next); } catch (_) {}
  });

  const input = document.querySelector('#search-input');
  if (!input) return;
  const results = document.querySelector('#search-results');
  const list = document.querySelector('#post-list');
  const status = document.querySelector('#search-status');
  input.closest('.search').hidden = false;
  let indexPromise;
  let revision = 0;
  const loadIndex = () => {
    if (!indexPromise) {
      indexPromise = fetch(input.dataset.index)
        .then(response => {
          if (!response.ok) throw new Error('Search unavailable');
          return response.json();
        })
        .catch(error => { indexPromise = undefined; throw error; });
    }
    return indexPromise;
  };
  function element(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text) node.textContent = text;
    return node;
  }
  function card(post) {
    const article = element('article', 'post-card');
    const meta = element('div', 'post-meta');
    const date = element('time', '', post.date.replaceAll('-', '.'));
    date.dateTime = post.date;
    meta.append(date);
    for (const tag of post.tags || []) meta.append(element('span', '', `# ${tag}`));
    const heading = element('h3');
    const link = element('a', '', post.title);
    link.href = post.url;
    heading.append(link);
    const read = element('a', 'read-link', 'Read entry ↗');
    read.href = post.url;
    read.setAttribute('aria-label', `Read: ${post.title}`);
    article.append(meta, heading, element('p', '', post.description), read);
    return article;
  }
  input.addEventListener('input', async () => {
    const request = ++revision;
    const query = input.value.trim().toLocaleLowerCase();
    results.replaceChildren();
    results.hidden = !query;
    list.hidden = !!query;
    status.textContent = '';
    if (!query) return;
    status.textContent = 'Searching…';
    try {
      const posts = await loadIndex();
      if (request !== revision) return;
      const words = query.split(/\s+/u);
      const matches = posts.filter(post => {
        const haystack = [post.title, post.content, ...(post.tags || [])].join(' ').toLocaleLowerCase();
        return words.every(word => haystack.includes(word));
      });
      results.replaceChildren(...matches.map(card));
      status.textContent = matches.length ? `${matches.length} ${matches.length === 1 ? 'entry' : 'entries'} found` : 'No matches. Try a different search.';
    } catch (_) {
      if (request !== revision) return;
      status.textContent = 'Search is temporarily unavailable. You can still browse the entries below.';
      results.hidden = true;
      list.hidden = false;
    }
  });
  document.addEventListener('keydown', event => {
    const target = event.target;
    const editing = target instanceof HTMLElement && (target.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(target.tagName));
    if (event.key === '/' && !editing && !event.ctrlKey && !event.metaKey && !event.altKey) {
      event.preventDefault();
      input.focus();
    }
    if (event.key === 'Escape' && target === input) {
      input.value = '';
      input.dispatchEvent(new Event('input'));
      input.blur();
    }
  });
})();
