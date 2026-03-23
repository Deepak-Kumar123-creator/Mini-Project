const FORM_FIELDS = [
    {
        id: 'patient_name', label: 'Patient Name', type: 'text',
        hint: 'Optional — used for record keeping',
        placeholder: 'e.g. John Doe', full: true
    },
    {
        id: 'age', label: 'Age', type: 'number',
        hint: 'Years (1–120)', min: 1, max: 120, placeholder: 'e.g. 52'
    },
    {
        id: 'sex', label: 'Sex', type: 'select',
        hint: '0 = Female, 1 = Male',
        options: [
            { value: '1', label: '1 – Male'   },
            { value: '0', label: '0 – Female' }
        ]
    },
    {
        id: 'cp', label: 'Chest Pain Type', type: 'select',
        hint: '0–3 scale',
        options: [
            { value: '0', label: '0 – Typical Angina'    },
            { value: '1', label: '1 – Atypical Angina'   },
            { value: '2', label: '2 – Non-anginal Pain'  },
            { value: '3', label: '3 – Asymptomatic'      }
        ]
    },
    {
        id: 'trestbps', label: 'Resting BP', type: 'number',
        hint: 'mmHg (80–220)', min: 80, max: 220, placeholder: 'e.g. 130'
    },
    {
        id: 'chol', label: 'Cholesterol', type: 'number',
        hint: 'mg/dl (100–600)', min: 100, max: 600, placeholder: 'e.g. 240'
    },
    {
        id: 'fbs', label: 'Fasting Blood Sugar > 120', type: 'select',
        hint: '1 = Yes, 0 = No',
        options: [
            { value: '0', label: '0 – No'  },
            { value: '1', label: '1 – Yes' }
        ]
    },
    {
        id: 'restecg', label: 'Resting ECG', type: 'select',
        hint: '0–2 scale',
        options: [
            { value: '0', label: '0 – Normal'      },
            { value: '1', label: '1 – ST-T Anomaly' },
            { value: '2', label: '2 – LV Hypertrophy' }
        ]
    },
    {
        id: 'thalach', label: 'Max Heart Rate', type: 'number',
        hint: 'bpm (60–220)', min: 60, max: 220, placeholder: 'e.g. 150'
    },
    {
        id: 'exang', label: 'Exercise-Induced Angina', type: 'select',
        hint: '1 = Yes, 0 = No',
        options: [
            { value: '0', label: '0 – No'  },
            { value: '1', label: '1 – Yes' }
        ]
    },
    {
        id: 'oldpeak', label: 'ST Depression (Oldpeak)', type: 'number',
        hint: '0.0 – 10.0', min: 0, max: 10, step: 0.1, placeholder: 'e.g. 1.5'
    },
    {
        id: 'slope', label: 'Slope of ST Segment', type: 'select',
        hint: '0–2 scale',
        options: [
            { value: '0', label: '0 – Upsloping'   },
            { value: '1', label: '1 – Flat'         },
            { value: '2', label: '2 – Downsloping'  }
        ]
    },
    {
        id: 'ca', label: 'Major Vessels (CA)', type: 'select',
        hint: 'Fluoroscopy colored vessels (0–4)',
        options: [
            { value: '0', label: '0 Vessels' },
            { value: '1', label: '1 Vessel'  },
            { value: '2', label: '2 Vessels' },
            { value: '3', label: '3 Vessels' },
            { value: '4', label: '4 Vessels' }
        ]
    },
    {
        id: 'thal', label: 'Thalassemia (Thal)', type: 'select',
        hint: '0–3 scale',
        options: [
            { value: '0', label: '0 – Normal'           },
            { value: '1', label: '1 – Fixed Defect'     },
            { value: '2', label: '2 – Normal (Type 2)'  },
            { value: '3', label: '3 – Reversible Defect'}
        ]
    }
];
function renderForm() {
    const container = document.getElementById('patient-form-container');
    if (!container) {
        console.error('[patient_form.js] #patient-form-container not found in DOM');
        return;
    }
    const fieldsHTML = FORM_FIELDS.map(field => {
        const labelHTML = `
            <label for="${field.id}">
                ${field.label}
                ${field.hint ? `<span class="hint">(${field.hint})</span>` : ''}
            </label>`;

        let inputHTML = '';
        if (field.type === 'select') {
            const optionsHTML = field.options.map(opt =>
                `<option value="${opt.value}">${opt.label}</option>`
            ).join('');
            inputHTML = `<select id="${field.id}" name="${field.id}">${optionsHTML}</select>`;

        } else if (field.type === 'text') {
            inputHTML = `
                <input
                    type="text"
                    id="${field.id}"
                    name="${field.id}"
                    placeholder="${field.placeholder || ''}"
                />`;
        } else {
            inputHTML = `
                <input
                    type="number"
                    id="${field.id}"
                    name="${field.id}"
                    min="${field.min ?? ''}"
                    max="${field.max ?? ''}"
                    step="${field.step ?? 1}"
                    placeholder="${field.placeholder || ''}"
                />`;
        }

        const fullClass = field.full ? ' full' : '';
        return `<div class="form-group${fullClass}">${labelHTML}${inputHTML}</div>`;
    }).join('');
    container.innerHTML = `
        <form id="patient-form" novalidate>
            <div class="form-grid">
                ${fieldsHTML}
            </div>

            <!-- Submit Button -->
            <button type="submit" class="btn-predict" id="btn-predict">
                <span class="spinner"></span>
                <span class="btn-text">
                    <i class="fas fa-brain"></i>&nbsp;&nbsp;Analyze Heart Disease Risk
                </span>
            </button>
        </form>
    `;
    document.getElementById('patient-form').addEventListener('submit', handleFormSubmit);
}
function handleFormSubmit(event) {
    event.preventDefault();
    const requiredNumericFields = [
        'age', 'trestbps', 'chol', 'thalach', 'oldpeak'
    ];
    for (const fieldId of requiredNumericFields) {
        const input = document.getElementById(fieldId);
        const value = input ? input.value.trim() : '';

        if (value === '') {
            showFieldError(input, `Please enter a value for ${fieldId.toUpperCase()}`);
            input.scrollIntoView({ behavior: 'smooth', block: 'center' });
            return;
        }

        const numVal = parseFloat(value);
        const fieldDef = FORM_FIELDS.find(f => f.id === fieldId);

        if (isNaN(numVal)) {
            showFieldError(input, `${fieldId} must be a valid number`);
            return;
        }

        if (fieldDef.min !== undefined && numVal < fieldDef.min) {
            showFieldError(input, `Minimum value for ${fieldId} is ${fieldDef.min}`);
            return;
        }

        if (fieldDef.max !== undefined && numVal > fieldDef.max) {
            showFieldError(input, `Maximum value for ${fieldId} is ${fieldDef.max}`);
            return;
        }
        clearFieldError(input);
    }
    const formData = {};

    FORM_FIELDS.forEach(field => {
        const element = document.getElementById(field.id);
        if (!element) return;

        const raw = element.value.trim();

        if (field.id === 'patient_name') {
            formData[field.id] = raw || 'Anonymous';
        } else if (field.type === 'number') {
            formData[field.id] = parseFloat(raw);
        } else if (field.type === 'select') {
            formData[field.id] = parseInt(raw, 10);
        }
    });
    submitPrediction(formData);
}
function showFieldError(input, message) {
    if (!input) return;
    input.style.borderColor = '#ef4444';
    input.style.boxShadow   = '0 0 0 3px rgba(239,68,68,0.2)';
    const errorMsg  = document.getElementById('error-msg');
    const errorText = document.getElementById('error-text');
    if (errorMsg && errorText) {
        errorText.textContent   = message;
        errorMsg.style.display  = 'flex';
        errorMsg.style.gap      = '10px';
        errorMsg.style.alignItems = 'center';
    }
}

function clearFieldError(input) {
    if (!input) return;
    input.style.borderColor = '';
    input.style.boxShadow   = '';
}
document.addEventListener('DOMContentLoaded', renderForm);
