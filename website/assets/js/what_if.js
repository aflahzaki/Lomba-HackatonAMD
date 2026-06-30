/**
 * LangkahKampus - What-If Simulator JavaScript
 * Handles debounced slider events, API calls, and comparison gauge visualization
 */

document.addEventListener('DOMContentLoaded', function() {
    initSliders();
    initWhatIfProgramSearch();
});

/* === Debounce Utility === */
function debounce(fn, delay) {
    var timer = null;
    return function() {
        var context = this;
        var args = arguments;
        clearTimeout(timer);
        timer = setTimeout(function() {
            fn.apply(context, args);
        }, delay);
    };
}

/* === Initialize Sliders === */
function initSliders() {
    var nilaiSlider = document.getElementById('nilaiSlider');
    var peringkatSlider = document.getElementById('peringkatSlider');
    var totalSiswaInput = document.getElementById('totalSiswaInput');
    var akreditasiSelect = document.getElementById('akreditasiSelect');

    if (!nilaiSlider || !peringkatSlider) return;

    var debouncedUpdate = debounce(runSimulation, 400);

    nilaiSlider.addEventListener('input', function() {
        document.getElementById('nilaiDisplay').textContent = this.value;
        debouncedUpdate();
    });

    peringkatSlider.addEventListener('input', function() {
        document.getElementById('peringkatDisplay').textContent = this.value;
        debouncedUpdate();
    });

    if (totalSiswaInput) {
        totalSiswaInput.addEventListener('input', debouncedUpdate);
    }

    if (akreditasiSelect) {
        akreditasiSelect.addEventListener('change', debouncedUpdate);
    }
}

/* === Run Simulation (API Call) === */
function runSimulation() {
    var nilai = parseFloat(document.getElementById('nilaiSlider').value);
    var peringkat = parseInt(document.getElementById('peringkatSlider').value);
    var totalSiswa = parseInt(document.getElementById('totalSiswaInput').value) || 200;
    var akreditasi = document.getElementById('akreditasiSelect').value;
    var targetProgram = document.getElementById('targetProgramId').value;

    var payload = {
        nilai_rata_rata: nilai,
        peringkat: peringkat,
        total_siswa: totalSiswa,
        akreditasi: akreditasi
    };

    if (targetProgram) {
        payload.target_program_id = targetProgram;
    }

    ajaxRequest('../api/what_if.php', 'POST', payload, function(error, response) {
        if (error) {
            showToast('danger', 'Gagal menjalankan simulasi: ' + error);
            return;
        }

        updateComparison(response);
        updateFactorImpact(response.factors || []);
    });
}

/* === Update Comparison Gauges === */
function updateComparison(response) {
    var currentProb = response.current_probability || 0;
    var newProb = response.new_probability || 0;
    var difference = response.difference || (newProb - currentProb);

    // Animate current gauge
    animateWhatIfGauge('currentGaugeCircle', 'currentPercentage', currentProb);

    // Animate new gauge
    animateWhatIfGauge('newGaugeCircle', 'newPercentage', newProb);

    // Update difference badge
    var differenceBadge = document.getElementById('differenceBadge');
    var differenceValue = document.getElementById('differenceValue');
    var differenceLabel = document.getElementById('differenceLabel');

    if (differenceBadge) {
        differenceBadge.classList.remove('hidden');
    }

    if (differenceValue) {
        var sign = difference >= 0 ? '+' : '';
        differenceValue.textContent = sign + difference + '%';

        if (difference > 0) {
            differenceValue.style.color = '#27AE60';
        } else if (difference < 0) {
            differenceValue.style.color = '#C0392B';
        } else {
            differenceValue.style.color = 'var(--color-text-light)';
        }
    }

    if (differenceLabel) {
        if (difference > 10) {
            differenceLabel.textContent = 'Peningkatan signifikan! Perubahan ini sangat berdampak.';
        } else if (difference > 0) {
            differenceLabel.textContent = 'Ada peningkatan peluang dari parameter baru.';
        } else if (difference < 0) {
            differenceLabel.textContent = 'Peluang menurun. Coba sesuaikan parameter lain.';
        } else {
            differenceLabel.textContent = 'Tidak ada perubahan peluang.';
        }
    }
}

/* === Animate a Single Gauge === */
function animateWhatIfGauge(circleId, textId, percentage) {
    var circle = document.getElementById(circleId);
    var text = document.getElementById(textId);
    if (!circle || !text) return;

    var radius = 65;
    var circumference = 2 * Math.PI * radius;
    var targetOffset = circumference - (percentage / 100) * circumference;

    // Set color based on percentage
    var color;
    if (percentage >= 70) {
        color = '#27AE60';
    } else if (percentage >= 40) {
        color = '#F39C12';
    } else {
        color = '#C0392B';
    }

    circle.style.stroke = color;
    circle.style.transition = 'stroke-dashoffset 0.8s ease';
    circle.style.strokeDashoffset = targetOffset;

    // Animate text counter
    var current = parseInt(text.textContent) || 0;
    var steps = 30;
    var increment = (percentage - current) / steps;
    var stepTime = 800 / steps;
    var frame = 0;

    var timer = setInterval(function() {
        frame++;
        current += increment;
        if (frame >= steps) {
            current = percentage;
            clearInterval(timer);
        }
        text.textContent = Math.round(current) + '%';
    }, stepTime);
}

/* === Update Factor Impact Display === */
function updateFactorImpact(factors) {
    var container = document.getElementById('factorImpact');
    var list = document.getElementById('factorList');
    if (!container || !list) return;

    if (factors.length === 0) {
        container.classList.add('hidden');
        return;
    }

    container.classList.remove('hidden');
    list.innerHTML = '';

    factors.forEach(function(factor) {
        var impact = factor.impact || 0;
        var color = impact >= 0 ? '#27AE60' : '#C0392B';
        var sign = impact >= 0 ? '+' : '';
        var barWidth = Math.min(Math.abs(impact) * 5, 100);

        var item = document.createElement('div');
        item.style.cssText = 'margin-bottom:0.75rem;';
        item.innerHTML = '<div style="display:flex;justify-content:space-between;margin-bottom:0.25rem;">' +
            '<span style="font-size:0.85rem;">' + factor.name + '</span>' +
            '<span style="font-size:0.85rem;font-weight:700;color:' + color + ';">' + sign + impact + '</span>' +
            '</div>' +
            '<div style="height:6px;background:var(--color-bg);border-radius:3px;overflow:hidden;">' +
            '<div style="height:100%;width:' + barWidth + '%;background:' + color + ';border-radius:3px;transition:width 0.5s ease;"></div>' +
            '</div>';

        list.appendChild(item);
    });
}

/* === Program Search (reuse pattern from prediksi.php) === */
function initWhatIfProgramSearch() {
    var searchInput = document.getElementById('programSearch');
    var resultsContainer = document.getElementById('programResults');
    var hiddenInput = document.getElementById('targetProgramId');

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
                        item.style.cssText = 'padding:0.75rem;cursor:pointer;border-bottom:1px solid var(--color-border);';
                        item.innerHTML = '<strong>' + program.name + '</strong><br><small>' + program.university + ' - ' + program.degree + '</small>';
                        item.addEventListener('click', function() {
                            searchInput.value = program.name + ' - ' + program.university;
                            if (hiddenInput) hiddenInput.value = program.id;
                            resultsContainer.classList.add('hidden');
                            // Trigger simulation with new program
                            runSimulation();
                        });
                        resultsContainer.appendChild(item);
                    });
                } else {
                    resultsContainer.innerHTML = '<div style="padding:0.75rem;color:var(--color-text-light);">Tidak ditemukan</div>';
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
