// GreenCampus - Main Interaction Scripts

document.addEventListener('DOMContentLoaded', () => {
  // 1. Image upload preview
  const photoInput = document.getElementById('waste-photo-input') || document.querySelector('input[type="file"]');
  const previewContainer = document.getElementById('image-preview-container');
  const previewImg = document.getElementById('image-preview');

  if (photoInput && previewContainer && previewImg) {
    photoInput.addEventListener('change', function() {
      const file = this.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
          previewImg.src = e.target.result;
          previewContainer.style.display = 'block';
        };
        reader.readAsDataURL(file);
      } else {
        previewContainer.style.display = 'none';
      }
    });
  }

  // 2. Auto-dismiss flash messages after 6 seconds
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(alert => {
    setTimeout(() => {
      alert.style.opacity = '0';
      alert.style.transform = 'translateY(-10px)';
      alert.style.transition = 'all 0.5s ease';
      setTimeout(() => alert.remove(), 500);
    }, 6000);
  });

  // 3. Copy redemption code button
  const copyButtons = document.querySelectorAll('.btn-copy-code');
  copyButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const code = btn.getAttribute('data-code');
      navigator.clipboard.writeText(code).then(() => {
        const originalText = btn.innerHTML;
        btn.innerHTML = '<i class="fa-solid fa-check"></i> Copied!';
        btn.classList.add('btn-primary');
        setTimeout(() => {
          btn.innerHTML = originalText;
          btn.classList.remove('btn-primary');
        }, 2500);
      });
    });
  });
});
