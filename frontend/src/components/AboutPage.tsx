import React from 'react';
import { motion } from 'framer-motion';
import { Brain, Database, Zap, Users, Github, Mail, ExternalLink } from 'lucide-react';

const AboutPage: React.FC = () => {
  const features = [
    {
      icon: <Brain className="w-6 h-6" />,
      title: "AI-Powered Intelligence",
      description: "Advanced natural language processing and machine learning algorithms to understand research queries"
    },
    {
      icon: <Database className="w-6 h-6" />,
      title: "Comprehensive Database",
      description: "Access to thousands of research papers from ArXiv across multiple scientific domains"
    },
    {
      icon: <Zap className="w-6 h-6" />,
      title: "Lightning Fast Search",
      description: "FAISS-powered vector search delivers results in milliseconds with high accuracy"
    },
    {
      icon: <Users className="w-6 h-6" />,
      title: "Researcher Focused",
      description: "Built by researchers, for researchers, with features that matter to the scientific community"
    }
  ];

  const techStack = [
    { name: "React", description: "Modern frontend framework" },
    { name: "FastAPI", description: "High-performance Python backend" },
    { name: "FAISS", description: "Vector similarity search" },
    { name: "Transformers", description: "AI language models" },
    { name: "SQLite", description: "Lightweight database" },
    { name: "TypeScript", description: "Type-safe development" }
  ];

  return (
    <div className="min-h-screen py-8">
      <div className="container">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-16"
        >
          <h1 className="text-4xl font-bold mb-4">About ArXiv Research Hub</h1>
          <p className="text-xl text-secondary max-w-3xl mx-auto">
            A modern, AI-powered platform designed to revolutionize how researchers discover 
            and explore scientific papers from the ArXiv repository.
          </p>
        </motion.div>

        {/* Mission */}
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="mb-16"
        >
          <div className="glass-card max-w-4xl mx-auto text-center">
            <h2 className="text-3xl font-bold mb-6">Our Mission</h2>
            <p className="text-lg text-secondary leading-relaxed">
              To democratize access to scientific knowledge by providing researchers with intelligent, 
              fast, and intuitive tools for discovering relevant research papers. We believe that 
              breakthrough discoveries happen when researchers can easily find and build upon existing work.
            </p>
          </div>
        </motion.section>

        {/* Features */}
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="mb-16"
        >
          <h2 className="text-3xl font-bold text-center mb-12">What Makes Us Different</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 + index * 0.1 }}
                className="card"
              >
                <div className="flex items-start gap-4">
                  <div className="flex-shrink-0 w-12 h-12 bg-gradient-to-r from-indigo-500/20 to-purple-500/20 rounded-xl flex items-center justify-center">
                    <div className="text-primary">
                      {feature.icon}
                    </div>
                  </div>
                  <div>
                    <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
                    <p className="text-secondary">{feature.description}</p>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </motion.section>

        {/* Tech Stack */}
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="mb-16"
        >
          <h2 className="text-3xl font-bold text-center mb-12">Built With Modern Technology</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {techStack.map((tech, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.5 + index * 0.05 }}
                className="card text-center"
              >
                <h3 className="text-lg font-semibold mb-2 text-primary">{tech.name}</h3>
                <p className="text-sm text-secondary">{tech.description}</p>
              </motion.div>
            ))}
          </div>
        </motion.section>

        {/* Stats */}
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="mb-16"
        >
          <div className="glass-card text-center">
            <h2 className="text-3xl font-bold mb-8">Platform Statistics</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div>
                <div className="text-4xl font-bold text-primary mb-2">4,000+</div>
                <div className="text-secondary">Research Papers Indexed</div>
              </div>
              <div>
                <div className="text-4xl font-bold text-primary mb-2">50+</div>
                <div className="text-secondary">Scientific Categories</div>
              </div>
              <div>
                <div className="text-4xl font-bold text-primary mb-2">1,000+</div>
                <div className="text-secondary">Unique Authors</div>
              </div>
            </div>
          </div>
        </motion.section>

        {/* Contact */}
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.7 }}
        >
          <div className="card max-w-2xl mx-auto text-center">
            <h2 className="text-2xl font-bold mb-6">Get In Touch</h2>
            <p className="text-secondary mb-8">
              Have questions, suggestions, or want to contribute? We'd love to hear from you!
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <a
                href="https://github.com"
                target="_blank"
                rel="noopener noreferrer"
                className="btn btn-outline"
              >
                <Github className="w-4 h-4" />
                View on GitHub
                <ExternalLink className="w-4 h-4" />
              </a>
              <a
                href="mailto:contact@arxivhub.com"
                className="btn btn-primary"
              >
                <Mail className="w-4 h-4" />
                Contact Us
              </a>
            </div>
          </div>
        </motion.section>
      </div>
    </div>
  );
};

export default AboutPage;