import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';

export interface Activity {
  id: string | number;
  message: string;
  time: string;
}

export interface ActivityListProps {
  title?: string;
  activities: Activity[];
}

export const ActivityList = ({ title = 'Recent Activity', activities }: ActivityListProps) => (
  <Card>
    <CardHeader>
      <CardTitle>{title}</CardTitle>
    </CardHeader>
    <CardContent>
      <ul className="space-y-2">
        {activities.map((act) => (
          <li key={act.id} className="flex justify-between text-sm">
            <span>{act.message}</span>
            <span className="text-muted-foreground">{act.time}</span>
          </li>
        ))}
      </ul>
    </CardContent>
  </Card>
);

export default ActivityList;
