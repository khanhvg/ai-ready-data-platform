import React, { useState } from 'react';
import { createRoot } from 'react-dom/client';
import { lessonContract } from './lesson-contract.mjs';
import './styles.css';

function Probe() {
  const [status, setStatus] = useState(lessonContract.status.baseline);

  return (
    <div className="probe-controls">
      <div className="controls" aria-label="Điều khiển khảo sát">
        <button
          type="button"
          data-testid="run-bounded-probe"
          onClick={() => setStatus(lessonContract.status.failure)}
        >
          Chạy khảo sát có giới hạn
        </button>
        <button
          type="button"
          data-testid="reset-lesson"
          onClick={() => setStatus(lessonContract.status.reset)}
        >
          Đặt lại bài học
        </button>
      </div>
      <p
        data-testid="lesson-status"
        role="status"
        aria-live="polite"
        aria-atomic="true"
        lang="en"
      >
        {status}
      </p>
    </div>
  );
}

const root = document.getElementById('probe');
if (root) createRoot(root).render(<Probe />);
