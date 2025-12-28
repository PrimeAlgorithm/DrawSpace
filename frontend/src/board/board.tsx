import { Canvas } from "./canvas/canvas";
import { Header } from "./header/header";
import { Toolbar } from "./toolbar/toolbar";

export const Board = () => {
  return (
    <div className="flex flex-col h-screen bg-background">
      <Header />
      <div className="flex flex-1 overflow-hidden">
        <Toolbar />
        <Canvas />
      </div>
    </div>
  );
};
