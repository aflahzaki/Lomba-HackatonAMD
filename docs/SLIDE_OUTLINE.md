# LangkahKampus - Slide Presentation Outline

10-slide presentation for AMD Hackathon ACT II - Unicorn Track submission.

**Language:** English (international judges)
**Format:** 16:9 slides
**Duration:** 5-7 minutes presentation

---

## Slide 1: Title

### Content
- **Title:** LangkahKampus - AI-Powered SNBP Admission Predictor
- **Subtitle:** Helping Indonesian Students Make Data-Driven University Choices
- **Event:** AMD Hackathon ACT II - Unicorn Track
- **Team:** [Team Name] - [Member Names]
- **Visual:** App screenshot or logo with "Powered by AMD" badge

### Talking Points
- Brief introduction of team
- One-liner about the project: "We built an ML-powered platform that predicts Indonesian university admission probabilities using AMD GPU acceleration"
- Set the tone: this is about real social impact through AI on AMD

### Images
- App landing page screenshot (from http://localhost:8080)
- AMD logo badge

---

## Slide 2: The Problem

### Content
- **Headline:** 1.8M+ Students, Zero Prediction Tools
- **Key Statistics:**
  - 1.8 million students compete in SNBP annually
  - 84 universities, 3,058 study programs
  - No existing tools to estimate admission probability
  - Students choose blindly, leading to mismatched applications
- **Impact:** Thousands of students miss opportunities due to poor strategy

### Talking Points
- SNBP is Indonesia's largest merit-based admission pathway
- Students only get 2 choices - wrong choices mean a wasted year
- Current approach: ask seniors, guess based on rumors, no data
- There is a clear gap for an AI-powered solution

### Images
- `references_images/snbp_acceptance_stats.png` - shows acceptance statistics

---

## Slide 3: Our Solution

### Content
- **Headline:** AI-Powered Admission Prediction + Personalized Guidance
- **Three pillars:**
  1. **ML Prediction** - XGBoost model predicting admission probability (R2 = 0.9457)
  2. **Smart Recommendations** - Alternative programs with higher chances
  3. **AI Advisor** - LLM-powered chatbot for personalized strategic guidance
- **Coverage:** 3,058 programs across 84 universities

### Talking Points
- End-to-end solution: from prediction to recommendation to personalized advice
- Trained on real admission data (SIDATA PTN)
- AI Advisor understands context from prediction results
- Supports multi-turn conversations for deeper guidance
- Fallback mechanisms ensure system always provides value

### Images
- Screenshot of prediction results page showing probability and variable breakdown
- Screenshot of AI Advisor chat

---

## Slide 4: Live Demo / Screenshots

### Content
- **Left panel:** Prediction input form with sample data
- **Right panel:** Results showing 72.5% probability with breakdown
- **Bottom:** AI Advisor conversation snippet
- **Call-out boxes:** Key features highlighted

### Talking Points
- Walk through user journey: enter grades, ranking, target program
- Show how probability is calculated with variable breakdown
- Show confidence intervals for transparency
- Demonstrate AI Advisor with prediction context
- Show alternative program recommendations

### Images
- Screenshots from the running application
- Variable breakdown visualization
- AI Advisor chat interface

---

## Slide 5: Technical Architecture

### Content
- **Architecture diagram:**
  ```
  Users --> PHP Frontend (Apache)
              |
              v
         AI Backend (FastAPI/Python)
         /        |          \
  XGBoost    Fireworks AI   MySQL 8.0
  (AMD GPU)  (AMD Hardware)  (3058 programs)
  ```
- **Tech Stack table:** PHP 8.2, Python 3.10, FastAPI, XGBoost, MySQL, Docker
- **Deployment:** Docker Compose (3 services)

### Talking Points
- Clean separation of concerns: frontend, AI backend, database
- Python backend handles all ML and AI operations
- Fireworks AI for LLM capabilities (Llama 3.1 8B)
- Docker Compose for easy deployment and reproducibility
- Database pre-loaded with official SIDATA PTN data

### Images
- Architecture diagram (clean, professional)
- `references_images/xai_framework_comparison.png` - XAI framework comparison

---

## Slide 6: AMD Platform Integration

### Content
- **Headline:** Built on AMD - From Training to Inference
- **Training:**
  - AMD Developer Cloud with Instinct MI210 (64GB HBM2e)
  - ROCm platform for GPU acceleration
  - XGBoost GPU hist method via HIP compatibility
  - 5-10x speedup vs CPU training
- **Inference:**
  - Fireworks AI running on AMD hardware
  - Llama 3.1 8B Instruct for AI Advisor
  - Low-latency LLM responses
- **Code snippet:** `device="cuda"` (works with ROCm via HIP)

### Talking Points
- AMD is used throughout the entire AI pipeline
- Training: ROCm enables XGBoost GPU acceleration seamlessly
- The HIP compatibility layer means `device='cuda'` just works on AMD GPUs
- Inference: Fireworks AI runs models on AMD hardware infrastructure
- Auto-detection: script detects ROCm via /opt/rocm, HIP_VISIBLE_DEVICES, rocm-smi
- Falls back gracefully to CPU when AMD GPU is not present
- Reference `docs/AMD_USAGE.md` for full technical details

### Images
- Code screenshot of `train_on_amd_cloud.py` (ROCm detection + GPU params)
- AMD Instinct MI210 specs graphic (optional)

---

## Slide 7: ML Model Performance

### Content
- **Headline:** High-Accuracy Predictions with AMD GPU Training
- **Metrics:**
  - R2 Score: 0.9457
  - MAE: 0.0234
  - RMSE: 0.0312
- **Charts:**
  - Feature importance visualization
  - Actual vs. predicted scatter plot
- **Training data:** SIDATA PTN (84 universities, 3,058 programs)

### Talking Points
- R2 of 0.9457 means our model explains ~95% of variance in admission outcomes
- Six key features: competition ratio, score average, ranking, accreditation, capacity, applicant trend
- Feature importance shows competition ratio is the strongest predictor
- Actual vs. predicted chart shows tight correlation with minimal outliers
- Prediction distribution matches real-world admission patterns
- Model trained with XGBoost optimized for AMD GPU histogram method

### Images
- `ai_backend/training/evaluation_charts/feature_importance.png`
- `ai_backend/training/evaluation_charts/actual_vs_predicted.png`
- `ai_backend/training/evaluation_charts/prediction_distribution.png`
- `ai_backend/training/evaluation_charts/residual_plot.png`

---

## Slide 8: Market Opportunity

### Content
- **TAM/SAM/SOM:**
  - TAM: All Indonesian high school students (6.9M)
  - SAM: Students applying to university via SNBP (1.8M)
  - SOM: Tech-savvy students in urban areas (300K+)
- **Market validation:**
  - Growing demand for EdTech in Indonesia
  - No direct competitor with ML prediction
  - Government push for digital education
- **Revenue model:** Freemium (basic free, premium features paid)

### Talking Points
- Indonesia's EdTech market is growing rapidly
- SNBP is annual - recurring user base every year
- No existing solution offers ML-based admission prediction
- Strong network effects: more users = more data = better predictions
- Scalable to other admission pathways (SNBT, Mandiri)

### Images
- `references_images/tam_sam_som_diagram.png`
- `references_images/market_validation_trends.png`

---

## Slide 9: Completeness & Roadmap

### Content
- **What is built:**
  - Full-stack application (containerized, deployable)
  - ML pipeline with AMD GPU training support
  - AI Advisor with multi-turn conversation
  - Real university data (3,058 programs)
  - Demo mode for showcase
  - Comprehensive documentation
- **Roadmap:**
  - Phase 1: Public beta launch
  - Phase 2: Mobile app
  - Phase 3: Integration with school systems
  - Phase 4: Expand to SNBT and Mandiri pathways

### Talking Points
- This is not a prototype - it is a complete, working application
- Every endpoint is functional and tested (47 tests passing)
- Docker Compose makes deployment trivial
- Demo script proves the full pipeline works end-to-end
- Clear path to production and scale

### Images
- Screenshot of passing tests or health check
- Simple roadmap timeline graphic

---

## Slide 10: Call to Action

### Content
- **Headline:** LangkahKampus - Empowering Students with AMD AI
- **Key differentiators:**
  - Real social impact (education accessibility)
  - Full AMD platform utilization (training + inference)
  - Production-ready application
  - Data-driven approach with proven accuracy
- **Links:**
  - GitHub: https://github.com/aflahzaki/Lomba-HackatonAMD
  - Demo: [App URL]
- **Closing:** "AI on AMD for Education Accessibility"
- **"Powered by AMD" badge prominently displayed**

### Talking Points
- Summarize the three key strengths: social impact, AMD integration, completeness
- Reiterate how AMD hardware enables the solution
- Thank the judges
- Invite them to explore the GitHub repo and try the demo
- Express vision: making university admission fair and transparent through AI

### Images
- App landing page screenshot
- "Powered by AMD" badge
- Team photo (optional)

---

## Presentation Tips

1. **Timing:** Spend more time on slides 3 (Solution), 4 (Demo), and 6 (AMD) - these align with judging criteria
2. **Visuals:** Use the evaluation charts and reference images - they add credibility
3. **Energy:** Start and end strong - first impression and last impression matter most
4. **AMD Focus:** Every time you mention a technical achievement, connect it back to AMD
5. **Story:** Frame it as "problem > solution > impact" narrative
6. **Practice:** Run through the presentation at least 3 times before recording
