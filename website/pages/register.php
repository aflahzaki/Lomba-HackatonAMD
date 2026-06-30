<?php
$page_title = 'Daftar';
$base_path = '../';
require_once $base_path . 'config/app.php';
require_once $base_path . 'includes/functions.php';

if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

if (is_logged_in()) {
    redirect('dashboard_student.php');
}

// Determine registration type
$type = isset($_GET['type']) ? $_GET['type'] : '';
?>
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?php echo $page_title . ' - ' . APP_NAME; ?></title>
    <link rel="icon" type="image/png" href="<?php echo $base_path; ?>assets/images/logo.png">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <link rel="stylesheet" href="<?php echo $base_path; ?>assets/css/style.css">
    <link rel="stylesheet" href="<?php echo $base_path; ?>assets/css/animations.css">
</head>
<body>
    <div class="auth-page">
        <canvas id="particleCanvas" class="particles-canvas"></canvas>

        <div class="auth-container" style="max-width:500px;">
            <div class="auth-card">
                <div class="auth-logo">
                    <img src="<?php echo $base_path; ?>assets/images/logo.png" alt="<?php echo APP_NAME; ?>">
                    <?php if ($type === 'siswa'): ?>
                        <h2>Daftar sebagai Siswa</h2>
                        <p class="text-muted">Buat akun siswa di <?php echo APP_NAME; ?></p>
                    <?php elseif ($type === 'guru'): ?>
                        <h2>Daftar sebagai Guru</h2>
                        <p class="text-muted">Buat akun guru di <?php echo APP_NAME; ?></p>
                    <?php else: ?>
                        <h2>Buat Akun Baru</h2>
                        <p class="text-muted">Bergabung dengan <?php echo APP_NAME; ?></p>
                    <?php endif; ?>
                </div>

                <?php
                $flash = get_flash_message();
                if ($flash):
                ?>
                <div class="toast toast-<?php echo $flash['type']; ?>" style="position:relative;top:auto;right:auto;margin-bottom:1rem;">
                    <i class="fas fa-info-circle"></i>
                    <span><?php echo $flash['message']; ?></span>
                </div>
                <?php endif; ?>

                <?php if ($type === ''): ?>
                <!-- Role Selection Landing -->
                <div class="form-group">
                    <label class="form-label" style="text-align:center;display:block;margin-bottom:1rem;">Pilih Peran Anda</label>
                    <div class="payment-methods">
                        <a href="register.php?type=siswa" class="payment-method" style="text-decoration:none;color:inherit;">
                            <i class="fas fa-user-graduate"></i>
                            <div><strong>Daftar sebagai Siswa</strong></div>
                            <small>Siswa SMA/SMK/MA yang ingin eksplorasi kampus</small>
                        </a>
                        <a href="register.php?type=guru" class="payment-method" style="text-decoration:none;color:inherit;">
                            <i class="fas fa-chalkboard-teacher"></i>
                            <div><strong>Daftar sebagai Guru</strong></div>
                            <small>Guru BK yang diundang oleh siswa</small>
                        </a>
                    </div>
                </div>

                <?php elseif ($type === 'siswa'): ?>
                <!-- Student Registration Form (2-step) -->
                <div class="progress-bar mb-3">
                    <div class="progress-fill" id="registerProgress" style="width: 50%"></div>
                </div>
                <div class="text-center mb-3" style="font-size:0.85rem;color:var(--color-text-light);">
                    Langkah <span id="currentStep">1</span> dari 2
                </div>

                <form id="registerForm" method="POST" action="<?php echo $base_path; ?>api/auth.php">
                    <input type="hidden" name="action" value="register">
                    <input type="hidden" name="csrf_token" value="<?php echo generate_csrf_token(); ?>">
                    <input type="hidden" name="role" value="student">

                    <!-- Step 1: Account Info -->
                    <div class="register-step active" id="step1">
                        <div class="form-group">
                            <label class="form-label" for="full_name">Nama Lengkap</label>
                            <input type="text" id="full_name" name="full_name" class="form-control" 
                                   placeholder="Masukkan nama lengkap" required>
                        </div>

                        <div class="form-group">
                            <label class="form-label" for="reg_email">Email</label>
                            <input type="email" id="reg_email" name="email" class="form-control" 
                                   placeholder="nama@email.com" required>
                        </div>

                        <div class="form-row">
                            <div class="form-group">
                                <label class="form-label" for="reg_password">Password</label>
                                <input type="password" id="reg_password" name="password" class="form-control" 
                                       placeholder="Min. 8 karakter" required>
                            </div>
                            <div class="form-group">
                                <label class="form-label" for="confirm_password">Konfirmasi</label>
                                <input type="password" id="confirm_password" name="confirm_password" class="form-control" 
                                       placeholder="Ulangi password" required>
                            </div>
                        </div>

                        <button type="button" class="btn btn-primary btn-block" onclick="nextStep(2)">
                            Lanjut <i class="fas fa-arrow-right"></i>
                        </button>
                    </div>

                    <!-- Step 2: School Details -->
                    <div class="register-step" id="step2" style="display:none;">
                        <!-- School Search Autocomplete -->
                        <div class="form-group" id="schoolSearchGroup" style="position:relative;">
                            <label class="form-label" for="school_search">Nama Sekolah</label>
                            <input type="text" id="school_search" class="form-control" 
                                   placeholder="Ketik nama sekolah..." autocomplete="off">
                            <input type="hidden" name="school_id" id="school_id" value="">
                            <input type="hidden" id="selected_school_type" value="">
                            <div id="schoolResults" style="display:none;position:absolute;top:100%;left:0;right:0;background:white;border:1px solid var(--color-border);border-radius:var(--radius-sm);max-height:200px;overflow-y:auto;z-index:100;box-shadow:var(--shadow-md);"></div>
                            <div id="schoolSelected" style="display:none;margin-top:0.5rem;padding:0.5rem 0.75rem;background:var(--color-bg);border-radius:var(--radius-sm);font-size:0.85rem;">
                                <span id="schoolSelectedText"></span>
                                <a href="#" id="schoolClearBtn" style="margin-left:0.5rem;color:var(--color-danger);font-size:0.8rem;">
                                    <i class="fas fa-times"></i> Hapus
                                </a>
                            </div>
                        </div>

                        <!-- Manual Entry Toggle -->
                        <div class="form-group" id="manualToggleGroup">
                            <a href="#" id="manualToggleLink" style="font-size:0.85rem;color:var(--color-primary);">
                                <i class="fas fa-edit"></i> Sekolah tidak ditemukan? Input manual
                            </a>
                        </div>

                        <!-- Manual School Entry Fields (hidden by default) -->
                        <div id="manualSchoolFields" style="display:none;">
                            <div class="form-group">
                                <label class="form-label" for="school_name_manual">Nama Sekolah</label>
                                <input type="text" id="school_name_manual" name="school_name_manual" class="form-control" 
                                       placeholder="Masukkan nama sekolah">
                            </div>
                            <div class="form-group">
                                <label class="form-label" for="school_type_manual">Jenis Sekolah</label>
                                <select id="school_type_manual" name="school_type_manual" class="form-control">
                                    <option value="">Pilih Jenis</option>
                                    <option value="SMA">SMA</option>
                                    <option value="SMK">SMK</option>
                                    <option value="MA">MA</option>
                                </select>
                            </div>
                            <div class="form-row">
                                <div class="form-group">
                                    <label class="form-label" for="school_province_manual">Provinsi</label>
                                    <input type="text" id="school_province_manual" name="school_province_manual" class="form-control" 
                                           placeholder="Provinsi">
                                </div>
                                <div class="form-group">
                                    <label class="form-label" for="school_city_manual">Kota/Kabupaten</label>
                                    <input type="text" id="school_city_manual" name="school_city_manual" class="form-control" 
                                           placeholder="Kota/Kabupaten">
                                </div>
                            </div>
                            <a href="#" id="backToSearchLink" style="font-size:0.85rem;color:var(--color-primary);">
                                <i class="fas fa-search"></i> Kembali ke pencarian sekolah
                            </a>
                        </div>

                        <!-- Jurusan / Major Track (dynamic based on school type) -->
                        <div class="form-group" id="majorTrackGroup" style="margin-top:1rem;">
                            <label class="form-label" for="major_track">Jurusan</label>
                            <select id="major_track" name="major_track" class="form-control">
                                <option value="">Pilih Jurusan</option>
                                <option value="IPA">IPA</option>
                                <option value="IPS">IPS</option>
                                <option value="Bahasa">Bahasa</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label style="display:flex;align-items:center;gap:0.5rem;font-size:0.85rem;cursor:pointer;">
                                <input type="checkbox" name="agree_terms" value="1" required>
                                Saya menyetujui <a href="#">Syarat &amp; Ketentuan</a> dan <a href="#">Kebijakan Privasi</a>
                            </label>
                        </div>

                        <div style="display:flex;gap:1rem;">
                            <button type="button" class="btn btn-outline btn-block" style="border-color:var(--color-border);color:var(--color-text);" onclick="prevStep(1)">
                                <i class="fas fa-arrow-left"></i> Kembali
                            </button>
                            <button type="submit" class="btn btn-primary btn-block btn-ripple">
                                <i class="fas fa-user-plus"></i> Daftar
                            </button>
                        </div>
                    </div>
                </form>

                <?php elseif ($type === 'guru'): ?>
                <!-- Guru Registration Form (single step) -->
                <form id="registerForm" method="POST" action="<?php echo $base_path; ?>api/auth.php">
                    <input type="hidden" name="action" value="register">
                    <input type="hidden" name="csrf_token" value="<?php echo generate_csrf_token(); ?>">
                    <input type="hidden" name="role" value="guru">

                    <div class="form-group">
                        <label class="form-label" for="full_name">Nama Lengkap</label>
                        <input type="text" id="full_name" name="full_name" class="form-control" 
                               placeholder="Masukkan nama lengkap" required>
                    </div>

                    <div class="form-group">
                        <label class="form-label" for="reg_email">Email</label>
                        <input type="email" id="reg_email" name="email" class="form-control" 
                               placeholder="nama@email.com" required>
                    </div>

                    <div class="form-row">
                        <div class="form-group">
                            <label class="form-label" for="reg_password">Password</label>
                            <input type="password" id="reg_password" name="password" class="form-control" 
                                   placeholder="Min. 8 karakter" required>
                        </div>
                        <div class="form-group">
                            <label class="form-label" for="confirm_password">Konfirmasi</label>
                            <input type="password" id="confirm_password" name="confirm_password" class="form-control" 
                                   placeholder="Ulangi password" required>
                        </div>
                    </div>

                    <div class="form-group">
                        <label class="form-label" for="invite_code">Kode Undangan</label>
                        <input type="text" id="invite_code" name="invite_code" class="form-control" 
                               placeholder="Masukkan 6 karakter kode" maxlength="6" style="text-transform:uppercase;letter-spacing:0.2em;font-weight:600;" required>
                        <small style="color:var(--color-text-muted);display:block;margin-top:0.3rem;">
                            Masukkan kode undangan yang diberikan oleh siswa Anda
                        </small>
                    </div>

                    <div class="form-group">
                        <label style="display:flex;align-items:center;gap:0.5rem;font-size:0.85rem;cursor:pointer;">
                            <input type="checkbox" name="agree_terms" value="1" required>
                            Saya menyetujui <a href="#">Syarat &amp; Ketentuan</a> dan <a href="#">Kebijakan Privasi</a>
                        </label>
                    </div>

                    <button type="submit" class="btn btn-primary btn-block btn-ripple">
                        <i class="fas fa-user-plus"></i> Daftar sebagai Guru
                    </button>
                </form>
                <?php endif; ?>

                <div class="text-center mt-3">
                    <p class="text-muted" style="font-size:0.9rem;">
                        Sudah punya akun? <a href="login.php"><strong>Masuk</strong></a>
                    </p>
                    <?php if ($type !== ''): ?>
                    <p class="text-muted" style="font-size:0.85rem;">
                        <a href="register.php"><i class="fas fa-arrow-left"></i> Kembali ke pilihan peran</a>
                    </p>
                    <?php endif; ?>
                </div>
            </div>
        </div>
    </div>

    <script src="<?php echo $base_path; ?>assets/js/main.js"></script>
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        initParticleBackground();
        initSchoolSearch();
        initManualToggle();
        initDynamicJurusan();
    });

    function nextStep(step) {
        document.querySelectorAll('.register-step').forEach(function(el) { el.style.display = 'none'; });
        document.getElementById('step' + step).style.display = 'block';
        document.getElementById('currentStep').textContent = step;
        document.getElementById('registerProgress').style.width = (step * 50) + '%';
    }

    function prevStep(step) {
        document.querySelectorAll('.register-step').forEach(function(el) { el.style.display = 'none'; });
        document.getElementById('step' + step).style.display = 'block';
        document.getElementById('currentStep').textContent = step;
        document.getElementById('registerProgress').style.width = (step * 50) + '%';
    }

    /* === School Search Autocomplete === */
    function initSchoolSearch() {
        var searchInput = document.getElementById('school_search');
        var resultsContainer = document.getElementById('schoolResults');
        var hiddenSchoolId = document.getElementById('school_id');
        var hiddenSchoolType = document.getElementById('selected_school_type');
        var selectedDiv = document.getElementById('schoolSelected');
        var selectedText = document.getElementById('schoolSelectedText');
        var clearBtn = document.getElementById('schoolClearBtn');

        if (!searchInput || !resultsContainer) return;

        var debounceTimer;

        searchInput.addEventListener('input', function() {
            var query = this.value.trim();
            clearTimeout(debounceTimer);

            if (query.length < 2) {
                resultsContainer.innerHTML = '';
                resultsContainer.style.display = 'none';
                return;
            }

            debounceTimer = setTimeout(function() {
                ajaxRequest('../api/search_schools.php?q=' + encodeURIComponent(query), 'GET', null, function(error, response) {
                    if (error) return;

                    resultsContainer.innerHTML = '';
                    resultsContainer.style.display = 'block';

                    if (response.schools && response.schools.length) {
                        response.schools.forEach(function(school) {
                            var item = document.createElement('div');
                            item.style.cssText = 'padding:0.6rem 0.75rem;cursor:pointer;border-bottom:1px solid var(--color-border);font-size:0.9rem;';
                            item.innerHTML = '<strong>' + school.name + '</strong><br><small style="color:var(--color-text-light);">' + (school.school_type || '') + ' - ' + (school.city || '') + ', ' + (school.province || '') + '</small>';

                            item.addEventListener('mouseenter', function() {
                                this.style.background = 'var(--color-bg)';
                            });
                            item.addEventListener('mouseleave', function() {
                                this.style.background = 'white';
                            });

                            item.addEventListener('click', function() {
                                hiddenSchoolId.value = school.id;
                                hiddenSchoolType.value = school.school_type || '';
                                searchInput.style.display = 'none';
                                resultsContainer.style.display = 'none';
                                selectedDiv.style.display = 'block';
                                selectedText.innerHTML = '<strong>' + school.name + '</strong> <small>(' + (school.school_type || '') + ' - ' + (school.city || '') + ')</small>';
                                updateJurusanOptions(school.school_type || 'SMA');
                            });

                            resultsContainer.appendChild(item);
                        });
                    } else {
                        resultsContainer.innerHTML = '<div style="padding:0.6rem 0.75rem;font-size:0.85rem;color:var(--color-text-light);">Tidak ditemukan. Gunakan input manual.</div>';
                    }
                });
            }, 300);
        });

        // Close results on outside click
        document.addEventListener('click', function(e) {
            if (!searchInput.contains(e.target) && !resultsContainer.contains(e.target)) {
                resultsContainer.style.display = 'none';
            }
        });

        // Clear selection
        if (clearBtn) {
            clearBtn.addEventListener('click', function(e) {
                e.preventDefault();
                hiddenSchoolId.value = '';
                hiddenSchoolType.value = '';
                searchInput.value = '';
                searchInput.style.display = 'block';
                selectedDiv.style.display = 'none';
                updateJurusanOptions('SMA');
            });
        }
    }

    /* === Manual Entry Toggle === */
    function initManualToggle() {
        var manualToggleLink = document.getElementById('manualToggleLink');
        var backToSearchLink = document.getElementById('backToSearchLink');
        var manualFields = document.getElementById('manualSchoolFields');
        var searchGroup = document.getElementById('schoolSearchGroup');
        var manualToggleGroup = document.getElementById('manualToggleGroup');
        var schoolTypeManual = document.getElementById('school_type_manual');

        if (!manualToggleLink || !manualFields) return;

        manualToggleLink.addEventListener('click', function(e) {
            e.preventDefault();
            searchGroup.style.display = 'none';
            manualToggleGroup.style.display = 'none';
            manualFields.style.display = 'block';
            // Clear autocomplete selection
            document.getElementById('school_id').value = '';
            document.getElementById('selected_school_type').value = '';
        });

        if (backToSearchLink) {
            backToSearchLink.addEventListener('click', function(e) {
                e.preventDefault();
                manualFields.style.display = 'none';
                searchGroup.style.display = 'block';
                manualToggleGroup.style.display = 'block';
                // Clear manual fields
                document.getElementById('school_name_manual').value = '';
                document.getElementById('school_type_manual').value = '';
                document.getElementById('school_province_manual').value = '';
                document.getElementById('school_city_manual').value = '';
                updateJurusanOptions('SMA');
            });
        }

        // Listen for manual school type change
        if (schoolTypeManual) {
            schoolTypeManual.addEventListener('change', function() {
                var selectedType = this.value || 'SMA';
                updateJurusanOptions(selectedType);
            });
        }
    }

    /* === Dynamic Jurusan Options === */
    function initDynamicJurusan() {
        // Default to SMA/MA options on load
        updateJurusanOptions('SMA');
    }

    function updateJurusanOptions(schoolType) {
        var majorSelect = document.getElementById('major_track');
        if (!majorSelect) return;

        var smaOptions = [
            { value: '', label: 'Pilih Jurusan' },
            { value: 'IPA', label: 'IPA' },
            { value: 'IPS', label: 'IPS' },
            { value: 'Bahasa', label: 'Bahasa' }
        ];

        var smkOptions = [
            { value: '', label: 'Pilih Jurusan' },
            { value: 'TKJ', label: 'TKJ' },
            { value: 'RPL', label: 'RPL' },
            { value: 'Multimedia', label: 'Multimedia' },
            { value: 'AKL', label: 'AKL' },
            { value: 'TBSM', label: 'TBSM' },
            { value: 'OTKP', label: 'OTKP' },
            { value: 'BDP', label: 'BDP' },
            { value: 'Farmasi', label: 'Farmasi' },
            { value: 'Keperawatan', label: 'Keperawatan' },
            { value: 'DKV', label: 'DKV' },
            { value: 'Teknik Kendaraan Ringan', label: 'Teknik Kendaraan Ringan' },
            { value: 'Teknik Instalasi Tenaga Listrik', label: 'Teknik Instalasi Tenaga Listrik' },
            { value: 'Tata Busana', label: 'Tata Busana' },
            { value: 'Tata Boga', label: 'Tata Boga' },
            { value: 'Animasi', label: 'Animasi' }
        ];

        var options = (schoolType === 'SMK') ? smkOptions : smaOptions;

        majorSelect.innerHTML = '';
        options.forEach(function(opt) {
            var option = document.createElement('option');
            option.value = opt.value;
            option.textContent = opt.label;
            majorSelect.appendChild(option);
        });
    }
    </script>
</body>
</html>
