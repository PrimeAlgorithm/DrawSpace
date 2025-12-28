import {
  Card,
  CardHeader,
  CardDescription,
  CardTitle,
} from "@/components/ui/card";

import type { Board } from "@/types";

export const UserCreatedBoard = ({ board }: { board: Board }) => {
  return (
    <Card
      key={board.id}
      className="cursor-pointer hover:border-primary transition-colors"
      onClick={() => {
        console.log("Open board:", board.id);
      }}
    >
      {/* Placeholder thumbnail */}
      <div className="h-48 bg-muted rounded-t-lg flex items-center justify-center">
        <p className="text-muted-foreground">Board Preview</p>
      </div>
      <CardHeader>
        <CardTitle className="text-lg">{board.name}</CardTitle>
        <CardDescription>
          Created {new Date(board.created_at).toLocaleDateString()}
        </CardDescription>
      </CardHeader>
    </Card>
  );
};
