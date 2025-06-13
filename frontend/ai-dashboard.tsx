'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { ChartContainer, ChartTooltip, ChartTooltipContent } from '@/components/ui/chart';
import { 
    AreaChart, 
    Area, 
    BarChart, 
    Bar, 
    LineChart, 
    Line, 
    XAxis, 
    YAxis, 
    CartesianGrid, 
    ResponsiveContainer 
} from 'recharts';
import { 
    Brain, 
    MessageCircle, 
    Activity, 
    Users, 
    Heart, 
    TrendingUp, 
    Bot, 
    Zap, 
    Eye,
    Settings
} from 'lucide-react';

// بيانات وهمية للمخططات
const emotionData = [
    { name: 'الاثنين', سعادة: 80, قلق: 20, حياد: 30 },
    { name: 'الثلاثاء', سعادة: 65, قلق: 35, حياد: 25 },
    { name: 'الأربعاء', سعادة: 90, قلق: 15, حياد: 40 },
    { name: 'الخميس', سعادة: 75, قلق: 25, حياد: 35 },
    { name: 'الجمعة', سعادة: 95, قلق: 10, حياد: 45 },
    { name: 'السبت', سعادة: 85, قلق: 20, حياد: 50 },
    { name: 'الأحد', سعادة: 70, قلق: 30, حياد: 30 },
];

const interactionsData = [
    { time: '09:00', تفاعلات: 12 },
    { time: '12:00', تفاعلات: 25 },
    { time: '15:00', تفاعلات: 18 },
    { time: '18:00', تفاعلات: 32 },
    { time: '21:00', تفاعلات: 28 },
];

const skillsData = [
    { skill: 'التعاطف', فعالية: 95 },
    { skill: 'الصداقة الرقمية', فعالية: 88 },
    { skill: 'التجسيد الذهني', فعالية: 92 },
    { skill: 'إنشاء الأشقاء', فعالية: 78 },
];

export default function AIDashboard() {
    const [activeTab, setActiveTab] = useState('overview');
    const [currentTime, setCurrentTime] = useState(new Date());
    const [chatInput, setChatInput] = useState('');

    useEffect(() => {
        const timer = setInterval(() => setCurrentTime(new Date()), 1000);
        return () => clearInterval(timer);
    }, []);

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white">
            {/* Header */}
            <header className="border-b border-purple-800/30 backdrop-blur-sm bg-black/20 p-6">
                <div className="max-w-7xl mx-auto flex justify-between items-center">
                    <div className="flex items-center space-x-4">
                        <div className="w-10 h-10 bg-gradient-to-r from-purple-500 to-pink-500 rounded-xl flex items-center justify-center">
                            <Brain className="w-6 h-6 text-white" />
                        </div>
                        <div>
                            <h1 className="text-2xl font-bold bg-gradient-to-r from-white to-purple-200 bg-clip-text text-transparent">
                                Zero System Dashboard
                            </h1>
                            <p className="text-sm text-gray-400">نظام الذكاء الاصطناعي العاطفي</p>
                        </div>
                    </div>
                    <div className="flex items-center space-x-4">
                        <Badge variant="success" className="bg-green-500/20 text-green-400">
                            ● نشط
                        </Badge>
                        <span className="text-sm text-gray-400">
                            {currentTime.toLocaleTimeString('ar-EG')}
                        </span>
                        <Avatar>
                            <AvatarImage src="/api/placeholder/40/40" />
                            <AvatarFallback className="bg-purple-600">AI</AvatarFallback>
                        </Avatar>
                    </div>
                </div>
            </header>

            <div className="max-w-7xl mx-auto p-6">
                <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
                    <TabsList className="grid w-full grid-cols-5 bg-black/40 border border-purple-800/30">
                        <TabsTrigger value="overview">نظرة عامة</TabsTrigger>
                        <TabsTrigger value="emotions">المشاعر</TabsTrigger>
                        <TabsTrigger value="chat">المحادثة</TabsTrigger>
                        <TabsTrigger value="skills">المهارات</TabsTrigger>
                        <TabsTrigger value="settings">الإعدادات</TabsTrigger>
                    </TabsList>

                    {/* نظرة عامة */}
                    <TabsContent value="overview" className="space-y-6">
                        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                            <Card className="bg-black/40 border-purple-800/30">
                                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                                    <CardTitle className="text-sm font-medium text-gray-300">
                                        إجمالي التفاعلات
                                    </CardTitle>
                                    <MessageCircle className="h-4 w-4 text-blue-400" />
                                </CardHeader>
                                <CardContent>
                                    <div className="text-2xl font-bold text-white">1,247</div>
                                    <p className="text-xs text-green-400">
                                        +12% من الأسبوع الماضي
                                    </p>
                                </CardContent>
                            </Card>

                            <Card className="bg-black/40 border-purple-800/30">
                                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                                    <CardTitle className="text-sm font-medium text-gray-300">
                                        المستخدمون النشطون
                                    </CardTitle>
                                    <Users className="h-4 w-4 text-green-400" />
                                </CardHeader>
                                <CardContent>
                                    <div className="text-2xl font-bold text-white">89</div>
                                    <p className="text-xs text-green-400">
                                        +5% اليوم
                                    </p>
                                </CardContent>
                            </Card>

                            <Card className="bg-black/40 border-purple-800/30">
                                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                                    <CardTitle className="text-sm font-medium text-gray-300">
                                        مستوى السعادة
                                    </CardTitle>
                                    <Heart className="h-4 w-4 text-pink-400" />
                                </CardHeader>
                                <CardContent>
                                    <div className="text-2xl font-bold text-white">92%</div>
                                    <p className="text-xs text-pink-400">
                                        ممتاز
                                    </p>
                                </CardContent>
                            </Card>

                            <Card className="bg-black/40 border-purple-800/30">
                                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                                    <CardTitle className="text-sm font-medium text-gray-300">
                                        وقت الاستجابة
                                    </CardTitle>
                                    <Zap className="h-4 w-4 text-yellow-400" />
                                </CardHeader>
                                <CardContent>
                                    <div className="text-2xl font-bold text-white">0.3s</div>
                                    <p className="text-xs text-yellow-400">
                                        متوسط سريع
                                    </p>
                                </CardContent>
                            </Card>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <Card className="bg-black/40 border-purple-800/30">
                                <CardHeader>
                                    <CardTitle className="text-white">التفاعلات اليومية</CardTitle>
                                </CardHeader>
                                <CardContent>
                                    <ChartContainer
                                        config={{
                                            تفاعلات: { label: "التفاعلات", color: "#8b5cf6" }
                                        }}
                                        className="h-80"
                                    >
                                        <LineChart data={interactionsData}>
                                            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                                            <XAxis dataKey="time" stroke="#9ca3af" />
                                            <YAxis stroke="#9ca3af" />
                                            <ChartTooltip content={<ChartTooltipContent />} />
                                            <Line 
                                                type="monotone" 
                                                dataKey="تفاعلات" 
                                                stroke="#8b5cf6" 
                                                strokeWidth={3}
                                                dot={{ fill: "#8b5cf6", strokeWidth: 2, r: 6 }}
                                            />
                                        </LineChart>
                                    </ChartContainer>
                                </CardContent>
                            </Card>

                            <Card className="bg-black/40 border-purple-800/30">
                                <CardHeader>
                                    <CardTitle className="text-white">النشاط الأخير</CardTitle>
                                </CardHeader>
                                <CardContent className="space-y-4">
                                    {[
                                        { user: "أحمد محمد", action: "طلب دعم نفسي", time: "منذ دقيقتين", status: "success" },
                                        { user: "فاطمة علي", action: "سؤال تقني", time: "منذ 5 دقائق", status: "active" },
                                        { user: "محمد حسن", action: "إنشاء أخ رقمي", time: "منذ 10 دقائق", status: "success" },
                                        { user: "سارة أحمد", action: "محادثة عامة", time: "منذ 15 دقيقة", status: "success" },
                                    ].map((activity, index) => (
                                        <div key={index} className="flex items-center justify-between p-3 rounded-lg bg-gray-800/50">
                                            <div className="flex items-center space-x-3">
                                                <div className={`w-2 h-2 rounded-full ${
                                                    activity.status === 'success' ? 'bg-green-400' : 
                                                    activity.status === 'active' ? 'bg-blue-400 animate-pulse' : 
                                                    'bg-yellow-400'
                                                }`} />
                                                <div>
                                                    <p className="font-medium text-white">{activity.user}</p>
                                                    <p className="text-sm text-gray-400">{activity.action}</p>
                                                </div>
                                            </div>
                                            <span className="text-xs text-gray-500">{activity.time}</span>
                                        </div>
                                    ))}
                                </CardContent>
                            </Card>
                        </div>
                    </TabsContent>

                    {/* تحليل المشاعر */}
                    <TabsContent value="emotions" className="space-y-6">
                        <Card className="bg-black/40 border-purple-800/30">
                            <CardHeader>
                                <CardTitle className="text-white">تحليل المشاعر الأسبوعي</CardTitle>
                                <CardDescription className="text-gray-400">
                                    توزيع المشاعر خلال الأسبوع الماضي
                                </CardDescription>
                            </CardHeader>
                            <CardContent>
                                <ChartContainer
                                    config={{
                                        سعادة: { label: "سعادة", color: "#10b981" },
                                        قلق: { label: "قلق", color: "#f59e0b" },
                                        حياد: { label: "حياد", color: "#6b7280" }
                                    }}
                                    className="h-96"
                                >
                                    <AreaChart data={emotionData}>
                                        <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                                        <XAxis dataKey="name" stroke="#9ca3af" />
                                        <YAxis stroke="#9ca3af" />
                                        <ChartTooltip content={<ChartTooltipContent />} />
                                        <Area type="monotone" dataKey="سعادة" stackId="1" stroke="#10b981" fill="#10b981" fillOpacity={0.6} />
                                        <Area type="monotone" dataKey="قلق" stackId="1" stroke="#f59e0b" fill="#f59e0b" fillOpacity={0.6} />
                                        <Area type="monotone" dataKey="حياد" stackId="1" stroke="#6b7280" fill="#6b7280" fillOpacity={0.6} />
                                    </AreaChart>
                                </ChartContainer>
                            </CardContent>
                        </Card>
                    </TabsContent>

                    {/* المحادثة */}
                    <TabsContent value="chat" className="space-y-6">
                        <Card className="bg-black/40 border-purple-800/30">
                            <CardHeader>
                                <CardTitle className="text-white flex items-center gap-2">
                                    <Bot className="w-5 h-5" />
                                    محادثة مع النظام
                                </CardTitle>
                            </CardHeader>
                            <CardContent className="space-y-4">
                                <div className="h-96 overflow-y-auto space-y-4 p-4 bg-gray-900/50 rounded-lg">
                                    <div className="flex justify-start">
                                        <div className="bg-purple-600 text-white p-3 rounded-lg max-w-xs">
                                            مرحباً! أنا نظام Zero System. كيف يمكنني مساعدتك اليوم؟
                                        </div>
                                    </div>
                                    <div className="flex justify-end">
                                        <div className="bg-blue-600 text-white p-3 rounded-lg max-w-xs">
                                            أشعر بالقلق بشأن مشروعي الجديد
                                        </div>
                                    </div>
                                    <div className="flex justify-start">
                                        <div className="bg-purple-600 text-white p-3 rounded-lg max-w-xs">
                                            أتفهم شعورك تماماً. القلق شعور طبيعي عند بدء مشروع جديد. دعنا نتحدث عن ما يقلقك تحديداً... 💙
                                        </div>
                                    </div>
                                </div>
                                <div className="flex gap-2">
                                    <Input
                                        placeholder="اكتب رسالتك هنا..."
                                        value={chatInput}
                                        onChange={(e) => setChatInput(e.target.value)}
                                        className="bg-gray-800 border-gray-600 text-white"
                                    />
                                    <Button className="bg-purple-600 hover:bg-purple-700">
                                        إرسال
                                    </Button>
                                </div>
                            </CardContent>
                        </Card>
                    </TabsContent>

                    {/* المهارات */}
                    <TabsContent value="skills" className="space-y-6">
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <Card className="bg-black/40 border-purple-800/30">
                                <CardHeader>
                                    <CardTitle className="text-white">فعالية المهارات</CardTitle>
                                </CardHeader>
                                <CardContent>
                                    <ChartContainer
                                        config={{
                                            فعالية: { label: "الفعالية %", color: "#8b5cf6" }
                                        }}
                                        className="h-80"
                                    >
                                        <BarChart data={skillsData}>
                                            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                                            <XAxis dataKey="skill" stroke="#9ca3af" fontSize={12} />
                                            <YAxis stroke="#9ca3af" />
                                            <ChartTooltip content={<ChartTooltipContent />} />
                                            <Bar dataKey="فعالية" fill="#8b5cf6" radius={[4, 4, 0, 0]} />
                                        </BarChart>
                                    </ChartContainer>
                                </CardContent>
                            </Card>

                            <Card className="bg-black/40 border-purple-800/30">
                                <CardHeader>
                                    <CardTitle className="text-white">حالة المهارات</CardTitle>
                                </CardHeader>
                                <CardContent className="space-y-4">
                                    {[
                                        { name: "مستشعر التعاطف", status: "نشط", performance: 95 },
                                        { name: "الصداقة الرقمية", status: "نشط", performance: 88 },
                                        { name: "التجسيد الذهني", status: "نشط", performance: 92 },
                                        { name: "إنشاء الأشقاء", status: "تطوير", performance: 78 },
                                    ].map((skill, index) => (
                                        <div key={index} className="flex items-center justify-between p-3 rounded-lg bg-gray-800/50">
                                            <div className="flex items-center space-x-3">
                                                <div className={`w-3 h-3 rounded-full ${
                                                    skill.status === 'نشط' ? 'bg-green-400' : 'bg-yellow-400'
                                                }`} />
                                                <span className="text-white">{skill.name}</span>
                                            </div>
                                            <div className="flex items-center space-x-2">
                                                <Badge variant={skill.status === 'نشط' ? 'default' : 'info'}>
                                                    {skill.status}
                                                </Badge>
                                                <span className="text-sm text-gray-400">{skill.performance}%</span>
                                            </div>
                                        </div>
                                    ))}
                                </CardContent>
                            </Card>
                        </div>
                    </TabsContent>

                    {/* الإعدادات */}
                    <TabsContent value="settings" className="space-y-6">
                        <Card className="bg-black/40 border-purple-800/30">
                            <CardHeader>
                                <CardTitle className="text-white flex items-center gap-2">
                                    <Settings className="w-5 h-5" />
                                    إعدادات النظام
                                </CardTitle>
                            </CardHeader>
                            <CardContent className="space-y-6">
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                    <div className="space-y-4">
                                        <h3 className="text-lg font-medium text-white">الإعدادات العامة</h3>
                                        <div className="space-y-3">
                                            <div className="flex items-center justify-between">
                                                <span className="text-gray-300">تسجيل التفاعلات</span>
                                                <Badge className="bg-green-500/20 text-green-400">مفعل</Badge>
                                            </div>
                                            <div className="flex items-center justify-between">
                                                <span className="text-gray-300">تحليل المشاعر</span>
                                                <Badge className="bg-green-500/20 text-green-400">مفعل</Badge>
                                            </div>
                                            <div className="flex items-center justify-between">
                                                <span className="text-gray-300">النسخ الاحتياطي</span>
                                                <Badge className="bg-blue-500/20 text-blue-400">تلقائي</Badge>
                                            </div>
                                        </div>
                                    </div>
                                    
                                    <div className="space-y-4">
                                        <h3 className="text-lg font-medium text-white">إحصائيات النظام</h3>
                                        <div className="space-y-3">
                                            <div className="flex items-center justify-between">
                                                <span className="text-gray-300">وقت التشغيل</span>
                                                <span className="text-white">15 يوم، 3 ساعات</span>
                                            </div>
                                            <div className="flex items-center justify-between">
                                                <span className="text-gray-300">استخدام الذاكرة</span>
                                                <span className="text-white">67%</span>
                                            </div>
                                            <div className="flex items-center justify-between">
                                                <span className="text-gray-300">الإصدار</span>
                                                <span className="text-white">v0.1.0</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </CardContent>
                        </Card>
                    </TabsContent>
                </Tabs>
            </div>
        </div>
    );
} 