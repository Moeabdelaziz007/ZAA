#!/bin/bash

# 🚀 Zentix AI - Complete System Startup Script
# Arabic Emotional AI - Powered by Zentix

echo "🚀 بدء تشغيل نظام Zentix AI"
echo "=================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 غير مثبت. يرجى تثبيت Python 3.8+ أولاً"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js غير مثبت. يرجى تثبيت Node.js 18+ أولاً"
    exit 1
fi

# Function to check if port is available
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null ; then
        echo "⚠️  المنفذ $port مستخدم بالفعل"
        return 1
    else
        return 0
    fi
}

# Check if ports are available
if ! check_port 5000; then
    echo "❌ المنفذ 5000 (Backend) مستخدم. يرجى إيقاف العملية أو استخدام منفذ آخر"
    exit 1
fi

if ! check_port 3000; then
    echo "❌ المنفذ 3000 (Frontend) مستخدم. يرجى إيقاف العملية أو استخدام منفذ آخر"
    exit 1
fi

echo "✅ فحص المتطلبات مكتمل"

# Start Backend
echo ""
echo "🐍 تشغيل الخلفية (Backend)..."
cd backend/

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 إنشاء بيئة افتراضية..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 تفعيل البيئة الافتراضية..."
source venv/bin/activate || {
    echo "❌ فشل في تفعيل البيئة الافتراضية"
    exit 1
}

# Install requirements
echo "📥 تثبيت متطلبات Python..."
pip install -r requirements.txt > /dev/null 2>&1 || {
    echo "❌ فشل في تثبيت متطلبات Python"
    exit 1
}

# Copy environment file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📄 نسخ ملف متغيرات البيئة..."
    cp env.example .env
fi

# Start FastAPI server in background
echo "🚀 تشغيل خادم FastAPI..."
nohup uvicorn backend.main:app --host 0.0.0.0 --port 8000 > backend.log 2>&1 &
BACKEND_PID=$!
echo "✅ الخلفية تعمل على المنفذ 8000 (PID: $BACKEND_PID)"

# Wait a moment for backend to start
sleep 3

# Check if backend is running
if ! ps -p $BACKEND_PID > /dev/null; then
    echo "❌ فشل في تشغيل الخلفية. تحقق من ملف backend.log"
    exit 1
fi

# Start Frontend
echo ""
echo "⚛️  تشغيل الواجهة (Frontend)..."
cd ../frontend/

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "📦 تثبيت متطلبات Node.js..."
    npm install > /dev/null 2>&1 || {
        echo "❌ فشل في تثبيت متطلبات Node.js"
        kill $BACKEND_PID
        exit 1
    }
fi

# Copy environment file if it doesn't exist
if [ ! -f ".env.local" ]; then
    echo "📄 نسخ ملف متغيرات البيئة للواجهة..."
    cp env.example .env.local
fi

# Start Next.js app in background
echo "🚀 تشغيل خادم Next.js..."
nohup npm run dev > frontend.log 2>&1 &
FRONTEND_PID=$!
echo "✅ الواجهة تعمل على المنفذ 3000 (PID: $FRONTEND_PID)"

# Wait for frontend to start
echo ""
echo "⏳ انتظار تشغيل الواجهة..."
sleep 10

# Check if both services are running
echo ""
echo "🔍 فحص حالة الخدمات..."

if ps -p $BACKEND_PID > /dev/null; then
    echo "✅ الخلفية (Backend) تعمل بنجاح"
else
    echo "❌ الخلفية متوقفة"
fi

if ps -p $FRONTEND_PID > /dev/null; then
    echo "✅ الواجهة (Frontend) تعمل بنجاح"
else
    echo "❌ الواجهة متوقفة"
fi

# Save PIDs for cleanup
echo $BACKEND_PID > .backend_pid
echo $FRONTEND_PID > .frontend_pid

echo ""
echo "🎉 تم تشغيل نظام Zentix AI بنجاح!"
echo "=================================="
echo "🌐 الواجهة: http://localhost:3000"
echo "🔌 API: http://localhost:5000"
echo ""
echo "👤 بيانات الدخول التجريبية:"
echo "   مدير: admin / admin123"
echo "   مستخدم: user / user123"
echo ""
echo "📝 ملفات السجل:"
echo "   الخلفية: backend/backend.log"
echo "   الواجهة: frontend/frontend.log"
echo ""
echo "🛑 لإيقاف النظام، استخدم:"
echo "   ./stop.sh"
echo ""
echo "🚀 استمتع بتجربة الذكاء الاصطناعي العاطفي العربي!"

# Keep script running and monitor services
echo ""
echo "📊 مراقبة النظام... (اضغط Ctrl+C للخروج)"
while true; do
    sleep 30
    if ! ps -p $BACKEND_PID > /dev/null; then
        echo "⚠️  $(date): الخلفية متوقفة!"
    fi
    if ! ps -p $FRONTEND_PID > /dev/null; then
        echo "⚠️  $(date): الواجهة متوقفة!"
    fi
done 