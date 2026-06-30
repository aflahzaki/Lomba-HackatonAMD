/**
 * LangkahKampus - Predictions JavaScript
 * Handles dynamic subjects, prediction form, result visualization,
 * variable breakdown, admission history, probability gauge,
 * Choice-2 trap warning, anti-bentrok stats, and recommendations
 */

document.addEventListener('DOMContentLoaded', function() {
    initDynamicSubjects();
    initPredictionForm();
    initProgramSearch();
});

/* === Dynamic Subject Inputs Based on Jurusan === */
function initDynamicSubjects() {
    var selector = document.getElementById('jurusanSelector');
    if (!selector) return;

    selector.addEventListener('change', function() {
        var jurusan = this.value;
        var container = document.getElementById('subjectsContainer');
        var addBtn = document.getElementById('addCustomSubjectBtn');

        if (!jurusan) {
            container.innerHTML = '<p class="text-muted" style="font-style:italic;">Pilih jurusan terlebih dahulu untuk menampilkan mata pelajaran.</p>';
            if (addBtn) addBtn.style.display = 'none';
            return;
        }

        // Show loading
        container.innerHTML = '<p class="text-muted"><i class="fas fa-spinner fa-spin"></i> Memuat mata pelajaran...</p>';

        // Fetch subjects from API
        ajaxRequest('../api/get_subjects.php?jurusan=' + encodeURIComponent(jurusan), 'GET', null, function(error, response) {
            if (error) {
                container.innerHTML = '<p class="text-muted" style="color:#C0392B;">Gagal memuat mata pelajaran. Silakan tambahkan secara manual.</p>';
                if (addBtn) addBtn.style.display = 'inline-block';
                return;
            }

            var subjects = response.subjects || [];
            container.innerHTML = '';

            if (subjects.length === 0) {
                container.innerHTML = '<p class="text-muted" style="font-style:italic;">Tidak ada data mata pelajaran untuk jurusan ini. Gunakan tombol di bawah untuk menambahkan secara manual.</p>';
            } else {
                subjects.forEach(function(subject) {
                    container.appendChild(createSubjectRow(subject));
                });
            }

            // Show add custom button
            if (addBtn) addBtn.style.display = 'inline-block';
        });
    });
}

/* === Create a Subject Input Row === */
function createSubjectRow(subjectName, isCustom) {
    var safeKey = subjectName.toLowerCase().replace(/[^a-z0-9]/g, '_');
    var row = document.createElement('div');
    row.className = 'mb-2 subject-row';
    row.setAttribute('data-subject', subjectName);

    var labelHtml = '';
    if (isCustom) {
        labelHtml = '<div class="d-flex align-center gap-1 mb-1">' +
            '<input type="text" class="form-control custom-subject-name" placeholder="Nama Mata Pelajaran" value="' + subjectName + '" style="flex:1;font-size:0.85rem;">' +
            '<button type="button" class="btn btn-outline" style="font-size:0.75rem;padding:0.25rem 0.5rem;color:#C0392B;border-color:#C0392B;" onclick="removeSubjectRow(this)">' +
            '<i class="fas fa-times"></i></button></div>';
    } else {
        labelHtml = '<label class="form-label">' + subjectName + '</label>';
    }

    var inputsHtml = '<div class="form-row" style="grid-template-columns:repeat(5,1fr);">';
    for (var sem = 1; sem <= 5; sem++) {
        inputsHtml += '<div class="form-group" style="margin-bottom:0.5rem;">' +
            '<input type="number" name="subject_' + safeKey + '_sem' + sem + '" ' +
            'class="form-control subject-score" placeholder="S' + sem + '" ' +
            'min="0" max="100" step="0.01" data-subject="' + subjectName + '" data-sem="' + sem + '" required>' +
            '</div>';
    }
    inputsHtml += '</div>';

    row.innerHTML = labelHtml + inputsHtml;
    return row;
}

/* === Add Custom Subject === */
function addCustomSubject() {
    var container = document.getElementById('subjectsContainer');
    if (!container) return;

    var customName = 'Mata Pelajaran Tambahan';
    var row = createSubjectRow(customName, true);
    container.appendChild(row);

    // Focus the name input
    var nameInput = row.querySelector('.custom-subject-name');
    if (nameInput) {
        nameInput.focus();
        nameInput.select();
    }
}

/* === Remove a Subject Row === */
function removeSubjectRow(btn) {
    var row = btn.closest('.subject-row');
    if (row) row.remove();
}

/* === Prediction Form Handler === */
function initPredictionForm() {
    var form = document.getElementById('predictionForm');
    if (!form) return;

    form.addEventListener('submit', function(e) {
        e.preventDefault();

        if (!validateForm(form)) return;

        // Show loading
        var submitBtn = form.querySelector('button[type="submit"]');
        var originalBtnText = submitBtn.innerHTML;

        submitBtn.innerHTML = '<div class="spinner" style="width:20px;height:20px;margin:0 auto;border-width:2px;"></div>';
        submitBtn.disabled = true;

        // Collect form data
        var formData = collectPredictionData(form);

        // Submit to API
        ajaxRequest('../api/predict.php', 'POST', formData, function(error, response) {
            submitBtn.innerHTML = originalBtnText;
            submitBtn.disabled = false;

            if (error) {
                showToast('danger', 'Gagal memproses prediksi: ' + error);
                return;
            }

            displayPredictionResult(response);
            displayVariableBreakdown(response.variables || []);
            displayAdmissionHistory(response.admission_history || []);
            displayChoice2Trap(response);
            displayAntiBentrokStats(response);
            displayRecommendations(response);
            displayWhatIfSimulator(response);
        });
    });
}

/* === Collect Form Data (Dynamic Subjects) === */
function collectPredictionData(form) {
    var data = {
        scores: {},
        school_ranking: parseInt(form.querySelector('[name="school_ranking"]').value) || 0,
        total_students: parseInt(form.querySelector('[name="total_students"]').value) || 0,
        school_accreditation: form.querySelector('[name="school_accreditation"]').value,
        target_program_id: form.querySelector('[name="target_program"]').value,
        jurusan: form.querySelector('[name="jurusan"]').value
    };

    // Collect semester scores dynamically from all subject rows
    var subjectRows = document.querySelectorAll('#subjectsContainer .subject-row');
    subjectRows.forEach(function(row) {
        // Determine subject name
        var subjectName = '';
        var customNameInput = row.querySelector('.custom-subject-name');
        if (customNameInput) {
            subjectName = customNameInput.value.trim() || 'Custom';
        } else {
            subjectName = row.getAttribute('data-subject') || 'Unknown';
        }

        // Collect scores for this subject
        var scoreInputs = row.querySelectorAll('.subject-score');
        var semesterScores = {};
        scoreInputs.forEach(function(input) {
            var sem = input.getAttribute('data-sem');
            semesterScores['sem' + sem] = parseFloat(input.value) || 0;
        });

        data.scores[subjectName] = semesterScores;
    });

    return data;
}

/* === Display Prediction Result (Gauge) === */
function displayPredictionResult(response) {
    var resultSection = document.getElementById('predictionResult');
    if (!resultSection) return;

    resultSection.classList.remove('hidden');
    resultSection.scrollIntoView({ behavior: 'smooth', block: 'start' });

    var probability = response.probability || 0;
    var confidence_lower = response.confidence_lower || 0;
    var confidence_upper = response.confidence_upper || 0;

    // Animate gauge
    animateGauge(probability);

    // Update confidence interval
    updateConfidenceBar(probability, confidence_lower, confidence_upper);

    // Update text
    var statusEl = document.getElementById('predictionStatus');
    if (statusEl) {
        var color = probability >= 70 ? 'green' : (probability >= 40 ? 'orange' : 'red');
        var status = probability >= 70 ? 'Peluang Tinggi' : (probability >= 40 ? 'Peluang Sedang' : 'Peluang Rendah');
        statusEl.textContent = status;
        statusEl.style.color = color === 'green' ? '#27AE60' : (color === 'orange' ? '#F39C12' : '#C0392B');
    }
}

/* === Display Variable Breakdown (6 progress bars) === */
function displayVariableBreakdown(variables) {
    var container = document.getElementById('variableBreakdown');
    if (!container) return;

    container.innerHTML = '';

    if (!variables || variables.length === 0) return;

    variables.forEach(function(variable, index) {
        var score = variable.normalized_score || 0;
        var weightPercent = Math.round(variable.weight * 100);
        var scorePercent = Math.round(score * 100);

        // Color coding: green if > 0.6, orange if 0.3-0.6, red if < 0.3
        var barColor;
        if (score > 0.6) {
            barColor = '#27AE60';
        } else if (score >= 0.3) {
            barColor = '#F39C12';
        } else {
            barColor = '#C0392B';
        }

        var item = document.createElement('div');
        item.className = 'variable-breakdown-item';
        item.style.cssText = 'margin-bottom:0.75rem;animation:fadeIn 0.3s ease;animation-delay:' + (index * 0.1) + 's;animation-fill-mode:both;';
        item.innerHTML = '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.25rem;">' +
            '<span style="font-size:0.85rem;font-weight:600;">' + variable.name + ' (' + weightPercent + '%)</span>' +
            '<span style="font-size:0.8rem;font-weight:700;color:' + barColor + ';">' + scorePercent + '%</span>' +
            '</div>' +
            '<div class="progress-bar" style="height:8px;margin-bottom:0.2rem;">' +
            '<div class="progress-fill" style="width:0%;background:' + barColor + ';transition:width 0.8s ease ' + (index * 0.1 + 0.3) + 's;"></div>' +
            '</div>' +
            '<small style="color:var(--color-text-light);font-size:0.75rem;">' + (variable.description || '') + '</small>';

        container.appendChild(item);

        // Animate width
        setTimeout(function() {
            var fill = item.querySelector('.progress-fill');
            if (fill) fill.style.width = scorePercent + '%';
        }, 100);
    });
}

/* === Display Admission History === */
function displayAdmissionHistory(history) {
    var section = document.getElementById('admissionHistorySection');
    var content = document.getElementById('admissionHistoryContent');
    if (!section || !content) return;

    section.classList.remove('hidden');
    section.style.animation = 'fadeIn 0.5s ease';

    if (!history || history.length === 0) {
        content.innerHTML = '<div style="background:var(--color-bg);border-radius:var(--radius-sm);padding:1rem;text-align:center;">' +
            '<i class="fas fa-info-circle" style="color:var(--color-accent-blue);font-size:1.2rem;"></i>' +
            '<p style="font-size:0.85rem;color:var(--color-text-light);margin-top:0.5rem;">' +
            'Data historis penerimaan dari sekolah Anda ke program ini belum tersedia.' +
            '</p></div>';
        return;
    }

    var tableHtml = '<table style="width:100%;border-collapse:collapse;font-size:0.85rem;">' +
        '<thead><tr style="border-bottom:2px solid var(--color-border);">' +
        '<th style="padding:0.5rem;text-align:left;">Tahun</th>' +
        '<th style="padding:0.5rem;text-align:center;">Pendaftar</th>' +
        '<th style="padding:0.5rem;text-align:center;">Diterima</th>' +
        '<th style="padding:0.5rem;text-align:center;">Rasio</th>' +
        '</tr></thead><tbody>';

    history.forEach(function(row) {
        var ratio = row.applicants > 0 ? Math.round((row.accepted / row.applicants) * 100) : 0;
        var ratioColor = ratio >= 50 ? '#27AE60' : (ratio >= 25 ? '#F39C12' : '#C0392B');
        tableHtml += '<tr style="border-bottom:1px solid var(--color-border);">' +
            '<td style="padding:0.5rem;">' + row.year + '</td>' +
            '<td style="padding:0.5rem;text-align:center;">' + row.applicants + '</td>' +
            '<td style="padding:0.5rem;text-align:center;">' + row.accepted + '</td>' +
            '<td style="padding:0.5rem;text-align:center;color:' + ratioColor + ';font-weight:600;">' + ratio + '%</td>' +
            '</tr>';
    });

    tableHtml += '</tbody></table>';
    content.innerHTML = tableHtml;
}

/* === Display Choice-2 Trap Warning === */
function displayChoice2Trap(response) {
    var warningEl = document.getElementById('choice2TrapWarning');
    if (!warningEl) return;

    if (response.blocks_choice2) {
        warningEl.classList.remove('hidden');
        warningEl.style.animation = 'fadeIn 0.5s ease';
    } else {
        warningEl.classList.add('hidden');
    }
}

/* === Display Anti-Bentrok Statistics === */
function displayAntiBentrokStats(response) {
    var statsEl = document.getElementById('antiBentrokStats');
    if (!statsEl) return;

    var peerCount = response.peer_count || 0;

    if (peerCount > 0) {
        statsEl.classList.remove('hidden');
        statsEl.style.animation = 'fadeIn 0.5s ease';

        var textEl = document.getElementById('peerStatText');
        var countEl = document.getElementById('peerCountValue');
        var barEl = document.getElementById('peerProgressBar');
        var riskEl = document.getElementById('peerRiskText');

        if (textEl) {
            textEl.innerHTML = '<strong>' + peerCount + ' siswa</strong> dari sekolahmu juga memilih prodi ini sebagai target.';
        }
        if (countEl) countEl.textContent = peerCount;

        // Progress bar (max at 10 peers for visual)
        var peerPercent = Math.min((peerCount / 10) * 100, 100);
        if (barEl) barEl.style.width = peerPercent + '%';

        if (riskEl) {
            if (peerCount >= 5) {
                riskEl.textContent = 'Tingkat persaingan internal TINGGI. Pertimbangkan prodi alternatif.';
                riskEl.style.color = '#C0392B';
            } else if (peerCount >= 3) {
                riskEl.textContent = 'Persaingan sedang. Pastikan peringkat Anda lebih unggul.';
                riskEl.style.color = '#F39C12';
            } else {
                riskEl.textContent = 'Persaingan rendah dari sekolah yang sama. Peluang baik!';
                riskEl.style.color = '#27AE60';
            }
        }
    } else {
        statsEl.classList.add('hidden');
    }
}

/* === Display Recommendations (ALWAYS shown) === */
function displayRecommendations(response) {
    var recSection = document.getElementById('recommendationsSection');
    var recCards = document.getElementById('recommendationCards');
    if (!recSection || !recCards) return;

    var recommendations = response.recommendations || [];

    if (recommendations.length > 0) {
        recSection.classList.remove('hidden');
        recSection.style.animation = 'fadeIn 0.5s ease';
        recCards.innerHTML = '';

        recommendations.forEach(function(rec) {
            var card = document.createElement('div');
            card.style.cssText = 'background:var(--color-bg);border-radius:var(--radius-sm);padding:0.75rem;margin-bottom:0.5rem;';
            card.innerHTML = '<div style="display:flex;align-items:center;justify-content:space-between;">' +
                '<div>' +
                '<strong style="font-size:0.9rem;">' + rec.name + '</strong><br>' +
                '<small style="color:var(--color-text-light);">' + rec.university + '</small>' +
                '</div>' +
                '<span style="font-size:0.85rem;font-weight:700;color:#27AE60;">Rasio ' + rec.ratio + ':1</span>' +
                '</div>' +
                '<small style="color:var(--color-accent-blue);"><i class="fas fa-chart-bar"></i> ' + rec.comparison + '</small>';
            recCards.appendChild(card);
        });
    } else {
        recSection.classList.add('hidden');
    }
}

/* === Display What-If Simulator === */
function displayWhatIfSimulator(response) {
    var simEl = document.getElementById('whatIfSimulator');
    if (!simEl) return;

    simEl.classList.remove('hidden');
    simEl.style.animation = 'fadeIn 0.5s ease';

    // Store base probability for slider calculation
    window._baseProbability = response.probability || 0;
}

/* === What-If Slider Update === */
function updateWhatIf(value) {
    var labelEl = document.getElementById('whatIfValue');
    var resultEl = document.getElementById('whatIfResult');
    if (labelEl) labelEl.textContent = '+' + value;

    var baseProbability = window._baseProbability || 50;
    var bonus = parseFloat(value) * 2.5;
    var newProb = Math.min(99, Math.round(baseProbability + bonus));

    if (resultEl) {
        resultEl.textContent = newProb + '%';
        resultEl.style.color = newProb >= 70 ? '#27AE60' : (newProb >= 40 ? '#F39C12' : '#C0392B');
    }
}

/* === Animated Circular Gauge === */
function animateGauge(percentage) {
    var gaugeEl = document.getElementById('gaugeCircle');
    var gaugeText = document.getElementById('gaugePercentage');
    if (!gaugeEl || !gaugeText) return;

    var radius = 90;
    var circumference = 2 * Math.PI * radius;

    gaugeEl.style.strokeDasharray = circumference;
    gaugeEl.style.strokeDashoffset = circumference;

    // Set color based on percentage
    var color;
    if (percentage >= 70) {
        color = '#27AE60';
    } else if (percentage >= 40) {
        color = '#F39C12';
    } else {
        color = '#C0392B';
    }
    gaugeEl.style.stroke = color;

    // Animate
    var targetOffset = circumference - (percentage / 100) * circumference;

    setTimeout(function() {
        gaugeEl.style.strokeDashoffset = targetOffset;

        // Counter for text
        var current = 0;
        var duration = 1500;
        var steps = 60;
        var increment = percentage / steps;
        var stepTime = duration / steps;

        var timer = setInterval(function() {
            current += increment;
            if (current >= percentage) {
                current = percentage;
                clearInterval(timer);
            }
            gaugeText.textContent = Math.round(current) + '%';
        }, stepTime);
    }, 200);
}

/* === Confidence Interval Bar === */
function updateConfidenceBar(probability, lower, upper) {
    var rangeEl = document.getElementById('confidenceRange');
    var pointEl = document.getElementById('confidencePoint');
    var lowerText = document.getElementById('confidenceLower');
    var upperText = document.getElementById('confidenceUpper');

    if (!rangeEl || !pointEl) return;

    rangeEl.style.left = (lower * 100) + '%';
    rangeEl.style.width = ((upper - lower) * 100) + '%';
    pointEl.style.left = (probability * 100) + '%';

    if (lowerText) lowerText.textContent = Math.round(lower * 100) + '%';
    if (upperText) upperText.textContent = Math.round(upper * 100) + '%';
}

/* === Program Search Autocomplete === */
function initProgramSearch() {
    var searchInput = document.getElementById('programSearch');
    var resultsContainer = document.getElementById('programResults');
    var hiddenInput = document.querySelector('[name="target_program"]');

    if (!searchInput || !resultsContainer) return;

    var debounceTimer;

    searchInput.addEventListener('input', function() {
        var query = this.value.trim();

        clearTimeout(debounceTimer);

        if (query.length < 2) {
            resultsContainer.innerHTML = '';
            resultsContainer.classList.add('hidden');
            return;
        }

        debounceTimer = setTimeout(function() {
            ajaxRequest('../api/search_programs.php?q=' + encodeURIComponent(query), 'GET', null, function(error, response) {
                if (error) return;

                resultsContainer.innerHTML = '';
                resultsContainer.classList.remove('hidden');

                if (response.programs && response.programs.length) {
                    response.programs.forEach(function(program) {
                        var item = document.createElement('div');
                        item.className = 'search-result-item';
                        item.innerHTML = '<strong>' + program.name + '</strong><br><small>' + program.university + ' - ' + program.degree + '</small>';
                        item.addEventListener('click', function() {
                            searchInput.value = program.name + ' - ' + program.university;
                            if (hiddenInput) hiddenInput.value = program.id;
                            resultsContainer.classList.add('hidden');
                        });
                        resultsContainer.appendChild(item);
                    });
                } else {
                    resultsContainer.innerHTML = '<div class="search-result-item text-muted">Tidak ditemukan</div>';
                }
            });
        }, 300);
    });

    // Close results on outside click
    document.addEventListener('click', function(e) {
        if (!searchInput.contains(e.target) && !resultsContainer.contains(e.target)) {
            resultsContainer.classList.add('hidden');
        }
    });
}
