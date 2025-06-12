"use client";
import React from "react";
import Cards from "@/components/dashboard/Cards";
import StatsWidget from "@/components/dashboard/StatsWidget";

const OverviewPage: React.FC = () => (
  <div className="space-y-6">
    <StatsWidget />
    <Cards />
  </div>
);

export default OverviewPage;
