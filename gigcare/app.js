const { useState, useEffect, useRef } = React;

// ── SVG Icon Components ─────────────────────────────────────
const Icons = {
  shield: () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
    </svg>
  ),
  home: () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/>
    </svg>
  ),
  clock: () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>
    </svg>
  ),
  user: () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>
    </svg>
  ),
  chevronDown: () => (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="6 9 12 15 18 9"/>
    </svg>
  ),
  logOut: () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/>
    </svg>
  ),
  settings: () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>
    </svg>
  ),
  alertTriangle: () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>
    </svg>
  ),
  checkCircle: () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/>
    </svg>
  ),
  mapPin: () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>
    </svg>
  ),
  smartphone: () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <rect x="5" y="2" width="14" height="20" rx="2" ry="2"/><line x1="12" y1="18" x2="12.01" y2="18"/>
    </svg>
  ),
  wifi: () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M5 12.55a11 11 0 0 1 14.08 0"/><path d="M1.42 9a16 16 0 0 1 21.16 0"/><path d="M8.53 16.11a6 6 0 0 1 6.95 0"/><line x1="12" y1="20" x2="12.01" y2="20"/>
    </svg>
  ),
  truck: () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <rect x="1" y="3" width="15" height="13"/><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/>
    </svg>
  ),
  lock: () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>
    </svg>
  ),
  users: () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>
    </svg>
  ),
  search: () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
    </svg>
  ),
  cloudRain: () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <line x1="16" y1="13" x2="16" y2="21"/><line x1="8" y1="13" x2="8" y2="21"/><line x1="12" y1="15" x2="12" y2="23"/><path d="M20 16.58A5 5 0 0 0 18 7h-1.26A8 8 0 1 0 4 15.25"/>
    </svg>
  ),
  wind: () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M9.59 4.59A2 2 0 1 1 11 8H2m10.59 11.41A2 2 0 1 0 14 16H2m15.73-8.27A2.5 2.5 0 1 1 19.5 12H2"/>
    </svg>
  ),
  sun: () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
    </svg>
  ),
  alertOctagon: () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polygon points="7.86 2 16.14 2 22 7.86 22 16.14 16.14 22 7.86 22 2 16.14 2 7.86 7.86 2"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
    </svg>
  ),
  activity: () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
    </svg>
  ),
  award: () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="8" r="7"/><polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88"/>
    </svg>
  ),
  zap: () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
    </svg>
  ),
  barChart: () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <line x1="12" y1="20" x2="12" y2="10"/><line x1="18" y1="20" x2="18" y2="4"/><line x1="6" y1="20" x2="6" y2="16"/>
    </svg>
  ),
  fileText: () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/>
    </svg>
  ),
  star: () => (
    <svg viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" strokeWidth="1">
      <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
    </svg>
  ),
  arrowRight: () => (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>
    </svg>
  ),
  check: () => (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="20 6 9 17 4 12"/>
    </svg>
  ),
  info: () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/>
    </svg>
  ),
  trendingDown: () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="23 18 13.5 8.5 8.5 13.5 1 6"/><polyline points="17 18 23 18 23 12"/>
    </svg>
  ),
  dollarSign: () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
    </svg>
  ),
};

// ── Mock Data ──────────────────────────────────────────────
const PLANS = [
  { id: 'basic',    name: 'Basic',    premium: 30, coverage: 1000 },
  { id: 'standard', name: 'Standard', premium: 50, coverage: 2000 },
  { id: 'premium',  name: 'Premium',  premium: 70, coverage: 3000 },
];

const RISK_MAP = {
  Bangalore: { score: 0.62, label: 'Medium', cls: 'risk-medium' },
  Mumbai:    { score: 0.78, label: 'High',   cls: 'risk-high'   },
  Delhi:     { score: 0.81, label: 'High',   cls: 'risk-high'   },
  Chennai:   { score: 0.55, label: 'Medium', cls: 'risk-medium' },
  Hyderabad: { score: 0.38, label: 'Low',    cls: 'risk-low'    },
};

const HISTORY = [
  { event: 'Heavy Rain Payout',   date: 'Mar 14, 2026', amount: 700, tier: 'green' },
  { event: 'AQI Alert Payout',    date: 'Mar 7, 2026',  amount: 450, tier: 'green' },
  { event: 'Heavy Rain Payout',   date: 'Feb 28, 2026', amount: 700, tier: 'yellow' },
];

const FRAUD_SIGNALS = [
  { key: 'gps',      Icon: Icons.mapPin,     label: 'GPS Consistency',            pass: true },
  { key: 'motion',   Icon: Icons.smartphone, label: 'Device Motion Pattern',      pass: true },
  { key: 'network',  Icon: Icons.wifi,       label: 'Network Signal Degraded',    pass: true },
  { key: 'platform', Icon: Icons.truck,      label: 'Platform Activity Match',    pass: true },
  { key: 'device',   Icon: Icons.lock,       label: 'Device Fingerprint',         pass: true },
  { key: 'cluster',  Icon: Icons.users,      label: 'No Cluster Ring Detected',   pass: true },
];

// ── Logo Component ─────────────────────────────────────────
function RevoLogo({ showTagline = false }) {
  return (
    <div className="nav-logo">
      <img src="logo.png" alt="Revo" />
      revo
      {showTagline && <span className="tagline">Income, uninterrupted.</span>}
    </div>
  );
}

// ── Arrow Icon ─────────────────────────────────────────────
const ArrowRight = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>
  </svg>
);

// ── Landing Page ───────────────────────────────────────────
function Landing({ onGetStarted }) {
  const scrollTo = (id) => {
    const el = document.getElementById(id);
    if (el) el.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <div className="landing">
      {/* Nav */}
      <nav className="landing-nav">
        <div className="landing-nav-logo">
          <img src="logo.png" alt="Revo" /> revo
        </div>
        <div className="landing-nav-links">
          <a href="#" onClick={e => { e.preventDefault(); scrollTo('how-it-works'); }}>How it Works</a>
          <a href="#" onClick={e => { e.preventDefault(); scrollTo('features'); }}>Features</a>
          <button className="landing-nav-cta" onClick={onGetStarted}>Get Started</button>
        </div>
      </nav>

      {/* Hero */}
      <section className="hero">
        <div className="hero-text">
          <div className="hero-badge">
            <Icons.zap /> AI-powered income protection
          </div>
          <h1>Income,<br/><span className="accent">uninterrupted.</span></h1>
          <p className="hero-sub">
            Revo monitors weather, traffic and city disruptions in real-time — and pays gig workers automatically when income drops.
          </p>
          <div className="hero-actions">
            <button className="hero-primary" onClick={onGetStarted}>
              Start Protection <ArrowRight />
            </button>
            <button className="hero-secondary" onClick={() => scrollTo('how-it-works')}>
              Learn More
            </button>
          </div>
        </div>

        <div className="hero-visual">
          <div className="hero-card">
            <div className="hero-card-label">Potential Coverage</div>
            <div className="hero-card-amount">₹2,000+</div>
            <div className="hero-card-tag">
              <Icons.zap /> Standard · ₹50/week
            </div>
            <div className="hero-mini-metrics">
              <div className="hero-mini-metric">
                <div className="hero-mini-metric-label">Avg. Earnings</div>
                <div className="hero-mini-metric-value green">₹800/day</div>
              </div>
              <div className="hero-mini-metric">
                <div className="hero-mini-metric-label">Typical Loss</div>
                <div className="hero-mini-metric-value red">₹500+</div>
              </div>
              <div className="hero-mini-metric">
                <div className="hero-mini-metric-label">Trust Score</div>
                <div className="hero-mini-metric-value orange">94/100</div>
              </div>
              <div className="hero-mini-metric">
                <div className="hero-mini-metric-label">Total Payouts</div>
                <div className="hero-mini-metric-value green">₹Cr+</div>
              </div>
            </div>
          </div>
          <div className="hero-float hero-float-1">
            <Icons.checkCircle /> Payout Verified
          </div>
          <div className="hero-float hero-float-2">
            <Icons.cloudRain /> Disruption Alert
          </div>
        </div>
      </section>

      {/* How it Works */}
      <section className="section" id="how-it-works">
        <div className="section-label">How it Works</div>
        <div className="section-title">Protected in 3 Simple Steps</div>
        <div className="section-sub">From sign-up to payout — the entire process is automated, instant, and transparent.</div>
        <div className="steps">
          <div className="step-card">
            <div className="step-number">1</div>
            <div className="step-icon"><Icons.user /></div>
            <div className="step-title">Register</div>
            <div className="step-desc">Tell us your city, platform, and weekly income. Takes under a minute.</div>
          </div>
          <div className="step-card">
            <div className="step-number">2</div>
            <div className="step-icon"><Icons.activity /></div>
            <div className="step-title">Risk Profile</div>
            <div className="step-desc">Our AI calculates your city's disruption risk using live weather and traffic signals.</div>
          </div>
          <div className="step-card">
            <div className="step-number">3</div>
            <div className="step-icon"><Icons.shield /></div>
            <div className="step-title">Get Covered</div>
            <div className="step-desc">Pick a plan. When disruptions hit, you get paid instantly via UPI — no paperwork.</div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="section" id="features">
        <div className="section-label">Why Revo</div>
        <div className="section-title">Built for the Gig Economy</div>
        <div className="section-sub">Traditional insurance doesn't work for delivery workers. Revo does.</div>
        <div className="features">
          <div className="feature-card">
            <div className="feature-icon orange"><Icons.cloudRain /></div>
            <div className="feature-title">Real-Time Triggers</div>
            <div className="feature-desc">Rainfall, heatwaves, AQI spikes, and curfews are monitored 24/7 via live APIs.</div>
          </div>
          <div className="feature-card">
            <div className="feature-icon green"><Icons.checkCircle /></div>
            <div className="feature-title">6-Signal Fraud Check</div>
            <div className="feature-desc">GPS, device fingerprint, network signal, and platform activity — all verified in seconds.</div>
          </div>
          <div className="feature-card">
            <div className="feature-icon grey"><Icons.zap /></div>
            <div className="feature-title">Instant UPI Payout</div>
            <div className="feature-desc">Approved claims are paid to your UPI account instantly. No forms, no delays.</div>
          </div>
          <div className="feature-card">
            <div className="feature-icon orange"><Icons.shield /></div>
            <div className="feature-title">Flexible Plans</div>
            <div className="feature-desc">Choose from Basic, Standard, or Premium — starting at just ₹25/week.</div>
          </div>
          <div className="feature-card">
            <div className="feature-icon green"><Icons.activity /></div>
            <div className="feature-title">Trust Score System</div>
            <div className="feature-desc">Build your score with each honest claim. Higher scores unlock better coverage.</div>
          </div>
          <div className="feature-card">
            <div className="feature-icon grey"><Icons.lock /></div>
            <div className="feature-title">Privacy First</div>
            <div className="feature-desc">Your data is encrypted end-to-end. Location is verified, never stored permanently.</div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <div className="cta-section">
        <div className="cta-box">
          <h2>Ready to protect your income?</h2>
          <p>Join the community of gig workers already protected by Revo.</p>
          <button onClick={onGetStarted}>
            Get Started Free <ArrowRight />
          </button>
        </div>
      </div>

      {/* Footer */}
      <footer className="landing-footer">
        <span>© 2026 Revo. Income, uninterrupted.</span>
        <span>
          <a href="#">Privacy</a> · <a href="#">Terms</a> · <a href="#">Contact</a>
        </span>
      </footer>
    </div>
  );
}

// ── User Dropdown ──────────────────────────────────────────
function UserDropdown({ worker, onSignOut, onTab }) {
  const [open, setOpen] = useState(false);
  const ref = useRef(null);

  useEffect(() => {
    const handler = (e) => { if (ref.current && !ref.current.contains(e.target)) setOpen(false); };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, []);

  const initials = (worker.name || 'U').split(' ').map(w => w[0]).join('').toUpperCase().slice(0,2);

  return (
    <div ref={ref} className={`nav-user ${open ? 'open' : ''}`} onClick={() => setOpen(!open)}>
      <div className="nav-avatar">{initials}</div>
      <span className="nav-username">{worker.name || 'User'}</span>
      <span className="nav-chevron"><Icons.chevronDown /></span>
      {open && (
        <div className="user-dropdown" onClick={e => e.stopPropagation()}>
          <button className="dropdown-item" onClick={() => { onTab('profile'); setOpen(false); }}>
            <Icons.user /> My Profile
          </button>
          <button className="dropdown-item" onClick={() => { onTab('policy'); setOpen(false); }}>
            <Icons.shield /> My Policy
          </button>
          <button className="dropdown-item" onClick={() => { onTab('history'); setOpen(false); }}>
            <Icons.clock /> Payout History
          </button>
          <div className="dropdown-divider" />
          <button className="dropdown-item" onClick={() => { setOpen(false); }}>
            <Icons.settings /> Settings
          </button>
          <button className="dropdown-item danger" onClick={() => { onSignOut(); setOpen(false); }}>
            <Icons.logOut /> Sign Out
          </button>
        </div>
      )}
    </div>
  );
}

// ── App ────────────────────────────────────────────────────
function App() {
  const [screen, setScreen] = useState('landing');
  const [tab, setTab] = useState('home');
  const [worker, setWorker] = useState({ name: '', city: 'Bangalore', platform: 'Swiggy', income: '6000', upi: '' });
  const [selectedPlan, setSelectedPlan] = useState(null);
  const [claimState, setClaimState] = useState(null);
  const [verifyStep, setVerifyStep] = useState(0);
  const [demoTier, setDemoTier] = useState('green');
  const [triggers, setTriggers] = useState([
    { name: 'Rainfall', Icon: Icons.cloudRain,     status: 'alert',   label: 'Alert' },
    { name: 'AQI',      Icon: Icons.wind,          status: 'normal',  label: 'Normal' },
    { name: 'Heat',     Icon: Icons.sun,           status: 'normal',  label: 'Normal' },
    { name: 'Curfew',   Icon: Icons.alertOctagon,  status: 'normal',  label: 'Normal' },
  ]);

  const risk = RISK_MAP[worker.city] || RISK_MAP['Bangalore'];
  const plan = PLANS.find(p => p.id === selectedPlan);
  const activeAlert = triggers.find(t => t.status === 'alert');

  useEffect(() => {
    if (screen !== 'dashboard') return;
    const id = setInterval(() => {
      setTriggers(prev => prev.map(t =>
        t.name === 'AQI'
          ? { ...t, status: t.status === 'normal' ? 'warning' : 'normal', label: t.status === 'normal' ? 'Warning' : 'Normal' }
          : t
      ));
    }, 8000);
    return () => clearInterval(id);
  }, [screen]);

  useEffect(() => {
    if (claimState !== 'verifying') return;
    setVerifyStep(0);
    const id = setInterval(() => {
      setVerifyStep(prev => {
        if (prev >= FRAUD_SIGNALS.length - 1) {
          clearInterval(id);
          setTimeout(() => setClaimState(demoTier), 600);
          return prev;
        }
        return prev + 1;
      });
    }, 420);
    return () => clearInterval(id);
  }, [claimState]);

  const startClaim = () => { setClaimState('verifying'); setVerifyStep(0); };
  const handleSignOut = () => { setScreen('landing'); setClaimState(null); setTab('home'); };

  if (screen === 'landing') return <Landing onGetStarted={() => setScreen('onboard')} />;
  if (screen === 'onboard') return <Onboard worker={worker} setWorker={setWorker} onNext={() => setScreen('risk')} />;
  if (screen === 'risk')    return <RiskProfile worker={worker} risk={risk} onNext={() => setScreen('policy')} />;
  if (screen === 'policy')  return <PolicySelect plan={selectedPlan} setPlan={setSelectedPlan} onNext={() => setScreen('dashboard')} />;

  return (
    <div className="pb-nav">
      <nav className="nav">
        <RevoLogo />
        <div className="nav-right">
          <UserDropdown worker={worker} onSignOut={handleSignOut} onTab={setTab} />
        </div>
      </nav>

      {/* ── HOME TAB ── */}
      {tab === 'home' && (
        <div className="container">
          <div className="dashboard-header">
            <h3>Your Coverage</h3>
            <div className="balance">₹{plan ? plan.coverage.toLocaleString() : '2,000'}</div>
            <span className="plan-tag">
              <Icons.zap />
              {plan ? plan.name : 'Standard'} · ₹{plan ? plan.premium : 50}/week
            </span>
          </div>

          <div className="metrics">
            <div className="metric-card">
              <div className="metric-label">Today's Earnings</div>
              <div className="metric-value red">₹300</div>
            </div>
            <div className="metric-card">
              <div className="metric-label">Normal Day</div>
              <div className="metric-value green">₹1,000</div>
            </div>
            <div className="metric-card">
              <div className="metric-label">Income Loss</div>
              <div className="metric-value red">₹700</div>
            </div>
            <div className="metric-card">
              <div className="metric-label">Trust Score</div>
              <div className="metric-value accent">94/100</div>
            </div>
          </div>

          {/* Demo tier selector */}
          {activeAlert && claimState === null && (
            <div className="demo-selector">
              <div className="demo-selector-label">Demo: simulate verification outcome</div>
              <div className="demo-selector-btns">
                {[
                  { t: 'green',  label: 'Auto-Approve', Icon: Icons.checkCircle },
                  { t: 'yellow', label: 'Soft Hold',    Icon: Icons.clock },
                  { t: 'red',    label: 'Review',       Icon: Icons.alertOctagon },
                ].map(({ t, label, Icon }) => (
                  <button key={t} className={`demo-btn ${demoTier === t ? `active-${t}` : ''}`} onClick={() => setDemoTier(t)}>
                    <Icon /> {label}
                  </button>
                ))}
              </div>
            </div>
          )}

          {activeAlert && claimState === null && (
            <div className="alert-banner alert-banner-danger">
              <div className="alert-icon" style={{ color: 'var(--red)' }}><Icons.alertTriangle /></div>
              <div>
                <div className="alert-title" style={{ color: 'var(--red)' }}>Disruption Detected – Heavy Rain</div>
                <div className="alert-desc" style={{ color: 'rgba(239,68,68,0.7)' }}>Rainfall threshold exceeded in {worker.city}. Initiating fraud verification before payout.</div>
                <button className="btn btn-primary" style={{ marginTop: 12, width: 'auto', padding: '8px 18px', fontSize: '0.85rem' }}
                  onClick={startClaim}>
                  <Icons.search /> Verify & Claim ₹700
                </button>
              </div>
            </div>
          )}

          {claimState === 'paid' && (
            <div className="alert-banner alert-banner-success">
              <div className="alert-icon" style={{ color: 'var(--green)' }}><Icons.checkCircle /></div>
              <div>
                <div className="alert-title" style={{ color: 'var(--green)' }}>Payout Sent – ₹700</div>
                <div className="alert-desc" style={{ color: 'rgba(34,197,94,0.7)' }}>All 6 signals verified. Transferred to your UPI account instantly.</div>
              </div>
            </div>
          )}

          {claimState === 'yellow' && (
            <div className="alert-banner alert-banner-warning">
              <div className="alert-icon" style={{ color: 'var(--yellow)' }}><Icons.clock /></div>
              <div>
                <div className="alert-title" style={{ color: 'var(--yellow)' }}>Claim Under Soft Hold</div>
                <div className="alert-desc" style={{ color: 'rgba(245,158,11,0.7)' }}>GPS signal was ambiguous due to poor network. We're verifying — usually resolves in 10–15 min.</div>
                <button className="btn btn-primary" style={{ marginTop: 10, width: 'auto', padding: '7px 16px', fontSize: '0.82rem', background: 'var(--yellow)', boxShadow: '0 2px 8px rgba(245,158,11,0.25)' }}
                  onClick={() => setClaimState('paid')}>
                  Confirm with Photo <Icons.arrowRight />
                </button>
              </div>
            </div>
          )}

          {claimState === 'red' && (
            <div className="alert-banner alert-banner-danger">
              <div className="alert-icon" style={{ color: 'var(--red)' }}><Icons.alertOctagon /></div>
              <div>
                <div className="alert-title" style={{ color: 'var(--red)' }}>Claim Flagged for Review</div>
                <div className="alert-desc" style={{ color: 'rgba(239,68,68,0.7)' }}>Multiple signals were inconsistent. A human reviewer will verify within 2 hours.</div>
                <div style={{ marginTop: 6, fontSize: '0.75rem', color: 'var(--red)', fontWeight: 600 }}>Appeal available if incorrectly flagged.</div>
              </div>
            </div>
          )}

          <div className="trigger-panel">
            <h4><Icons.activity /> Live Triggers</h4>
            {triggers.map(t => (
              <div className="trigger-row" key={t.name}>
                <div className="trigger-name">
                  <span style={{ color: t.status === 'alert' ? 'var(--red)' : t.status === 'warning' ? 'var(--yellow)' : 'var(--text-faint)' }}>
                    <t.Icon />
                  </span>
                  {t.name}
                </div>
                <span className={`trigger-status status-${t.status}`}>{t.label}</span>
              </div>
            ))}
          </div>

          <SignalPanel />
        </div>
      )}

      {/* ── HISTORY TAB ── */}
      {tab === 'history' && (
        <div className="container">
          <div className="card" style={{ marginBottom: 16 }}>
            <h2>Payout History</h2>
            <p className="subtitle">All past claims and verification outcomes</p>
            <div className="history-list">
              {(claimState === 'paid'
                ? [{ event: 'Heavy Rain Payout', date: 'Mar 20, 2026', amount: 700, tier: 'green' }, ...HISTORY]
                : HISTORY
              ).map((h, i) => (
                <div className="history-item" key={i}>
                  <div>
                    <div className="history-event">{h.event}</div>
                    <div className="history-date">{h.date}</div>
                  </div>
                  <div style={{ textAlign: 'right' }}>
                    <div className="history-amount">+₹{h.amount}</div>
                    <span className="tier-badge" style={{
                      background: h.tier==='green'?'var(--green-muted)':h.tier==='yellow'?'var(--yellow-muted)':'var(--red-muted)',
                      color: h.tier==='green'?'var(--green)':h.tier==='yellow'?'var(--yellow)':'var(--red)' }}>
                      {h.tier==='green'?'Auto-Approved':h.tier==='yellow'?'Soft Hold':'Reviewed'}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* ── POLICY TAB ── */}
      {tab === 'policy' && (
        <div className="container">
          <div className="card">
            <h2>My Policy</h2>
            <p className="subtitle">Active weekly plan</p>
            <div className={`risk-badge ${risk.cls}`}>
              <Icons.barChart /> Risk: {risk.label} ({(risk.score * 100).toFixed(0)}%)
            </div>
            <div style={{ marginBottom: 16 }}>
              {PLANS.map(p => (
                <div key={p.id} className={`plan-card ${selectedPlan === p.id ? 'selected' : ''}`}
                  onClick={() => setSelectedPlan(p.id)} style={{ marginBottom: 10 }}>
                  <div>
                    <div className="plan-name">{p.name}</div>
                    <div className="plan-coverage">Coverage up to ₹{p.coverage.toLocaleString()}</div>
                  </div>
                  <div className="plan-price">₹{p.premium}<span>/wk</span></div>
                </div>
              ))}
            </div>
            <button className="btn btn-primary">Update Plan</button>
          </div>
        </div>
      )}

      {/* ── PROFILE TAB ── */}
      {tab === 'profile' && (
        <div className="container">
          <div className="card" style={{ marginBottom: 16 }}>
            <div className="profile-header">
              <div className="profile-avatar">
                {(worker.name || 'U').split(' ').map(w => w[0]).join('').toUpperCase().slice(0,2)}
              </div>
              <div className="profile-name">{worker.name || 'User'}</div>
              <div className="profile-sub">{worker.platform} · {worker.city}</div>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 0, marginBottom: 20 }}>
              {[
                ['Name', worker.name || 'User', Icons.user],
                ['City', worker.city, Icons.mapPin],
                ['Platform', worker.platform, Icons.truck],
                ['Weekly Income', `₹${worker.income}`, Icons.dollarSign],
                ['UPI ID', worker.upi || 'Not set', Icons.zap],
                ['Member Since', 'Jan 2026', Icons.clock],
                ['Trust Score', '94 / 100', Icons.award],
                ['False Flags', '0', Icons.shield],
              ].map(([k, v, Icon]) => (
                <div key={k} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '11px 0', borderBottom: '1px solid var(--border)' }}>
                  <span style={{ color: 'var(--text-muted)', fontSize: '0.85rem', display: 'flex', alignItems: 'center', gap: 8 }}>
                    <span style={{ width: 16, height: 16, display: 'inline-flex', color: 'var(--text-faint)' }}><Icon /></span>
                    {k}
                  </span>
                  <span style={{ fontWeight: 600, fontSize: '0.85rem', color: 'var(--text)' }}>{v}</span>
                </div>
              ))}
            </div>
            <button className="btn btn-secondary" onClick={handleSignOut}>
              <Icons.logOut /> Sign Out
            </button>
          </div>
        </div>
      )}

      {/* Bottom Nav */}
      <div className="bottom-nav">
        {[
          { id: 'home',    Icon: Icons.home,     label: 'Home' },
          { id: 'history', Icon: Icons.fileText,  label: 'History' },
          { id: 'policy',  Icon: Icons.shield,    label: 'Policy' },
          { id: 'profile', Icon: Icons.user,      label: 'Profile' },
        ].map(n => (
          <div key={n.id} className={`bottom-nav-item ${tab === n.id ? 'active' : ''}`} onClick={() => setTab(n.id)}>
            <n.Icon />
            {n.label}
          </div>
        ))}
      </div>

      {/* Verification Modal */}
      {claimState === 'verifying' && (
        <div className="modal-overlay">
          <div className="modal" style={{ textAlign: 'left' }}>
            <div style={{ textAlign: 'center', marginBottom: 18 }}>
              <div style={{ width: 44, height: 44, margin: '0 auto 10px', color: 'var(--accent-light)' }}><Icons.search /></div>
              <h3>Verifying Your Claim</h3>
              <p style={{ fontSize: '0.82rem', color: 'var(--text-faint)', marginTop: 4, marginBottom: 0 }}>Running 6-signal fraud check...</p>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
              {FRAUD_SIGNALS.map((s, i) => (
                <div key={s.key} className="verify-row" style={{ opacity: i <= verifyStep ? 1 : 0.2 }}>
                  <span style={{ width: 18, height: 18, color: i <= verifyStep ? 'var(--accent-light)' : 'var(--text-faint)', display: 'inline-flex' }}><s.Icon /></span>
                  <span style={{ flex: 1, fontSize: '0.85rem', fontWeight: 500, color: 'var(--text)' }}>{s.label}</span>
                  {i <= verifyStep
                    ? <span style={{ color: 'var(--green)', fontWeight: 700, fontSize: '0.8rem', display: 'flex', alignItems: 'center', gap: 3 }}><Icons.check /> Pass</span>
                    : <span style={{ color: 'var(--text-faint)', fontSize: '0.8rem' }}>—</span>
                  }
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Green tier auto-approve modal */}
      {claimState === 'green' && (
        <div className="modal-overlay" onClick={() => setClaimState('paid')}>
          <div className="modal" onClick={e => e.stopPropagation()}>
            <div className="check" style={{ color: 'var(--green)' }}><Icons.checkCircle /></div>
            <h3>All Signals Verified</h3>
            <div style={{ display: 'flex', gap: 5, justifyContent: 'center', flexWrap: 'wrap', margin: '10px 0' }}>
              {FRAUD_SIGNALS.map(s => (
                <span key={s.key} style={{ background: 'var(--green-muted)', color: 'var(--green)', fontSize: '0.7rem', padding: '3px 8px', borderRadius: 8, fontWeight: 600, display: 'inline-flex', alignItems: 'center', gap: 3 }}>
                  <span style={{ width: 11, height: 11, display: 'inline-flex' }}><s.Icon /></span>
                  {s.label.split(' ').slice(0, 2).join(' ')}
                </span>
              ))}
            </div>
            <div className="amount">₹700</div>
            <p>Genuine disruption confirmed. Payout sent to your UPI instantly.</p>
            <button className="btn btn-primary" onClick={() => setClaimState('paid')}>Done</button>
          </div>
        </div>
      )}
    </div>
  );
}

// ── Signal Confidence Panel ────────────────────────────────
function SignalPanel() {
  const signals = [
    { label: 'GPS Consistency',    value: 92, color: 'var(--green)', Icon: Icons.mapPin },
    { label: 'Platform Activity',  value: 88, color: 'var(--green)', Icon: Icons.truck },
    { label: 'Device Motion',      value: 76, color: 'var(--yellow)', Icon: Icons.smartphone },
    { label: 'Network Match',      value: 95, color: 'var(--green)', Icon: Icons.wifi },
    { label: 'Cluster Risk',       value: 4,  color: 'var(--green)', invert: true, Icon: Icons.users },
  ];
  return (
    <div className="trigger-panel">
      <h4><Icons.shield /> Signal Confidence</h4>
      {signals.map(s => (
        <div key={s.label} style={{ marginBottom: 10 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '0.78rem', marginBottom: 4 }}>
            <span style={{ color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: 6, fontWeight: 500 }}>
              <span style={{ width: 14, height: 14, display: 'inline-flex', color: 'var(--text-faint)' }}><s.Icon /></span>
              {s.label}
            </span>
            <span style={{ fontWeight: 600, color: s.color }}>
              {s.invert ? `${s.value}% risk` : `${s.value}%`}
            </span>
          </div>
          <div className="signal-bar-track">
            <div className="signal-bar-fill" style={{ width: `${s.invert ? 100 - s.value : s.value}%`, background: s.color }}></div>
          </div>
        </div>
      ))}
      <div className="info-hint" style={{ marginTop: 10 }}>
        <Icons.info />
        <span>Isolation Forest + Graph Neural Network · Updated every 30s</span>
      </div>
    </div>
  );
}

// ── Onboarding Screen ──────────────────────────────────────
function Onboard({ worker, setWorker, onNext }) {
  const valid = worker.name.trim().length > 1;
  return (
    <div>
      <nav className="nav">
        <RevoLogo showTagline={true} />
        <div className="nav-steps">
          <span className="nav-step active">1. Register</span>
          <span className="nav-step">2. Risk</span>
          <span className="nav-step">3. Policy</span>
        </div>
      </nav>
      <div className="container">
        <div className="card">
          <div className="progress-bar">
            <div className="progress-step done"></div>
            <div className="progress-step"></div>
            <div className="progress-step"></div>
          </div>
          <h2>Welcome to Revo</h2>
          <p className="subtitle">AI-powered income protection for delivery workers</p>
          <div className="form-group">
            <label>Full Name</label>
            <input placeholder="e.g. Rahul Kumar" value={worker.name}
              onChange={e => setWorker({ ...worker, name: e.target.value })} />
          </div>
          <div className="form-group">
            <label>City</label>
            <select value={worker.city} onChange={e => setWorker({ ...worker, city: e.target.value })}>
              {['Bangalore','Mumbai','Delhi','Chennai','Hyderabad'].map(c => <option key={c}>{c}</option>)}
            </select>
          </div>
          <div className="form-group">
            <label>Delivery Platform</label>
            <select value={worker.platform} onChange={e => setWorker({ ...worker, platform: e.target.value })}>
              {['Swiggy','Zomato','Blinkit','Zepto','Dunzo'].map(p => <option key={p}>{p}</option>)}
            </select>
          </div>
          <div className="form-group">
            <label>Average Weekly Income (₹)</label>
            <input type="number" placeholder="6000" value={worker.income}
              onChange={e => setWorker({ ...worker, income: e.target.value })} />
          </div>
          <div className="form-group">
            <label>UPI ID</label>
            <input placeholder="yourname@upi" value={worker.upi}
              onChange={e => setWorker({ ...worker, upi: e.target.value })} />
          </div>
          <button className="btn btn-primary" disabled={!valid} onClick={onNext}
            style={{ opacity: valid ? 1 : 0.5 }}>
            Continue <Icons.arrowRight />
          </button>
        </div>
      </div>
    </div>
  );
}

// ── Risk Profile Screen ────────────────────────────────────
function RiskProfile({ worker, risk, onNext }) {
  return (
    <div>
      <nav className="nav">
        <RevoLogo />
        <div className="nav-steps">
          <span className="nav-step">1. Register</span>
          <span className="nav-step active">2. Risk</span>
          <span className="nav-step">3. Policy</span>
        </div>
      </nav>
      <div className="container">
        <div className="card">
          <div className="progress-bar">
            <div className="progress-step done"></div>
            <div className="progress-step done"></div>
            <div className="progress-step"></div>
          </div>
          <h2>Your Risk Profile</h2>
          <p className="subtitle">AI analysis for {worker.city}</p>
          <div className={`risk-badge ${risk.cls}`} style={{ marginBottom: 20 }}>
            <Icons.barChart />
            Risk Level: {risk.label} · Score {(risk.score * 100).toFixed(0)}/100
          </div>
          <div style={{ marginBottom: 20 }}>
            <div style={{ background: 'var(--bg-surface)', borderRadius: 6, height: 6, overflow: 'hidden' }}>
              <div style={{ width: `${risk.score * 100}%`, height: '100%', borderRadius: 6, transition: 'width 1s',
                background: risk.score > 0.7 ? 'var(--red)' : risk.score > 0.5 ? 'var(--yellow)' : 'var(--green)' }}></div>
            </div>
          </div>
          {[
            { label: 'Avg Rainfall Days/Month', value: risk.score > 0.7 ? '18' : risk.score > 0.5 ? '12' : '7', Icon: Icons.cloudRain },
            { label: 'AQI Exceedance Days',     value: risk.score > 0.7 ? '22' : risk.score > 0.5 ? '14' : '5', Icon: Icons.wind },
            { label: 'Historical Disruptions',  value: risk.score > 0.7 ? 'High' : risk.score > 0.5 ? 'Moderate' : 'Low', Icon: Icons.activity },
            { label: 'Fraud Risk Index',        value: risk.score > 0.7 ? 'Elevated' : 'Low', Icon: Icons.alertTriangle },
            { label: 'AI Model',                value: 'Gradient Boosting', Icon: Icons.zap },
          ].map(({ label, value, Icon }) => (
            <div key={label} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '11px 0', borderBottom: '1px solid var(--border)', fontSize: '0.85rem' }}>
              <span style={{ color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: 8 }}>
                <span style={{ width: 15, height: 15, display: 'inline-flex', color: 'var(--text-faint)' }}><Icon /></span>
                {label}
              </span>
              <span style={{ fontWeight: 600, color: 'var(--text)' }}>{value}</span>
            </div>
          ))}
          <button className="btn btn-primary" style={{ marginTop: 22 }} onClick={onNext}>
            Choose a Plan <Icons.arrowRight />
          </button>
        </div>
      </div>
    </div>
  );
}

// ── Policy Selection Screen ────────────────────────────────
function PolicySelect({ plan, setPlan, onNext }) {
  return (
    <div>
      <nav className="nav">
        <RevoLogo />
        <div className="nav-steps">
          <span className="nav-step">1. Register</span>
          <span className="nav-step">2. Risk</span>
          <span className="nav-step active">3. Policy</span>
        </div>
      </nav>
      <div className="container">
        <div className="card">
          <div className="progress-bar">
            <div className="progress-step done"></div>
            <div className="progress-step done"></div>
            <div className="progress-step done"></div>
          </div>
          <h2>Choose Your Plan</h2>
          <p className="subtitle">Weekly subscription · Cancel anytime</p>
          <div className="plans">
            {PLANS.map(p => (
              <div key={p.id} className={`plan-card ${plan === p.id ? 'selected' : ''}`} onClick={() => setPlan(p.id)}>
                <div>
                  <div className="plan-name" style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                    {p.name}
                    {p.id === 'standard' && <span style={{ width: 13, height: 13, color: 'var(--yellow)', display: 'inline-flex' }}><Icons.star /></span>}
                  </div>
                  <div className="plan-coverage">Coverage up to ₹{p.coverage.toLocaleString()}/week</div>
                </div>
                <div className="plan-price">₹{p.premium}<span>/wk</span></div>
              </div>
            ))}
          </div>
          <div className="info-hint" style={{ marginBottom: 20 }}>
            <Icons.lock />
            <span>6-signal fraud verification · Auto-payout on genuine claims · UPI instant transfer</span>
          </div>
          <button className="btn btn-primary" disabled={!plan} onClick={onNext}
            style={{ opacity: plan ? 1 : 0.5 }}>
            Activate Policy <Icons.arrowRight />
          </button>
        </div>
      </div>
    </div>
  );
}

// ── Mount ──────────────────────────────────────────────────
ReactDOM.createRoot(document.getElementById('root')).render(<App />);
