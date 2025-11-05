document.addEventListener("DOMContentLoaded", () => {
  // Auto-dismiss alerts after 5 seconds
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(alert => {
    setTimeout(() => {
      // Check if the alert still exists and hasn't been manually dismissed
      if (alert && alert.parentNode) {
        // Use Bootstrap's alert hide method
        const bsAlert = new bootstrap.Alert(alert);
        bsAlert.close();
      }
    }, 5000); // 5 seconds
  });
});