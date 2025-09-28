import React from "react";
import { Link, useLocation } from "react-router-dom";
import { createPageUrl } from "@/utils";
import { Shield, Eye, EyeOff, History } from "lucide-react";

export default function Layout({ children, currentPageName }) {
  const location = useLocation();

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      <style jsx>{`
        :root {
          --primary: 219 234 254;
          --primary-foreground: 30 41 59;
          --secondary: 51 65 85;
          --secondary-foreground: 248 250 252;
          --accent: 59 130 246;
          --accent-foreground: 248 250 252;
          --background: 15 23 42;
          --foreground: 248 250 252;
          --muted: 51 65 85;
          --muted-foreground: 148 163 184;
          --border: 51 65 85;
          --card: 30 41 59;
          --card-foreground: 248 250 252;
        }
      `}</style>
      
      {/* Header */}
      <header className="border-b border-slate-700/50 bg-slate-800/50 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <Link to={createPageUrl("Dashboard")} className="flex items-center gap-3 group">
              <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-lg flex items-center justify-center group-hover:scale-105 transition-transform">
                <Shield className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-white">SteganoCrypt</h1>
                <p className="text-xs text-slate-400">Hide messages in plain sight</p>
              </div>
            </Link>
            
            <nav className="hidden md:flex items-center gap-6">
              <Link 
                to={createPageUrl("Dashboard")} 
                className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-colors ${
                  location.pathname === createPageUrl("Dashboard") 
                    ? 'bg-blue-600 text-white' 
                    : 'text-slate-300 hover:text-white hover:bg-slate-700'
                }`}
              >
                <Shield className="w-4 h-4" />
                Dashboard
              </Link>
              <Link 
                to={createPageUrl("History")} 
                className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-colors ${
                  location.pathname === createPageUrl("History") 
                    ? 'bg-blue-600 text-white' 
                    : 'text-slate-300 hover:text-white hover:bg-slate-700'
                }`}
              >
                <History className="w-4 h-4" />
                History
              </Link>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {children}
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-700/50 bg-slate-800/30 mt-16">
        <div className="container mx-auto px-4 py-6">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <p className="text-slate-400 text-sm">
              Secure steganography for modern communications
            </p>
            <div className="flex items-center gap-4 text-slate-500 text-sm">
              <span>Powered by advanced cryptography</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}