import { Button } from "@/components/ui/button";
import { Plus } from "lucide-react";

export const TopHeader = () => {
  return (
    <header className="border-b px-6 py-4 flex items-center justify-between">
      <div>
        <h1 className="text-2xl font-bold">Your Boards</h1>
        <p className="text-sm text-muted-foreground">
          Create and manage your whiteboards
        </p>
      </div>
      <Button>
        <Plus className="mr-2 h-4 w-4" />
        New Board
      </Button>
    </header>
  );
};
