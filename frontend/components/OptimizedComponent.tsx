import React, { useCallback, useMemo } from 'react';

interface Item {
  id: number;
  name: string;
  active: boolean;
}

interface OptimizedComponentProps {
  items: Item[];
}

export const OptimizedComponent = ({ items }: OptimizedComponentProps) => {
  // تحسين الدوال باستخدام useCallback
  const handleClick = useCallback((id: number) => {
    console.log(`تم النقر على العنصر ${id}`);
  }, []);

  // تحسين الحسابات باستخدام useMemo
  const filteredItems = useMemo(() => {
    return items.filter(item => item.active);
  }, [items]);

  return (
    <div>
      {filteredItems.map(item => (
        <button
          key={item.id}
          onClick={() => handleClick(item.id)}
          className="p-2 m-1 bg-blue-100 rounded"
        >
          {item.name}
        </button>
      ))}
    </div>
  );
}; 