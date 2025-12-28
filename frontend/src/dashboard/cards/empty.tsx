import { Button } from "@/components/ui/button";
import { Plus } from "lucide-react";

export const Empty = () => {
  return (
    <div className="flex flex-col items-center justify-center h-full text-center">
      <h2 className="text-xl font-semibold mb-2">No boards yet</h2>
      <p className="text-muted-foreground mb-4">
        Create your first whiteboard to get started
      </p>
      <Button>
        <Plus className="mr-2 h-4 w-4" />
        Create Board
      </Button>
    </div>
  );
};
