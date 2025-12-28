import { Button } from "@/components/ui/button";
import {
  MousePointer2,
  Square,
  Circle,
  Minus,
  ArrowRight,
  Type,
} from "lucide-react";
import { Separator } from "@/components/ui/separator";

export const Toolbar = () => {
  return (
    <aside className="border-r p-3 flex flex-col gap-2">
      <Button variant="ghost" size="icon" className="w-10 h-10">
        <MousePointer2 className="h-5 w-5" />
      </Button>

      <Separator />

      <Button variant="ghost" size="icon" className="w-10 h-10">
        <Square className="h-5 w-5" />
      </Button>
      <Button variant="ghost" size="icon" className="w-10 h-10">
        <Circle className="h-5 w-5" />
      </Button>
      <Button variant="ghost" size="icon" className="w-10 h-10">
        <Minus className="h-5 w-5" />
      </Button>
      <Button variant="ghost" size="icon" className="w-10 h-10">
        <ArrowRight className="h-5 w-5" />
      </Button>
      <Button variant="ghost" size="icon" className="w-10 h-10">
        <Type className="h-5 w-5" />
      </Button>

      <Separator />

      <div className="w-10 h-10 rounded border-2 bg-black" />
    </aside>
  );
};
