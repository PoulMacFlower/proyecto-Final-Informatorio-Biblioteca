document.addEventListener("DOMContentLoaded", function() {
    let successAlert = document.querySelector('.alert-success');

    if (successAlert) {
      setTimeout(function() {
        successAlert.style.display = 'none';
      }, 1500);
    }
  });
  