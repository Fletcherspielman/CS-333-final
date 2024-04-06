function toggleHighContrast() {
    const body = document.body;
    body.classList.toggle('high-contrast');
    // Optionally, store the preference in localStorage for persistence
    localStorage.setItem('highContrastMode', body.classList.contains('high-contrast'));
  }