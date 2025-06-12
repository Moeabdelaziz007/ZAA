"use client";

import React from "react";
import { useRouter } from "next/router";
import AuthPage from "@/components/auth/AuthPage";

export default function AuthPageWrapper() {
  const router = useRouter();
  return <AuthPage onLoginSuccess={() => router.push('/dashboard/overview')} />;
}
