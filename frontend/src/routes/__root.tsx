import { createRootRoute, Outlet, useLocation } from "@tanstack/react-router";
// import { TanStackRouterDevtools } from "@tanstack/react-router-devtools";
import { QueryProvider } from "../providers/QueryProvider";
import { Layout } from "../components/Layout";

function RootComponent() {
  const location = useLocation();
  const isAdminRoute = location.pathname.startsWith("/admin");

  return (
    <QueryProvider>
      {isAdminRoute ? (
        <Outlet />
      ) : (
        <Layout>
          <Outlet />
        </Layout>
      )}
      {/* <TanStackRouterDevtools /> */}
    </QueryProvider>
  );
}

export const Route = createRootRoute({
  component: RootComponent,
});
