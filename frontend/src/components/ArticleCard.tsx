import React from 'react';
import { motion } from 'framer-motion';
import { Calendar, User, Tag, FileText, ExternalLink } from 'lucide-react';
import { Article } from '../types';

interface ArticleCardProps {
  article: Article;
  index: number;
}

const ArticleCard: React.FC<ArticleCardProps> = ({ article, index }) => {
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const truncateText = (text: string, maxLength: number) => {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
  };

  const getCategories = (categories: string) => {
    return categories.split(',').map(cat => cat.trim()).slice(0, 3);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1, duration: 0.5 }}
      whileHover={{ y: -4 }}
      className="card group cursor-pointer"
    >
      <div className="space-y-4">
        {/* Header */}
        <div className="flex items-start justify-between gap-4">
          <h3 className="text-xl font-semibold leading-tight group-hover:text-primary transition-colors">
            {article.title}
          </h3>
          <button className="flex-shrink-0 p-2 rounded-lg bg-surface-light/50 opacity-0 group-hover:opacity-100 transition-opacity">
            <ExternalLink className="w-4 h-4" />
          </button>
        </div>

        {/* Abstract */}
        <div className="flex gap-3">
          <FileText className="w-5 h-5 text-muted mt-1 flex-shrink-0" />
          <p className="text-secondary leading-relaxed">
            {truncateText(article.abstract, 300)}
          </p>
        </div>

        {/* Metadata */}
        <div className="flex flex-wrap gap-4 text-sm">
          {/* Authors */}
          {article.authors && (
            <div className="flex items-center gap-2">
              <User className="w-4 h-4 text-muted" />
              <span className="text-secondary">
                {truncateText(article.authors, 80)}
              </span>
            </div>
          )}

          {/* Date */}
          <div className="flex items-center gap-2">
            <Calendar className="w-4 h-4 text-muted" />
            <span className="text-secondary">
              {formatDate(article.published)}
            </span>
          </div>
        </div>

        {/* Categories */}
        {article.categories && (
          <div className="flex items-start gap-2">
            <Tag className="w-4 h-4 text-muted mt-1 flex-shrink-0" />
            <div className="flex flex-wrap gap-2">
              {getCategories(article.categories).map((category, idx) => (
                <span
                  key={idx}
                  className="px-3 py-1 bg-primary/10 text-primary text-xs rounded-full border border-primary/20 font-medium"
                >
                  {category}
                </span>
              ))}
              {article.categories.split(',').length > 3 && (
                <span className="px-3 py-1 bg-surface-light text-muted text-xs rounded-full font-medium">
                  +{article.categories.split(',').length - 3}
                </span>
              )}
            </div>
          </div>
        )}

        {/* Hover indicator */}
        <div className="h-1 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full opacity-0 group-hover:opacity-100 transition-opacity" />
      </div>
    </motion.div>
  );
};

export default ArticleCard;