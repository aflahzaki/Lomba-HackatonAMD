/**
 * LangkahKampus - Batch Prediction JavaScript
 * Handles CSV file parsing, batch API calls, color-coded table rendering, and CSV export
 */

document.addEventListener('DOMContentLoaded', function() {
    initFileUpload();
});

/* === Global State === */
var parsedStudents = [];
var batchResults = [];

/* === Initialize File Upload === */
function initFileUpload() {
    var uploadArea = document.getElementById('uploadArea');
    var fileInput = document.getElementById('csvFileInput');

    if (!uploadArea || !fileInput) return;

    // Click to upload
    uploadArea.addEventListener('click', function() {
        fileInput.click();
    });

    // File selected
    fileInput.addEventListener('change', function() {
        if (this.files && this.files[0]) {
            handleFile(this.files[0]);
        }
    });

    // Drag and drop
    uploadArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        uploadArea.style.borderColor = 'var(--color-accent-blue)';
        uploadArea.style.background = 'rgba(52,152,219,0.05)';
    });

    uploadArea.addEventListener('dragleave', function(e) {
        e.preventDefault();
        uploadArea.style.borderColor = 'var(--color-border)';
        uploadArea.style.background = '';
    });

    uploadArea.addEventListener('drop', function(e) {
        e.preventDefault();
        uploadArea.style.borderColor = 'var(--color-border)';
        uploadArea.style.background = '';

        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleFile(e.dataTransfer.files[0]);
        }
    });
}

/* === Handle File Selection === */
function handleFile(file) {
    if (!file.name.toLowerCase().endsWith('.csv')) {
        showToast('danger', 'Format file tidak valid. Gunakan file CSV.');
        return;
    }

    var reader = new FileReader();
    reader.onload = function(e) {
        var content = e.target.result;
        var parsed = parseCSV(content);

        if (parsed.length === 0) {
            showToast('danger', 'File CSV kosong atau format tidak sesuai.');
            return;
        }

        if (parsed.length > 500) {
            showToast('warning', 'Maksimal 500 baris. Hanya 500 baris pertama yang akan diproses.');
            parsed = parsed.slice(0, 500);
        }

        parsedStudents = parsed;

        // Show file info
        var fileInfo = document.getElementById('fileInfo');
        var fileName = document.getElementById('fileName');
        var fileRows = document.getElementById('fileRows');
        var submitBtn = document.getElementById('batchSubmitBtn');

        if (fileInfo) fileInfo.classList.remove('hidden');
        if (fileName) fileName.textContent = file.name;
        if (fileRows) fileRows.textContent = '(' + parsed.length + ' siswa)';
        if (submitBtn) submitBtn.disabled = false;

        showToast('success', parsed.length + ' data siswa berhasil dimuat.');
    };

    reader.onerror = function() {
        showToast('danger', 'Gagal membaca file. Pastikan file valid.');
    };

    reader.readAsText(file);
}

/* === Parse CSV Content === */
function parseCSV(content) {
    var lines = content.split(/\r\n|\n/).filter(function(line) {
        return line.trim() !== '';
    });

    if (lines.length < 2) return []; // Need header + at least 1 data row

    var headers = lines[0].split(',').map(function(h) {
        return h.trim().toLowerCase();
    });

    // Validate required headers
    var requiredHeaders = ['nama', 'nilai_rata_rata', 'peringkat', 'total_siswa', 'akreditasi', 'target_prodi'];
    var hasAllHeaders = requiredHeaders.every(function(req) {
        return headers.indexOf(req) !== -1;
    });

    if (!hasAllHeaders) {
        showToast('danger', 'Header CSV tidak lengkap. Diperlukan: ' + requiredHeaders.join(', '));
        return [];
    }

    var students = [];
    for (var i = 1; i < lines.length; i++) {
        var values = parseCSVLine(lines[i]);
        if (values.length < headers.length) continue;

        var student = {};
        headers.forEach(function(header, idx) {
            student[header] = values[idx] ? values[idx].trim() : '';
        });

        // Validate numeric fields
        if (student.nama && student.nilai_rata_rata) {
            students.push({
                nama: student.nama,
                nilai_rata_rata: parseFloat(student.nilai_rata_rata) || 0,
                peringkat: parseInt(student.peringkat) || 1,
                total_siswa: parseInt(student.total_siswa) || 100,
                akreditasi: student.akreditasi || 'B',
                target_prodi: student.target_prodi || '-'
            });
        }
    }

    return students;
}

/* === Parse a Single CSV Line (handle quoted fields) === */
function parseCSVLine(line) {
    var result = [];
    var current = '';
    var inQuotes = false;

    for (var i = 0; i < line.length; i++) {
        var char = line[i];

        if (char === '"') {
            inQuotes = !inQuotes;
        } else if (char === ',' && !inQuotes) {
            result.push(current);
            current = '';
        } else {
            current += char;
        }
    }
    result.push(current);

    return result;
}

/* === Submit Batch Prediction === */
function submitBatch() {
    if (parsedStudents.length === 0) {
        showToast('warning', 'Tidak ada data siswa untuk diproses.');
        return;
    }

    var submitBtn = document.getElementById('batchSubmitBtn');
    var loadingEl = document.getElementById('batchLoading');
    var resultsEl = document.getElementById('batchResults');

    // Show loading
    if (submitBtn) submitBtn.disabled = true;
    if (loadingEl) loadingEl.classList.remove('hidden');
    if (resultsEl) resultsEl.classList.add('hidden');

    var payload = {
        students: parsedStudents
    };

    ajaxRequest('../api/batch_predict.php', 'POST', payload, function(error, response) {
        if (loadingEl) loadingEl.classList.add('hidden');
        if (submitBtn) submitBtn.disabled = false;

        if (error) {
            showToast('danger', 'Gagal memproses prediksi batch: ' + error);
            return;
        }

        if (response.results && response.results.length > 0) {
            batchResults = response.results;
            renderResults(response.results);
            showToast('success', 'Prediksi batch selesai! ' + response.results.length + ' siswa diproses.');
        } else {
            showToast('warning', 'Tidak ada hasil yang dikembalikan.');
        }
    });
}

/* === Render Results Table === */
function renderResults(results) {
    var resultsSection = document.getElementById('batchResults');
    var tbody = document.getElementById('resultsBody');
    var summary = document.getElementById('resultSummary');

    if (!resultsSection || !tbody) return;

    resultsSection.classList.remove('hidden');

    // Count categories
    var highCount = 0;
    var medCount = 0;
    var lowCount = 0;

    tbody.innerHTML = '';

    results.forEach(function(result, index) {
        var prob = result.probability || 0;
        var color, bgColor, status;

        if (prob >= 70) {
            color = '#27AE60';
            bgColor = 'rgba(39,174,96,0.1)';
            status = 'Tinggi';
            highCount++;
        } else if (prob >= 40) {
            color = '#F39C12';
            bgColor = 'rgba(243,156,18,0.1)';
            status = 'Sedang';
            medCount++;
        } else {
            color = '#C0392B';
            bgColor = 'rgba(192,57,43,0.1)';
            status = 'Rendah';
            lowCount++;
        }

        var row = document.createElement('tr');
        row.style.cssText = 'border-bottom:1px solid var(--color-border);';
        row.innerHTML = '<td style="padding:0.75rem 0.5rem;">' + (index + 1) + '</td>' +
            '<td style="padding:0.75rem 0.5rem;font-weight:600;">' + escapeHtml(result.nama) + '</td>' +
            '<td style="padding:0.75rem 0.5rem;">' + result.nilai_rata_rata + '</td>' +
            '<td style="padding:0.75rem 0.5rem;">' + result.peringkat + '/' + result.total_siswa + '</td>' +
            '<td style="padding:0.75rem 0.5rem;">' + escapeHtml(result.akreditasi) + '</td>' +
            '<td style="padding:0.75rem 0.5rem;">' + escapeHtml(result.target_prodi) + '</td>' +
            '<td style="padding:0.75rem 0.5rem;">' +
            '<div style="display:flex;align-items:center;gap:0.5rem;">' +
            '<div style="width:60px;height:6px;background:var(--color-bg);border-radius:3px;overflow:hidden;">' +
            '<div style="height:100%;width:' + prob + '%;background:' + color + ';border-radius:3px;"></div></div>' +
            '<strong style="color:' + color + ';">' + prob + '%</strong></div></td>' +
            '<td style="padding:0.75rem 0.5rem;"><span style="background:' + bgColor + ';color:' + color + ';padding:0.25rem 0.75rem;border-radius:20px;font-size:0.8rem;font-weight:600;">' + status + '</span></td>';

        tbody.appendChild(row);
    });

    // Update summary cards
    var highEl = document.getElementById('highCount');
    var medEl = document.getElementById('medCount');
    var lowEl = document.getElementById('lowCount');

    if (highEl) highEl.textContent = highCount;
    if (medEl) medEl.textContent = medCount;
    if (lowEl) lowEl.textContent = lowCount;

    if (summary) {
        summary.textContent = results.length + ' siswa diproses';
    }

    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/* === Export Results to CSV === */
function exportCSV() {
    if (batchResults.length === 0) {
        showToast('warning', 'Tidak ada hasil untuk diekspor.');
        return;
    }

    var csvContent = 'No,Nama,Nilai Rata-rata,Peringkat,Total Siswa,Akreditasi,Target Prodi,Probabilitas (%),Status\n';

    batchResults.forEach(function(result, index) {
        var status = result.probability >= 70 ? 'Tinggi' : (result.probability >= 40 ? 'Sedang' : 'Rendah');
        csvContent += (index + 1) + ',' +
            '"' + (result.nama || '').replace(/"/g, '""') + '",' +
            (result.nilai_rata_rata || 0) + ',' +
            (result.peringkat || 0) + ',' +
            (result.total_siswa || 0) + ',' +
            (result.akreditasi || '') + ',' +
            '"' + (result.target_prodi || '').replace(/"/g, '""') + '",' +
            (result.probability || 0) + ',' +
            status + '\n';
    });

    var blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    var url = URL.createObjectURL(blob);
    var link = document.createElement('a');
    link.setAttribute('href', url);
    link.setAttribute('download', 'hasil_prediksi_batch_' + getDateString() + '.csv');
    link.style.display = 'none';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);

    showToast('success', 'File CSV berhasil diunduh.');
}

/* === Clear File === */
function clearFile() {
    parsedStudents = [];
    batchResults = [];

    var fileInput = document.getElementById('csvFileInput');
    var fileInfo = document.getElementById('fileInfo');
    var submitBtn = document.getElementById('batchSubmitBtn');
    var resultsSection = document.getElementById('batchResults');

    if (fileInput) fileInput.value = '';
    if (fileInfo) fileInfo.classList.add('hidden');
    if (submitBtn) submitBtn.disabled = true;
    if (resultsSection) resultsSection.classList.add('hidden');
}

/* === Utility: Escape HTML === */
function escapeHtml(str) {
    if (!str) return '';
    var div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

/* === Utility: Date String === */
function getDateString() {
    var now = new Date();
    return now.getFullYear() + '-' +
        String(now.getMonth() + 1).padStart(2, '0') + '-' +
        String(now.getDate()).padStart(2, '0');
}
