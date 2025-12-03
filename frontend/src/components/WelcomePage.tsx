import React from 'react';
import { motion } from 'framer-motion';
import { Search, Brain, Zap, Database, ArrowRight, Sparkles, BookOpen, Users, TrendingUp } from 'lucide-react';

interface WelcomePageProps {
  onGetStarted: () => void;
}

const WelcomePage: React.FC<WelcomePageProps> = ({ onGetStarted }) => {
  const features = [
    {
      icon: <Brain className="w-8 h-8" />,
      title: "AI-Powered Search",
      description: "Advanced natural language processing understands your research queries and finds the most relevant papers"
    },
    {
      icon: <Search className="w-8 h-8" />,
      title: "Semantic Search",
      description: "FAISS-powered vector search delivers precise results from our comprehensive research database"
    },
    {
      icon: <Zap className="w-8 h-8" />,
      title: "Lightning Fast",
      description: "Get instant results with our optimized search algorithms and modern infrastructure"
    },
    {
      icon: <Database className="w-8 h-8" />,
      title: "Comprehensive Database",
      description: "Access thousands of curated research papers from ArXiv across multiple scientific domains"
    }
  ];

  const stats = [
    { icon: <BookOpen className="w-6 h-6" />, value: "4,000+", label: "Research Papers" },
    { icon: <Users className="w-6 h-6" />, value: "1,000+", label: "Authors" },
    { icon: <TrendingUp className="w-6 h-6" />, value: "50+", label: "Categories" }
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="py-20">
        <div className="container">
          <div className="text-center max-w-4xl mx-auto">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="mb-8"
            >
              <div className="inline-flex items-center gap-2 bg-gradient-to-r from-indigo-500/10 to-purple-500/10 border border-indigo-500/20 rounded-full px-4 py-2 mb-6">
                <Sparkles className="w-4 h-4 text-indigo-400" />
                <span className="text-sm font-medium text-indigo-300">AI-Powered Research Discovery</span>
              </div>
              
              <h1 className="text-6xl font-extrabold mb-6 leading-tight">
                <span className="text-primary">Discover</span> Research Papers
                <br />
                <span className="bg-gradient-to-r from-indigo-400 via-purple-400 to-cyan-400 bg-clip-text text-transparent">
                  with AI Intelligence
                </span>
              </h1>
              
              <p className="text-xl text-secondary mb-8 leading-relaxed">
                Transform your research workflow with our intelligent search engine. 
                Find relevant papers instantly using natural language queries and advanced AI algorithms.
              </p>
              
              <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
                <motion.button
                  onClick={onGetStarted}
                  className="btn btn-primary btn-lg group w-full sm:w-auto"
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                >
                  Start Exploring
                  <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                </motion.button>
                
                <button className="btn btn-outline btn-lg w-full sm:w-auto">
                  <BookOpen className="w-5 h-5" />
                  Learn More
                </button>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-12">
        <div className="container">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2, duration: 0.6 }}
            className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-3xl mx-auto"
          >
            {stats.map((stat, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 + index * 0.1, duration: 0.6 }}
                className="text-center"
              >
                <div className="inline-flex items-center justify-center w-12 h-12 bg-gradient-to-r from-indigo-500/20 to-purple-500/20 rounded-xl mb-4">
                  <div className="text-indigo-400">
                    {stat.icon}
                  </div>
                </div>
                <div className="text-3xl font-bold text-primary mb-2">{stat.value}</div>
                <div className="text-secondary">{stat.label}</div>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20">
        <div className="container">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4, duration: 0.6 }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl font-bold mb-4">Powerful Features</h2>
            <p className="text-xl text-secondary max-w-2xl mx-auto">
              Our platform combines cutting-edge AI technology with intuitive design 
              to revolutionize how you discover and explore research papers.
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.5 + index * 0.1, duration: 0.6 }}
                whileHover={{ y: -8 }}
                className="card text-center group"
              >
                <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-indigo-500/20 to-purple-500/20 rounded-2xl mb-6 group-hover:scale-110 transition-transform">
                  <div className="text-indigo-400">
                    {feature.icon}
                  </div>
                </div>
                <h3 className="text-xl font-semibold mb-3">{feature.title}</h3>
                <p className="text-secondary leading-relaxed">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20">
        <div className="container">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.8, duration: 0.6 }}
            className="glass-card text-center max-w-4xl mx-auto"
          >
            <h2 className="text-3xl font-bold mb-4">Ready to Transform Your Research?</h2>
            <p className="text-xl text-secondary mb-8">
              Join thousands of researchers who are already using our AI-powered platform 
              to discover breakthrough papers and accelerate their work.
            </p>
            <motion.button
              onClick={onGetStarted}
              className="btn btn-primary btn-lg"
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              Get Started Now
              <ArrowRight className="w-5 h-5" />
            </motion.button>
          </motion.div>
        </div>
      </section>
    </div>
  );
};

export default WelcomePage;