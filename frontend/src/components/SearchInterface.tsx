import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Search, Brain, Filter, Loader, Sparkles, ChevronDown } from 'lucide-react';
import { searchArticles, getYears } from '../services/api';
import { SearchRequest, Article } from '../types';
import ArticleCard from './ArticleCard';

const SearchInterface: React.FC = () => {
  const [query, setQuery] = useState('');
  const [filters, setFilters] = useState({
    year_filter: '',
    category_filter: '',
    author_filter: '',
    title_filter: '',
    abstract_filter: ''
  });
  const [results, setResults] = useState<Article[]>([]);
  const [loading, setLoading] = useState(false);
  const [searchType, setSearchType] = useState<'manual' | 'ai'>('ai');
  const [explanation, setExplanation] = useState('');
  const [years, setYears] = useState<string[]>([]);
  const [showFilters, setShowFilters] = useState(false);

  useEffect(() => {
    const fetchYears = async () => {
      try {
        const yearsList = await getYears();
        setYears(yearsList);
      } catch (error) {
        console.error('Failed to fetch years:', error);
      }
    };
    fetchYears();
  }, []);

  const handleSearch = async () => {
    if (!query.trim()) return;

    setLoading(true);
    try {
      const request: SearchRequest = {
        query,
        search_type: searchType,
        ...filters
      };

      const response = await searchArticles(request);
      setResults(response.articles);
      setExplanation(response.explanation || '');
      
      // Save results to localStorage for export functionality
      localStorage.setItem('searchResults', JSON.stringify(response.articles));
    } catch (error) {
      console.error('Search failed:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  return (
    <div className="min-h-screen py-8">
      <div className="container">
        {/* Search Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h1 className="text-4xl font-bold mb-4">
            Search Research Papers
          </h1>
          <p className="text-xl text-secondary">
            Use AI-powered search to find the most relevant research papers
          </p>
        </motion.div>

        {/* Search Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="card mb-8 max-w-4xl mx-auto"
        >
          <div className="space-y-6">
            {/* Search Input */}
            <div className="relative">
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Enter your research question or keywords..."
                className="input text-lg py-4 pr-12"
              />
              <Search className="absolute right-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-muted" />
            </div>

            {/* Search Options */}
            <div className="flex flex-col sm:flex-row gap-4 items-stretch sm:items-center sm:justify-between">
              <div className="flex gap-2 flex-wrap">
                <button
                  onClick={() => setSearchType('ai')}
                  className={`btn ${searchType === 'ai' ? 'btn-primary' : 'btn-secondary'}`}
                >
                  <Brain className="w-4 h-4" />
                  AI Search
                </button>
                <button
                  onClick={() => setSearchType('manual')}
                  className={`btn ${searchType === 'manual' ? 'btn-primary' : 'btn-secondary'}`}
                >
                  <Search className="w-4 h-4" />
                  Manual Search
                </button>
              </div>

              <div className="flex gap-2 flex-wrap">
                <button
                  onClick={() => setShowFilters(!showFilters)}
                  className="btn btn-secondary flex-1 sm:flex-initial"
                >
                  <Filter className="w-4 h-4" />
                  Filters
                  <ChevronDown className={`w-4 h-4 transition-transform ${showFilters ? 'rotate-180' : ''}`} />
                </button>

                <button
                  onClick={handleSearch}
                  disabled={loading || !query.trim()}
                  className="btn btn-primary flex-1 sm:flex-initial"
                >
                  {loading ? (
                    <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  ) : (
                    <Search className="w-4 h-4" />
                  )}
                  Search
                </button>
              </div>
            </div>

            {/* Advanced Filters */}
            <AnimatePresence>
              {showFilters && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  exit={{ opacity: 0, height: 0 }}
                  className="border-t pt-6"
                >
                  <h3 className="text-lg font-semibold mb-4">Advanced Filters</h3>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div>
                      <label className="block text-sm font-medium mb-2">Publication Year</label>
                      <select
                        value={filters.year_filter}
                        onChange={(e) => setFilters({ ...filters, year_filter: e.target.value })}
                        className="select"
                      >
                        <option value="">All Years</option>
                        {years.map(year => (
                          <option key={year} value={year}>{year}</option>
                        ))}
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-2">Category</label>
                      <input
                        type="text"
                        value={filters.category_filter}
                        onChange={(e) => setFilters({ ...filters, category_filter: e.target.value })}
                        placeholder="e.g., cs.AI, stat.ML"
                        className="input"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-2">Author</label>
                      <input
                        type="text"
                        value={filters.author_filter}
                        onChange={(e) => setFilters({ ...filters, author_filter: e.target.value })}
                        placeholder="Author name"
                        className="input"
                      />
                    </div>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </motion.div>

        {/* AI Explanation */}
        <AnimatePresence>
          {explanation && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="card mb-8 max-w-4xl mx-auto bg-gradient-to-r from-indigo-500/10 to-purple-500/10 border-indigo-500/20"
            >
              <div className="flex items-start gap-3">
                <div className="flex-shrink-0">
                  <div className="w-8 h-8 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-lg flex items-center justify-center">
                    <Sparkles className="w-4 h-4 text-white" />
                  </div>
                </div>
                <div>
                  <h3 className="font-semibold mb-2 text-indigo-300">AI Assistant</h3>
                  <p className="text-secondary leading-relaxed">{explanation}</p>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Results */}
        <AnimatePresence>
          {results.length > 0 && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="space-y-6"
            >
              <div className="flex items-center justify-between">
                <h2 className="text-2xl font-bold">
                  Found {results.length} papers
                </h2>
                <div className="text-sm text-secondary">
                  Search completed in {searchType === 'ai' ? 'AI' : 'Manual'} mode
                </div>
              </div>
              
              <div className="space-y-4">
                {results.map((article, index) => (
                  <ArticleCard key={article.id} article={article} index={index} />
                ))}
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Loading State */}
        <AnimatePresence>
          {loading && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="flex items-center justify-center py-12"
            >
              <div className="card text-center max-w-md mx-auto">
                <div className="w-12 h-12 border-4 border-primary/30 border-t-primary rounded-full animate-spin mx-auto mb-4" />
                <h3 className="font-semibold mb-2">Searching Research Papers</h3>
                <p className="text-secondary">Please wait while we find the most relevant papers...</p>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Empty State */}
        {!loading && results.length === 0 && query && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-center py-12"
          >
            <div className="card max-w-md mx-auto">
              <Search className="w-12 h-12 text-muted mx-auto mb-4" />
              <h3 className="font-semibold mb-2">No Results Found</h3>
              <p className="text-secondary mb-4">
                Try adjusting your search terms or filters to find more results.
              </p>
              <button
                onClick={() => setShowFilters(true)}
                className="btn btn-outline"
              >
                Adjust Filters
              </button>
            </div>
          </motion.div>
        )}
      </div>
    </div>
  );
};

export default SearchInterface;