/**
 * Component: AIAgent
 * Author: محمد عبدالعزيز (Amrikyy)
 * 
 * Description (EN): AI-powered agent component for user interaction and support, with bilingual support and analytics integration.
 * الوصف (ع): مكون ذكي للتفاعل مع المستخدم والدعم، مع دعم اللغتين وتكامل التحليلات.
 * 
 * Props:
 * - lang: 'ar' | 'en'    // لغة الواجهة
 * - onAnalytics: (data: any) => void  // دالة لتتبع التفاعلات
 */

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useAnalytics } from '@/hooks/useAnalytics';

interface Message {
  id: string;
  user: string;
  ai: string;
  timestamp: Date;
}

interface AIAgentProps {
  lang?: 'ar' | 'en';
  onAnalytics?: (data: any) => void;
}

const translations = {
  ar: {
    ask: 'اسألني أي شيء...',
    send: 'إرسال',
    you: 'أنت',
    thinking: 'جاري التفكير...',
    error: 'عذراً، حدث خطأ. حاول مرة أخرى.'
  },
  en: {
    ask: 'Ask me anything...',
    send: 'Send',
    you: 'You',
    thinking: 'Thinking...',
    error: 'Sorry, an error occurred. Please try again.'
  }
};

export const AIAgent: React.FC<AIAgentProps> = ({ 
  lang = 'ar',
  onAnalytics 
}) => {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const { trackEvent } = useAnalytics();
  const t = translations[lang];

  const sendMessage = async () => {
    if (!input.trim()) return;

    setIsLoading(true);
    const userMessage = input;
    setInput('');

    try {
      const response = await fetch('/api/ai-agent', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          message: userMessage,
          lang 
        }),
      });

      if (!response.ok) throw new Error('API Error');

      const data = await response.json();
      
      const newMessage: Message = {
        id: Date.now().toString(),
        user: userMessage,
        ai: data.reply,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, newMessage]);
      
      // Track interaction
      trackEvent('ai_interaction', {
        type: 'message_sent',
        language: lang,
        message_length: userMessage.length
      });

      if (onAnalytics) {
        onAnalytics({
          type: 'message_sent',
          message: userMessage,
          response: data.reply,
          lang
        });
      }
    } catch (error) {
      console.error('AI Agent Error:', error);
      trackEvent('ai_error', { error: error instanceof Error ? error.message : String(error) });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto p-4 bg-white dark:bg-gray-800 rounded-lg shadow-lg">
      <div className="h-[400px] overflow-y-auto mb-4 space-y-4">
        <AnimatePresence>
          {messages.map((message) => (
            <motion.div
              key={message.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="p-3 rounded-lg"
            >
              <div className="font-bold text-primary-600 dark:text-primary-400">
                {t.you}:
              </div>
              <div className="mb-2">{message.user}</div>
              <div className="font-bold text-secondary-600 dark:text-secondary-400">
                AI:
              </div>
              <div>{message.ai}</div>
            </motion.div>
          ))}
        </AnimatePresence>
        {isLoading && (
          <div className="text-center text-gray-500 dark:text-gray-400">
            {t.thinking}
          </div>
        )}
      </div>

      <div className="flex gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
          placeholder={t.ask}
          className="flex-1 p-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600"
          dir={lang === 'ar' ? 'rtl' : 'ltr'}
        />
        <button
          onClick={sendMessage}
          disabled={isLoading}
          className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50"
        >
          {t.send}
        </button>
      </div>
    </div>
  );
}; 