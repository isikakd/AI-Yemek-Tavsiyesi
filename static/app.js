// ── Yardımcı fonksiyonlar ─────────────────────────────────────────────────────

function calColor(cal) {
  if (cal < 300) return '#4ade80';
  if (cal < 500) return '#facc15';
  if (cal < 700) return '#fb923c';
  return '#f87171';
}

function switchTab(tab) {
  document.querySelectorAll('.tab').forEach((t, i) =>
    t.classList.toggle('active', ['suggest', 'fridge'][i] === tab)
  );
  document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
  document.getElementById('panel-' + tab).classList.add('active');
}

// ── Kart render ───────────────────────────────────────────────────────────────

function renderCards(yemekler, containerId) {
  const wrap = document.getElementById(containerId);
  wrap.innerHTML = '';

  yemekler.forEach(y => {
    const pct  = Math.min((y.kalori / 800) * 100, 100);
    const cc   = calColor(y.kalori);
    const tags = (y.etiketler || []).slice(0, 2)
      .map(e => `<span class="chip chip-tag">#${e}</span>`).join('');

    wrap.innerHTML += `
      <div class="recipe-card" data-emoji="${y.emoji}"
           onclick='openModal(${JSON.stringify(y).replace(/'/g, "&#39;")})'>
        <div class="card-top">
          <div>
            <span class="card-emoji">${y.emoji}</span>
            <div class="card-name">${y.isim}</div>
          </div>
          <div class="kcal-badge">
            <span class="kcal-num" style="color:${cc}">${y.kalori}</span>
            <span class="kcal-lbl">KCAL</span>
          </div>
        </div>
        <div class="calbar-wrap">
          <div class="calbar" style="width:${pct}%;background:${cc}"></div>
        </div>
        <div class="chips">
          <span class="chip chip-time">⏱ ${y.sure}</span>
          <span class="chip chip-diff">📊 ${y.zorluk}</span>
          ${tags}
        </div>
        <div class="expand-hint">Tarif için tıkla →</div>
      </div>`;
  });
}

// ── API istekleri ─────────────────────────────────────────────────────────────

async function apiPost(endpoint, body) {
  const res = await fetch(endpoint, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  });
  const data = await res.json();
  if (data.error) throw new Error(data.error);
  return data;
}

async function withLoading(btnId, spinnerId, errId, resultId, fn) {
  const btn     = document.getElementById(btnId);
  const spinner = document.getElementById(spinnerId);
  const errBox  = document.getElementById(errId);
  const resWrap = document.getElementById(resultId);

  btn.disabled = true;
  spinner.classList.add('show');
  errBox.style.display = 'none';
  resWrap.innerHTML = '';

  try {
    const data = await fn();
    renderCards(data.yemekler, resultId);
    resWrap.scrollIntoView({ behavior: 'smooth' });
  } catch (e) {
    errBox.textContent = '⚠️ ' + e.message;
    errBox.style.display = 'block';
  } finally {
    spinner.classList.remove('show');
    btn.disabled = false;
  }
}

// ── Olay dinleyicileri ────────────────────────────────────────────────────────

function getSuggestions() {
  withLoading('btn-suggest', 'suggest-spinner', 'suggest-error', 'suggest-results',
    () => apiPost('/api/suggest', {
      meal:    document.getElementById('meal').value,
      diet:    document.getElementById('diet').value,
      cuisine: document.getElementById('cuisine').value,
    })
  );
}

function getFridgeIdeas() {
  const text = document.getElementById('fridge-text').value.trim();
  if (!text) return;
  withLoading('btn-fridge', 'fridge-spinner', 'fridge-error', 'fridge-results',
    () => apiPost('/api/fridge', { text })
  );
}

// ── Modal ─────────────────────────────────────────────────────────────────────

function openModal(y) {
  document.getElementById('m-emoji').textContent   = y.emoji;
  document.getElementById('m-title').textContent   = y.isim;
  document.getElementById('m-kcal').innerHTML      =
    `⏱ ${y.sure} &nbsp;|&nbsp; 📊 ${y.zorluk} &nbsp;|&nbsp; 🔥 <span>${y.kalori} kcal</span>`;
  document.getElementById('m-protein').textContent = y.besin?.protein || '—';
  document.getElementById('m-carb').textContent    = y.besin?.karbonhidrat || '—';
  document.getElementById('m-fat').textContent     = y.besin?.yag || '—';
  document.getElementById('m-ingredients').innerHTML =
    (y.malzemeler || []).map(m => `<span class="ingredient">🥄 ${m}</span>`).join('');
  document.getElementById('m-recipe').textContent  = y.tarif;
  document.getElementById('overlay').classList.add('show');
}

function closeModal(e) {
  if (!e || e.target === document.getElementById('overlay') ||
      e.currentTarget.tagName === 'BUTTON') {
    document.getElementById('overlay').classList.remove('show');
  }
}
