/**
 * @component Footer
 * @author محمد عبدالعزيز (Amrikyy)
 * @description Footer component for displaying copyright and links at the bottom of the page
 * @description_ar مكون القدم لعرض حقوق النشر والروابط في أسفل الصفحة
 * @props None
 */

import React from 'react';
import PointsPage from "@/pages/points-page";
import ServicesPage from "@/pages/services-page";
import MobileNav from "@/components/layout/mobile-nav";
import Footer from "@/components/layout/footer";
import { AuthProvider } from "@/hooks/use-auth";
import { QueryClientProvider } from "@tanstack/react-query";
import { queryClient } from "./lib/queryClient";

const FooterComponent = () => {
  return (
    <footer className="bg-background border-t border-border p-4 text-center text-sm text-muted-foreground">
      <p>© 2024 Zentix AI. جميع الحقوق محفوظة.</p>
    </footer>
  );
};

export default FooterComponent; 