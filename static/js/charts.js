// Native SVG + HTML controls. No dependencies or interpolated medical values.
(() => {
  for (const chart of document.querySelectorAll('[data-chart]')) {
    const svg = chart.querySelector('svg');
    const buttons = [...chart.querySelectorAll('[data-chart-point]')];
    const dots = [...chart.querySelectorAll('[data-chart-dot]')];
    const cursor = chart.querySelector('.chart-cursor');
    const output = chart.querySelector('output');
    const tooltip = chart.querySelector('[data-chart-tooltip]');
    const controls = chart.querySelector('.chart-controls');
    if (!svg || !cursor || !output || !tooltip || !controls || !buttons.length || buttons.length !== dots.length) continue;
    controls.hidden = false;
    let active = -1;

    function select(index) {
      if (active !== index) {
        active = index;
        buttons.forEach((button, i) => button.setAttribute('aria-pressed', String(i === index)));
        dots.forEach((dot, i) => dot.classList.toggle('is-active', i === index));
        const button = buttons[index];
        output.textContent = `${button.dataset.label}: ${button.dataset.value}`;
        tooltip.textContent = output.textContent;
      }
      const x = dots[index].getAttribute('cx');
      cursor.setAttribute('x1', x);
      cursor.setAttribute('x2', x);
      cursor.removeAttribute('hidden');
    }
    function hideTooltip() { tooltip.hidden = true; }
    function move(event) {
      const rect = svg.getBoundingClientRect();
      if (!rect.width) return;
      const x = (event.clientX - rect.left) * svg.viewBox.baseVal.width / rect.width;
      let closest = 0;
      dots.forEach((dot, i) => {
        if (Math.abs(Number(dot.getAttribute('cx')) - x) < Math.abs(Number(dots[closest].getAttribute('cx')) - x)) closest = i;
      });
      select(closest);
      tooltip.hidden = false;
      const box = tooltip.getBoundingClientRect();
      tooltip.style.left = `${Math.max(8, Math.min(event.clientX + 16, innerWidth - box.width - 8))}px`;
      tooltip.style.top = `${Math.max(8, Math.min(event.clientY + 16, innerHeight - box.height - 8))}px`;
    }
    svg.addEventListener('pointermove', move);
    svg.addEventListener('pointerdown', move);
    svg.addEventListener('pointerleave', hideTooltip);
    svg.addEventListener('pointercancel', hideTooltip);
    buttons.forEach((button, index) => {
      button.addEventListener('click', () => { select(index); hideTooltip(); });
      button.addEventListener('focus', () => { select(index); hideTooltip(); });
      button.addEventListener('keydown', event => {
        let next;
        if (event.key === 'ArrowRight') next = (index + 1) % buttons.length;
        if (event.key === 'ArrowLeft') next = (index - 1 + buttons.length) % buttons.length;
        if (event.key === 'Home') next = 0;
        if (event.key === 'End') next = buttons.length - 1;
        if (next !== undefined) { event.preventDefault(); buttons[next].focus(); }
      });
    });
    window.addEventListener('scroll', hideTooltip, {passive: true, capture: true});
    window.addEventListener('resize', hideTooltip, {passive: true});
  }
})();
