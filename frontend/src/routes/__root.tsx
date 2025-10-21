import { createRootRoute, Outlet } from "@tanstack/react-router";
import { TanStackRouterDevtools } from "@tanstack/react-router-devtools";
import { QueryProvider } from "../providers/QueryProvider";
import { Layout } from "../components/Layout";

export const Route = createRootRoute({
  component: () => (
    <QueryProvider>
      <Layout>
        <Outlet />
      </Layout>
      <TanStackRouterDevtools />
    </QueryProvider>
  ),
});
