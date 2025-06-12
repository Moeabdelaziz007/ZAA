"use client";
import React from "react";

export const Cards: React.FC = () => {
  return (
    <div className="space-y-4">
      <div className="p-4 bg-gray-100 rounded-md">Card 1</div>
      <div className="p-4 bg-gray-100 rounded-md">Card 2</div>
      <div className="p-4 bg-gray-100 rounded-md">Card 3</div>
    </div>
  );
};

export default Cards;
