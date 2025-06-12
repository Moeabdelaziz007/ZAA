import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';

export interface StatsCardProps {
  title: string;
  value: string | number;
  description?: string;
}

export const StatsCard = ({ title, value, description }: StatsCardProps) => (
  <Card>
    <CardHeader>
      <CardTitle>{title}</CardTitle>
    </CardHeader>
    <CardContent>
      <p className="text-2xl font-bold">{value}</p>
      {description && (
        <p className="text-sm text-muted-foreground">{description}</p>
      )}
    </CardContent>
  </Card>
);

export default StatsCard;
