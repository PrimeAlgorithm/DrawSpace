import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
} from "@/components/ui/dropdown-menu";
import {
  SidebarFooter,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar";
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar";
import { ChevronUp } from "lucide-react";
import { useAuth } from "@/context/AuthContext";

export const AppSidebarFooter = () => {
  const { user } = useAuth()

  return (
    <SidebarFooter>
      <SidebarMenu>
        <SidebarMenuItem>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <SidebarMenuButton size="lg">
                <Avatar className="h-8 w-8">
                  <AvatarImage src="https://github.com/evilrabbit.png" />
                  <AvatarFallback>ER</AvatarFallback>
                </Avatar>
                <div className="flex flex-col gap-0.5 leading-none">
                  <span className="font-semibold">{user?.name}</span>
                  <span className="text-xs">{user?.email}</span>
                </div>
                <ChevronUp className="ml-auto" />
              </SidebarMenuButton>
            </DropdownMenuTrigger>

            <DropdownMenuContent
              side="top"
              className="w-[var(--radix-dropdown-menu-trigger-width)] min-w-56"
            >
              {/* <DropdownMenuItem>
                <span>Account Settings</span>
              </DropdownMenuItem>
              <DropdownMenuItem>
                <span>Billing</span>
              </DropdownMenuItem>
              <DropdownMenuSeparator /> */}
              <DropdownMenuItem>
                <span>Sign Out</span>
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </SidebarMenuItem>
      </SidebarMenu>
    </SidebarFooter>
  );
};
