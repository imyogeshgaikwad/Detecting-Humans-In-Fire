// Detection thresholds (easy to configure)
const FIRE_THRESHOLD = 90;
const HUMAN_THRESHOLD = 70;

export function showNotification(res) {
  // Apply thresholds
  const fireDetected = res.fire_confidence >= FIRE_THRESHOLD;
  const humanDetected = res.human_confidence >= HUMAN_THRESHOLD;
  
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
    <div style="background: ${alertColor}; padding: 16px; display: flex; justify-content: space-between; align-items: center;">
      <div style="display: flex; align-items: center; gap: 12px;">
        <span style="font-size: 24px;">${alertIcon}</span>
        <span style="font-weight: bold; font-size: 18px;">${alertTitle}</span>
      </div>
      <button onclick="this.closest('#detection-notification').remove()" 
              style="background: rgba(255,255,255,0.2); border: none; color: white; width: 28px; height: 28px; border-radius: 50%; cursor: pointer; font-size: 18px; display: flex; align-items: center; justify-content: center; padding: 0;">
        ×
      </button>
    </div>
    
    <div style="padding: 20px;">
      <div style="margin-bottom: 16px;">
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
          <span style="font-size: 20px;">🔥</span>
          <span style="font-weight: 600;">Fire</span>
        </div>
        <div style="font-size: 14px; opacity: 0.9;">
          ${fireDetected ? '⚠️ Fire present' : '✓ No fire detected'}
        </div>
      </div>

      <div style="margin-bottom: ${criticalAlert ? '16px' : '0'};">
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
          <span style="font-size: 20px;">👤</span>
          <span style="font-weight: 600;">Human</span>
        </div>
        <div style="font-size: 14px; opacity: 0.9;">
          ${humanDetected ? '⚠️ Human present' : '✓ No human detected'}
        </div>
      </div>

      ${criticalAlert ? `
        <div style="background: rgba(255,255,255,0.15); padding: 12px; border-radius: 8px; margin-top: 16px;">
          <div style="font-weight: bold; margin-bottom: 4px;">⚠️ Emergency Situation</div>
          <div style="font-size: 13px; opacity: 0.95;">Fire detected with human presence. Immediate action required!</div>
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