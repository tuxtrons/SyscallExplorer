import React from 'react'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { 
  Terminal, 
  Activity, 
  Code, 
  Settings, 
  ArrowRight,
  Cpu,
  MemoryStick,
  Network,
  FileText
} from 'lucide-react'

const features = [
  {
    icon: Terminal,
    title: 'System Call Explorer',
    description: 'Interactive exploration of Linux system calls with real-time parameter visualization',
    href: '/syscalls',
    color: 'text-blue-500'
  },
  {
    icon: Activity,
    title: 'Performance Analysis',
    description: 'Monitor and analyze system call performance with detailed metrics and insights',
    href: '/analysis',
    color: 'text-green-500'
  },
  {
    icon: Code,
    title: 'Code Examples',
    description: 'Learn from practical examples and generate code patterns for common use cases',
    href: '/examples',
    color: 'text-purple-500'
  },
  {
    icon: Settings,
    title: 'Analysis Tools',
    description: 'Integrated strace and system analysis tools for deep system call investigation',
    href: '/tools',
    color: 'text-orange-500'
  }
]

const stats = [
  { icon: Cpu, label: 'System Calls', value: '350+', description: 'Documented system calls' },
  { icon: MemoryStick, label: 'Examples', value: '50+', description: 'Code examples available' },
  { icon: Network, label: 'Categories', value: '8', description: 'System call categories' },
  { icon: FileText, label: 'Tutorials', value: '20+', description: 'Learning materials' }
]

export default function HomePage() {
  return (
    <div className="min-h-full">
      {/* Hero Section */}
      <div className="relative bg-gradient-to-br from-primary/5 via-background to-secondary/5">
        <div className="max-w-7xl mx-auto px-6 py-24">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-center"
          >
            <h1 className="text-4xl md:text-6xl font-bold text-foreground mb-6">
              Master System Calls
              <span className="block text-primary">Interactively</span>
            </h1>
            <p className="text-xl text-muted-foreground mb-8 max-w-3xl mx-auto">
              Explore, analyze, and understand Linux system calls with real-time visualization, 
              performance monitoring, and interactive code generation tools.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/syscalls"
                className="inline-flex items-center px-6 py-3 rounded-lg bg-primary text-primary-foreground font-medium hover:bg-primary/90 transition-colors"
              >
                Explore System Calls
                <ArrowRight className="ml-2 h-4 w-4" />
              </Link>
              <Link
                to="/examples"
                className="inline-flex items-center px-6 py-3 rounded-lg border border-border text-foreground font-medium hover:bg-accent transition-colors"
              >
                View Examples
              </Link>
            </div>
          </motion.div>
        </div>
      </div>

      {/* Stats Section */}
      <div className="max-w-7xl mx-auto px-6 py-16">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
          {stats.map((stat, index) => (
            <motion.div
              key={stat.label}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              className="text-center"
            >
              <div className="bg-card p-6 rounded-lg border border-border">
                <stat.icon className="h-8 w-8 text-primary mx-auto mb-4" />
                <div className="text-2xl font-bold text-foreground mb-1">{stat.value}</div>
                <div className="text-sm font-medium text-foreground mb-1">{stat.label}</div>
                <div className="text-xs text-muted-foreground">{stat.description}</div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Features Section */}
      <div className="max-w-7xl mx-auto px-6 py-16">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <h2 className="text-3xl font-bold text-foreground mb-4">
            Everything You Need to Learn System Calls
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            From basic exploration to advanced analysis, our platform provides comprehensive 
            tools for understanding system call behavior and performance.
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 gap-8">
          {features.map((feature, index) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
            >
              <Link
                to={feature.href}
                className="block bg-card p-6 rounded-lg border border-border hover:border-primary/20 hover:shadow-lg transition-all duration-300 group"
              >
                <div className="flex items-start space-x-4">
                  <div className={`p-2 rounded-lg bg-primary/10 ${feature.color} group-hover:scale-110 transition-transform duration-300`}>
                    <feature.icon className="h-6 w-6" />
                  </div>
                  <div className="flex-1">
                    <h3 className="text-xl font-semibold text-foreground mb-2 group-hover:text-primary transition-colors">
                      {feature.title}
                    </h3>
                    <p className="text-muted-foreground mb-4">
                      {feature.description}
                    </p>
                    <div className="flex items-center text-primary text-sm font-medium">
                      Learn more
                      <ArrowRight className="ml-1 h-4 w-4 group-hover:translate-x-1 transition-transform" />
                    </div>
                  </div>
                </div>
              </Link>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Getting Started Section */}
      <div className="bg-muted/30">
        <div className="max-w-7xl mx-auto px-6 py-16">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-center"
          >
            <h2 className="text-3xl font-bold text-foreground mb-4">
              Ready to Start Exploring?
            </h2>
            <p className="text-lg text-muted-foreground mb-8 max-w-2xl mx-auto">
              Begin your journey into system call mastery with our interactive tutorials 
              and hands-on examples.
            </p>
            <Link
              to="/syscalls"
              className="inline-flex items-center px-8 py-4 rounded-lg bg-primary text-primary-foreground font-medium hover:bg-primary/90 transition-colors text-lg"
            >
              Start Learning
              <ArrowRight className="ml-2 h-5 w-5" />
            </Link>
          </motion.div>
        </div>
      </div>
    </div>
  )
}