'use client';
import { useRealTimeData, dashboardApi } from '@/lib/api';
import StatsCard from '@/components/dashboard/StatsCard';
import ActivityList from '@/components/dashboard/ActivityList';

export default function OverviewPage() {
  const { data: stats } = useRealTimeData(dashboardApi.getStats);
  const { data: activities } = useRealTimeData(dashboardApi.getActivities);

  return (
    <div className="space-y-6 p-4">
      <h1 className="text-2xl font-bold">Dashboard Overview</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <StatsCard title="Total Interactions" value={stats?.total_interactions ?? '-'} />
        <StatsCard title="Active Users" value={stats?.active_users ?? '-'} />
        <StatsCard title="Happiness" value={stats?.happiness_level ?? '-'} />
      </div>
      <ActivityList
        title="Latest Activity"
        activities={activities?.activities ?? []}
      />
    </div>
  );
}
