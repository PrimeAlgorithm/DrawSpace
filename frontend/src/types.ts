export interface Board {
  id: string;
  name: string;
  created_at: string;
}

export interface BoardListProps {
  boards: Board[];
}
