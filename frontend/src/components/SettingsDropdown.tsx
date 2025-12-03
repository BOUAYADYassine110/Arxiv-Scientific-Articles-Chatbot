import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Settings, Moon, Sun, Search, Layout, Download, Palette, Zap } from 'lucide-react';

interface SettingsDropdownProps {
  darkMode: boolean;
  onToggleDarkMode: () => void;
}

const SettingsDropdown: React.FC<SettingsDropdownProps> = ({ darkMode, onToggleDarkMode }) => {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const settingsItems = [
    {
      icon: darkMode ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />,
      label: 'Theme',
      description: darkMode ? 'Switch to light mode' : 'Switch to dark mode',
      action: onToggleDarkMode,
      color: 'from-amber-500 to-orange-500',
      special: true
    },
    {
      icon: <Search className="w-5 h-5" />,
      label: 'Search',
      description: 'Configure search preferences',
      action: () => alert('Search preferences coming soon!'),
      color: 'from-blue-500 to-cyan-500',
      special: false
    },
    {
      icon: <Layout className="w-5 h-5" />,
      label: 'Display',
      description: 'Customize layout and view',
      action: () => alert('Display settings coming soon!'),
      color: 'from-purple-500 to-pink-500',
      special: false
    },
    {
      icon: <Download className="w-5 h-5" />,
      label: 'Export',
      description: 'Download search results',
      action: () => {
        try {
          const rawData = localStorage.getItem('searchResults');
          if (!rawData) {
            alert('No search results to export. Please perform a search first.');
            return;
          }
          const results = JSON.parse(rawData);
          if (!Array.isArray(results) || results.length === 0) {
            alert('No search results to export. Please perform a search first.');
            return;
          }
          const dataStr = JSON.stringify(results, null, 2);
          const dataBlob = new Blob([dataStr], { type: 'application/json' });
          const url = URL.createObjectURL(dataBlob);
          const link = document.createElement('a');
          link.href = url;
          link.download = `arxiv-search-results-${new Date().toISOString().split('T')[0]}.json`;
          link.click();
          URL.revokeObjectURL(url);
        } catch (error) {
          alert('Error exporting data. Please try again.');
        }
      },
      color: 'from-green-500 to-emerald-500',
      special: false
    }
  ];

  return (
    <div className="relative" ref={dropdownRef}>
      {/* Settings Button */}
      <motion.button
        onClick={() => setIsOpen(!isOpen)}
        className="btn btn-secondary !p-2 rounded-xl transition-all duration-200 group"
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        aria-label="Settings"
      >
        <motion.div
          animate={{ rotate: isOpen ? 90 : 0 }}
          transition={{ duration: 0.2, ease: "easeInOut" }}
        >
          <Settings className="w-5 h-5 text-muted group-hover:text-primary transition-colors" />
        </motion.div>
        
        {/* Active indicator */}
        <motion.div
          className="absolute -top-1 -right-1 w-3 h-3 bg-primary rounded-full"
          initial={{ scale: 0 }}
          animate={{ scale: isOpen ? 1 : 0 }}
          transition={{ duration: 0.2 }}
        />
      </motion.button>

      {/* Dropdown Panel */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: 10 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 10 }}
            transition={{ 
              type: "spring", 
              stiffness: 400, 
              damping: 25,
              mass: 0.5
            }}
            className="absolute right-0 top-full mt-2 w-80 card shadow-2xl z-50 overflow-hidden"
          >
            {/* Header */}
            <div className="p-6 pb-4">
              <div className="flex items-center gap-3 mb-2">
                <div className="p-2 bg-gradient-to-r from-primary to-secondary rounded-lg">
                  <Palette className="w-4 h-4 text-white" />
                </div>
                <div>
                  <h3 className="font-semibold text-lg text-primary">Settings</h3>
                  <p className="text-xs text-secondary">Customize your experience</p>
                </div>
              </div>
            </div>

            {/* Settings Grid */}
            <div className="px-6 pb-6">
              <div className="space-y-2">
                {settingsItems.map((item, index) => (
                  <motion.button
                    key={index}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ 
                      delay: index * 0.1,
                      type: "spring",
                      stiffness: 300,
                      damping: 20
                    }}
                    onClick={() => {
                      item.action();
                      if (!item.special) {
                        setIsOpen(false);
                      }
                    }}
                    className="btn btn-secondary relative !p-3 rounded-lg transition-all duration-200 text-left group overflow-hidden !h-auto !min-h-0 !flex !flex-row !items-center !justify-start w-full"
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                  >
                    {/* Background gradient on hover */}
                    <motion.div
                      className={`absolute inset-0 bg-gradient-to-br ${item.color} opacity-0 group-hover:opacity-10 transition-opacity duration-200`}
                      initial={{ scale: 0.8 }}
                      whileHover={{ scale: 1 }}
                    />
                    
                    <div className="relative z-10">
                      {/* Icon */}
                      <motion.div 
                        className={`inline-flex p-2 rounded-lg bg-gradient-to-br ${item.color} mr-3 flex-shrink-0`}
                        whileHover={{ scale: 1.1 }}
                        transition={{ type: "spring", stiffness: 400, damping: 25 }}
                      >
                        <div className="text-white">
                          {item.icon}
                        </div>
                      </motion.div>
                      
                      {/* Content */}
                      <div className="flex-1 min-w-0">
                        <h4 className="font-medium text-sm text-primary mb-1">{item.label}</h4>
                        <p className="text-xs text-secondary leading-tight truncate">{item.description}</p>
                      </div>
                    </div>

                    {/* Hover effect */}
                    <motion.div
                      className="absolute top-2 right-2 w-2 h-2 bg-primary rounded-full opacity-0 group-hover:opacity-100"
                      initial={{ scale: 0 }}
                      whileHover={{ scale: 1 }}
                      transition={{ delay: 0.1 }}
                    />
                  </motion.button>
                ))}
              </div>
            </div>

            {/* Footer */}
            <motion.div 
              className="px-6 py-4 bg-surface-light border-t"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.6 }}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <motion.div
                    className="w-2 h-2 bg-green-500 rounded-full"
                    animate={{ scale: [1, 1.2, 1] }}
                    transition={{ duration: 2, repeat: Infinity }}
                  />
                  <span className="text-xs text-secondary">System Online</span>
                </div>
                <div className="flex items-center gap-2">
                  <Zap className="w-3 h-3 text-primary" />
                  <span className="text-xs text-muted">v1.0.0</span>
                </div>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default SettingsDropdown;