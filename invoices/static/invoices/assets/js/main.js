/**
* NiceAdmin Replica JS
*/
(function() {
  "use strict";

  /**
   * Easy selector helper function
   */
  const select = (el, all = false) => {
    el = el.trim()
    if (all) {
      return [...document.querySelectorAll(el)]
    } else {
      return document.querySelector(el)
    }
  }

  /**
   * Easy event listener function
   */
  const on = (type, el, listener, all = false) => {
    if (all) {
      select(el, true).forEach(e => e.addEventListener(type, listener))
    } else {
      select(el, false).addEventListener(type, listener)
    }
  }

  /**
   * Sidebar toggle
   */
  if (select('.toggle-sidebar-btn')) {
    on('click', '.toggle-sidebar-btn', function(e) {
      select('body').classList.toggle('toggle-sidebar')
    })
  }

  /**
   * Dark mode toggle
   */
  const themeToggleBtn = document.querySelector('.theme-toggle-btn');
  if(themeToggleBtn) {
    themeToggleBtn.addEventListener('click', () => {
      const currentTheme = document.documentElement.getAttribute('data-bs-theme');
      const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-bs-theme', newTheme);
      
      // Update icon
      if(newTheme === 'dark') {
        themeToggleBtn.innerHTML = '<i class="bi bi-sun"></i>';
      } else {
        themeToggleBtn.innerHTML = '<i class="bi bi-moon-stars"></i>';
      }
      
      // Save preference
      localStorage.setItem('theme', newTheme);
    });
    
    // Load preference
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-bs-theme', savedTheme);
    if(savedTheme === 'dark') {
      themeToggleBtn.innerHTML = '<i class="bi bi-sun"></i>';
    } else {
      themeToggleBtn.innerHTML = '<i class="bi bi-moon-stars"></i>';
    }
  }

})();
