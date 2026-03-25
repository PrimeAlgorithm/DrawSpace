import type { LucideIcon } from "lucide-react";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface FeatureCardProps {
  icon: LucideIcon;
  title: string;
  description: string;
}

export const FeatureCard = ({
  icon: Icon,
  title,
  description,
}: FeatureCardProps) => {
  return (
    <Card className="gap-4 border-white/10 bg-black/75 py-5 shadow-none">
      <CardHeader className="px-5">
        <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-white/8 text-white">
          <Icon className="h-5 w-5" />
        </div>
        <CardTitle className="text-lg text-slate-100">{title}</CardTitle>
      </CardHeader>
      <CardContent className="px-5">
        <p className="text-sm leading-6 text-slate-400">{description}</p>
      </CardContent>
    </Card>
  );
};
