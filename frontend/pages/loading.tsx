/**
 * LoadingPage
 * Displays a full-screen loading indicator with neon green accent color and glassmorphism effect.
 * 
 * صفحة تحميل تعرض مؤشر تحميل دائري في منتصف الشاشة مع تأثير زجاجي ولون أخضر نيون.
 */
import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { LoadingIndicator } from '../components/StaticComponent';
import { FadeIn } from '../components/ui/effects/FadeIn';
import { Logo } from '../components/common/Logo';
import { motion } from 'framer-motion';

const LoadingPage: React.FC = () => {
  const router = useRouter();
  const [progress, setProgress] = useState(0);
  const [hasSeenIntro, setHasSeenIntro] = useState(false);

  useEffect(() => {
    // محاكاة تقدم التحميل
    const timer = setInterval(() => {
      setProgress(prev => {
        // زيادة سريعة أولاً، ثم أبطأ عند الاقتراب من 100%
        const increment = 100 - prev < 20 ? 1 : 5;
        const newProgress = Math.min(prev + increment, 99);
        return newProgress;
      });
    }, 300);

    // تحقق مما إذا كان المستخدم قد شاهد المقدمة من قبل
    const seenIntro = localStorage.getItem('hasSeenIntro');
    if (seenIntro) {
      router.replace('/welcome');
      return;
    }

    // إظهار المقدمة لمدة 3 ثوانٍ ثم الانتقال
    const navigationTimer = setTimeout(async () => {
      try {
        await router.replace('/welcome');
      } catch (error) {
        console.error('Navigation failed:', error);
        // يمكن إظهار رسالة خطأ للمستخدم هنا
      }
    }, 3000);

    return () => {
      clearInterval(timer);
      clearTimeout(navigationTimer);
    };
  }, [router]);

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 1.5 }}
      className="min-h-screen flex flex-col justify-center items-center bg-gradient-to-br from-green-900 via-green-700 to-green-500 dark:from-gray-900 dark:via-gray-800 dark:to-gray-700 backdrop-blur-lg animate-gradient-x"
    >
      <Logo size="large" />
      <LoadingIndicator size="large" accentColor="green-500" showProgress progress={progress} />
      <h2 className="mt-8 text-2xl font-bold text-green-900 dark:text-green-200 animate-pulse">
        جاري التحميل...
        <span className="block text-base font-normal text-gray-500 dark:text-gray-300 mt-2">Loading, please wait</span>
      </h2>
    </motion.div>
  );
};

export default LoadingPage;
