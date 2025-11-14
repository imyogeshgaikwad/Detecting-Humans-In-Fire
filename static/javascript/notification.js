export function showNotification(res) {
  // Remove any existing notification
  const existing = document.getElementById('detection-notification');
  if (existing) existing.remove();

  // Create notification container
  const notification = document.createElement('div');
  notification.id = 'detection-notification';
  notification.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 0;
    border-radius: 16px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.3);
    z-index: 10000;
    min-width: 320px;
    max-width: 400px;
    animation: slideIn 0.4s ease-out;
    overflow: hidden;
  `;

  // Determine alert level
  const fireDetected = res.fire_detected;
  const humanDetected = res.human_detected;
  const criticalAlert = fireDetected && humanDetected;
  
  let alertColor = '#667eea';
  let alertIcon = '🔍';
  let alertTitle = 'Detection Results';
  
  if (criticalAlert) {
    alertColor = '#ef4444';
    alertIcon = '🚨';
    alertTitle = 'CRITICAL ALERT';
  } else if (fireDetected) {
    alertColor = '#f97316';
    alertIcon = '🔥';
    alertTitle = 'Fire Detected';
  } else if (humanDetected) {
    alertColor = '#3b82f6';
    alertIcon = '👤';
    alertTitle = 'Human Detected';
  }

  notification.innerHTML = `
    <div style="background: ${alertColor}; padding: 16px; display: flex; align-items: center; justify-content: space-between;">
      <div style="display: flex; align-items: center; gap: 12px;">
        <span style="font-size: 28px;">${alertIcon}</span>
        <span style="font-size: 18px; font-weight: bold;">${alertTitle}</span>
      </div>
      <button onclick="this.closest('#detection-notification').remove()" style="background: rgba(255,255,255,0.2); border: none; color: white; width: 28px; height: 28px; border-radius: 50%; cursor: pointer; font-size: 18px; display: flex; align-items: center; justify-content: center; transition: background 0.2s;">
        ×
      </button>
    </div>
    
    <div style="padding: 20px; background: white; color: #1f2937;">
      <!-- Fire Detection -->
      <div style="margin-bottom: 16px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
          <span style="font-weight: 600; display: flex; align-items: center; gap: 8px;">
            🔥 Fire
          </span>
          <span style="font-size: 20px; font-weight: bold; color: ${fireDetected ? '#ef4444' : '#6b7280'};">
            ${res.fire_confidence}%
          </span>
        </div>
        <div style="background: #e5e7eb; height: 8px; border-radius: 4px; overflow: hidden;">
          <div style="background: ${fireDetected ? '#ef4444' : '#9ca3af'}; height: 100%; width: ${res.fire_confidence}%; transition: width 0.5s ease-out;"></div>
        </div>
        <div style="margin-top: 4px; font-size: 12px; color: #6b7280;">
          ${fireDetected ? '⚠️ Fire present' : '✓ No fire detected'}
        </div>
      </div>

      <!-- Human Detection -->
      <div>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
          <span style="font-weight: 600; display: flex; align-items: center; gap: 8px;">
            👤 Human
          </span>
          <span style="font-size: 20px; font-weight: bold; color: ${humanDetected ? '#3b82f6' : '#6b7280'};">
            ${res.human_confidence}%
          </span>
        </div>
        <div style="background: #e5e7eb; height: 8px; border-radius: 4px; overflow: hidden;">
          <div style="background: ${humanDetected ? '#3b82f6' : '#9ca3af'}; height: 100%; width: ${res.human_confidence}%; transition: width 0.5s ease-out;"></div>
        </div>
        <div style="margin-top: 4px; font-size: 12px; color: #6b7280;">
          ${humanDetected ? '⚠️ Human present' : '✓ No human detected'}
        </div>
      </div>

      ${criticalAlert ? `
        <div style="margin-top: 16px; padding: 12px; background: #fee2e2; border-left: 4px solid #ef4444; border-radius: 4px;">
          <div style="font-weight: bold; color: #991b1b; margin-bottom: 4px;">⚠️ Emergency Situation</div>
          <div style="font-size: 13px; color: #7f1d1d;">Fire detected with human presence. Immediate action required!</div>
        </div>
      ` : ''}
    </div>
  `;

  // Add animation styles
  const style = document.createElement('style');
  style.textContent = `
    @keyframes slideIn {
      from {
        transform: translateX(400px);
        opacity: 0;
      }
      to {
        transform: translateX(0);
        opacity: 1;
      }
    }
    #detection-notification button:hover {
      background: rgba(255,255,255,0.3) !important;
    }
  `;
  document.head.appendChild(style);

  document.body.appendChild(notification);

  // Auto-remove after 8 seconds (or 12 for critical alerts)
  setTimeout(() => {
    if (notification.parentNode) {
      notification.style.animation = 'slideIn 0.3s ease-out reverse';
      setTimeout(() => notification.remove(), 300);
    }
  }, criticalAlert ? 12000 : 8000);
}