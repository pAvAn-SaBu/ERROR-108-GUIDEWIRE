# ⚡ Revo

### AI-Powered Parametric Insurance for Gig Delivery Workers

---

## 1. Persona & Scenario

### Persona
**Rahul – Food Delivery Partner (Swiggy)**  
Location: Bangalore  
Average daily work: 8 hours  
Average weekly income: ₹6000

### Scenario
On a normal day Rahul completes deliveries and earns his full income. However, during extreme rainfall or severe pollution:
- Delivery demand drops
- Orders reduce
- Rahul cannot work full hours

**Example:**  
Normal day income → ₹1000  
Heavy rain day income → ₹300  
**Income loss → ₹700**  
Revo detects the disruption automatically and **provides compensation for the lost income**.

---

## 2. Application Workflow

1. **Worker Onboarding** — Delivery workers register using their location, platform details, and payment information.
2. **Risk Profiling** — AI models analyze environmental risks associated with the worker's location.
3. **Policy Selection** — Workers choose a weekly insurance plan.
4. **Real-Time Monitoring** — The system continuously monitors environmental conditions through external APIs.
5. **Parametric Trigger Detection** — When disruption thresholds are exceeded, the system automatically triggers a claim.
6. **Fraud Verification** — Fraud detection algorithms validate the worker's location and activity.
7. **Instant Payout** — Compensation is sent via UPI or a payment gateway.

---

## 3. Weekly Premium Model

Gig workers earn on a weekly basis, so Revo uses a **weekly subscription-based insurance model**.  
Weekly Premium = Base Premium + Risk Adjustment

| Plan | Weekly Premium | Coverage |
|------|----------------|----------|
| Basic | ₹30 | ₹1000 |
| Standard | ₹50 | ₹2000 |
| Premium | ₹70 | ₹3000 |

*Premiums may vary depending on location risk and historical disruption patterns.*

---

## 4. Parametric Triggers

Revo uses **parametric triggers** based on measurable external conditions instead of manual claims.

| Event | Trigger Condition |
|-------|-------------------|
| Heavy Rain | Rainfall exceeds city-specific threshold |
| Extreme Heat | Temperature above safe working level |
| Air Pollution | AQI exceeds safe limit |
| Curfew / Zone Closure | Government restriction detected |

To avoid hardcoding thresholds, Revo uses **historical weather percentiles and anomaly detection models** to identify extreme environmental conditions.

---

## 5. Platform Choice: Mobile Application

Revo will be implemented primarily as a **mobile application**.  
Gig workers interact with delivery platforms mainly through smartphones, making mobile the most accessible platform.

**Advantages:**
- Easy onboarding and policy management
- Real-time notifications about disruptions and payouts
- GPS-based location validation for fraud prevention
- Seamless integration with UPI payments
- Higher adoption among gig workers

The backend architecture will support both mobile and web interfaces, but the primary user experience will be **mobile-first**.

---

## 6. AI / ML Integration

AI plays a central role in the Revo platform.

### Risk Prediction
AI models analyze historical environmental and disruption data to estimate location-based risk scores (e.g., Random Forest, Gradient Boosting).  
**Output:** Risk score (0–1)

### Dynamic Premium Calculation
Premium pricing is adjusted based on location risk. Lower risk area = lower premium; high risk area = higher premium.

### Anomaly Detection for Disruptions
AI models (Isolation Forest, One-Class SVM) detect abnormal conditions such as unusual rainfall or pollution spikes.

### Fraud Detection
Models identify suspicious activity: GPS spoofing, fake location reporting, duplicate claims, or worker inactivity during disruption.

---

## 7. System Architecture

`Mobile Application` ↓ `Frontend Interface` ↓ `Backend API Services` ↓ `AI Risk Engine` ↓ `Trigger Detection System` ↓ `Fraud Detection Module` ↓ `Payment Gateway`

**External Data Sources:**
- Weather APIs
- Air Quality APIs
- Traffic / disruption APIs

---

## 8. Technology Stack

- **Frontend:** React Native (Mobile App)
- **Backend:** Python FastAPI
- **AI / ML:** Python (Scikit-learn, Pandas, NumPy)
- **Database:** PostgreSQL
- **External APIs:** Weather API, AQI API
- **Cloud Infrastructure:** AWS / GCP

---

## 9. Development Plan

- **Phase 1 – Ideation & Architecture:** Define persona, design workflow, plan AI integration.
- **Phase 2 – Core Platform:** Onboarding, policy management, premium calculation, trigger monitoring, claims processing.
- **Phase 3 – Optimization:** Fraud detection models, instant payout simulation, worker/admin dashboards.

---

## 10. Expected Impact

Revo provides gig workers with **automatic financial protection against income loss caused by environmental disruptions**. By combining parametric insurance, AI risk modeling, and real-time monitoring, Revo delivers **fast, transparent, and scalable micro-insurance for the gig economy**.

---

## ⚡ Project Showcase

### **💡 Inspiration**
Gig workers are the backbone of our modern economy, yet they are the most vulnerable to climate and city disruptions. We were inspired by the story of "Rahul," a delivery partner whose daily income can drop by 70% due to a single heavy downpour. Traditional insurance is too slow and bureaucratic for these micro-losses. We wanted to build a solution that was **instant, automated, and invisible.**

### **🚀 What it does**
**Revo** is an AI-powered parametric insurance platform. Instead of manual claims, it uses real-time data from weather and city APIs to detect income-threatening events (heavy rain, heatwaves, or curfews). When a disruption threshold is crossed in a worker’s specific zone, the system automatically triggers a claim. After a 4-second **6-signal fraud verification**, the payout is sent instantly via UPI—no paperwork, no waiting.

### **🛠️ How we built it**
We built a high-fidelity web prototype using **React 18** and a custom **Vanilla CSS Design System** focused on "Glassmorphism" for a premium feel. The core engine simulates real-time API polling and features a state-managed onboarding flow. The "special sauce" is our logic for **Multi-Signal Behavioral Fingerprinting**, which cross-references GPS movement, device sensors, and network signal degradation to verify claims without penalizing honest workers.

### **🚧 Challenges we ran into**
One of the biggest challenges was balancing a complex, data-heavy "Fraud Verification" process with a user experience that felt fast and frictionless. We solved this by designing an animated 3-tier resolution flow that keeps the worker informed in real-time while the AI works in the background.

### **🏆 Accomplishments that we're proud of**
We are incredibly proud of the **UI/UX transition** from a basic concept to a professional-grade landing page and dashboard. Achieving a full user journey—from initial landing to a verified claim payout—in a single, seamless flow was a major milestone for the team.

### **📖 What we learned**
We learned that **parametric triggers** are not just about weather; they are about trust. Building an insurance product for the gig economy requires moving away from "proof of loss" and toward "proof of event" backed by deep behavioral analytics. Simple GPS isn't enough; multi-signal verification is the only way to scale trust.

### **🔮 What's next for Revo**
*   **Native Mobile App:** Moving from a web prototype to a full React Native mobile application.
*   **Live API Integration:** Connecting the dashboard to actual Hyperlocal Weather and AQI APIs.
*   **Expansion:** Integrating directly with delivery platform APIs (Swiggy, Zomato, Uber) to use active delivery logs as a 7th verification signal.

