<?php
$page_title = 'AI Advisor';
$page_scripts = ['advisor.js'];
include '../includes/header.php';
?>

<div class="dashboard-page">
    <div class="dashboard-header">
        <div class="container">
            <h1><i class="fas fa-robot"></i> AI Advisor SNBP</h1>
            <p>Tanya apa saja tentang strategi SNBP, pilihan program studi, dan tips meningkatkan peluang lolos. Advisor kami didukung oleh Fireworks AI.</p>
        </div>
    </div>

    <div class="container">
        <div style="max-width:800px;margin:0 auto;">
            <div class="card" data-aos="fade-up">
                <!-- Chat Messages Area -->
                <div id="chatMessages" style="height:400px;overflow-y:auto;padding:1rem;border:1px solid var(--color-border);border-radius:var(--radius-sm);margin-bottom:1rem;background:var(--color-bg);">
                    <!-- Welcome message -->
                    <div class="chat-message chat-bot">
                        <div class="chat-avatar">
                            <i class="fas fa-robot"></i>
                        </div>
                        <div class="chat-bubble">
                            <p>Halo! Saya AI Advisor LangkahKampus. Saya dapat membantu Anda dengan:</p>
                            <ul style="margin:0.5rem 0;padding-left:1.2rem;font-size:0.9rem;">
                                <li>Strategi pemilihan program studi SNBP</li>
                                <li>Analisis peluang berdasarkan hasil prediksi</li>
                                <li>Tips meningkatkan nilai dan peringkat</li>
                                <li>Informasi tentang universitas dan program studi</li>
                            </ul>
                            <p style="margin-top:0.5rem;">Silakan ketik pertanyaan Anda di bawah!</p>
                        </div>
                    </div>
                </div>

                <!-- Suggestion Chips -->
                <div id="suggestionChips" style="margin-bottom:1rem;display:flex;flex-wrap:wrap;gap:0.5rem;">
                    <button class="btn btn-outline btn-sm suggestion-chip" onclick="sendSuggestion('Bagaimana strategi memilih prodi SNBP?')">
                        <i class="fas fa-lightbulb"></i> Strategi Prodi
                    </button>
                    <button class="btn btn-outline btn-sm suggestion-chip" onclick="sendSuggestion('Apa itu Choice-2 Trap dan bagaimana menghindarinya?')">
                        <i class="fas fa-exclamation-triangle"></i> Choice-2 Trap
                    </button>
                    <button class="btn btn-outline btn-sm suggestion-chip" onclick="sendSuggestion('Tips meningkatkan peluang SNBP')">
                        <i class="fas fa-chart-line"></i> Tips Peluang
                    </button>
                    <button class="btn btn-outline btn-sm suggestion-chip" onclick="sendSuggestion('Bagaimana cara membaca hasil prediksi?')">
                        <i class="fas fa-question-circle"></i> Baca Prediksi
                    </button>
                </div>

                <!-- Chat Input -->
                <form id="chatForm" style="display:flex;gap:0.5rem;">
                    <input type="text" id="chatInput" class="form-control" placeholder="Ketik pertanyaan Anda tentang SNBP..." autocomplete="off" required style="flex:1;">
                    <button type="submit" class="btn btn-primary" id="chatSendBtn">
                        <i class="fas fa-paper-plane"></i> Kirim
                    </button>
                </form>
            </div>

            <!-- Info Card -->
            <div class="card mt-2" data-aos="fade-up" data-aos-delay="200">
                <h4 class="mb-2"><i class="fas fa-info-circle text-blue"></i> Tentang AI Advisor</h4>
                <ul style="font-size:0.9rem;color:var(--color-text-light);line-height:2;">
                    <li><i class="fas fa-check text-green"></i> Didukung oleh Fireworks AI (LLM)</li>
                    <li><i class="fas fa-check text-green"></i> Memahami konteks SNBP dan data SIDATA</li>
                    <li><i class="fas fa-check text-green"></i> Dapat menganalisis hasil prediksi Anda</li>
                    <li><i class="fas fa-check text-green"></i> Memberikan saran yang dipersonalisasi</li>
                </ul>
            </div>
        </div>
    </div>
</div>

<?php include '../includes/footer.php'; ?>
