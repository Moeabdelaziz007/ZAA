'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  Settings, 
  Bell, 
  Shield, 
  Palette, 
  Globe, 
  Save, 
  RefreshCw,
  Monitor,
  Database,
  AlertTriangle,
  CheckCircle
} from 'lucide-react';
import { settingsApi } from '@/lib/api';
import { useToast } from '@/lib/toast';

interface SettingsData {
  logging_enabled: boolean;
  emotion_analysis: boolean;
  auto_backup: boolean;
  language: string;
  theme: string;
  notifications: boolean;
}

export default function SettingsPage() {
  const [settings, setSettings] = useState<SettingsData>({
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

  // Load settings on component mount
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

  const handleSettingChange = (key: keyof SettingsData, value: any) => {
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

  const resetSettings = () => {
    setSettings({
      logging_enabled: true,
      emotion_analysis: true,
      auto_backup: true,
      language: 'ar',
      theme: 'dark',
      notifications: true,
    });
    setHasChanges(true);
    info('تم إعادة التعيين', 'تم إعادة تعيين الإعدادات للقيم الافتراضية');
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
          <div className="flex gap-2">
            <Button
              variant="outline"
              onClick={resetSettings}
              className="bg-gray-800 border-gray-600 text-gray-300"
            >
              إعادة تعيين
            </Button>
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
          </div>
        )}
      </div>

      <Tabs defaultValue="general" className="space-y-6">
        <TabsList className="grid w-full grid-cols-4 bg-black/40 border border-purple-800/30">
          <TabsTrigger value="general" className="flex items-center gap-2">
            <Settings className="w-4 h-4" />
            عام
          </TabsTrigger>
          <TabsTrigger value="ai" className="flex items-center gap-2">
            <Monitor className="w-4 h-4" />
            الذكاء الاصطناعي
          </TabsTrigger>
          <TabsTrigger value="security" className="flex items-center gap-2">
            <Shield className="w-4 h-4" />
            الأمان
          </TabsTrigger>
          <TabsTrigger value="advanced" className="flex items-center gap-2">
            <Database className="w-4 h-4" />
            متقدم
          </TabsTrigger>
        </TabsList>

        {/* General Settings */}
        <TabsContent value="general" className="space-y-6">
          <Card className="bg-black/40 border-purple-800/30">
            <CardHeader>
              <CardTitle className="text-white flex items-center gap-2">
                <Palette className="w-5 h-5" />
                المظهر واللغة
              </CardTitle>
              <CardDescription className="text-gray-400">
                تخصيص مظهر التطبيق واللغة
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label className="text-gray-300">السمة</Label>
                  <select
                    value={settings.theme}
                    onChange={(e) => handleSettingChange('theme', e.target.value)}
                    className="w-full p-2 bg-gray-800 border border-gray-600 rounded-md text-white"
                  >
                    <option value="dark">مظلم</option>
                    <option value="light">فاتح</option>
                    <option value="auto">تلقائي</option>
                  </select>
                </div>
                
                <div className="space-y-2">
                  <Label className="text-gray-300">اللغة</Label>
                  <select
                    value={settings.language}
                    onChange={(e) => handleSettingChange('language', e.target.value)}
                    className="w-full p-2 bg-gray-800 border border-gray-600 rounded-md text-white"
                  >
                    <option value="ar">العربية</option>
                    <option value="en">English</option>
                  </select>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-black/40 border-purple-800/30">
            <CardHeader>
              <CardTitle className="text-white flex items-center gap-2">
                <Bell className="w-5 h-5" />
                الإشعارات
              </CardTitle>
              <CardDescription className="text-gray-400">
                إدارة إعدادات الإشعارات
              </CardDescription>
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
              <CardTitle className="text-white">إعدادات الذكاء الاصطناعي</CardTitle>
              <CardDescription className="text-gray-400">
                تحكم في ميزات الذكاء الاصطناعي
              </CardDescription>
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
              <CardDescription className="text-gray-400">
                إعدادات الأمان وحماية البيانات
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-4">
                <div className="p-4 bg-green-500/10 border border-green-500/20 rounded-lg">
                  <div className="flex items-center gap-2 mb-2">
                    <CheckCircle className="w-5 h-5 text-green-400" />
                    <h4 className="font-medium text-white">حماية البيانات</h4>
                  </div>
                  <p className="text-sm text-gray-400">جميع البيانات محمية بالتشفير</p>
                </div>

                <div className="p-4 bg-blue-500/10 border border-blue-500/20 rounded-lg">
                  <div className="flex items-center gap-2 mb-2">
                    <CheckCircle className="w-5 h-5 text-blue-400" />
                    <h4 className="font-medium text-white">JWT Authentication</h4>
                  </div>
                  <p className="text-sm text-gray-400">نظام مصادقة آمن باستخدام JSON Web Tokens</p>
                </div>

                <div className="p-4 bg-yellow-500/10 border border-yellow-500/20 rounded-lg">
                  <div className="flex items-center gap-2 mb-2">
                    <AlertTriangle className="w-5 h-5 text-yellow-400" />
                    <h4 className="font-medium text-white">انتباه</h4>
                  </div>
                  <p className="text-sm text-gray-400">هذا إصدار تجريبي - لا تستخدم بيانات حساسة</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Advanced Settings */}
        <TabsContent value="advanced" className="space-y-6">
          <Card className="bg-black/40 border-purple-800/30">
            <CardHeader>
              <CardTitle className="text-white flex items-center gap-2">
                <Database className="w-5 h-5" />
                الإعدادات المتقدمة
              </CardTitle>
              <CardDescription className="text-gray-400">
                إعدادات للمطورين والمستخدمين المتقدمين
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="flex items-center justify-between p-4 bg-gray-800/50 rounded-lg">
                <div>
                  <h4 className="font-medium text-white">النسخ الاحتياطي التلقائي</h4>
                  <p className="text-sm text-gray-400">إنشاء نسخ احتياطية للبيانات تلقائياً</p>
                </div>
                <Button
                  variant={settings.auto_backup ? "default" : "outline"}
                  size="sm"
                  onClick={() => handleSettingChange('auto_backup', !settings.auto_backup)}
                  className={settings.auto_backup ? "bg-green-600 hover:bg-green-700" : ""}
                >
                  {settings.auto_backup ? 'مفعل' : 'معطل'}
                </Button>
              </div>

              <div className="space-y-4">
                <h4 className="font-medium text-white">معلومات النظام</h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="p-3 bg-gray-800/50 rounded-lg">
                    <p className="text-sm text-gray-400">إصدار التطبيق</p>
                    <p className="font-medium text-white">v0.1.0</p>
                  </div>
                  <div className="p-3 bg-gray-800/50 rounded-lg">
                    <p className="text-sm text-gray-400">إصدار API</p>
                    <p className="font-medium text-white">v1</p>
                  </div>
                  <div className="p-3 bg-gray-800/50 rounded-lg">
                    <p className="text-sm text-gray-400">البيئة</p>
                    <Badge className="bg-blue-500/20 text-blue-400">تطوير</Badge>
                  </div>
                  <div className="p-3 bg-gray-800/50 rounded-lg">
                    <p className="text-sm text-gray-400">الحالة</p>
                    <Badge className="bg-green-500/20 text-green-400">نشط</Badge>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
} 