/**
 * RepoBase Frontend Application Logic
 * Handles Command Palette, Toasts, Sidebar, and Global Interactions
 */

document.addEventListener('DOMContentLoaded', () => {
    initToasts();
    initSidebar();
    initCommandPalette();
    initGlobalShortcuts();
});

// --- Security Utilities ---
window.escapeHTML = (str) => {
    if (!str) return '';
    return str.replace(/[&<>'"]/g, 
        tag => ({
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            "'": '&#39;',
            '"': '&quot;'
        }[tag] || tag)
    );
};

// --- Toast System ---
function initToasts() {
    // Expose globally
    window.showToast = (message, type = 'info', description = '') => {
        const container = document.getElementById('toast-container');
        if (!container) return;

        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        
        let iconSvg = '';
        if (type === 'success') {
            iconSvg = '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline>';
        } else if (type === 'error' || type === 'danger') {
            iconSvg = '<circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line>';
        } else if (type === 'warning') {
            iconSvg = '<path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line>';
        } else {
            iconSvg = '<circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line>';
        }

        toast.innerHTML = `
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                ${iconSvg}
            </svg>
            <div style="display:flex; flex-direction:column;">
                <strong style="font-weight:600;">${message}</strong>
                ${description ? `<span style="font-size:0.85rem; color:var(--text-secondary);">${description}</span>` : ''}
            </div>
        `;
        
        container.appendChild(toast);
        
        setTimeout(() => {
            toast.style.animation = 'fadeOutRight 0.3s forwards';
            setTimeout(() => toast.remove(), 300);
        }, 4000);
    };
}

// --- Sidebar Toggle ---
function initSidebar() {
    window.toggleSidebar = () => {
        const sidebar = document.getElementById('sidebar');
        if (sidebar) {
            sidebar.classList.toggle('collapsed');
        }
    };
}

// --- Global Shortcuts ---
function initGlobalShortcuts() {
    document.addEventListener('keydown', (e) => {
        // Ignore if typing in an input or textarea
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
            // Esc escapes inputs
            if (e.key === 'Escape') {
                e.target.blur();
                closeAllModals();
            }
            return;
        }

        if (e.key === 'k' && (e.metaKey || e.ctrlKey)) {
            e.preventDefault();
            toggleCommandPalette();
        } else if (e.key === 'n' || e.key === 'N') {
            e.preventDefault();
            const btn = document.getElementById('btn-create-repo-global');
            if (btn) btn.click();
        } else if (e.key === '/') {
            e.preventDefault();
            toggleCommandPalette();
        } else if (e.key === 'Escape') {
            closeAllModals();
        }
    });
}

function closeAllModals() {
    document.querySelectorAll('.modal-overlay.active').forEach(m => m.classList.remove('active'));
}

// --- Command Palette ---
function toggleCommandPalette() {
    const palette = document.getElementById('command-palette');
    const input = document.getElementById('cmd-input');
    if (!palette) return;

    if (palette.classList.contains('active')) {
        palette.classList.remove('active');
        input.blur();
    } else {
        palette.classList.add('active');
        input.value = '';
        input.focus();
        renderCmdResults('');
    }
}

function initCommandPalette() {
    const palette = document.getElementById('command-palette');
    const input = document.getElementById('cmd-input');
    const resultsContainer = document.getElementById('cmd-results');
    if (!palette || !input || !resultsContainer) return;

    // Close on click outside
    palette.addEventListener('click', (e) => {
        if (e.target === palette) toggleCommandPalette();
    });

    const staticCommands = [
        { title: 'Create Repository', icon: 'plus', action: () => { toggleCommandPalette(); document.getElementById('btn-create-repo-global')?.click(); } },
        { title: 'Go to Dashboard', icon: 'home', action: () => { window.location.href = '/'; } },
        { title: 'Toggle Sidebar', icon: 'sidebar', action: () => { toggleCommandPalette(); toggleSidebar(); } },
    ];

    let currentItems = [];
    let selectedIndex = 0;

    // Fetch repos for search
    let reposCache = [];
    fetch('/api/repos')
        .then(res => res.json())
        .then(data => { reposCache = data; })
        .catch(() => {});

    window.renderCmdResults = (query) => {
        const q = query.toLowerCase();
        let items = [];

        // Add static commands
        staticCommands.forEach(cmd => {
            if (cmd.title.toLowerCase().includes(q)) {
                items.push(cmd);
            }
        });

        // Add repos
        reposCache.forEach(repo => {
            if (repo.name.toLowerCase().includes(q) || (repo.description && repo.description.toLowerCase().includes(q))) {
                items.push({
                    title: `Go to ${repo.name}`,
                    subtitle: 'Repository',
                    icon: 'database',
                    action: () => { window.location.href = `/repo/${repo.id}/`; }
                });
            }
        });

        currentItems = items;
        selectedIndex = 0;

        if (items.length === 0) {
            resultsContainer.innerHTML = `<div style="padding: 1rem; color: var(--text-muted); text-align: center;">No results found.</div>`;
            return;
        }

        resultsContainer.innerHTML = items.map((item, idx) => `
            <div class="cmd-item ${idx === 0 ? 'active' : ''}" data-idx="${idx}">
                <div class="cmd-item-icon">${getIcon(item.icon)}</div>
                <div style="display:flex; flex-direction:column;">
                    <span style="font-weight:500;">${window.escapeHTML(item.title)}</span>
                    ${item.subtitle ? `<span style="font-size:0.75rem; opacity:0.7;">${window.escapeHTML(item.subtitle)}</span>` : ''}
                </div>
            </div>
        `).join('');

        // Attach clicks
        resultsContainer.querySelectorAll('.cmd-item').forEach(el => {
            el.addEventListener('click', () => {
                const idx = parseInt(el.getAttribute('data-idx'));
                currentItems[idx].action();
            });
            el.addEventListener('mousemove', () => {
                updateSelection(parseInt(el.getAttribute('data-idx')));
            });
        });
    };

    function updateSelection(index) {
        if (index < 0) index = 0;
        if (index >= currentItems.length) index = currentItems.length - 1;
        selectedIndex = index;
        
        const elements = resultsContainer.querySelectorAll('.cmd-item');
        elements.forEach((el, idx) => {
            if (idx === selectedIndex) {
                el.classList.add('active');
                el.scrollIntoView({ block: 'nearest' });
            } else {
                el.classList.remove('active');
            }
        });
    }

    input.addEventListener('input', (e) => {
        renderCmdResults(e.target.value);
    });

    input.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowDown') {
            e.preventDefault();
            updateSelection(selectedIndex + 1);
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            updateSelection(selectedIndex - 1);
        } else if (e.key === 'Enter') {
            e.preventDefault();
            if (currentItems[selectedIndex]) {
                currentItems[selectedIndex].action();
            }
        }
    });
}

function getIcon(name) {
    if (name === 'plus') return '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>';
    if (name === 'home') return '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>';
    if (name === 'sidebar') return '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><line x1="9" y1="3" x2="9" y2="21"></line></svg>';
    if (name === 'database') return '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3"></ellipse><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"></path><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"></path></svg>';
    return '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle></svg>';
}

// Utility: Hash string to color
window.getRepoIdentity = (name) => {
    let hash = 0;
    for (let i = 0; i < name.length; i++) {
        hash = name.charCodeAt(i) + ((hash << 5) - hash);
    }
    const h = hash % 360;
    return `hsl(${h}, 70%, 60%)`;
};
