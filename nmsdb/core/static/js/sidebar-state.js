/**
 * Sidebar state persistence
 */
document.addEventListener('DOMContentLoaded', function() {
    // Store current sidebar expanded state
    const sidenavAccordion = document.getElementById('sidenavAccordion');
    
    if (sidenavAccordion) {
        // Save expanded state when clicking on nav items
        const navLinks = sidenavAccordion.querySelectorAll('.nav-link[data-bs-toggle="collapse"]');
        
        navLinks.forEach(navLink => {
            navLink.addEventListener('click', function(event) {
                // Only handle parent menu clicks, not child item clicks
                if (this.getAttribute('data-bs-toggle') === 'collapse') {
                    const targetId = this.getAttribute('data-bs-target').replace('#', '');
                    
                    // Wait for Bootstrap collapse to complete
                    setTimeout(() => {
                        const isExpanded = !this.classList.contains('collapsed');
                        localStorage.setItem(`nmsdb-nav-${targetId}`, isExpanded ? 'expanded' : 'collapsed');
                    }, 350);
                }
            });
            
            // Check if we're on the home/landing page
            const isHomePage = window.location.pathname === '/' || 
                              window.location.pathname.endsWith('/index.html') ||
                              window.location.pathname.endsWith('/landing_page.html');
            
            // Only restore saved states if not on the home page
            if (!isHomePage) {
                // Restore state from localStorage on page load
                const targetId = navLink.getAttribute('data-bs-target').replace('#', '');
                const savedState = localStorage.getItem(`nmsdb-nav-${targetId}`);
                
                // Only apply the saved state if the menu isn't already active due to the current page
                const relatedCollapse = document.getElementById(targetId);
                if (relatedCollapse && savedState === 'expanded' && !relatedCollapse.classList.contains('show')) {
                    // Programmatically trigger click (let Bootstrap handle the toggle)
                    navLink.click();
                }
            }
        });
        
        // Prevent child links from triggering parent collapse
        const childLinks = sidenavAccordion.querySelectorAll('.sb-sidenav-menu-nested .nav-link');
        childLinks.forEach(childLink => {
            childLink.addEventListener('click', function(event) {
                // Stop the event from bubbling up to parent elements
                event.stopPropagation();
            });
        });
    }
});