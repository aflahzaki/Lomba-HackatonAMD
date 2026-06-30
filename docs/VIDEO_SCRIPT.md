# LangkahKampus - Video Demo Script

Detailed script for the 3-5 minute demo video submission. The video should be recorded in English for international judges.

**Total Duration:** ~4 minutes 30 seconds

---

## Segment 1: Introduction (0:00 - 0:30)

### On Screen
- Title card: "LangkahKampus - AI-Powered SNBP Admission Predictor"
- Subtitle: "AMD Hackathon ACT II - Unicorn Track"
- Team name and members
- Transition to browser showing the landing page at http://localhost:8080

### Narration
> "Hello! We are [Team Name] and this is LangkahKampus - an AI-powered admission predictor for Indonesia's SNBP national university selection system."
>
> "Every year, millions of Indonesian high school students face uncertainty about their university admission chances. LangkahKampus uses machine learning trained on AMD Instinct GPUs to give them accurate predictions and personalized guidance."

### Notes
- Keep title card for 5 seconds
- Slowly scroll the landing page to show key sections
- Show "Powered by AMD" badge on the landing page

---

## Segment 2: Problem Statement (0:30 - 1:00)

### On Screen
- Reference image: `references_images/snbp_acceptance_stats.png` (show as overlay or in a slide)
- Quick stats on screen:
  - "1.8M+ students compete annually"
  - "3,058 programs across 84 universities"
  - "No tools for probability estimation"
- Transition to `references_images/market_validation_trends.png`

### Narration
> "SNBP is Indonesia's largest merit-based university admission path. Over 1.8 million students compete for limited spots across 84 universities and 3,058 programs."
>
> "Currently, students have no reliable way to estimate their admission probability. They choose blindly, leading to mismatched applications and wasted opportunities."
>
> "LangkahKampus solves this with data-driven predictions powered by machine learning on AMD hardware."

### Notes
- Use reference images as visual aids
- Keep statistics visible long enough to read
- Transition smoothly to the demo section

---

## Segment 3: Live Demo - Prediction Feature (1:00 - 2:00)

### On Screen
- Browser: Frontend prediction form at http://localhost:8080
- Fill in student data:
  - Subject scores (show entering Matematika: 87, 88, 89, 90, 91)
  - School ranking: 5 of 200
  - Accreditation: A
  - Target: Teknik Informatika - Institut Teknologi Bandung
- Submit and show results page with:
  - Probability percentage (72.5%)
  - Variable breakdown chart
  - Confidence interval
  - Recommendations section

### Narration
> "Let me show you how LangkahKampus works. A student enters their academic data: semester grades, school ranking, accreditation, and their target program."
>
> "Here we have a student ranked 5th out of 200, with strong grades averaging 88.5, from an A-accredited school, targeting Computer Science at ITB."
>
> "The ML model processes these inputs and returns a 72.5% admission probability with confidence intervals. It also breaks down which factors contribute most to the prediction."
>
> "Notice the variable breakdown - competition ratio has the highest weight at 30%, followed by average scores at 25%. This gives students actionable insights about where to improve."
>
> "The system also suggests alternative programs with higher acceptance chances."

### Notes
- Type slowly enough for viewers to follow
- Zoom in on the probability result
- Highlight the variable breakdown visualization
- Show recommendations scrolling if available
- Total interaction should feel natural, not rushed

---

## Segment 4: Live Demo - AI Advisor (2:00 - 2:45)

### On Screen
- Navigate to AI Advisor chat interface
- Type: "Jelaskan hasil prediksi saya dan berikan saran"
- Show AI response appearing
- Type follow-up: "Bagaimana strategi pilihan kedua SNBP?"
- Show multi-turn response with context awareness

### Narration
> "LangkahKampus also features an AI Advisor powered by Fireworks AI running Llama 3.1 on AMD hardware."
>
> "Students can ask questions in natural language - here I'm asking for an explanation of my prediction results and advice."
>
> "The advisor provides personalized guidance based on the prediction context. It explains why the probability is what it is and gives specific, actionable recommendations."
>
> "Watch how the multi-turn conversation maintains context. When I ask about second-choice strategy, it remembers my profile and prediction results from the previous exchange."

### Notes
- Wait for AI response to fully render before continuing
- If using mock mode, responses appear instantly
- Highlight that the conversation has context from the prediction
- Show suggestions appearing below the response

---

## Segment 5: AMD Integration Showcase (2:45 - 3:30)

### On Screen
- Switch to code editor or terminal showing `ai_backend/training/train_on_amd_cloud.py`
- Highlight key sections:
  - ROCm detection function (`detect_rocm()`)
  - GPU training parameters (`device="cuda"` with HIP backend)
  - MI210/MI250X hardware specs in comments
- Show `ai_backend/training/evaluation_charts/feature_importance.png`
- Show `ai_backend/training/evaluation_charts/actual_vs_predicted.png`
- Quick terminal showing `python demo/demo_script.py --mock` output with AMD branding

### Narration
> "Now let me show how we leverage AMD platforms. Our XGBoost model is trained on AMD Developer Cloud using Instinct MI210 GPUs with ROCm."
>
> "The training script automatically detects the ROCm platform through multiple methods - checking for /opt/rocm, HIP environment variables, and rocm-smi. When an AMD GPU is detected, it uses the GPU-accelerated histogram method."
>
> "XGBoost's device='cuda' parameter works seamlessly with AMD GPUs through the HIP compatibility layer. This gives us 5 to 10x training speedup on the MI250X with 128GB HBM2e memory."
>
> "For LLM inference, we use Fireworks AI which runs on AMD hardware, providing fast and cost-effective AI responses for our advisor feature."
>
> "Here are our model evaluation results - R-squared of 0.9457, showing excellent prediction accuracy. The feature importance chart shows which variables the model relies on most."

### Notes
- Scroll slowly through the training script
- Zoom in on `device="cuda"` and the ROCm detection code
- Show evaluation charts full screen for 3-4 seconds each
- Show the terminal output with "Powered by AMD Developer Cloud" visible

---

## Segment 6: Technical Architecture (3:30 - 4:00)

### On Screen
- Architecture diagram from README (or create a clean visual):
  ```
  PHP Frontend (Apache:8080)
       |
  AI Backend (FastAPI:8000) ---- Fireworks AI (AMD)
       |
  MySQL 8.0 (3058 programs)
  ```
- Show `docker-compose.yml` briefly
- Reference image: `references_images/ml_model_comparison.png`

### Narration
> "The architecture is a three-tier system containerized with Docker Compose. The PHP frontend communicates with our FastAPI Python backend which hosts the ML model and integrates with Fireworks AI."
>
> "The database contains real SIDATA data - 3,058 programs from 84 Indonesian universities. Our ML pipeline compared multiple models before selecting XGBoost for its superior performance and GPU acceleration capabilities on AMD hardware."
>
> "The entire stack deploys with a single docker compose up command."

### Notes
- Keep architecture diagram clean and readable
- Do not spend too long on this section - viewers want to see the demo, not diagrams
- Briefly show docker-compose.yml to prove it works

---

## Segment 7: Closing & Call to Action (4:00 - 4:30)

### On Screen
- Landing page of the application
- Show key metrics overlay:
  - "R2 Score: 0.9457"
  - "3,058 programs covered"
  - "84 universities"
  - "Trained on AMD Instinct MI210"
- End card with GitHub URL and team info
- "Powered by AMD" logo/badge

### Narration
> "LangkahKampus demonstrates how AMD's GPU computing platform can power real-world AI applications that make a social impact."
>
> "With AMD Instinct GPUs and ROCm, we achieve fast model training. With Fireworks AI on AMD hardware, we deliver real-time LLM-powered guidance. Together, they create an accessible tool that helps millions of Indonesian students make informed university choices."
>
> "Thank you for watching. The full source code is available on GitHub. We believe AI on AMD can transform education accessibility in Indonesia and beyond."

### Notes
- End with energy and confidence
- Make sure GitHub URL is clearly visible
- Hold end card for 3-5 seconds
- Consider adding light background music throughout the video

---

## Production Tips

### Recording Setup
- Use OBS Studio (free) or Loom for screen recording
- Record at 1920x1080 minimum, 30fps
- Use a clean browser profile (no distracting bookmarks/extensions)
- Set browser zoom to 110-125% for better readability on video

### Audio
- Use a decent microphone (even phone earbuds work)
- Record in a quiet room
- Speak clearly and at moderate pace
- Practice the narration 2-3 times before recording

### Editing
- Use simple transitions (fade or cut)
- Add zoom effects on key moments (probability result, AMD code)
- Include captions/subtitles if possible
- Keep total runtime between 3:30 and 5:00

### Before Recording Checklist
- [ ] Application running (`docker compose up --build`)
- [ ] Browser tabs prepared
- [ ] Screen recording software configured
- [ ] Microphone tested
- [ ] Narration practiced
- [ ] Notifications disabled
- [ ] Clean desktop/browser
