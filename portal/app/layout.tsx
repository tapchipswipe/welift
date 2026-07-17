import type { Metadata } from "next";
import { ClerkProvider } from "@clerk/nextjs";
import "./globals.css";

export const metadata: Metadata = {
  title: "We Lift Dispatcher Portal",
  description: "Mobile-first dispatcher portal for gate code management",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <ClerkProvider>
      <html
        lang="en"
        className="h-full antialiased"
      >
        <body className="min-h-full flex flex-col bg-slate-950 text-slate-100">{children}</body>
      </html>
    </ClerkProvider>
  );
}


