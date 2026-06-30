<?php
$page_title = 'Pembayaran';
include '../includes/header.php';

// Demo user data
$predictions_used = 3;
$predictions_limit = FREE_PREDICTIONS_LIMIT;
$referral_code = 'LK-A3B4C5';
$referral_unique_clicks = 2;
?>

<div class="dashboard-page">
    <div class="dashboard-header">
        <div class="container">
            <h1><i class="fas fa-credit-card"></i> Tambah Prediksi</h1>
            <p>Prediksi gratis Anda telah habis. Pilih salah satu cara untuk menambah kuota prediksi.</p>
        </div>
    </div>

    <div class="container">
        <!-- Usage Status -->
        <div class="card mb-3" data-aos="fade-up">
            <div class="d-flex align-center justify-between mb-2">
                <h4><i class="fas fa-chart-bar text-blue"></i> Status Penggunaan</h4>
                <span class="badge badge-warning"><?php echo $predictions_used; ?>/<?php echo $predictions_limit; ?> prediksi gratis digunakan</span>
            </div>
            <div class="progress-bar" style="height:10px;">
                <div class="progress-fill" style="width:<?php echo ($predictions_used / $predictions_limit) * 100; ?>%;background:linear-gradient(90deg,var(--color-accent-blue),<?php echo $predictions_used >= $predictions_limit ? '#C0392B' : 'var(--color-accent-green)'; ?>);"></div>
            </div>
            <p class="text-muted mt-1" style="font-size:0.85rem;">
                <?php if ($predictions_used >= $predictions_limit): ?>
                    <i class="fas fa-exclamation-circle text-red"></i> Kuota prediksi gratis habis. Bayar atau bagikan link referral untuk menambah kuota.
                <?php else: ?>
                    <i class="fas fa-info-circle"></i> Anda masih memiliki <?php echo $predictions_limit - $predictions_used; ?> prediksi gratis.
                <?php endif; ?>
            </p>
        </div>

        <!-- Two Options -->
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:2rem;" class="mb-4">
            <!-- Option 1: Payment -->
            <div class="card" data-aos="fade-up" data-aos-delay="100">
                <div class="text-center mb-3">
                    <div style="width:60px;height:60px;border-radius:50%;background:linear-gradient(135deg,var(--color-accent-blue),#1557b0);display:inline-flex;align-items:center;justify-content:center;color:#fff;font-size:1.5rem;margin-bottom:1rem;">
                        <i class="fas fa-wallet"></i>
                    </div>
                    <h3>Bayar Langsung</h3>
                    <p class="text-muted">Akses instan ke prediksi tambahan</p>
                </div>

                <div class="pricing-grid mb-3" style="grid-template-columns:1fr;">
                    <div class="pricing-card" style="border:2px solid var(--color-accent-blue);">
                        <div class="pricing-name">Paket Prediksi</div>
                        <div class="pricing-price"><?php echo format_rupiah(PRICE_BASIC_PREDICTION); ?> - <?php echo format_rupiah(PRICE_DEEP_RECOMMENDATION); ?> <span>/paket</span></div>
                        <ul class="pricing-features">
                            <li><i class="fas fa-check"></i> 5x prediksi lengkap</li>
                            <li><i class="fas fa-check"></i> Probabilitas + Confidence Interval</li>
                            <li><i class="fas fa-check"></i> Choice-2 Trap Warning</li>
                            <li><i class="fas fa-check"></i> Anti-Bentrok Statistics</li>
                            <li><i class="fas fa-check"></i> Rekomendasi Alternatif</li>
                            <li><i class="fas fa-check"></i> What-If Simulator</li>
                        </ul>
                    </div>
                </div>

                <h5 class="mb-2">Pilih Metode Pembayaran:</h5>
                <div class="payment-methods">
                    <div class="payment-method" onclick="selectPayment(this, 'bca')">
                        <i class="fas fa-university"></i>
                        <div><strong>Transfer BCA</strong></div>
                    </div>
                    <div class="payment-method" onclick="selectPayment(this, 'mandiri')">
                        <i class="fas fa-university"></i>
                        <div><strong>Transfer Mandiri</strong></div>
                    </div>
                    <div class="payment-method" onclick="selectPayment(this, 'gopay')">
                        <i class="fas fa-mobile-alt"></i>
                        <div><strong>GoPay</strong></div>
                    </div>
                    <div class="payment-method" onclick="selectPayment(this, 'ovo')">
                        <i class="fas fa-mobile-alt"></i>
                        <div><strong>OVO</strong></div>
                    </div>
                    <div class="payment-method" onclick="selectPayment(this, 'dana')">
                        <i class="fas fa-mobile-alt"></i>
                        <div><strong>DANA</strong></div>
                    </div>
                    <div class="payment-method" onclick="selectPayment(this, 'qris')">
                        <i class="fas fa-qrcode"></i>
                        <div><strong>QRIS</strong></div>
                    </div>
                </div>

                <button class="btn btn-primary btn-lg btn-block btn-ripple mt-3" onclick="processPayment()">
                    <i class="fas fa-lock"></i> Bayar Sekarang
                </button>
            </div>

            <!-- Option 2: Referral -->
            <div class="card" data-aos="fade-up" data-aos-delay="200">
                <div class="text-center mb-3">
                    <div style="width:60px;height:60px;border-radius:50%;background:linear-gradient(135deg,var(--color-accent-green),#1d8348);display:inline-flex;align-items:center;justify-content:center;color:#fff;font-size:1.5rem;margin-bottom:1rem;">
                        <i class="fas fa-share-alt"></i>
                    </div>
                    <h3>Bagikan ke Teman</h3>
                    <p class="text-muted">Gratis! Dapatkan prediksi tambahan dengan share</p>
                </div>

                <div style="background:rgba(39,174,96,0.05);border:2px solid var(--color-accent-green);border-radius:var(--radius-md);padding:1.5rem;text-align:center;margin-bottom:1.5rem;">
                    <p style="font-size:0.9rem;margin-bottom:1rem;">Setiap <strong><?php echo REFERRAL_CLICKS_REQUIRED; ?> klik unik</strong> dari IP berbeda = <strong><?php echo REFERRAL_UNLOCK_PREDICTIONS; ?> prediksi gratis</strong> tambahan!</p>

                    <div style="background:var(--color-bg);border-radius:var(--radius-sm);padding:0.75rem;margin-bottom:1rem;">
                        <label class="form-label" style="font-size:0.8rem;">Link Referral Anda:</label>
                        <div class="d-flex align-center gap-1">
                            <input type="text" class="form-control" id="referralLinkInput" value="<?php echo APP_URL; ?>/ref/<?php echo $referral_code; ?>" readonly style="font-size:0.85rem;">
                            <button class="btn btn-sm btn-primary" onclick="copyReferralLink()">
                                <i class="fas fa-copy"></i> Salin
                            </button>
                        </div>
                    </div>

                    <!-- Progress -->
                    <div class="mb-2">
                        <div class="d-flex justify-between mb-1">
                            <small>Progress klik unik:</small>
                            <strong><?php echo $referral_unique_clicks; ?>/<?php echo REFERRAL_CLICKS_REQUIRED; ?></strong>
                        </div>
                        <div class="progress-bar" style="height:12px;">
                            <div class="progress-fill" style="width:<?php echo ($referral_unique_clicks / REFERRAL_CLICKS_REQUIRED) * 100; ?>%;background:linear-gradient(90deg,var(--color-accent-green),var(--color-accent-blue));"></div>
                        </div>
                        <small class="text-muted">Butuh <?php echo REFERRAL_CLICKS_REQUIRED - $referral_unique_clicks; ?> klik unik lagi untuk unlock</small>
                    </div>
                </div>

                <h5 class="mb-2">Bagikan via:</h5>
                <div class="d-flex flex-wrap gap-1">
                    <button class="btn btn-sm btn-outline" style="border-color:#25D366;color:#25D366;" onclick="shareVia('whatsapp')">
                        <i class="fab fa-whatsapp"></i> WhatsApp
                    </button>
                    <button class="btn btn-sm btn-outline" style="border-color:#1DA1F2;color:#1DA1F2;" onclick="shareVia('twitter')">
                        <i class="fab fa-twitter"></i> Twitter
                    </button>
                    <button class="btn btn-sm btn-outline" style="border-color:#4267B2;color:#4267B2;" onclick="shareVia('facebook')">
                        <i class="fab fa-facebook"></i> Facebook
                    </button>
                    <button class="btn btn-sm btn-outline" style="border-color:#0077B5;color:#0077B5;" onclick="shareVia('linkedin')">
                        <i class="fab fa-linkedin"></i> LinkedIn
                    </button>
                </div>

                <div class="mt-3" style="background:var(--color-bg);border-radius:var(--radius-sm);padding:1rem;">
                    <h5 style="font-size:0.85rem;"><i class="fas fa-info-circle text-blue"></i> Cara Kerja:</h5>
                    <ol style="font-size:0.8rem;color:var(--color-text-light);line-height:2;padding-left:1rem;">
                        <li>Salin link referral Anda</li>
                        <li>Bagikan ke teman-teman</li>
                        <li>Setiap <?php echo REFERRAL_CLICKS_REQUIRED; ?> orang berbeda yang klik = <?php echo REFERRAL_UNLOCK_PREDICTIONS; ?> prediksi gratis</li>
                        <li>Tidak ada batas jumlah referral!</li>
                    </ol>
                </div>
            </div>
        </div>

        <!-- Promo Code -->
        <div class="card mb-4" data-aos="fade-up" data-aos-delay="300">
            <h4 class="mb-2"><i class="fas fa-tag text-blue"></i> Punya Kode Promo?</h4>
            <div class="d-flex gap-1" style="max-width:400px;">
                <input type="text" class="form-control" placeholder="Masukkan kode promo" id="promoCode">
                <button class="btn btn-outline" style="border-color:var(--color-accent-blue);color:var(--color-accent-blue);white-space:nowrap;" onclick="applyPromo()">Terapkan</button>
            </div>
        </div>
    </div>
</div>

<script>
function selectPayment(el, method) {
    document.querySelectorAll('.payment-method').forEach(function(m) { m.classList.remove('selected'); });
    el.classList.add('selected');
}

function processPayment() {
    var selected = document.querySelector('.payment-method.selected');
    if (!selected) {
        showToast('warning', 'Silakan pilih metode pembayaran');
        return;
    }

    showToast('info', 'Memproses pembayaran...');

    setTimeout(function() {
        showToast('success', 'Pembayaran berhasil! 5 prediksi tambahan telah diaktifkan.');
    }, 2000);
}

function copyReferralLink() {
    var input = document.getElementById('referralLinkInput');
    if (input) {
        navigator.clipboard.writeText(input.value);
        showToast('success', 'Link referral berhasil disalin!');
    }
}

function shareVia(platform) {
    var link = document.getElementById('referralLinkInput').value;
    var text = 'Cek peluang SNBP kamu di LangkahKampus! Prediksi berbasis AI: ';
    var urls = {
        whatsapp: 'https://wa.me/?text=' + encodeURIComponent(text + link),
        twitter: 'https://twitter.com/intent/tweet?text=' + encodeURIComponent(text) + '&url=' + encodeURIComponent(link),
        facebook: 'https://www.facebook.com/sharer/sharer.php?u=' + encodeURIComponent(link),
        linkedin: 'https://www.linkedin.com/sharing/share-offsite/?url=' + encodeURIComponent(link)
    };
    window.open(urls[platform], '_blank', 'width=600,height=400');
}

function applyPromo() {
    var code = document.getElementById('promoCode').value.trim();
    if (code.toLowerCase() === 'langkah2025') {
        showToast('success', 'Kode promo berhasil! 2 prediksi gratis ditambahkan.');
    } else if (code) {
        showToast('danger', 'Kode promo tidak valid');
    }
}
</script>

<?php include '../includes/footer.php'; ?>
