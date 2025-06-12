import React from 'react';

interface GridLayoutProps {
  children: React.ReactNode;
}

export const GridLayout = ({ children }: GridLayoutProps) => {
  return (
    <div className="
      grid
      grid-cols-1
      sm:grid-cols-2
      md:grid-cols-3
      lg:grid-cols-4
      gap-4
      p-4
    ">
      {children}
    </div>
  );
}; 