'use client';

import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';

interface RegisterFormProps {
  onRegister?: () => void;
}

export default function RegisterForm({ onRegister }: RegisterFormProps) {
  const [formData, setFormData] = useState({ username: '', password: '', email: '' });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onRegister?.();
  };

  return (
    <Card className="bg-black/40 border-purple-800/30 backdrop-blur-sm">
      <CardHeader className="space-y-1">
        <CardTitle className="text-2xl text-center text-white">إنشاء حساب</CardTitle>
        <CardDescription className="text-center text-gray-400">
          قم بإنشاء حساب جديد للوصول إلى لوحة التحكم
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="email" className="text-gray-300">
              البريد الإلكتروني
            </Label>
            <Input
              id="email"
              name="email"
              type="email"
              placeholder="example@email.com"
              value={formData.email}
              onChange={handleChange}
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="username" className="text-gray-300">
              اسم المستخدم
            </Label>
            <Input
              id="username"
              name="username"
              type="text"
              placeholder="ادخل اسم المستخدم"
              value={formData.username}
              onChange={handleChange}
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="password" className="text-gray-300">
              كلمة المرور
            </Label>
            <Input
              id="password"
              name="password"
              type="password"
              placeholder="كلمة المرور"
              value={formData.password}
              onChange={handleChange}
            />
          </div>
          <Button type="submit" className="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white">
            تسجيل
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
