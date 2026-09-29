/* =====================================================================
   Constella Portal — Application Logic
   Constellation canvas, cosmic navigation, search, theming & PWA engine
   ===================================================================== */

(function () {
  'use strict';
  var S = window.SITE || { courses: [] };
  var $ = function (s, el) { return (el || document).querySelector(s); };
  var $$ = function (s, el) { return Array.prototype.slice.call((el || document).querySelectorAll(s)); };
  var esc = function (v) { return String(v == null ? '' : v).replace(/[&<>"']/g, function (c) { return ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'})[c]; }); };

  /* ---------- storage (fails quietly if the browser blocks it) ---------- */
  var OPENED_KEY = 'cs:opened';
  var opened = new Set();
  try { opened = new Set(JSON.parse(localStorage.getItem(OPENED_KEY) || '[]')); } catch (e) {}
  function saveOpened() { try { localStorage.setItem(OPENED_KEY, JSON.stringify(Array.from(opened))); } catch (e) {} }

  /* ---------- seeded random so every course keeps its own fixed shape ---------- */
  function hash(s) { var h = 2166136261; for (var i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); } return h >>> 0; }
  function mulberry(a) { return function () { a |= 0; a = a + 0x6D2B79F5 | 0; var t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }

  var W = 760, H = 280, PAD = 44;

  function layout(course) {
    var maxWeek = course.weeks.reduce(function (m, w) { return Math.max(m, w.week); }, 0);
    var n = Math.max(course.totalWeeks || 0, maxWeek, 2);
    var r = mulberry(hash(course.id));
    var phase = r() * 6.28, pts = [], dust = [], i;
    for (i = 0; i < n; i++) {
      var x = PAD + i * (W - 2 * PAD) / (n - 1);
      var y = H / 2 + Math.sin(i * 0.95 + phase) * 62 + (r() - 0.5) * 54;
      pts.push({ x: x, y: Math.max(44, Math.min(H - 52, y)) });
    }
    for (i = 0; i < 70 && dust.length < 40; i++) {
      var d = { x: r() * W, y: r() * H, r: 0.6 + r() * 1.3, o: 0.15 + r() * 0.3 };
      var clear = pts.every(function (p) { return Math.abs(p.x - d.x) > 26 || d.y < p.y - 26 || d.y > p.y + 44; });
      if (clear) dust.push(d);
    }
    return { n: n, pts: pts, dust: dust, maxWeek: maxWeek };
  }

  function pathD(pts) { return pts.map(function (p, i) { return (i ? 'L' : 'M') + p.x.toFixed(1) + ' ' + p.y.toFixed(1); }).join(''); }

  function skySVG(course, L) {
    var byWeek = {}; course.weeks.forEach(function (w) { byWeek[w.week] = w; });
    var gid = 'g-' + course.id;
    var stars = L.pts.map(function (p, i) {
      var wk = i + 1, w = byWeek[wk], fx = (p.x / W).toFixed(4), fy = (p.y / H).toFixed(4);
      var cx = p.x.toFixed(1), cy = p.y.toFixed(1);
      if (!w) {
        return '<g class="star off" data-week="' + wk + '" data-tip="Week ' + wk + '" data-sub="Coming soon" data-off="1" data-fx="' + fx + '" data-fy="' + fy + '">' +
          '<circle class="core" cx="' + cx + '" cy="' + cy + '" r="3.6"/>' +
          '<text class="wk" x="' + cx + '" y="' + (p.y + 26).toFixed(1) + '">' + wk + '</text></g>';
      }
      var isLatest = wk === L.maxWeek, key = course.id + ':' + wk;
      var label = 'Week ' + wk + ': ' + w.title;
      var delay = (0.3 + (i / Math.max(L.maxWeek - 1, 1)) * 1.6).toFixed(2);
      var when = fmtDate(w.date);
      var metaStr = [when, w.duration].filter(Boolean).join(' • ');
      var topicsStr = w.topics && w.topics.length ? w.topics.slice(0, 3).join(', ') + (w.topics.length > 3 ? '…' : '') : '';

      return '<a class="star' + (isLatest ? ' latest' : '') + '" href="' + esc(w.file) + '" data-key="' + esc(key) + '" data-label="' + esc(label) + '" aria-label="' + esc(label) + '"' +
        ' data-tip="' + esc(w.title) + '" data-sub="Week ' + wk + '" data-week="' + wk + '"' +
        (isLatest ? ' data-latest="1"' : '') +
        (metaStr ? ' data-meta="' + esc(metaStr) + '"' : '') +
        (topicsStr ? ' data-topics="' + esc(topicsStr) + '"' : '') +
        ' data-fx="' + fx + '" data-fy="' + fy + '" style="--d:' + delay + 's">' +
        (isLatest ? '<circle class="pulse" cx="' + cx + '" cy="' + cy + '" r="10"/>' : '') +
        '<circle class="halo" cx="' + cx + '" cy="' + cy + '" r="21" fill="url(#' + gid + ')"/>' +
        '<path class="spark" d="M' + (p.x - 15).toFixed(1) + ' ' + cy + 'H' + (p.x + 15).toFixed(1) + 'M' + cx + ' ' + (p.y - 15).toFixed(1) + 'V' + (p.y + 15).toFixed(1) + '"/>' +
        '<circle class="core" cx="' + cx + '" cy="' + cy + '" r="' + (isLatest ? 8.4 : 6.4) + '"/>' +
        '<text class="wk" x="' + cx + '" y="' + (p.y + 28).toFixed(1) + '">' + wk + '</text></a>';
    }).join('');

    var dust = L.dust.map(function (d) { return '<circle class="dust" cx="' + d.x.toFixed(1) + '" cy="' + d.y.toFixed(1) + '" r="' + d.r.toFixed(2) + '" opacity="' + d.o.toFixed(2) + '"/>'; }).join('');
    var live = L.maxWeek > 1 ? '<path class="path-live" d="' + pathD(L.pts.slice(0, L.maxWeek)) + '"/>' : '';
    var comet = L.maxWeek > 1 ? '<g class="comet" aria-hidden="true">' + [3.4, 3, 2.6, 2.2, 1.8, 1.4, 1.1, .8].map(function (r) { return '<circle r="' + r + '" cx="0" cy="0" opacity="0"/>'; }).join('') + '</g>' : '';

    return '<svg viewBox="0 0 ' + W + ' ' + H + '" role="group" aria-label="Sessions of ' + esc(course.title) + ' as a constellation">' +
      '<defs><radialGradient id="' + gid + '"><stop offset="0" style="stop-color:var(--acc);stop-opacity:.55"/><stop offset="1" style="stop-color:var(--acc);stop-opacity:0"/></radialGradient></defs>' +
      dust + '<path class="path-all" d="' + pathD(L.pts) + '"/>' + live + stars + comet + '</svg>';
  }

  function topicText(t) {
    t = t || [];
    var shown = t.slice(0, 4).join(', ');
    return t.length > 4 ? shown + ' and ' + (t.length - 4) + ' more' : shown;
  }
  function fmtDate(d) {
    if (!d) return '';
    var dt = new Date(d + 'T00:00:00');
    return isNaN(dt) ? '' : dt.toLocaleDateString('en-GB', { day: 'numeric', month: 'short' });
  }

  /* ---------- hero text ---------- */
  var title = S.title || 'Course Sessions';
  document.title = title + ' — Interactive Course Sessions';
  $('#brandName').textContent = title;
  var h1 = $('#heroTitle'), ci = 0;
  h1.setAttribute('aria-label', title);
  h1.innerHTML = title.split(/\s+/).map(function (w) {
    return '<span class="w" aria-hidden="true">' + w.split('').map(function (c) { return '<span class="ch" style="--i:' + (ci++) + '">' + esc(c) + '</span>'; }).join('') + '</span>';
  }).join(' ');
  $('#heroTag').textContent = S.tagline || '';
  var ownerLine = [S.owner ? 'By ' + S.owner : '', S.affiliation || ''].filter(Boolean).join(', ');
  $('#heroOwner').textContent = ownerLine; $('#heroOwner').hidden = !ownerLine;

  var courses = S.courses || [];
  var root = $('#courses');
  if (!courses.length) {
    $('#empty').hidden = false;
    $('#empty').textContent = 'No courses yet. Add your first course in courses.js.';
  }

  // the most recent session across all courses
  var featured = null;
  courses.forEach(function (c) {
    c.weeks.forEach(function (w) {
      var k = (w.date || '') + String(w.week).padStart(3, '0');
      if (!featured || k > featured.k) featured = { c: c, w: w, k: k };
    });
  });
  if (featured) {
    var lt = $('#latest');
    lt.hidden = false;
    lt.style.setProperty('--h', featured.c.hue == null ? 172 : featured.c.hue);
    lt.innerHTML = '<span class="where"><i class="dot"></i>Latest session, ' + esc(featured.c.title) + ' week ' + featured.w.week + '</span>' +
      '<span class="name">' + esc(featured.w.title) + '</span>' +
      '<a class="btn" href="' + esc(featured.w.file) + '" data-key="' + esc(featured.c.id + ':' + featured.w.week) + '">Open session</a>';
  }

  /* ---------- build the courses ---------- */
  var C1 = 2 * Math.PI * 32, C2 = 2 * Math.PI * 23;
  var courseEls = courses.map(function (course) {
    var L = layout(course);
    var weeksAsc = course.weeks.slice().sort(function (a, b) { return a.week - b.week; });
    var rows = weeksAsc.map(function (w, idx) {
      var key = course.id + ':' + w.week;
      var search = (w.title + ' ' + (w.topics || []).join(' ')).toLowerCase();
      var isLatest = w.week === L.maxWeek;
      var when = fmtDate(w.date);
      var metaStr = [when, w.duration].filter(Boolean).join(' • ');

      return '<li class="row' + (isLatest ? ' is-latest' : '') + '" style="--i:' + idx + '" data-key="' + esc(key) + '" data-search="' + esc(search) + '">' +
        '<div class="num">' + w.week + '<small>Week</small></div>' +
        '<div class="row-content">' +
          '<h3><a href="' + esc(w.file) + '" data-key="' + esc(key) + '">' + esc(w.title) + '</a></h3>' +
          '<p class="topics">' + esc(topicText(w.topics)) + '</p>' +
          '<div class="meta">' +
            (isLatest ? '<span class="badge new">New</span>' : '') +
            '<span class="badge done" data-done hidden>Opened</span>' +
            (metaStr ? '<span class="meta-info">' + esc(metaStr) + '</span>' : '') +
            '<span class="go">Open session <svg class="go-arrow" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 8h10M9 4l4 4-4 4"/></svg></span>' +
          '</div>' +
        '</div></li>';
    }).join('');

    var el = document.createElement('section');
    el.className = 'course';
    el.id = 'c-' + course.id;
    el.style.setProperty('--h', course.hue == null ? 172 : course.hue);
    el.innerHTML =
      '<div class="wrap">' +
      '<div class="course-head">' +
        '<div class="course-info"><h2>' + esc(course.title) + '</h2>' +
        (course.subtitle ? '<p class="sub">' + esc(course.subtitle) + '</p>' : '') +
        (course.description ? '<p class="desc">' + esc(course.description) + '</p>' : '') +
        '<div class="prog"><div class="ring" style="--c:' + C1.toFixed(1) + ';--c2:' + C2.toFixed(1) + ';--f:' + Math.min(1, course.weeks.length / L.n).toFixed(3) + ';--f2:0" role="img" aria-label="' + course.weeks.length + ' of ' + L.n + ' sessions published">' +
        '<svg viewBox="0 0 76 76" aria-hidden="true"><circle class="trk" cx="38" cy="38" r="32"/><circle class="o" cx="38" cy="38" r="32"/><circle class="trk" cx="38" cy="38" r="23" style="stroke-width:4"/><circle class="i" cx="38" cy="38" r="23"/></svg>' +
        '<em>' + course.weeks.length + '/' + L.n + '</em></div>' +
        '<div><span><b>' + course.weeks.length + '</b> of ' + L.n + ' sessions published</span><span data-mine>You opened 0 of ' + course.weeks.length + '</span></div></div></div>' +
        '<div class="col-sky"><div class="nebula" aria-hidden="true"></div>' +
        '<div class="sky-scroll-wrap">' +
          '<div class="sky-fade-l" aria-hidden="true"></div>' +
          '<div class="sky-scroll"><div class="sky">' + skySVG(course, L) + '</div></div>' +
          '<div class="sky-fade-r" aria-hidden="true"></div>' +
          '<div class="tip" role="tooltip" aria-hidden="true"><div class="tip-inner"></div><div class="tip-arrow" aria-hidden="true"></div></div>' +
        '</div>' +
        '<div class="sky-hint" aria-hidden="true">✦ Swipe to explore constellation ✦</div>' +
        '<ul class="legend"><li><span class="sw nw"></span>Newest</li><li><span class="sw"></span>Not opened yet</li><li><span class="sw op"></span>Opened</li><li><span class="sw of"></span>Coming soon</li></ul></div>' +
      '</div>' +
      '<ol class="rows">' + rows + '</ol></div>';
    root.appendChild(el);

    var live = $('.path-live', el), len = 0;
    if (live) { len = live.getTotalLength(); live.style.setProperty('--len', len.toFixed(1)); }
    return { el: el, course: course, path: live, len: len, comet: $$('.comet circle', el), cometAt: 0, cometOn: false };
  });

  /* ---------- constellation scroll fade update ---------- */
  $$('.sky-scroll').forEach(function(sc) {
    var wrap = sc.closest('.sky-scroll-wrap');
    if (!wrap) return;
    var fadeL = $('.sky-fade-l', wrap), fadeR = $('.sky-fade-r', wrap);
    function updateFade() {
      var max = sc.scrollWidth - sc.clientWidth;
      if (max > 12) {
        if (fadeL) fadeL.style.opacity = sc.scrollLeft > 14 ? '1' : '0';
        if (fadeR) fadeR.style.opacity = (max - sc.scrollLeft) > 14 ? '1' : '0';
      } else {
        if (fadeL) fadeL.style.opacity = '0';
        if (fadeR) fadeR.style.opacity = '0';
      }
    }
    sc.addEventListener('scroll', updateFade, { passive: true });
    sc.addEventListener('scroll', hideTips, { passive: true });
    window.addEventListener('resize', updateFade, { passive: true });
    setTimeout(updateFade, 120);
  });

  /* ---------- opened state ---------- */
  function refresh() {
    $$('.star[data-key], .row[data-key]').forEach(function (n) {
      var isOpen = opened.has(n.dataset.key);
      n.classList.toggle('opened', isOpen);
      var d = $('[data-done]', n); if (d) d.hidden = !isOpen;
      if (n.dataset.label) n.setAttribute('aria-label', n.dataset.label + (isOpen ? ' (opened)' : ''));
    });
    courseEls.forEach(function (ce) {
      var total = ce.course.weeks.length;
      var n = ce.course.weeks.filter(function (w) { return opened.has(ce.course.id + ':' + w.week); }).length;
      $('[data-mine]', ce.el).textContent = 'You opened ' + n + ' of ' + total;
      $('.ring', ce.el).style.setProperty('--f2', total ? (n / total).toFixed(3) : 0);
    });
  }
  refresh();

  $('#reset').addEventListener('click', function () {
    if (!opened.size || confirm('Clear the list of sessions you opened on this device?')) { opened.clear(); saveOpened(); refresh(); }
  });

  /* ---------- creative cosmic session transition ---------- */
  function clearPortals() {
    $$('.starlight-portal').forEach(function (p) {
      p.classList.remove('active');
      setTimeout(function () { if (p.parentNode) p.remove(); }, 200);
    });
  }
  window.addEventListener('pageshow', clearPortals);
  window.addEventListener('popstate', clearPortals);
  document.addEventListener('visibilitychange', function () { if (!document.hidden) clearPortals(); });
  clearPortals();

  function openSession(a, e) {
    var href = a.getAttribute('href');
    if (!href) return;
    clearPortals();

    var x = e && e.clientX, y = e && e.clientY;
    if (x == null || (e && !e.detail)) {
      var b = a.getBoundingClientRect();
      x = b.left + b.width / 2;
      y = b.top + b.height / 2;
    }
    var c = a.closest('.course');
    var hue = c ? c.style.getPropertyValue('--h') : '172';
    
    var portal = document.createElement('div');
    portal.className = 'starlight-portal';
    portal.style.setProperty('--x', (x || innerWidth / 2) + 'px');
    portal.style.setProperty('--y', (y || innerHeight / 2) + 'px');
    portal.style.setProperty('--wh', hue || '172');
    document.body.appendChild(portal);
    
    requestAnimationFrame(function () {
      requestAnimationFrame(function () {
        portal.classList.add('active');
      });
    });
    
    setTimeout(function () {
      location.href = href;
    }, 280);

    // Auto-remove portal after navigation so returning back via bfcache/browser history never stays stuck
    setTimeout(function () {
      if (portal && portal.parentNode) {
        portal.classList.remove('active');
        setTimeout(function () { if (portal.parentNode) portal.remove(); }, 250);
      }
    }, 700);
  }

  /* ---------- touch & click navigation ---------- */
  var touchedKey = null;

  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[data-key]');
    if (!a) return;
    opened.add(a.dataset.key); saveOpened(); refresh();
    if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || a.getAttribute('target') === '_blank') return;
    e.preventDefault();
    openSession(a, e);
  });

  document.addEventListener('auxclick', function (e) {
    var a = e.target.closest && e.target.closest('a[data-key]');
    if (a) { opened.add(a.dataset.key); saveOpened(); refresh(); }
  });

  /* ---------- hover link between stars and rows, tooltip, row spotlight ---------- */
  var lastKey = null;
  function setHl(key) {
    if (key === lastKey) return; lastKey = key;
    $$('.hl').forEach(function (n) { n.classList.remove('hl'); });
    if (key) $$('.row[data-key="' + key + '"], .star[data-key="' + key + '"]').forEach(function (n) { n.classList.add('hl'); });
  }
  function hideTips() {
    $$('.tip.on').forEach(function (t) { t.classList.remove('on'); });
  }

  function showTip(star) {
    var wrap = star.closest('.sky-scroll-wrap');
    if (!wrap) return;
    var tip = $('.tip', wrap);
    if (!tip) return;
    var inner = $('.tip-inner', tip) || tip;

    var isOff = star.classList.contains('off') || star.dataset.off === '1';
    var isLatest = star.classList.contains('latest') || star.dataset.latest === '1';
    var isOpen = star.dataset.key && opened.has(star.dataset.key);
    var wk = star.dataset.week || '';
    var title = star.dataset.tip || '';
    var meta = star.dataset.meta || '';
    var topics = star.dataset.topics || '';

    var badgeHtml = '';
    if (isOff) {
      badgeHtml = '<span class="tip-badge tip-badge-soon">Coming soon</span>';
    } else if (isLatest) {
      badgeHtml = '<span class="tip-badge tip-badge-new">✦ Newest</span>';
    } else if (isOpen) {
      badgeHtml = '<span class="tip-badge tip-badge-done">✓ Opened</span>';
    } else {
      badgeHtml = '<span class="tip-badge tip-badge-ready">Available</span>';
    }

    var weekHtml = wk ? '<div class="tip-week"><span class="tip-sparkle">✦</span> Week ' + esc(wk) + '</div>' : '';
    var metaHtml = meta ? '<div class="tip-meta"><span>⏱ ' + esc(meta) + '</span></div>' : '';
    var topicsHtml = topics ? '<div class="tip-topics">' + esc(topics) + '</div>' : '';
    var actionHtml = isOff
      ? '<div class="tip-action tip-action-soon">Unlocks in upcoming lectures</div>'
      : '<div class="tip-action"><span class="tip-action-text">Click to open session</span><span class="tip-action-arrow">↗</span></div>';

    inner.innerHTML =
      '<div class="tip-header">' + weekHtml + badgeHtml + '</div>' +
      '<div class="tip-title">' + esc(title) + '</div>' +
      (metaHtml || topicsHtml ? '<div class="tip-details">' + metaHtml + topicsHtml + '</div>' : '') +
      actionHtml;

    var wrapRect = wrap.getBoundingClientRect();
    var target = $('.core', star) || star;
    var starRect = target.getBoundingClientRect();
    var starCenterX = starRect.left + starRect.width / 2 - wrapRect.left;
    var starTopY = starRect.top - wrapRect.top;
    var starBottomY = starRect.bottom - wrapRect.top;
    var wrapWidth = wrap.clientWidth;

    tip.classList.add('measuring');
    var tipWidth = tip.offsetWidth || 280;
    var tipHeight = tip.offsetHeight || 90;
    tip.classList.remove('measuring');

    // Horizontal clamping: keep tooltip 100% inside wrap bounds
    var halfTip = tipWidth / 2;
    var minCenter = halfTip + 10;
    var maxCenter = wrapWidth - halfTip - 10;
    var center;
    if (maxCenter < minCenter) {
      center = wrapWidth / 2;
    } else {
      center = Math.max(minCenter, Math.min(starCenterX, maxCenter));
    }
    tip.style.left = center + 'px';

    // Position pointer arrow directly toward the star center
    var arrowOffset = starCenterX - center;
    var maxArrow = Math.max(0, halfTip - 22);
    arrowOffset = Math.max(-maxArrow, Math.min(arrowOffset, maxArrow));
    tip.style.setProperty('--arrow-x', arrowOffset + 'px');

    // Vertical placement: flip below if close to the top of the canvas
    var roomAbove = starTopY;
    if (roomAbove < tipHeight + 20) {
      tip.classList.add('tip-bottom');
      tip.style.top = (starBottomY + 12) + 'px';
    } else {
      tip.classList.remove('tip-bottom');
      tip.style.top = (starTopY - 12) + 'px';
    }

    tip.classList.add('on');
  }

  function onOver(e) {
    var star = e.target.closest && e.target.closest('.star');
    var keyed = e.target.closest && e.target.closest('[data-key]');
    setHl(keyed ? keyed.dataset.key : null);
    if (star) {
      showTip(star);
    } else {
      hideTips();
    }
  }
  root.addEventListener('mouseover', onOver);
  root.addEventListener('focusin', onOver);
  root.addEventListener('mouseleave', function () { setHl(null); hideTips(); });
  root.addEventListener('focusout', function () { setHl(null); hideTips(); });
  window.addEventListener('resize', hideTips);
  window.addEventListener('scroll', hideTips, { passive: true });

  // Touch tap handling for stars
  document.addEventListener('touchstart', function(e) {
    var star = e.target.closest && e.target.closest('.star');
    if (star) {
      var key = star.dataset.key || ('off-' + (star.dataset.week || ''));
      if (key && touchedKey !== key) {
        touchedKey = key;
        setHl(star.dataset.key || null);
        hideTips();
        showTip(star);
        return;
      }
    } else if (!e.target.closest('.tip') && !e.target.closest('.row')) {
      touchedKey = null;
      hideTips();
    }
  }, { passive: true });

  root.addEventListener('mousemove', function (e) {
    var row = e.target.closest && e.target.closest('.row');
    if (!row) return;
    var r = row.getBoundingClientRect();
    row.style.setProperty('--mx', (e.clientX - r.left) + 'px');
    row.style.setProperty('--my', (e.clientY - r.top) + 'px');
  });

  /* ---------- search with clear button ---------- */
  var input = $('#q');
  var clearBtn = $('#searchClear');
  function applyFilter() {
    var q = input.value.trim().toLowerCase(), any = false;
    if (clearBtn) clearBtn.hidden = !input.value;
    courseEls.forEach(function (ce) {
      var courseMatch = !q || (ce.course.title + ' ' + (ce.course.subtitle || '')).toLowerCase().indexOf(q) > -1;
      var shown = 0;
      $$('.row', ce.el).forEach(function (r) {
        var m = courseMatch || r.dataset.search.indexOf(q) > -1;
        r.hidden = !m; if (m) shown++;
        var s = $('.star[data-key="' + r.dataset.key + '"]', ce.el); if (s) s.classList.toggle('dim', !m);
      });
      ce.el.hidden = shown === 0;
      if (shown) any = true;
    });
    var empty = $('#empty');
    if (courses.length) {
      empty.hidden = any;
      empty.textContent = 'Nothing matches “' + input.value.trim() + '”. Try a topic like loops or functions.';
    }
  }
  input.addEventListener('input', applyFilter);
  if (clearBtn) {
    clearBtn.addEventListener('click', function () {
      input.value = '';
      applyFilter();
      input.focus();
    });
  }
  document.addEventListener('keydown', function (e) {
    if (e.key === '/' && document.activeElement !== input && !/input|textarea/i.test(document.activeElement.tagName)) { e.preventDefault(); input.focus(); }
    if (e.key === 'Escape' && document.activeElement === input) { input.value = ''; applyFilter(); input.blur(); }
  });

  /* ---------- theme, with a circular reveal where supported ---------- */
  var isLight = document.documentElement.dataset.theme === 'light';
  var themeMeta = $('#themeColorMeta');
  function updateThemeMeta(theme) {
    if (themeMeta) themeMeta.setAttribute('content', theme === 'light' ? '#f4f6fc' : '#070b17');
  }
  function applyTheme(next) {
    document.documentElement.dataset.theme = next; isLight = next === 'light';
    updateThemeMeta(next);
    try {
      localStorage.setItem('cs:theme', next);
      localStorage.setItem('deck_theme', next);
    } catch (e) {}
  }
  window.addEventListener('storage', function (e) {
    if (e.key === 'cs:theme' || e.key === 'deck_theme') {
      var next = (e.newValue === 'light') ? 'light' : 'dark';
      if (document.documentElement.dataset.theme !== next) {
        applyTheme(next);
      }
    }
  });
  $('#theme').addEventListener('click', function (e) {
    var next = document.documentElement.dataset.theme === 'light' ? 'dark' : 'light';
    if (!document.startViewTransition) { applyTheme(next); return; }
    var b = e.currentTarget.getBoundingClientRect(), x = b.left + b.width / 2, y = b.top + b.height / 2;
    var r = Math.hypot(Math.max(x, innerWidth - x), Math.max(y, innerHeight - y));
    var t = document.startViewTransition(function () { applyTheme(next); });
    t.ready.then(function () {
      document.documentElement.animate(
        { clipPath: ['circle(0px at ' + x + 'px ' + y + 'px)', 'circle(' + r + 'px at ' + x + 'px ' + y + 'px)'] },
        { duration: 650, easing: 'cubic-bezier(.6,0,.2,1)', pseudoElement: '::view-transition-new(root)' }
      );
    }).catch(function () {});
  });

  /* ---------- reveal each course when it scrolls into view (smooth threshold) ---------- */
  function enter(ce) { ce.el.classList.add('in'); ce.cometAt = performance.now() + 2400; }
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var ce = courseEls.filter(function (c) { return c.el === en.target; })[0];
        if (ce) enter(ce); io.unobserve(en.target);
      });
    }, { threshold: 0.05, rootMargin: '100px 0px 100px 0px' });
    courseEls.forEach(function (ce) { io.observe(ce.el); });
  } else {
    courseEls.forEach(enter);
  }

  /* ---------- scroll progress bar ---------- */
  var bar = $('#bar');
  function onScroll() {
    var max = document.documentElement.scrollHeight - innerHeight;
    bar.style.transform = 'scaleX(' + (max > 0 ? Math.min(1, scrollY / max) : 0).toFixed(4) + ')';
  }
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();

  /* ---------- latest card: pointer tilt + glow follow (desktop only) ---------- */
  var latestCard = $('#latest');
  if (latestCard && window.matchMedia('(hover: hover)').matches) {
    latestCard.addEventListener('pointermove', function (e) {
      var r = latestCard.getBoundingClientRect();
      var px = (e.clientX - r.left) / r.width, py = (e.clientY - r.top) / r.height;
      latestCard.style.setProperty('--mx', (px * 100).toFixed(1) + '%');
      latestCard.style.setProperty('--my', (py * 100).toFixed(1) + '%');
      latestCard.style.transform = 'perspective(700px) rotateX(' + ((0.5 - py) * 7).toFixed(2) + 'deg) rotateY(' + ((px - 0.5) * 9).toFixed(2) + 'deg)';
    });
    latestCard.addEventListener('pointerleave', function () { latestCard.style.transform = 'perspective(700px) rotateX(0) rotateY(0)'; });
  }

  /* =====================================================================
     the living sky: twinkling stars, parallax on scroll, shooting stars,
     and constellations that connect under the cursor (battery optimized)
     ===================================================================== */
  var cv = $('#stars'), ctx = cv.getContext('2d');
  var vw = 0, vh = 0, sky = [], mx = -999, my = -999, shoot = null, nextShoot = 0, last = 0;
  var isPageVisible = true;

  function initSky() {
    var dpr = Math.min(window.devicePixelRatio || 1, 1.5);
    vw = innerWidth; vh = innerHeight;
    cv.width = vw * dpr; cv.height = vh * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    var r = mulberry(20260922), n = Math.min(vw < 640 ? 110 : (vw < 900 ? 180 : 300), Math.round(vw * vh / 5200));
    sky = [];
    for (var i = 0; i < n; i++) {
      var z = 0.2 + r() * 0.8;
      sky.push({ x: r() * vw, y: r() * vh, z: z, r: 0.35 + z * 1.05, a: 0.25 + z * 0.6, sp: 0.6 + r() * 1.8, ph: r() * 6.28, warm: r() > 0.86 });
    }
  }

  function draw(now, dt, still) {
    ctx.clearRect(0, 0, vw, vh);
    var sy = still ? 0 : (window.scrollY || 0), t = now / 1000;
    var px = still || mx < 0 ? 0 : (mx / vw - 0.5), py = still || my < 0 ? 0 : (my / vh - 0.5);
    var near = [], R = 150, i, s, x, y, a;
    for (i = 0; i < sky.length; i++) {
      s = sky[i];
      x = s.x - px * 16 * s.z;
      y = (((s.y - sy * 0.14 * s.z) % vh) + vh) % vh - py * 16 * s.z;
      a = s.a * (still ? 1 : 0.62 + 0.38 * Math.sin(t * s.sp + s.ph));
      ctx.beginPath(); ctx.arc(x, y, s.r, 0, 6.2832);
      ctx.fillStyle = isLight ? 'rgba(15,22,60,' + (a * 0.22).toFixed(3) + ')' : (s.warm ? 'rgba(255,212,121,' : 'rgba(210,220,255,') + a.toFixed(3) + ')';
      ctx.fill();
      if (!still && mx > 0) {
        var dx = x - mx, dy = y - my, d = Math.sqrt(dx * dx + dy * dy);
        if (d < R) near.push({ x: x, y: y, d: d, r: s.r });
      }
    }
    if (near.length) {
      near.sort(function (p, q) { return p.d - q.d; });
      near = near.slice(0, 10);
      var lc = isLight ? '25,35,110' : '190,200,255', hc = isLight ? '25,35,110' : '255,225,150';
      ctx.lineWidth = 1;
      for (i = 0; i < near.length; i++) {
        var p = near[i], f = 1 - p.d / R;
        for (var j = i + 1; j < near.length; j++) {
          var q = near[j], ddx = p.x - q.x, ddy = p.y - q.y, dd = Math.sqrt(ddx * ddx + ddy * ddy);
          if (dd < 120) {
            ctx.strokeStyle = 'rgba(' + lc + ',' + (0.32 * f * (1 - dd / 120) * (isLight ? 1.2 : 1)).toFixed(3) + ')';
            ctx.beginPath(); ctx.moveTo(p.x, p.y); ctx.lineTo(q.x, q.y); ctx.stroke();
          }
        }
        ctx.fillStyle = 'rgba(' + hc + ',' + (0.35 + 0.55 * f).toFixed(3) + ')';
        ctx.beginPath(); ctx.arc(p.x, p.y, p.r + 1 + 1.6 * f, 0, 6.2832); ctx.fill();
      }
      ctx.strokeStyle = 'rgba(' + lc + ',' + (0.28 * (1 - near[0].d / R)).toFixed(3) + ')';
      ctx.beginPath(); ctx.moveTo(mx, my); ctx.lineTo(near[0].x, near[0].y); ctx.stroke();
    }
    if (still) return;

    /* shooting star every so often (dark theme only) */
    if (!isLight && !shoot && now > nextShoot) {
      var ang = (18 + Math.random() * 22) * Math.PI / 180, sp = 950 + Math.random() * 500;
      shoot = { x: Math.random() * vw * 0.65, y: Math.random() * vh * 0.3, vx: Math.cos(ang) * sp, vy: Math.sin(ang) * sp, life: 0, max: 0.85 };
    }
    if (shoot) {
      shoot.life += dt; shoot.x += shoot.vx * dt; shoot.y += shoot.vy * dt;
      var k = 1 - shoot.life / shoot.max;
      if (k <= 0) { shoot = null; nextShoot = now + 7000 + Math.random() * 8000; }
      else {
        var tx = shoot.x - shoot.vx * 0.16, ty = shoot.y - shoot.vy * 0.16;
        var g = ctx.createLinearGradient(tx, ty, shoot.x, shoot.y);
        g.addColorStop(0, 'rgba(255,255,255,0)'); g.addColorStop(1, 'rgba(255,240,200,' + (0.9 * k).toFixed(3) + ')');
        ctx.strokeStyle = g; ctx.lineWidth = 1.8; ctx.lineCap = 'round';
        ctx.beginPath(); ctx.moveTo(tx, ty); ctx.lineTo(shoot.x, shoot.y); ctx.stroke();
      }
    }
    cometTick(now);
  }

  function cometTick(now) {
    for (var c = 0; c < courseEls.length; c++) {
      var ce = courseEls[c];
      if (!ce.path || !ce.len || !ce.cometAt || now < ce.cometAt || ce.el.hidden) continue;
      var cycle = 7000, run = 5000, ph = (now - ce.cometAt) % cycle, els = ce.comet;
      if (ph >= run) {
        if (ce.cometOn) { for (var z = 0; z < els.length; z++) els[z].setAttribute('opacity', 0); ce.cometOn = false; }
        continue;
      }
      ce.cometOn = true;
      var t = ph / run, e = t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
      var fade = t > 0.93 ? (1 - t) / 0.07 : 1;
      for (var k = 0; k < els.length; k++) {
        var pt = ce.path.getPointAtLength(Math.max(0, e - k * 0.011) * ce.len);
        els[k].setAttribute('cx', pt.x); els[k].setAttribute('cy', pt.y);
        els[k].setAttribute('opacity', ((1 - k / els.length) * 0.95 * fade).toFixed(3));
      }
    }
  }

  function loop(now) {
    if (!isPageVisible) return;
    var dt = last ? Math.min(0.05, (now - last) / 1000) : 0.016; last = now;
    draw(now, dt, false);
    requestAnimationFrame(loop);
  }

  /* Page visibility battery saver */
  document.addEventListener('visibilitychange', function () {
    isPageVisible = !document.hidden;
    if (isPageVisible) {
      last = performance.now();
      requestAnimationFrame(loop);
    }
  });

  window.addEventListener('pointermove', function (e) { if (e.pointerType !== 'touch') { mx = e.clientX; my = e.clientY; } }, { passive: true });
  document.documentElement.addEventListener('mouseleave', function () { mx = my = -999; });
  var rz; window.addEventListener('resize', function () { clearTimeout(rz); rz = setTimeout(initSky, 200); });
  initSky();
  nextShoot = performance.now() + 4500;
  requestAnimationFrame(loop);

  /* =====================================================================
     PWA Integration: Service Worker Auto-Update & Immediate Activation
     ===================================================================== */
  var refreshing = false;
  var updateToast = $('#updateToast');
  var updateReloadBtn = $('#updateReloadBtn');
  var checkUpdateBtn = $('#checkUpdateBtn');
  var newWorkerWaiting = null;
  var swRegistration = null;

  function promptUserForUpdate(worker) {
    newWorkerWaiting = worker;
    if (updateToast) {
      updateToast.hidden = false;
      if (updateReloadBtn) {
        updateReloadBtn.disabled = false;
        updateReloadBtn.textContent = 'Update Now';
      }
    }
  }

  function triggerUpdateReload() {
    if (updateReloadBtn) {
      updateReloadBtn.disabled = true;
      updateReloadBtn.textContent = 'Updating...';
    }

    var reloaded = false;
    function doReload() {
      if (reloaded) return;
      reloaded = true;
      window.location.reload();
    }

    // 1. Tell new waiting worker to activate immediately
    if (newWorkerWaiting) {
      try {
        newWorkerWaiting.postMessage({ type: 'SKIP_WAITING' });
      } catch (e) {}
    }

    if (swRegistration && swRegistration.waiting) {
      try {
        swRegistration.waiting.postMessage({ type: 'SKIP_WAITING' });
      } catch (e) {}
    }

    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.getRegistration().then(function (reg) {
        if (reg && reg.waiting) {
          try {
            reg.waiting.postMessage({ type: 'SKIP_WAITING' });
          } catch (e) {}
        }
      }).catch(function () {});

      // 2. When controller changes, reload
      navigator.serviceWorker.addEventListener('controllerchange', function () {
        doReload();
      }, { once: true });
    }

    // 3. Fallback: if controllerchange doesn't fire within 350ms, reload anyway
    setTimeout(doReload, 350);
  }

  if (updateReloadBtn) {
    updateReloadBtn.addEventListener('click', triggerUpdateReload);
  }

  if ('serviceWorker' in navigator) {
    // When the new worker takes control, reload seamlessly to render new content
    navigator.serviceWorker.addEventListener('controllerchange', function () {
      if (refreshing) return;
      refreshing = true;
      window.location.reload();
    });

    window.addEventListener('load', function () {
      navigator.serviceWorker.register('./sw.js').then(function (reg) {
        swRegistration = reg;
        console.log('[PWA] Service Worker registered:', reg.scope);

        // 1. Force immediate update check on initial page load
        reg.update().catch(function () {});

        // 2. Force check whenever tab / PWA window is brought to foreground
        document.addEventListener('visibilitychange', function () {
          if (!document.hidden) {
            reg.update().catch(function () {});
          }
        });

        // 3. Periodic check every 2 minutes
        setInterval(function () {
          reg.update().catch(function () {});
        }, 2 * 60 * 1000);

        // 4. If a worker is already waiting in background
        if (reg.waiting && navigator.serviceWorker.controller) {
          promptUserForUpdate(reg.waiting);
        }

        // 5. When an update is detected and installed
        reg.addEventListener('updatefound', function () {
          var newWorker = reg.installing;
          if (!newWorker) return;
          newWorker.addEventListener('statechange', function () {
            if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
              // New version is installed and waiting
              promptUserForUpdate(newWorker);
            }
          });
        });

        // 6. Manual "Check for updates" button in footer
        if (checkUpdateBtn) {
          checkUpdateBtn.addEventListener('click', function () {
            checkUpdateBtn.textContent = 'Checking...';
            reg.update().then(function () {
              setTimeout(function () {
                if (reg.waiting) {
                  promptUserForUpdate(reg.waiting);
                  checkUpdateBtn.textContent = 'Update available!';
                  setTimeout(function () { checkUpdateBtn.textContent = 'Check for updates'; }, 3000);
                } else {
                  checkUpdateBtn.textContent = 'Up to date ✓';
                  setTimeout(function () { checkUpdateBtn.textContent = 'Check for updates'; }, 2500);
                }
              }, 1200);
            }).catch(function () {
              checkUpdateBtn.textContent = 'Check for updates';
            });
          });
        }
      }).catch(function (err) {
        console.warn('[PWA] Service Worker registration failed:', err);
      });
    });
  }

  var deferredPrompt = null;
  var installHeaderBtn = $('#installHeaderBtn');
  var installPrompt = $('#installPrompt');
  var iosModal = $('#iosModal');
  var isStandalone = window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone === true;
  var isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;
  var isDismissed = false;
  try { isDismissed = localStorage.getItem('cs:install-dismissed') === '1'; } catch (e) {}

  if (!isStandalone) {
    window.addEventListener('beforeinstallprompt', function (e) {
      e.preventDefault();
      deferredPrompt = e;
      if (installHeaderBtn) installHeaderBtn.hidden = false;
      if (installPrompt && !isDismissed) installPrompt.hidden = false;
    });

    if (isIOS) {
      if (installHeaderBtn) installHeaderBtn.hidden = false;
      if (installPrompt && !isDismissed) installPrompt.hidden = false;
    }
  }

  function handleInstallClick() {
    if (deferredPrompt) {
      deferredPrompt.prompt();
      deferredPrompt.userChoice.then(function (choice) {
        if (choice.outcome === 'accepted') {
          if (installPrompt) installPrompt.hidden = true;
          if (installHeaderBtn) installHeaderBtn.hidden = true;
        }
        deferredPrompt = null;
      });
    } else if (isIOS) {
      if (iosModal) iosModal.hidden = false;
    }
  }

  if (installHeaderBtn) installHeaderBtn.addEventListener('click', handleInstallClick);
  if ($('#instAccept')) $('#instAccept').addEventListener('click', handleInstallClick);
  if ($('#instDismiss')) $('#instDismiss').addEventListener('click', function () {
    if (installPrompt) installPrompt.hidden = true;
    try { localStorage.setItem('cs:install-dismissed', '1'); } catch (e) {}
  });
  if ($('#iosClose')) $('#iosClose').addEventListener('click', function () { if (iosModal) iosModal.hidden = true; });
  if ($('#iosBackdrop')) $('#iosBackdrop').addEventListener('click', function () { if (iosModal) iosModal.hidden = true; });
  if ($('#iosGotIt')) $('#iosGotIt').addEventListener('click', function () {
    if (iosModal) iosModal.hidden = true;
    if (installPrompt) installPrompt.hidden = true;
    try { localStorage.setItem('cs:install-dismissed', '1'); } catch (e) {}
  });

  /* Online / Offline status notification */
  var offlineToast = $('#offlineToast');
  function updateOnlineStatus() {
    if (!offlineToast) return;
    offlineToast.hidden = navigator.onLine;
  }
  window.addEventListener('online', updateOnlineStatus);
  window.addEventListener('offline', updateOnlineStatus);
  updateOnlineStatus();

})();
