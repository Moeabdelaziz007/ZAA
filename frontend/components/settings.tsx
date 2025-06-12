'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  Settings, 
  Bell, 
  Shield, 
  Save, 
  RefreshCw,
  Monitor,
  CheckCircle,
  AlertTriangle
} from 'lucide-react';
import { settingsApi } from '@/lib/api';
import { useToast } from '@/lib/toast';

export default function SettingsComponent() {
  const [settings, setSettings] = useState({
    logging_enabled: true,
    emotion_analysis: true,
    auto_backup: true,
    language: 'ar',
    theme: 'dark',
    notifications: true,
  });
  const [isLoading, setIsLoading] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [hasChanges, setHasChanges] = useState(false);
  
  const { success, error, info } = useToast();

  useEffect(() => {
    loadSettings();
  }, []);

  const loadSettings = async () => {
    setIsLoading(true);
    try {
      const response = await settingsApi.getSettings();
      if (response.error) {
        error('خطأ في تحميل الإعدادات', response.error);
      } else if (response.data) {
        setSettings(response.data.settings);
      }
    } catch (err) {
      error('خطأ غير متوقع', 'فشل في تحميل الإعدادات');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSettingChange = (key: string, value: any) => {
    setSettings(prev => ({ ...prev, [key]: value }));
    setHasChanges(true);
  };

  const saveSettings = async () => {
    setIsSaving(true);
    try {
      const response = await settingsApi.updateSettings(settings);
      if (response.error) {
        error('خطأ في حفظ الإعدادات', response.error);
      } else {
        success('تم الحفظ بنجاح', 'تم حفظ جميع الإعدادات');
        setHasChanges(false);
      }
    } catch (err) {
      error('خطأ غير متوقع', 'فشل في حفظ الإعدادات');
    } finally {
      setIsSaving(false);
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center space-y-4">
          <RefreshCw className="w-8 h-8 animate-spin mx-auto text-purple-400" />
          <p className="text-gray-400">جاري تحميل الإعدادات...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gradient-to-r from-purple-500 to-pink-500 rounded-xl flex items-center justify-center">
            <Settings className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white">إعدادات النظام</h1>
            <p className="text-gray-400">تخصيص وإدارة إعدادات Zentix AI</p>
          </div>
        </div>
        
        {hasChanges && (
          <Button
            onClick={saveSettings}
            disabled={isSaving}
            className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700"
          >
            {isSaving ? (
              <>
                <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
                جاري الحفظ...
              </>
            ) : (
              <>
                <Save className="w-4 h-4 mr-2" />
                حفظ التغييرات
              </>
            )}
          </Button>
        )}
      </div>

      <Tabs defaultValue="general" className="space-y-6">
        <TabsList className="grid w-full grid-cols-3 bg-black/40 border border-purple-800/30">
          <TabsTrigger value="general">عام</TabsTrigger>
          <TabsTrigger value="ai">الذكاء الاصطناعي</TabsTrigger>
          <TabsTrigger value="security">الأمان</TabsTrigger>
        </TabsList>

        {/* General Settings */}
        <TabsContent value="general" className="space-y-6">
          <Card className="bg-black/40 border-purple-800/30">
            <CardHeader>
              <CardTitle className="text-white flex items-center gap-2">
                <Bell className="w-5 h-5" />
                الإشعارات والمظهر
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <h4 className="font-medium text-white">تفعيل الإشعارات</h4>
                  <p className="text-sm text-gray-400">استقبال إشعارات النظام والتحديثات</p>
                </div>
                <Button
                  variant={settings.notifications ? "default" : "outline"}
                  size="sm"
                  onClick={() => handleSettingChange('notifications', !settings.notifications)}
                  className={settings.notifications ? "bg-green-600 hover:bg-green-700" : ""}
                >
                  {settings.notifications ? 'مفعل' : 'معطل'}
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* AI Settings */}
        <TabsContent value="ai" className="space-y-6">
          <Card className="bg-black/40 border-purple-800/30">
            <CardHeader>
              <CardTitle className="text-white flex items-center gap-2">
                <Monitor className="w-5 h-5" />
                إعدادات الذكاء الاصطناعي
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="flex items-center justify-between p-4 bg-gray-800/50 rounded-lg">
                <div>
                  <h4 className="font-medium text-white">تحليل المشاعر</h4>
                  <p className="text-sm text-gray-400">تحليل المشاعر في النصوص والمحادثات</p>
                </div>
                <Button
                  variant={settings.emotion_analysis ? "default" : "outline"}
                  size="sm"
                  onClick={() => handleSettingChange('emotion_analysis', !settings.emotion_analysis)}
                  className={settings.emotion_analysis ? "bg-green-600 hover:bg-green-700" : ""}
                >
                  {settings.emotion_analysis ? 'مفعل' : 'معطل'}
                </Button>
              </div>

              <div className="flex items-center justify-between p-4 bg-gray-800/50 rounded-lg">
                <div>
                  <h4 className="font-medium text-white">تسجيل التفاعلات</h4>
                  <p className="text-sm text-gray-400">حفظ المحادثات لتحسين الأداء</p>
                </div>
                <Button
                  variant={settings.logging_enabled ? "default" : "outline"}
                  size="sm"
                  onClick={() => handleSettingChange('logging_enabled', !settings.logging_enabled)}
                  className={settings.logging_enabled ? "bg-green-600 hover:bg-green-700" : ""}
                >
                  {settings.logging_enabled ? 'مفعل' : 'معطل'}
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Security Settings */}
        <TabsContent value="security" className="space-y-6">
          <Card className="bg-black/40 border-purple-800/30">
            <CardHeader>
              <CardTitle className="text-white flex items-center gap-2">
                <Shield className="w-5 h-5" />
                الأمان والخصوصية
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="p-4 bg-green-500/10 border border-green-500/20 rounded-lg">
                <div className="flex items-center gap-2 mb-2">
                  <CheckCircle className="w-5 h-5 text-green-400" />
                  <h4 className="font-medium text-white">حماية البيانات</h4>
                </div>
                <p className="text-sm text-gray-400">جميع البيانات محمية بالتشفير</p>
              </div>

              <div className="p-4 bg-yellow-500/10 border border-yellow-500/20 rounded-lg">
                <div className="flex items-center gap-2 mb-2">
                  <AlertTriangle className="w-5 h-5 text-yellow-400" />
                  <h4 className="font-medium text-white">انتباه</h4>
                </div>
                <p className="text-sm text-gray-400">هذا إصدار تجريبي - لا تستخدم بيانات حساسة</p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
} 