/**
 * LangkahKampus - Metrics Dashboard JavaScript
 * Fetches system metrics via GET, renders stat cards, and auto-refreshes every 30 seconds
 */

document.addEventListener('DOMContentLoaded', function() {
    refreshMetrics();
    setInterval(refreshMetrics, 30000);
});

/* === Fetch and Render Metrics === */
function refreshMetrics() {
    ajaxRequest('../api/metrics.php', 'GET', null, function(error, response) {
        if (error) {
            showToast('danger', 'Gagal memuat metrics: ' + error);
            return;
        }

        var metrics = response.metrics || {};
        renderStatCards(metrics);
        renderPopularPrograms(metrics.popular_programs || []);
        renderSystemInfo(metrics);
        updateLastRefresh();
    });
}

/* === Render Main Stat Cards === */
function renderStatCards(metrics) {
    var totalEl = document.getElementById('totalPredictions');
    var avgEl = document.getElementById('avgResponseTime');
    var todayEl = document.getElementById('predictionsToday');
    var usersEl = document.getElementById('activeUsers');

    if (totalEl) {
        animateNumber(totalEl, parseInt(metrics.total_predictions) || 0);
    }
    if (avgEl) {
        animateNumber(avgEl, parseInt(metrics.avg_response_time_ms) || 0, 'ms');
    }
    if (todayEl) {
        animateNumber(todayEl, parseInt(metrics.predictions_today) || 0);
    }
    if (usersEl) {
        animateNumber(usersEl, parseInt(metrics.active_users) || 0);
    }
}

/* === Animate Number Counter === */
function animateNumber(element, target, suffix) {
    suffix = suffix || '';
    var current = parseInt(element.textContent) || 0;
    var steps = 30;
    var increment = (target - current) / steps;
    var stepTime = 500 / steps;
    var frame = 0;

    if (current === target) {
        element.textContent = target + suffix;
        return;
    }

    var timer = setInterval(function() {
        frame++;
        current += increment;
        if (frame >= steps) {
            current = target;
            clearInterval(timer);
        }
        element.textContent = Math.round(current) + suffix;
    }, stepTime);
}

/* === Render Popular Programs === */
function renderPopularPrograms(programs) {
    var container = document.getElementById('popularPrograms');
    if (!container) return;

    if (programs.length === 0) {
        container.innerHTML = '<p class="text-muted">Belum ada data program populer.</p>';
        return;
    }

    var maxCount = programs[0].count || 1;
    var html = '';

    programs.forEach(function(program, index) {
        var percentage = Math.round((program.count / maxCount) * 100);
        var colors = ['#3498DB', '#27AE60', '#F39C12', '#9B59B6', '#E74C3C'];
        var color = colors[index % colors.length];

        html += '<div style="margin-bottom:1rem;">' +
            '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.25rem;">' +
            '<span style="font-size:0.85rem;font-weight:600;">' + (index + 1) + '. ' + program.name + '</span>' +
            '<span style="font-size:0.8rem;color:' + color + ';font-weight:700;">' + program.count + ' prediksi</span>' +
            '</div>' +
            '<div style="height:6px;background:var(--color-bg);border-radius:3px;overflow:hidden;">' +
            '<div style="height:100%;width:' + percentage + '%;background:' + color + ';border-radius:3px;transition:width 0.8s ease;"></div>' +
            '</div></div>';
    });

    container.innerHTML = html;
}

/* === Render System Info === */
function renderSystemInfo(metrics) {
    var uptimeEl = document.getElementById('uptime');
    var versionEl = document.getElementById('modelVersion');
    var trainedEl = document.getElementById('lastTrained');

    if (uptimeEl && metrics.uptime_hours !== undefined) {
        var hours = parseInt(metrics.uptime_hours);
        var days = Math.floor(hours / 24);
        var remainingHours = hours % 24;
        uptimeEl.textContent = days > 0 ? days + 'd ' + remainingHours + 'h' : hours + 'h';
    }

    if (versionEl && metrics.model_version) {
        versionEl.textContent = metrics.model_version;
    }

    if (trainedEl && metrics.last_trained) {
        trainedEl.textContent = metrics.last_trained;
    }
}

/* === Update Last Refresh Timestamp === */
function updateLastRefresh() {
    var el = document.getElementById('lastUpdate');
    if (!el) return;

    var now = new Date();
    var timeStr = String(now.getHours()).padStart(2, '0') + ':' +
        String(now.getMinutes()).padStart(2, '0') + ':' +
        String(now.getSeconds()).padStart(2, '0');

    el.textContent = 'Terakhir diperbarui: ' + timeStr;
}
