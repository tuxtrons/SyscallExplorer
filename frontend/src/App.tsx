import { Routes, Route } from 'react-router-dom'
import { motion } from 'framer-motion'
import Layout from './components/layout/Layout'
import HomePage from './pages/HomePage'
import SystemCallsPage from './pages/SystemCallsPage'
import SystemCallDetailPage from './pages/SystemCallDetailPage'
import AnalysisPage from './pages/AnalysisPage'
import ExamplesPage from './pages/ExamplesPage'
import ToolsPage from './pages/ToolsPage'
import { ThemeProvider } from './contexts/ThemeContext'

function App() {
  return (
    <ThemeProvider>
      <div className="min-h-screen bg-background text-foreground">
        <Layout>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.3 }}
          >
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/syscalls" element={<SystemCallsPage />} />
              <Route path="/syscalls/:name" element={<SystemCallDetailPage />} />
              <Route path="/analysis" element={<AnalysisPage />} />
              <Route path="/examples" element={<ExamplesPage />} />
              <Route path="/tools" element={<ToolsPage />} />
            </Routes>
          </motion.div>
        </Layout>
      </div>
    </ThemeProvider>
  )
}

export default App