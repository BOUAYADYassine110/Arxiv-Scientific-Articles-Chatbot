import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Search, Home, Info } from 'lucide-react';
import SettingsDropdown from './SettingsDropdown';

interface NavbarProps {
  currentPage: 'welcome' | 'search' | 'about';
  onNavigate: (page: 'welcome' | 'search' | 'about') => void;
}

const Navbar: React.FC<NavbarProps> = ({ currentPage, onNavigate }) => {
  const [darkMode, setDarkMode] = useState(true);

  const handleToggleDarkMode = () => {
    const newMode = !darkMode;
    setDarkMode(newMode);
    
    // Apply theme with smooth transition
    document.documentElement.style.transition = 'all 0.3s ease';
    
    if (newMode) {
      document.documentElement.classList.remove('light-mode');
      localStorage.setItem('theme', 'dark');
    } else {
      document.documentElement.classList.add('light-mode');
      localStorage.setItem('theme', 'light');
    }
    
    // Remove transition after animation
    setTimeout(() => {
      document.documentElement.style.transition = '';
    }, 300);
  };

  // Initialize theme from localStorage
  React.useEffect(() => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'light') {
      setDarkMode(false);
      document.documentElement.classList.add('light-mode');
    } else {
      setDarkMode(true);
      document.documentElement.classList.remove('light-mode');
    }
  }, []);

  return (
    <motion.nav 
      className="navbar"
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="nav-container">
        <div className="nav-logo">
          ArXiv Research Hub
        </div>
        
        <ul className="nav-links">
          <li>
            <button
              onClick={() => onNavigate('welcome')}
              className={`nav-link ${currentPage === 'welcome' ? 'active' : ''}`}
            >
              <Home className="w-4 h-4" />
              <span>Home</span>
            </button>
          </li>
          <li>
            <button
              onClick={() => onNavigate('search')}
              className={`nav-link ${currentPage === 'search' ? 'active' : ''}`}
            >
              <Search className="w-4 h-4" />
              <span>Search</span>
            </button>
          </li>
          <li>
            <button
              onClick={() => onNavigate('about')}
              className={`nav-link ${currentPage === 'about' ? 'active' : ''}`}
            >
              <Info className="w-4 h-4" />
              <span>About</span>
            </button>
          </li>
        </ul>
        
        <div className="flex items-center gap-4">
          <SettingsDropdown 
            darkMode={darkMode} 
            onToggleDarkMode={handleToggleDarkMode} 
          />
        </div>
      </div>
    </motion.nav>
  );
};

export default Navbar;