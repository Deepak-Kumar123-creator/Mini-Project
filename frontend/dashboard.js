const API_BASE = 'http://127.0.0.1:5000/api';
async function submitPrediction(formData) {
    const btn        = document.getElementById('btn-predict');
    const resultPanel = document.getElementById('result-panel');
    const errorMsg   = document.getElementById('error-msg');
    const errorText  = document.getElementById('error-text');
    resultPanel.style.display = 'none';
    errorMsg.style.display    = 'none';
    btn.classList.add('loading');

    try {
        const response = await fetch(`${API_BASE}/predict`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        if (!response.ok || data.status === 'error') {
            throw new Error(data.message || `Server error: ${response.status}`);
        }
        renderResult(data);
        resultPanel.style.display = 'block';
        setTimeout(() => {
            resultPanel.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 100);

    } catch (err) {
        errorText.textContent = err.message || 'Could not connect to the server. Is the Flask backend running?';
        errorMsg.style.display = 'flex';
        errorMsg.style.gap = '10px';
        errorMsg.style.alignItems = 'center';
        console.error('[Prediction Error]', err);
    } finally {
        btn.classList.remove('loading');
    }
}

// =============================================================================
// 2. RENDER PREDICTION RESULT
// =============================================================================

/**
 * renderResult(data)
 * Builds the HTML for the prediction result card using the API response.
 *
 * @param {object} data - API response from /api/predict
 * @param {number} data.prediction  - 0 or 1
 * @param {number} data.risk_score  - 0.0 to 1.0
 * @param {string} data.risk_level  - 'LOW' | 'MODERATE' | 'HIGH'
 * @param {string} data.message     - Human-readable result
 * @param {number} data.confidence  - Percentage
 * @param {number} data.patient_id  - Saved DB id
 */
function renderResult(data) {
    const { prediction, risk_score, risk_level, message, confidence, patient_id } = data;
    const icon     = prediction === 1 ? 'fa-heart-crack' : 'fa-heart';
    const iconColor = prediction === 1 ? '#ef4444' : '#10b981';
    const diagLabel = prediction === 1 ? 'Heart Disease Detected' : 'No Heart Disease Detected';
    const badgeIcon = {
        LOW:      'fa-shield-heart',
        MODERATE: 'fa-triangle-exclamation',
        HIGH:     'fa-heart-pulse'
    }[risk_level] || 'fa-circle-info';

    const riskPercent = Math.round(risk_score * 100);

    const html = `
        <!-- Diagnosis Label -->
        <div style="display:flex; align-items:center; gap:14px; margin-bottom:20px;">
            <div style="width:52px;height:52px;border-radius:50%;background:${iconColor}22;
                        display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                <i class="fas ${icon}" style="font-size:22px;color:${iconColor}"></i>
            </div>
            <div>
                <div style="font-size:20px;font-weight:700;">${diagLabel}</div>
                <div style="font-size:13px;color:var(--text-muted);margin-top:3px;">
                    Patient Record #${patient_id || 'N/A'}
                </div>
            </div>
        </div>

        <!-- Risk Badge -->
        <span class="risk-badge ${risk_level}">
            <i class="fas ${badgeIcon}"></i>
            ${risk_level} RISK
        </span>

        <!-- Risk Score Meter -->
        <div class="risk-meter-wrap">
            <div class="risk-meter-label">
                <span>Risk Score</span>
                <span>${riskPercent}%</span>
            </div>
            <div class="risk-meter-bar">
                <div class="risk-meter-fill ${risk_level}" id="meter-fill" style="width:0%"></div>
            </div>
        </div>

        <!-- Message -->
        <div class="result-message">
            <i class="fas fa-circle-info" style="color:var(--primary);margin-right:8px;"></i>
            ${message}
        </div>

        <!-- Meta Stats -->
        <div class="result-meta">
            <div class="meta-item">
                <div class="meta-value">${riskPercent}%</div>
                <div class="meta-label">Risk Score</div>
            </div>
            <div class="meta-item">
                <div class="meta-value">${confidence}%</div>
                <div class="meta-label">Confidence</div>
            </div>
            <div class="meta-item">
                <div class="meta-value" style="font-size:16px;">${risk_level}</div>
                <div class="meta-label">Risk Level</div>
            </div>
            <div class="meta-item">
                <div class="meta-value" style="font-size:16px;">${prediction === 1 ? 'Positive' : 'Negative'}</div>
                <div class="meta-label">Diagnosis</div>
            </div>
        </div>

        <!-- Disclaimer -->
        <p style="margin-top:24px;font-size:12px;color:var(--text-muted);
                  padding:12px;background:rgba(255,255,255,0.02);border-radius:8px;
                  border:1px solid var(--border);">
            <i class="fas fa-circle-exclamation" style="color:var(--warning);margin-right:6px;"></i>
            <strong>Medical Disclaimer:</strong> This AI prediction is for informational purposes only 
            and does not constitute medical advice. Always consult a licensed healthcare professional.
        </p>
    `;

    document.getElementById('result-content').innerHTML = html;
    setTimeout(() => {
        const fill = document.getElementById('meter-fill');
        if (fill) fill.style.width = `${riskPercent}%`;
    }, 150);
}
async function loadDashboard() {
    const container = document.getElementById('stats-container');

    try {
        const res  = await fetch(`${API_BASE}/stats`);
        const data = await res.json();

        if (!res.ok || data.status !== 'success') {
            throw new Error(data.message || 'Failed to load stats');
        }

        const s = data.stats;

        container.innerHTML = `
            <!-- Summary Stats Grid -->
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-icon">👥</div>
                    <div class="stat-value">${s.total_patients}</div>
                    <div class="stat-label">Total Patients</div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon">❤️</div>
                    <div class="stat-value">${s.heart_disease_cases}</div>
                    <div class="stat-label">Heart Disease Cases</div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon">✅</div>
                    <div class="stat-value">${s.healthy_cases}</div>
                    <div class="stat-label">Healthy Patients</div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon">📊</div>
                    <div class="stat-value">${Math.round(s.avg_risk_score * 100)}%</div>
                    <div class="stat-label">Avg Risk Score</div>
                </div>
            </div>

            <!-- Risk Distribution -->
            <div class="card">
                <div class="card-title"><i class="fas fa-chart-pie"></i> Risk Level Distribution</div>
                <div class="card-subtitle">Breakdown of all patients by risk category</div>
                ${buildRiskBar('HIGH',     s.high_risk_count,     s.total_patients, '#ef4444')}
                ${buildRiskBar('MODERATE', s.moderate_risk_count, s.total_patients, '#f59e0b')}
                ${buildRiskBar('LOW',      s.low_risk_count,      s.total_patients, '#10b981')}
            </div>
        `;
    } catch (err) {
        container.innerHTML = `
            <div class="card" style="text-align:center;padding:60px">
                <i class="fas fa-exclamation-triangle" style="font-size:36px;color:var(--danger)"></i>
                <p style="margin-top:16px;color:var(--text-muted)">${err.message}</p>
                <p style="font-size:13px;color:rgba(148,163,184,0.5);margin-top:8px">
                    Make sure the Flask backend is running on port 5000.
                </p>
            </div>`;
    }
}
function buildRiskBar(label, count, total, color) {
    const pct = total > 0 ? Math.round((count / total) * 100) : 0;
    return `
        <div style="margin-bottom:18px;">
            <div style="display:flex;justify-content:space-between;font-size:13px;margin-bottom:6px;">
                <span style="font-weight:600;color:${color}">${label}</span>
                <span style="color:var(--text-muted)">${count} patients (${pct}%)</span>
            </div>
            <div style="height:8px;background:rgba(255,255,255,0.05);border-radius:50px;overflow:hidden;">
                <div style="width:${pct}%;height:100%;background:${color};border-radius:50px;
                            transition:width 1s ease;"></div>
            </div>
        </div>
    `;
}
async function loadHistory() {
    const container = document.getElementById('history-container');

    try {
        const res  = await fetch(`${API_BASE}/patients?limit=100`);
        const data = await res.json();

        if (!res.ok || data.status !== 'success') {
            throw new Error(data.message || 'Failed to load patients');
        }

        if (data.patients.length === 0) {
            container.innerHTML = `
                <div style="text-align:center;padding:50px;color:var(--text-muted)">
                    <i class="fas fa-inbox" style="font-size:40px;opacity:0.3"></i>
                    <p style="margin-top:14px">No patient records found yet. Run a prediction first!</p>
                </div>`;
            return;
        }

        const rows = data.patients.map(p => {
            const badgeClass = p.risk_level === 'HIGH'     ? 'badge-danger'
                             : p.risk_level === 'MODERATE' ? 'badge-warning'
                             :                               'badge-success';
            const date = new Date(p.created_at).toLocaleDateString('en-IN', {
                day: '2-digit', month: 'short', year: 'numeric',
                hour: '2-digit', minute: '2-digit'
            });
            return `
                <tr>
                    <td>#${p.id}</td>
                    <td>${p.name}</td>
                    <td>${p.age}</td>
                    <td>${p.sex_label}</td>
                    <td>${Math.round(p.risk_score * 100)}%</td>
                    <td><span class="badge ${badgeClass}">${p.risk_level}</span></td>
                    <td>${p.prediction_label}</td>
                    <td style="color:var(--text-muted);font-size:12px">${date}</td>
                </tr>`;
        }).join('');

        container.innerHTML = `
            <div class="table-wrap">
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Patient</th>
                            <th>Age</th>
                            <th>Sex</th>
                            <th>Risk %</th>
                            <th>Level</th>
                            <th>Diagnosis</th>
                            <th>Date</th>
                        </tr>
                    </thead>
                    <tbody>${rows}</tbody>
                </table>
            </div>
            <p style="margin-top:16px;font-size:13px;color:var(--text-muted);text-align:right;">
                Showing ${data.patients.length} of ${data.total} records
            </p>
        `;
    } catch (err) {
        container.innerHTML = `
            <div style="text-align:center;padding:40px;color:var(--text-muted)">
                <i class="fas fa-exclamation-triangle" style="font-size:28px;color:var(--danger)"></i>
                <p style="margin-top:12px">${err.message}</p>
            </div>`;
    }
}
