 mzfkbd-codex/create-dashboard-components-and-pages
=======
 codex/create-dashboard-components-and-pages
"use client";
import React from "react";
import Charts from "@/components/dashboard/Charts";

const AnalyticsPage: React.FC = () => (
  <div className="space-y-6">
    <Charts />
  </div>
);

export default AnalyticsPage;
=======
 main
'use client';
import { useEffect, useState } from 'react';
import { dashboardApi } from '@/lib/api';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';

export default function AnalyticsPage() {
  const [data, setData] = useState<any[]>([]);

  useEffect(() => {
    dashboardApi.getInteractions().then((res) => {
      if (res.data) {
        const d = (res.data.data || res.data) as any[];
        setData(d);
      }
    });
  }, []);

  return (
    <div className="p-4 space-y-6">
      <h1 className="text-2xl font-bold">Analytics</h1>
      <div className="w-full h-64">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data} margin={{ top: 5, right: 20, left: 10, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="time" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="تفاعلات" stroke="#8884d8" />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
 mzfkbd-codex/create-dashboard-components-and-pages
=======
 main
 main
