// Client-side filtering for teachers, talks, and events
(function() {
  'use strict';

  function initFilters(containerId, filtersId, noResultsId) {
    var container = document.getElementById(containerId);
    var filtersEl = document.getElementById(filtersId);
    var noResults = document.getElementById(noResultsId || 'no-results');
    if (!container || !filtersEl) return;

    var selects = filtersEl.querySelectorAll('select[data-filter]');
    if (!selects.length) return;

    var items = container.children;

    selects.forEach(function(select) {
      select.addEventListener('change', applyFilters);
    });

    function applyFilters() {
      var filters = {};
      selects.forEach(function(select) {
        var key = select.getAttribute('data-filter');
        var val = select.value;
        if (val) filters[key] = val.toLowerCase();
      });

      var visibleCount = 0;
      for (var i = 0; i < items.length; i++) {
        var item = items[i];
        var show = true;

        for (var key in filters) {
          var dataVal = (item.getAttribute('data-' + key) || '').toLowerCase();
          if (dataVal.indexOf(filters[key]) === -1) {
            show = false;
            break;
          }
        }

        item.style.display = show ? '' : 'none';
        if (show) visibleCount++;
      }

      if (noResults) {
        noResults.classList.toggle('hidden', visibleCount > 0);
      }
    }
  }

  // Initialize on DOM ready
  document.addEventListener('DOMContentLoaded', function() {
    initFilters('teacher-grid', 'teacher-filters');
    initFilters('talk-list', 'talk-filters');
    initFilters('event-list', 'event-filters');
  });
})();
