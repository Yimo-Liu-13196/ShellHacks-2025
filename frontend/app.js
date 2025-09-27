(function () {
  const DEFAULT_BASE_URL = typeof document !== 'undefined' && document.body?.dataset?.apiBase
    ? document.body.dataset.apiBase
    : 'http://localhost:8000';
  const apiBaseUrl =
    window.API_BASE_URL ||
    (typeof import !== 'undefined' && typeof import.meta !== 'undefined' && import.meta.env
      ? import.meta.env.VITE_API_BASE_URL
      : undefined) ||
    DEFAULT_BASE_URL;

  const hydrateResult = (element, payload) => {
    element.textContent = JSON.stringify(payload, null, 2);
  };

  const reportError = (element, error) => {
    const message = error?.detail || error?.message || error || 'Unknown error';
    element.textContent = `Error: ${message}`;
  };

  const postJSON = async (path, body) => {
    const response = await fetch(`${apiBaseUrl}${path}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    if (!response.ok) {
      const errPayload = await response.json().catch(() => ({}));
      const message = errPayload.detail || response.statusText;
      throw new Error(message);
    }
    return response.json();
  };

  document.querySelector('#appointment-form')?.addEventListener('submit', async (event) => {
    event.preventDefault();
    const form = event.currentTarget;
    const resultEl = document.querySelector('#appointment-result');
    resultEl.textContent = 'Scheduling…';

    const payload = {
      doctor_type: form.doctor_type.value,
      preferred_days: form.preferred_days.value.split(',').map((s) => s.trim()).filter(Boolean),
      patient_name: form.patient_name.value,
      patient_email: form.patient_email.value,
    };

    try {
      const data = await postJSON('/api/appointment/schedule', payload);
      hydrateResult(resultEl, data);
    } catch (error) {
      reportError(resultEl, error);
    }
  });

  document.querySelector('#insurance-form')?.addEventListener('submit', async (event) => {
    event.preventDefault();
    const form = event.currentTarget;
    const resultEl = document.querySelector('#insurance-result');
    resultEl.textContent = 'Looking up plan…';

    try {
      const data = await postJSON('/api/insurance/check', { query: form.query.value });
      hydrateResult(resultEl, data);
    } catch (error) {
      reportError(resultEl, error);
    }
  });

  document.querySelector('#records-form')?.addEventListener('submit', async (event) => {
    event.preventDefault();
    const form = event.currentTarget;
    const resultEl = document.querySelector('#records-result');
    resultEl.textContent = 'Fetching record…';

    try {
      const data = await postJSON('/api/records/access', { query: form.query.value });
      hydrateResult(resultEl, data);
    } catch (error) {
      reportError(resultEl, error);
    }
  });

  document.querySelector('#knowledge-form')?.addEventListener('submit', async (event) => {
    event.preventDefault();
    const form = event.currentTarget;
    const resultEl = document.querySelector('#knowledge-result');
    resultEl.textContent = 'Consulting HealthcareLoop…';

    const payload = {
      question: form.question.value,
      context: form.context.value || undefined,
    };

    try {
      const data = await postJSON('/api/knowledge', payload);
      hydrateResult(resultEl, data);
    } catch (error) {
      reportError(resultEl, error);
    }
  });
})();
