/**
 * LangkahKampus - Dashboard JavaScript
 * Charts, tables, filters, export functionality
 */

document.addEventListener('DOMContentLoaded', function() {
    initDashboardCharts();
    initTableFilters();
    initSlotCounters();
});

/* === Dashboard Charts (Canvas-based) === */
function initDashboardCharts() {
    drawAcceptanceChart();
    drawSubjectChart();
}

function drawAcceptanceChart() {
    var canvas = document.getElementById('acceptanceChart');
    if (!canvas) return;

    var ctx = canvas.getContext('2d');
    var data = [
        { label: '2021', value: 72 },
        { label: '2022', value: 78 },
        { label: '2023', value: 82 },
        { label: '2024', value: 85 },
        { label: '2025', value: 88 }
    ];

    drawBarChart(ctx, canvas, data, '#1A73E8');
}

function drawSubjectChart() {
    var canvas = document.getElementById('subjectChart');
    if (!canvas) return;

    var ctx = canvas.getContext('2d');
    var data = [
        { label: 'MTK', value: 88 },
        { label: 'IND', value: 85 },
        { label: 'ENG', value: 82 },
        { label: 'FIS', value: 90 },
        { label: 'KIM', value: 86 },
        { label: 'BIO', value: 84 }
    ];

    drawBarChart(ctx, canvas, data, '#27AE60');
}

function drawBarChart(ctx, canvas, data, color) {
    var width = canvas.width = canvas.offsetWidth;
    var height = canvas.height = canvas.offsetHeight || 200;
    var padding = 40;
    var barWidth = (width - padding * 2) / data.length - 10;
    var maxValue = Math.max.apply(null, data.map(function(d) { return d.value; }));

    // Clear
    ctx.clearRect(0, 0, width, height);

    // Draw bars
    data.forEach(function(item, index) {
        var barHeight = ((item.value / maxValue) * (height - padding * 2));
        var x = padding + index * (barWidth + 10);
        var y = height - padding - barHeight;

        // Bar
        ctx.fillStyle = color;
        ctx.globalAlpha = 0.8;
        ctx.beginPath();
        ctx.roundRect(x, y, barWidth, barHeight, [4, 4, 0, 0]);
        ctx.fill();
        ctx.globalAlpha = 1;

        // Label
        ctx.fillStyle = '#6C757D';
        ctx.font = '11px Inter, sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(item.label, x + barWidth / 2, height - 15);

        // Value
        ctx.fillStyle = '#2C3E50';
        ctx.font = 'bold 12px Inter, sans-serif';
        ctx.fillText(item.value + '%', x + barWidth / 2, y - 8);
    });
}

/* === Table Filters === */
function initTableFilters() {
    var filterInputs = document.querySelectorAll('[data-filter-table]');

    filterInputs.forEach(function(input) {
        var tableId = input.getAttribute('data-filter-table');
        var table = document.getElementById(tableId);
        if (!table) return;

        input.addEventListener('input', function() {
            var query = this.value.toLowerCase();
            var rows = table.querySelectorAll('tbody tr');

            rows.forEach(function(row) {
                var text = row.textContent.toLowerCase();
                row.style.display = text.indexOf(query) !== -1 ? '' : 'none';
            });
        });
    });
}

/* === Slot Counters for Anti-Bentrok === */
function initSlotCounters() {
    var slotCells = document.querySelectorAll('[data-slot-animate]');

    slotCells.forEach(function(cell) {
        var target = parseInt(cell.textContent);
        if (isNaN(target)) return;

        cell.textContent = '0';

        var observer = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    animateSlotCounter(cell, target);
                    observer.unobserve(cell);
                }
            });
        }, { threshold: 0.5 });

        observer.observe(cell);
    });
}

function animateSlotCounter(element, target) {
    var current = 0;
    var duration = 1000;
    var steps = 30;
    var increment = target / steps;
    var stepTime = duration / steps;

    var timer = setInterval(function() {
        current += increment;
        if (current >= target) {
            current = target;
            clearInterval(timer);
        }
        element.textContent = Math.floor(current);
    }, stepTime);
}

/* === Export Table to CSV === */
function exportTableToCSV(tableId, filename) {
    var table = document.getElementById(tableId);
    if (!table) return;

    var csv = [];
    var rows = table.querySelectorAll('tr');

    rows.forEach(function(row) {
        var cols = row.querySelectorAll('td, th');
        var rowData = [];
        cols.forEach(function(col) {
            rowData.push('"' + col.textContent.trim().replace(/"/g, '""') + '"');
        });
        csv.push(rowData.join(','));
    });

    var blob = new Blob([csv.join('\n')], { type: 'text/csv;charset=utf-8;' });
    var link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = filename || 'export.csv';
    link.click();
}

/* === Refresh Slot Data === */
function refreshSlotData() {
    showToast('info', 'Memperbarui data slot...');

    // Simulate API call
    setTimeout(function() {
        showToast('success', 'Data slot berhasil diperbarui');
    }, 1500);
}
