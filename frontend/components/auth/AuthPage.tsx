'use client';

import React from 'react';
import { Badge } from '@/components/ui/badge';
import { Brain } from 'lucide-react';
import LoginForm from './LoginForm';

interface AuthPageProps {
  onLoginSuccess?: () => void;
}

export default function AuthPage({ onLoginSuccess }: AuthPageProps) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center p-4">
      <div className="w-full max-w-md space-y-6">
        {/* Header */}
        <div className="text-center space-y-4">
          <div className="w-16 h-16 bg-gradient-to-r from-purple-500 to-pink-500 rounded-2xl flex items-center justify-center mx-auto">
            <Brain className="w-8 h-8 text-white" />
          </div>
          <div>
            <h1 className="text-3xl font-bold bg-gradient-to-r from-white to-purple-200 bg-clip-text text-transparent">
              Zentix AI
            </h1>
            <p className="text-gray-400 mt-2">Arabic Emotional AI - Powered by Zentix</p>
          </div>
        </div>

        {/* Login Form */}
        <LoginForm onLoginSuccess={onLoginSuccess} />

        {/* Features */}
        <div className="space-y-4">
          <div className="text-center">
            <h3 className="text-lg font-medium text-white mb-3">✨ مميزات النظام</h3>
          </div>
          <div className="grid grid-cols-1 gap-3">
            {[
              { icon: '🧠', title: 'ذكاء اصطناعي عاطفي', desc: 'يفهم مشاعرك ويتفاعل معها' },
              { icon: '💬', title: 'محادثة ذكية', desc: 'تفاعل طبيعي باللغة العربية' },
              { icon: '📊', title: 'تحليل المشاعر', desc: 'مراقبة وتحليل الحالة النفسية' },
              { icon: '⚡', title: 'استجابة سريعة', desc: 'أداء عالي وموثوق' },
            ].map((feature, index) => (
              <div key={index} className="flex items-center gap-3 p-3 rounded-lg bg-gray-800/50 border border-gray-700/50">
                <span className="text-2xl">{feature.icon}</span>
                <div>
                  <h4 className="font-medium text-white">{feature.title}</h4>
                  <p className="text-sm text-gray-400">{feature.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Footer */}
        <div className="text-center space-y-2">
          <p className="text-sm text-gray-500">© 2024 Zentix AI. جميع الحقوق محفوظة.</p>
          <Badge className="bg-green-500/20 text-green-400">نسخة تجريبية v0.1.0</Badge>
        </div>
      </div>
    </div>
  );
}
