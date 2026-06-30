    </main>
    <!-- End Main Content -->

    <!-- Footer -->
    <footer class="footer">
        <div class="footer-wave">
            <svg viewBox="0 0 1440 100" xmlns="http://www.w3.org/2000/svg">
                <path fill="currentColor" d="M0,40 C360,80 720,0 1080,40 C1260,60 1380,50 1440,40 L1440,100 L0,100 Z"/>
            </svg>
        </div>
        <div class="footer-content">
            <div class="container">
                <div class="footer-grid">
                    <!-- Brand -->
                    <div class="footer-brand">
                        <div class="footer-logo">
                            <img src="<?php echo $base_path; ?>assets/images/logo.png" alt="<?php echo APP_NAME; ?>">
                            <span><?php echo APP_NAME; ?></span>
                        </div>
                        <p class="footer-description">
                            Platform prediksi penerimaan SNBP berbasis Machine Learning untuk membantu siswa SMA/SMK/MA meraih impian kuliah mereka.
                        </p>
                        <div class="footer-social">
                            <a href="#" class="social-link"><i class="fab fa-instagram"></i></a>
                            <a href="#" class="social-link"><i class="fab fa-twitter"></i></a>
                            <a href="#" class="social-link"><i class="fab fa-linkedin"></i></a>
                            <a href="#" class="social-link"><i class="fab fa-youtube"></i></a>
                        </div>
                    </div>

                    <!-- Quick Links -->
                    <div class="footer-links">
                        <h4>Menu Cepat</h4>
                        <ul>
                            <li><a href="<?php echo $base_path; ?>index.php">Beranda</a></li>
                            <li><a href="<?php echo $base_path; ?>pages/prediksi.php">Prediksi SNBP</a></li>
                            <li><a href="<?php echo $base_path; ?>pages/peta_universitas.php">Peta Universitas</a></li>
                            <li><a href="<?php echo $base_path; ?>pages/pembayaran.php">Harga</a></li>
                            <li><a href="<?php echo $base_path; ?>pages/tentang.php">Tentang Kami</a></li>
                        </ul>
                    </div>

                    <!-- Features -->
                    <div class="footer-links">
                        <h4>Fitur</h4>
                        <ul>
                            <li><a href="<?php echo $base_path; ?>pages/prediksi.php">Prediksi ML</a></li>
                            <li><a href="<?php echo $base_path; ?>pages/rekomendasi.php">Rekomendasi Prodi</a></li>
                            <li><a href="<?php echo $base_path; ?>pages/anti_bentrok.php">Statistik Anti-Bentrok</a></li>
                            <li><a href="<?php echo $base_path; ?>pages/validator.php">Validasi Pilihan</a></li>
                            <li><a href="<?php echo $base_path; ?>pages/peta_universitas.php">Peta PTN</a></li>
                        </ul>
                    </div>

                    <!-- Contact -->
                    <div class="footer-links">
                        <h4>Kontak</h4>
                        <ul>
                            <li><i class="fas fa-envelope"></i> info@langkahkampus.id</li>
                            <li><i class="fas fa-phone"></i> +62 812-3456-7890</li>
                            <li><i class="fas fa-map-marker-alt"></i> Bandung, Jawa Barat</li>
                        </ul>
                    </div>
                </div>

                <div class="footer-bottom">
                    <p>&copy; <?php echo date('Y'); ?> <?php echo APP_NAME; ?>. All rights reserved.</p>
                    <div class="footer-bottom-links">
                        <a href="#">Kebijakan Privasi</a>
                        <a href="#">Syarat & Ketentuan</a>
                    </div>
                </div>
            </div>
        </div>
    </footer>

    <!-- AOS Animation Library -->
    <script src="https://unpkg.com/aos@2.3.1/dist/aos.js"></script>

    <!-- Leaflet JS (for map pages) -->
    <?php if (isset($use_leaflet) && $use_leaflet): ?>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script src="<?php echo $base_path; ?>assets/js/maps.js"></script>
    <?php endif; ?>

    <!-- Core JS -->
    <script src="<?php echo $base_path; ?>assets/js/main.js"></script>

    <!-- Page-specific JS -->
    <?php if (isset($page_scripts) && is_array($page_scripts)): ?>
        <?php foreach ($page_scripts as $script): ?>
        <script src="<?php echo $base_path; ?>assets/js/<?php echo $script; ?>"></script>
        <?php endforeach; ?>
    <?php endif; ?>

    <script>
        // Initialize AOS
        AOS.init({
            duration: 800,
            easing: 'ease-out-cubic',
            once: true,
            offset: 50
        });
    </script>
</body>
</html>
