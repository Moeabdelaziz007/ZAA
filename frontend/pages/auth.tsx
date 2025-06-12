'use client';

import React from 'react';
import { useRouter } from 'next/router';
import AuthPageComponent from '@/components/auth/AuthPage';

export default function AuthPage() {
  const router = useRouter();

  return (
    <AuthPageComponent onLoginSuccess={() => router.push('/dashboard')} />
  );
}
