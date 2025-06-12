'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Badge } from '@/components/ui/badge';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { 
  User, 
  Mail, 
  Calendar, 
  Activity, 
  MessageCircle, 
  Heart, 
  TrendingUp,
  Edit3,
  Save,
  RefreshCw,
  Shield,
  Clock,
  CheckCircle
} from 'lucide-react';
import { authApi } from '@/lib/api';
import { useToast } from '@/lib/toast';

interface UserProfile {
  id: string;
  username: string;
  name: string;
  email: string;
  role: string;
}

export default function ProfileComponent() {
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isEditing, setIsEditing] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [editForm, setEditForm] = useState({
    name: '',
    email: '',
  });
  
  const { success, error } = useToast();

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    setIsLoading(true);
    try {
      const response = await authApi.getProfile();
      if (response.error) {
        error('خطأ في تحميل الملف الشخصي', response.error);
      } else if (response.data) {
        setProfile(response.data.user);
        setEditForm({
          name: response.data.user.name,
          email: response.data.user.email,
        });
      }
    } catch (err) {
      error('خطأ غير متوقع', 'فشل في تحميل الملف الشخصي');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSave = async () => {
    setIsSaving(true);
    try {
      // Note: In a real app, you'd have an API endpoint to update profile
      success('تم التحديث', 'تم تحديث الملف الشخصي بنجاح');
      setIsEditing(false);
      if (profile) {
        setProfile({ ...profile, ...editForm });
      }
    } catch (err) {
      error('خطأ في التحديث', 'فشل في تحديث الملف الشخصي');
    } finally {
      setIsSaving(false);
    }
  };

  const handleCancel = () => {
    if (profile) {
      setEditForm({
        name: profile.name,
        email: profile.email,
      });
    }
    setIsEditing(false);
  };

  const getUserStats = () => {
    // Mock stats - in a real app, fetch from API
    return {
      totalInteractions: 247,
      averageEmotion: 'سعادة',
      joinDate: '2024-01-15',
      lastActive: 'منذ ساعة',
      favoriteFeature: 'المحادثة الذكية',
      emotionTrend: '+15%',
    };
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center space-y-4">
          <RefreshCw className="w-8 h-8 animate-spin mx-auto text-purple-400" />
          <p className="text-gray-400">جاري تحميل الملف الشخصي...</p>
        </div>
      </div>
    );
  }

  if (!profile) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-400">فشل في تحميل الملف الشخصي</p>
        <Button onClick={loadProfile} className="mt-4">
          إعادة المحاولة
        </Button>
      </div>
    );
  }

  const stats = getUserStats();

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gradient-to-r from-purple-500 to-pink-500 rounded-xl flex items-center justify-center">
            <User className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white">الملف الشخصي</h1>
            <p className="text-gray-400">إدارة معلوماتك وإحصائياتك</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Profile Info */}
        <div className="lg:col-span-1 space-y-6">
          <Card className="bg-black/40 border-purple-800/30">
            <CardHeader className="text-center">
              <Avatar className="w-24 h-24 mx-auto">
                <AvatarImage src={`https://api.dicebear.com/7.x/avataaars/svg?seed=${profile.username}`} />
                <AvatarFallback className="bg-purple-600 text-white text-2xl">
                  {profile.name.charAt(0)}
                </AvatarFallback>
              </Avatar>
              <CardTitle className="text-white mt-4">{profile.name}</CardTitle>
              <CardDescription className="text-gray-400">@{profile.username}</CardDescription>
              <div className="flex justify-center">
                <Badge 
                  className={`${
                    profile.role === 'admin' 
                      ? 'bg-red-500/20 text-red-400' 
                      : 'bg-blue-500/20 text-blue-400'
                  }`}
                >
                  {profile.role === 'admin' ? 'مدير' : 'مستخدم'}
                </Badge>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              {!isEditing ? (
                <>
                  <div className="flex items-center gap-3 text-gray-300">
                    <Mail className="w-4 h-4" />
                    <span className="text-sm">{profile.email}</span>
                  </div>
                  <div className="flex items-center gap-3 text-gray-300">
                    <Calendar className="w-4 h-4" />
                    <span className="text-sm">انضم في {stats.joinDate}</span>
                  </div>
                  <div className="flex items-center gap-3 text-gray-300">
                    <Clock className="w-4 h-4" />
                    <span className="text-sm">آخر نشاط: {stats.lastActive}</span>
                  </div>
                  <Button
                    onClick={() => setIsEditing(true)}
                    variant="outline"
                    className="w-full bg-gray-800 border-gray-600 text-gray-300"
                  >
                    <Edit3 className="w-4 h-4 mr-2" />
                    تعديل الملف الشخصي
                  </Button>
                </>
              ) : (
                <div className="space-y-4">
                  <div className="space-y-2">
                    <Label className="text-gray-300">الاسم</Label>
                    <Input
                      value={editForm.name}
                      onChange={(e) => setEditForm(prev => ({ ...prev, name: e.target.value }))}
                      className="bg-gray-800 border-gray-600 text-white"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label className="text-gray-300">البريد الإلكتروني</Label>
                    <Input
                      value={editForm.email}
                      onChange={(e) => setEditForm(prev => ({ ...prev, email: e.target.value }))}
                      className="bg-gray-800 border-gray-600 text-white"
                    />
                  </div>
                  <div className="flex gap-2">
                    <Button
                      onClick={handleSave}
                      disabled={isSaving}
                      className="flex-1 bg-green-600 hover:bg-green-700"
                    >
                      {isSaving ? (
                        <RefreshCw className="w-4 h-4 animate-spin" />
                      ) : (
                        <>
                          <Save className="w-4 h-4 mr-2" />
                          حفظ
                        </>
                      )}
                    </Button>
                    <Button
                      onClick={handleCancel}
                      variant="outline"
                      className="flex-1 bg-gray-800 border-gray-600"
                    >
                      إلغاء
                    </Button>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Security Info */}
          <Card className="bg-black/40 border-purple-800/30">
            <CardHeader>
              <CardTitle className="text-white flex items-center gap-2">
                <Shield className="w-5 h-5" />
                الأمان
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-gray-300">كلمة المرور</span>
                <Badge className="bg-green-500/20 text-green-400">محدثة</Badge>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-300">المصادقة الثنائية</span>
                <Badge className="bg-gray-500/20 text-gray-400">غير مفعلة</Badge>
              </div>
              <Button
                variant="outline"
                size="sm"
                className="w-full bg-gray-800 border-gray-600 text-gray-300"
              >
                تغيير كلمة المرور
              </Button>
            </CardContent>
          </Card>
        </div>

        {/* Stats and Activity */}
        <div className="lg:col-span-2 space-y-6">
          {/* Stats Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <Card className="bg-black/40 border-purple-800/30">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-400">إجمالي التفاعلات</p>
                    <p className="text-2xl font-bold text-white">{stats.totalInteractions}</p>
                  </div>
                  <MessageCircle className="w-8 h-8 text-purple-400" />
                </div>
              </CardContent>
            </Card>

            <Card className="bg-black/40 border-purple-800/30">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-400">المشاعر الغالبة</p>
                    <p className="text-2xl font-bold text-white">{stats.averageEmotion}</p>
                  </div>
                  <Heart className="w-8 h-8 text-pink-400" />
                </div>
              </CardContent>
            </Card>

            <Card className="bg-black/40 border-purple-800/30">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-400">تحسن المزاج</p>
                    <p className="text-2xl font-bold text-white">{stats.emotionTrend}</p>
                  </div>
                  <TrendingUp className="w-8 h-8 text-green-400" />
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Activity Summary */}
          <Card className="bg-black/40 border-purple-800/30">
            <CardHeader>
              <CardTitle className="text-white flex items-center gap-2">
                <Activity className="w-5 h-5" />
                ملخص النشاط
              </CardTitle>
              <CardDescription className="text-gray-400">
                نظرة عامة على تفاعلاتك مع النظام
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-4">
                  <h4 className="font-medium text-white">الميزة المفضلة</h4>
                  <div className="p-4 bg-purple-500/10 border border-purple-500/20 rounded-lg">
                    <p className="text-purple-400 font-medium">{stats.favoriteFeature}</p>
                    <p className="text-sm text-gray-400 mt-1">الأكثر استخداماً</p>
                  </div>
                </div>

                <div className="space-y-4">
                  <h4 className="font-medium text-white">إنجازات حديثة</h4>
                  <div className="space-y-2">
                    <div className="flex items-center gap-2 p-2 bg-green-500/10 border border-green-500/20 rounded-lg">
                      <CheckCircle className="w-4 h-4 text-green-400" />
                      <span className="text-sm text-white">تفاعل 100 مرة</span>
                    </div>
                    <div className="flex items-center gap-2 p-2 bg-blue-500/10 border border-blue-500/20 rounded-lg">
                      <CheckCircle className="w-4 h-4 text-blue-400" />
                      <span className="text-sm text-white">استخدم جميع الميزات</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Recent Activity */}
              <div className="space-y-4">
                <h4 className="font-medium text-white">النشاط الأخير</h4>
                <div className="space-y-3">
                  {[
                    { action: 'محادثة مع الذكاء الاصطناعي', time: 'منذ 30 دقيقة', mood: 'سعادة' },
                    { action: 'تحليل مشاعر النص', time: 'منذ ساعة', mood: 'هدوء' },
                    { action: 'عرض الإحصائيات', time: 'منذ ساعتين', mood: 'فضول' },
                  ].map((activity, index) => (
                    <div key={index} className="flex items-center justify-between p-3 bg-gray-800/50 rounded-lg">
                      <div>
                        <p className="text-white font-medium">{activity.action}</p>
                        <p className="text-sm text-gray-400">{activity.time}</p>
                      </div>
                      <Badge className="bg-blue-500/20 text-blue-400">
                        {activity.mood}
                      </Badge>
                    </div>
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
} 