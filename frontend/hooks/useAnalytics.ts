/**
 * Hook: useAnalytics
 * Author: محمد عبدالعزيز (Amrikyy)
 * 
 * Description (EN): Custom hook for tracking user interactions and events
 * الوصف (ع): مكون مخصص لتتبع تفاعلات المستخدم والأحداث
 */

import { useCallback } from 'react';

interface AnalyticsEvent {
  name: string;
  properties?: Record<string, any>;
}

export const useAnalytics = () => {
  const trackEvent = useCallback((name: string, properties?: Record<string, any>) => {
    // في بيئة الإنتاج، يمكن إضافة تكامل مع خدمات التحليلات مثل Google Analytics أو Mixpanel
    if (process.env.NODE_ENV === 'development') {
      console.log('Analytics Event:', { name, properties });
    }
  }, []);

  return { trackEvent };
}; 