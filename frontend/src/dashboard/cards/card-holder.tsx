import { Empty } from "./empty";
import type { BoardListProps } from "@/types";
import { UserCreatedBoard } from "./user-created-board";

export const CardHolder = ({ boards }: BoardListProps) => {
  return (
    <div className="flex-1 p-6 overflow-auto">
      {boards.length === 0 ? (
        <Empty />
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {boards.map((board) => (
            <UserCreatedBoard board={board} />
          ))}
        </div>
      )}
    </div>
  );
};
