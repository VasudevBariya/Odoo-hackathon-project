/* =========================================================
   TRAVELOOP — Minimal Frontend JS
   Tab toggling, password show/hide, duration calc,
   checklist animation, mobile notes panel toggle, delete confirm
   ========================================================= */
(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function () {

        // 1. Login / Signup tab toggle ------------------------------------
        document.querySelectorAll('.tl-tabs').forEach(function (tabs) {
            tabs.addEventListener('click', function (e) {
                var btn = e.target.closest('button[data-tl-tab]');
                if (!btn) return;
                var target = btn.getAttribute('data-tl-tab');
                tabs.querySelectorAll('button').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                document.querySelectorAll('[data-tl-pane]').forEach(function (pane) {
                    pane.style.display = (pane.getAttribute('data-tl-pane') === target) ? 'block' : 'none';
                });
            });
        });

        // 2. Password show / hide -----------------------------------------
        document.querySelectorAll('[data-tl-toggle-pw]').forEach(function (btn) {
            btn.addEventListener('click', function () {
                var input = document.getElementById(btn.getAttribute('data-tl-toggle-pw'));
                if (!input) return;
                input.type = input.type === 'password' ? 'text' : 'password';
                btn.innerHTML = input.type === 'password'
                    ? '<i class="fa-solid fa-eye"></i>'
                    : '<i class="fa-solid fa-eye-slash"></i>';
            });
        });

        // 3. Trip form — auto-calc duration_days --------------------------
        var startEl = document.getElementById('tl_start_date');
        var endEl   = document.getElementById('tl_end_date');
        var durEl   = document.getElementById('tl_duration_display');
        function recalcDuration() {
            if (!startEl || !endEl || !durEl) return;
            var s = startEl.value ? new Date(startEl.value) : null;
            var e = endEl.value ? new Date(endEl.value) : null;
            if (s && e) {
                if (e < s) {
                    durEl.textContent = '⚠ End date is before start date';
                    durEl.style.color = 'var(--danger)';
                    return;
                }
                var diff = Math.round((e - s) / 86400000) + 1;
                durEl.textContent = '📅 ' + diff + ' day' + (diff > 1 ? 's' : '');
                durEl.style.color = 'var(--text)';
            }
        }
        if (startEl) startEl.addEventListener('change', recalcDuration);
        if (endEl)   endEl.addEventListener('change', recalcDuration);

        // 4. Budget % display ---------------------------------------------
        document.querySelectorAll('[data-tl-budget]').forEach(function (el) {
            var spent  = parseFloat(el.getAttribute('data-spent')) || 0;
            var total  = parseFloat(el.getAttribute('data-total')) || 0;
            var pct    = total > 0 ? Math.min((spent / total) * 100, 999) : 0;
            var fill   = el.querySelector('.tl-progress-fill');
            if (fill) {
                fill.style.width = Math.min(pct, 100) + '%';
                if (spent > total) fill.classList.add('over');
            }
        });

        // 5. Checklist checkbox green flash -------------------------------
        document.querySelectorAll('.tl-check-row input[type=checkbox]').forEach(function (cb) {
            cb.addEventListener('change', function () {
                var row = cb.closest('.tl-check-row');
                if (!row) return;
                if (cb.checked) {
                    row.classList.add('packed', 'tl-flash');
                    setTimeout(() => row.classList.remove('tl-flash'), 600);
                } else {
                    row.classList.remove('packed');
                }
            });
        });

        // 6. Notes mobile panel toggle ------------------------------------
        document.querySelectorAll('[data-tl-open-note]').forEach(function (el) {
            el.addEventListener('click', function () {
                var layout = document.querySelector('.tl-notes-layout');
                if (layout && window.innerWidth < 992) {
                    layout.classList.add('show-editor');
                }
            });
        });
        document.querySelectorAll('[data-tl-back-list]').forEach(function (el) {
            el.addEventListener('click', function () {
                var layout = document.querySelector('.tl-notes-layout');
                if (layout) layout.classList.remove('show-editor');
            });
        });

        // 7. Delete confirmation modal ------------------------------------
        document.querySelectorAll('[data-tl-confirm-delete]').forEach(function (btn) {
            btn.addEventListener('click', function (e) {
                var msg = btn.getAttribute('data-tl-confirm-delete') || 'Are you sure you want to delete this?';
                if (!window.confirm(msg)) {
                    e.preventDefault();
                    e.stopPropagation();
                }
            });
        });

        // Unsaved-changes indicator on note editor
        var noteEditor = document.querySelector('.tl-note-textarea');
        var unsavedDot = document.querySelector('.tl-unsaved');
        if (noteEditor && unsavedDot) {
            unsavedDot.style.display = 'none';
            noteEditor.addEventListener('input', function () {
                unsavedDot.style.display = 'inline-block';
            });
        }
    });
})();
