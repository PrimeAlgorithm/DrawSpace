import { SidebarProvider, SidebarInset } from "@/components/ui/sidebar";
import { AppSidebar } from "./sidebar/app-sidebar";
import { TopHeader } from "./header/top-header";
import { CardHolder } from "./cards/card-holder";
import { useAuth } from "@/context/AuthContext";
import { Navigate } from "react-router";

export const Dashboard = () => {
  const boards = [
    { id: "1", name: "Project Planning", created_at: "2025-01-15" },
    { id: "2", name: "Design Wireframes", created_at: "2025-01-14" },
    { id: "3", name: "Team Brainstorm", created_at: "2025-01-13" },
  ];

  const { user, loading } = useAuth();
  if (loading) return <div>Loading...</div>;
  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return (
    <SidebarProvider>
      <AppSidebar />
      <SidebarInset>
        <div className="flex flex-col h-screen">
          <TopHeader />
          <main>
            <CardHolder boards={boards} />
          </main>
        </div>
      </SidebarInset>
    </SidebarProvider >
  );
};
