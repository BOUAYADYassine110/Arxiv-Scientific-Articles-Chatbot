import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Navbar from './components/Navbar';
import WelcomePage from './components/WelcomePage';
import SearchInterface from './components/SearchInterface';
import AboutPage from './components/AboutPage';

function App() {
  const [currentPage, setCurrentPage] = useState<'welcome' | 'search' | 'about'>('welcome');

  const handleNavigate = (page: 'welcome' | 'search' | 'about') => {
    setCurrentPage(page);
  };

  return (
    <div className="App min-h-screen">
      <Navbar currentPage={currentPage} onNavigate={handleNavigate} />
      
      <AnimatePresence mode="wait">
        {currentPage === 'welcome' && (
          <motion.div
            key="welcome"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            transition={{ duration: 0.3 }}
          >
            <WelcomePage onGetStarted={() => setCurrentPage('search')} />
          </motion.div>
        )}
        {currentPage === 'search' && (
          <motion.div
            key="search"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 20 }}
            transition={{ duration: 0.3 }}
          >
            <SearchInterface />
          </motion.div>
        )}
        {currentPage === 'about' && (
          <motion.div
            key="about"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
          >
            <AboutPage />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

export default App;