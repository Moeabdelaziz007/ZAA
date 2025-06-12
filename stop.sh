#!/bin/bash

# 🛑 Zentix AI - System Shutdown Script
# Arabic Emotional AI - Powered by Zentix

echo "🛑 إيقاف نظام Zentix AI"
echo "========================="

# Function to kill process by PID
kill_process() {
    local pid=$1
    local name=$2
    
    if [ -n "$pid" ] && ps -p $pid > /dev/null 2>&1; then
        echo "🔄 إيقاف $name (PID: $pid)..."
        kill $pid
        sleep 2
        
        # Force kill if still running
        if ps -p $pid > /dev/null 2>&1; then
            echo "💥 فرض إيقاف $name..."
            kill -9 $pid
        fi
        
        if ! ps -p $pid > /dev/null 2>&1; then
            echo "✅ تم إيقاف $name بنجاح"
        else
            echo "❌ فشل في إيقاف $name"
        fi
    else
        echo "⚠️  $name غير متشغل أو معرف العملية غير صحيح"
    fi
}

# Read PIDs from files
BACKEND_PID=""
FRONTEND_PID=""

if [ -f ".backend_pid" ]; then
    BACKEND_PID=$(cat .backend_pid)
fi

if [ -f ".frontend_pid" ]; then
    FRONTEND_PID=$(cat .frontend_pid)
fi

# Kill processes
if [ -n "$BACKEND_PID" ]; then
    kill_process $BACKEND_PID "الخلفية (Backend)"
else
    echo "⚠️  معرف عملية الخلفية غير موجود"
fi

if [ -n "$FRONTEND_PID" ]; then
    kill_process $FRONTEND_PID "الواجهة (Frontend)"
else
    echo "⚠️  معرف عملية الواجهة غير موجود"
fi

# Kill any remaining Flask or Next.js processes
echo ""
echo "🔍 البحث عن عمليات متبقية..."

# Kill Flask processes on port 5000
FLASK_PIDS=$(lsof -ti:5000)
if [ -n "$FLASK_PIDS" ]; then
    echo "🔄 إيقاف عمليات Flask المتبقية..."
    echo $FLASK_PIDS | xargs kill -9 2>/dev/null || true
fi

# Kill Next.js processes on port 3000
NEXTJS_PIDS=$(lsof -ti:3000)
if [ -n "$NEXTJS_PIDS" ]; then
    echo "🔄 إيقاف عمليات Next.js المتبقية..."
    echo $NEXTJS_PIDS | xargs kill -9 2>/dev/null || true
fi

# Clean up PID files
if [ -f ".backend_pid" ]; then
    rm .backend_pid
    echo "🗑️  تم حذف ملف معرف الخلفية"
fi

if [ -f ".frontend_pid" ]; then
    rm .frontend_pid
    echo "🗑️  تم حذف ملف معرف الواجهة"
fi

# Clean up log files (optional)
read -p "🗑️  هل تريد حذف ملفات السجل؟ (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if [ -f "backend/backend.log" ]; then
        rm backend/backend.log
        echo "🗑️  تم حذف سجل الخلفية"
    fi
    if [ -f "frontend/frontend.log" ]; then
        rm frontend/frontend.log
        echo "🗑️  تم حذف سجل الواجهة"
    fi
fi

echo ""
echo "✅ تم إيقاف نظام Zentix AI بنجاح"
echo "================================="
echo "💡 لتشغيل النظام مرة أخرى، استخدم:"
echo "   ./start.sh"
echo ""
echo "🙏 شكراً لاستخدام Zentix AI!" 