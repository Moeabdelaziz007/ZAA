import { Switch, Route } from "wouter";
import { Toaster } from "@/components/ui/toaster";
import NotFound from "@/pages/not-found";
import HomePage from "@/pages/home-page";
import AuthPage from "@/pages/auth-page";
import PropertyDetailPage from "@/pages/property-detail-page";
import MessagesPage from "@/pages/messages-page";
import PointsPage from "@/pages/points-page";
import ServicesPage from "@/pages/services-page";
import { MobileNav } from "@/components/layout/mobile-nav";
import { Footer } from "@/components/layout/footer";
import { AuthProvider } from "@/hooks/use-auth";
import { QueryClientProvider } from "@tanstack/react-query";
import { queryClient } from "./lib/queryClient";

function Router() {
  return (
    <Switch>
      <Route path="/" component={HomePage} />
      <Route path="/property/:id" component={PropertyDetailPage} />
      <Route path="/auth" component={AuthPage} />
      <Route path="/messages" component={MessagesPage} />
      <Route path="/points" component={PointsPage} />
      <Route path="/services" component={ServicesPage} />
      <Route component={NotFound} />
    </Switch>
  );
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <div className="flex flex-col min-h-screen bg-background">
          <main className="flex-1">
            <Router />
          </main>
          <Footer />
          <MobileNav />
          <Toaster />
        </div>
      </AuthProvider>
    </QueryClientProvider>
  );
}

export default App;
