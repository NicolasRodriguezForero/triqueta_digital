import {
  createFileRoute,
  Link,
  Outlet,
  useLocation,
} from "@tanstack/react-router";
import {
  LayoutDashboard,
  Calendar,
  Database,
  CheckSquare,
  Sparkles,
  User,
  LogOut,
  Home,
} from "lucide-react";
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarInset,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarProvider,
  SidebarRail,
  SidebarTrigger,
} from "@/components/ui/sidebar";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { useAuth } from "@/contexts/AuthContext";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";

export const Route = createFileRoute("/admin")({
  component: AdminLayout,
});

function AdminLayout() {
  const location = useLocation();
  const { user, logout } = useAuth();

  const navItems = [
    {
      to: "/admin/dashboard",
      label: "Dashboard",
      icon: LayoutDashboard,
    },
    {
      to: "/admin/actividades",
      label: "Actividades",
      icon: Calendar,
    },
    {
      to: "/admin/etl",
      label: "Gestión ETL",
      icon: Database,
    },
    {
      to: "/admin/actividades/pendientes",
      label: "Validación",
      icon: CheckSquare,
    },
  ];

  const handleLogout = async () => {
    await logout();
  };

  return (
    <SidebarProvider>
      <Sidebar>
        <SidebarHeader>
          <div className="flex items-center gap-2 px-2 py-2">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-primary to-accent-foreground flex items-center justify-center">
              <Sparkles className="w-5 h-5 text-primary-foreground" />
            </div>
            <div className="flex flex-col">
              <span className="text-sm font-bold">Triqueta</span>
              <span className="text-xs text-muted-foreground">Admin</span>
            </div>
          </div>
        </SidebarHeader>

        <SidebarContent>
          <SidebarGroup>
            <SidebarGroupLabel>Panel de Administración</SidebarGroupLabel>
            <SidebarGroupContent>
              <SidebarMenu>
                {navItems.map((item) => {
                  const isActive = location.pathname === item.to;
                  return (
                    <SidebarMenuItem key={item.to}>
                      <SidebarMenuButton
                        asChild
                        isActive={isActive}
                        tooltip={item.label}
                      >
                        <Link to={item.to}>
                          <item.icon className="h-4 w-4" />
                          <span>{item.label}</span>
                        </Link>
                      </SidebarMenuButton>
                    </SidebarMenuItem>
                  );
                })}
              </SidebarMenu>
            </SidebarGroupContent>
          </SidebarGroup>
        </SidebarContent>

        <SidebarFooter>
          <SidebarMenu>
            {user && (
              <SidebarMenuItem>
                <Popover>
                  <PopoverTrigger asChild>
                    <SidebarMenuButton
                      tooltip="Ver perfil y opciones"
                      className="w-full"
                    >
                      <div className="w-8 h-8 rounded-full bg-gradient-to-br from-primary to-accent-foreground flex items-center justify-center shrink-0">
                        <User className="h-4 w-4 text-primary-foreground" />
                      </div>
                      <div className="flex flex-col min-w-0 flex-1 text-left">
                        <span className="text-sm font-medium truncate">
                          {user.perfil?.nombre_completo ||
                            user.email.split("@")[0]}
                        </span>
                        <span className="text-xs text-muted-foreground truncate">
                          {user.email}
                        </span>
                      </div>
                    </SidebarMenuButton>
                  </PopoverTrigger>
                  <PopoverContent
                    side="right"
                    align="end"
                    className="w-64 p-0"
                    sideOffset={8}
                  >
                    <div className="p-4">
                      {/* User Info */}
                      <div className="flex items-center gap-3 mb-4">
                        <div className="w-10 h-10 rounded-full bg-gradient-to-br from-primary to-accent-foreground flex items-center justify-center shrink-0">
                          <User className="h-5 w-5 text-primary-foreground" />
                        </div>
                        <div className="flex flex-col min-w-0 flex-1">
                          <span className="text-sm font-semibold truncate">
                            {user.perfil?.nombre_completo ||
                              user.email.split("@")[0]}
                          </span>
                          <span className="text-xs text-muted-foreground truncate">
                            {user.email}
                          </span>
                          {user.is_admin && (
                            <span className="text-xs text-primary font-medium mt-1">
                              Administrador
                            </span>
                          )}
                        </div>
                      </div>

                      <Separator className="mb-3" />

                      {/* Actions */}
                      <div className="space-y-1">
                        <Button
                          variant="ghost"
                          className="w-full justify-start gap-2"
                          asChild
                        >
                          <Link to="/">
                            <Home className="h-4 w-4" />
                            <span>Volver al sitio</span>
                          </Link>
                        </Button>
                        <Button
                          variant="ghost"
                          className="w-full justify-start gap-2 text-destructive hover:text-destructive hover:bg-destructive/10"
                          onClick={handleLogout}
                        >
                          <LogOut className="h-4 w-4" />
                          <span>Cerrar sesión</span>
                        </Button>
                      </div>
                    </div>
                  </PopoverContent>
                </Popover>
              </SidebarMenuItem>
            )}
          </SidebarMenu>
        </SidebarFooter>
        <SidebarRail />
      </Sidebar>

      <SidebarInset>
        <header className="flex h-16 shrink-0 items-center gap-2 border-b px-4">
          <SidebarTrigger className="-ml-1" />
          <h1 className="text-xl font-bold">Panel de Administrador</h1>
        </header>
        <div className="flex flex-1 flex-col gap-4 overflow-y-auto">
          <Outlet />
        </div>
      </SidebarInset>
    </SidebarProvider>
  );
}
