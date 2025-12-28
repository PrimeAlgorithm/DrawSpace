import { Button } from "@/components/ui/button";
import { ArrowLeft } from "lucide-react";

export const Header = () => {
  return (
    <header className="border-b px-4 py-2 flex items-center justify-between">
      <div className="flex items-center gap-5">
        <Button variant="ghost" size="icon">
          <ArrowLeft className="h-5 w-5" />
        </Button>
        <h1 className="text-lg font-semibold">Board Name</h1>
      </div>
      <div className="flex items-center gap-2">
        <Button variant="outline" size="sm">
          Share
        </Button>
        <Button variant="outline" size="sm">
          Export
        </Button>
      </div>
    </header>
  );
};
