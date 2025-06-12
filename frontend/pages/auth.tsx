"use client";

  <<<<<<< codex/create-dashboard-components-and-pages
  import React, { useState, useEffect } from "react";
  import { useRouter } from "next/router";
  import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
  } from "@/components/ui/card";
  import { Button } from "@/components/ui/button";
  import { Input } from "@/components/ui/input";
  import { Label } from "@/components/ui/label";
  import { Badge } from "@/components/ui/badge";
  import { Brain, Eye, EyeOff, Loader2, Lock, User } from "lucide-react";
  import { authApi } from "@/lib/api";
  import { useToast } from "@/lib/toast";

  export default function AuthPage() {
    const [formData, setFormData] = useState({
      username: "",
      password: "",
    });
    const [showPassword, setShowPassword] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [errors, setErrors] = useState<{ [key: string]: string }>({});

    const router = useRouter();
    const { success, error } = useToast();

    // Check if user is already authenticated
    useEffect(() => {
      if (authApi.isAuthenticated()) {
        router.push("/dashboard/overview");
      }
    }, [router]);

    const validateForm = () => {
      const newErrors: { [key: string]: string } = {};

      if (!formData.username.trim()) {
        newErrors.username = "اسم المستخدم مطلوب";
      }

      if (!formData.password) {
        newErrors.password = "كلمة المرور مطلوبة";
      } else if (formData.password.length < 3) {
        newErrors.password = "كلمة المرور قصيرة جداً";
      }

      setErrors(newErrors);
      return Object.keys(newErrors).length === 0;
    };

    const handleSubmit = async (e: React.FormEvent) => {
      e.preventDefault();

      if (!validateForm()) {
        return;
      }

      setIsLoading(true);

      try {
        const response = await authApi.login(
          formData.username,
          formData.password,
        );

        if (response.error) {
          error("فشل تسجيل الدخول", response.error);
        } else if (response.data) {
          success("تم تسجيل الدخول بنجاح", `مرحباً ${response.data.user.name}!`);
          router.push("/dashboard/overview");
        }
      } catch (err) {
        error("خطأ غير متوقع", "حدث خطأ أثناء تسجيل الدخول");
      } finally {
        setIsLoading(false);
      }
    };

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      const { name, value } = e.target;
      setFormData((prev) => ({ ...prev, [name]: value }));

      // Clear error when user starts typing
      if (errors[name]) {
        setErrors((prev) => ({ ...prev, [name]: "" }));
      }
    };

    const fillDemoCredentials = (type: "admin" | "user") => {
      const credentials = {
        admin: { username: "admin", password: "admin123" },
        user: { username: "user", password: "user123" },
      };

      setFormData(credentials[type]);
      setErrors({});
    };

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
              <p className="text-gray-400 mt-2">
                Arabic Emotional AI - Powered by Zentix
              </p>
            </div>
          </div>

          {/* Demo Credentials */}
          <div className="space-y-3">
            <div className="text-center">
              <Badge variant="secondary" className="bg-blue-500/20 text-blue-400">
                🚀 جرب النظام الآن
              </Badge>
            </div>
            <div className="flex gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => fillDemoCredentials("admin")}
                className="flex-1 bg-purple-500/10 border-purple-500/20 text-purple-400 hover:bg-purple-500/20"
              >
                مدير
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => fillDemoCredentials("user")}
                className="flex-1 bg-blue-500/10 border-blue-500/20 text-blue-400 hover:bg-blue-500/20"
              >
                مستخدم
              </Button>
            </div>
          </div>

          {/* Login Form */}
          <Card className="bg-black/40 border-purple-800/30 backdrop-blur-sm">
            <CardHeader className="space-y-1">
              <CardTitle className="text-2xl text-center text-white">
                تسجيل الدخول
              </CardTitle>
              <CardDescription className="text-center text-gray-400">
                ادخل بياناتك للوصول إلى لوحة التحكم
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="username" className="text-gray-300">
                    اسم المستخدم
                  </Label>
                  <div className="relative">
                    <User className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                    <Input
                      id="username"
                      name="username"
                      type="text"
                      placeholder="ادخل اسم المستخدم"
                      value={formData.username}
                      onChange={handleInputChange}
                      className={`pl-10 bg-gray-800 border-gray-600 text-white ${
                        errors.username ? "border-red-500" : ""
                      }`}
                      disabled={isLoading}
                    />
                  </div>
                  {errors.username && (
                    <p className="text-sm text-red-400">{errors.username}</p>
                  )}
                </div>

                <div className="space-y-2">
                  <Label htmlFor="password" className="text-gray-300">
                    كلمة المرور
                  </Label>
                  <div className="relative">
                    <Lock className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                    <Input
                      id="password"
                      name="password"
                      type={showPassword ? "text" : "password"}
                      placeholder="ادخل كلمة المرور"
                      value={formData.password}
                      onChange={handleInputChange}
                      className={`pl-10 pr-10 bg-gray-800 border-gray-600 text-white ${
                        errors.password ? "border-red-500" : ""
                      }`}
                      disabled={isLoading}
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute right-3 top-3 text-gray-400 hover:text-gray-300"
                      disabled={isLoading}
                    >
                      {showPassword ? (
                        <EyeOff className="h-4 w-4" />
                      ) : (
                        <Eye className="h-4 w-4" />
                      )}
                    </button>
                  </div>
                  {errors.password && (
                    <p className="text-sm text-red-400">{errors.password}</p>
                  )}
                </div>

                <Button
                  type="submit"
                  className="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white"
                  disabled={isLoading}
                >
                  {isLoading ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      جاري تسجيل الدخول...
                    </>
                  ) : (
                    "تسجيل الدخول"
                  )}
                </Button>
              </form>
            </CardContent>
          </Card>

          {/* Features */}
          <div className="space-y-4">
            <div className="text-center">
              <h3 className="text-lg font-medium text-white mb-3">
                ✨ مميزات النظام
              </h3>
            </div>
            <div className="grid grid-cols-1 gap-3">
              {[
                {
                  icon: "🧠",
                  title: "ذكاء اصطناعي عاطفي",
                  desc: "يفهم مشاعرك ويتفاعل معها",
                },
                {
                  icon: "💬",
                  title: "محادثة ذكية",
                  desc: "تفاعل طبيعي باللغة العربية",
                },
                {
                  icon: "📊",
                  title: "تحليل المشاعر",
                  desc: "مراقبة وتحليل الحالة النفسية",
                },
                { icon: "⚡", title: "استجابة سريعة", desc: "أداء عالي وموثوق" },
              ].map((feature, index) => (
                <div
                  key={index}
                  className="flex items-center gap-3 p-3 rounded-lg bg-gray-800/50 border border-gray-700/50"
                >
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
            <p className="text-sm text-gray-500">
              © 2024 Zentix AI. جميع الحقوق محفوظة.
            </p>
            <Badge className="bg-green-500/20 text-green-400">
              نسخة تجريبية v0.1.0
            </Badge>
          </div>
        </div>
      </div>
  =======
  import React from 'react';
  import { useRouter } from 'next/router';
  import AuthPageComponent from '@/components/auth/AuthPage';

  export default function AuthPage() {
    const router = useRouter();

    return (
      <AuthPageComponent onLoginSuccess={() => router.push('/dashboard')} />
  >>>>>>> main
    );
}
