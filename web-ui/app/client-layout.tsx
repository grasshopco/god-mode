'use client';

import { ThemeProvider } from '@grasshop/ui';
import { Toaster } from "@/components/ui/sonner";

export default function ClientLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <ThemeProvider>
      <Toaster />
      <div className="min-h-screen">
        {children}
      </div>
    </ThemeProvider>
  );
} 