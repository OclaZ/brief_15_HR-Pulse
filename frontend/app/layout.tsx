import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "HR Pulse",
  description: "HR Pulse est une application de feedback continu pour les employés, conçue pour améliorer l'engagement et la satisfaction au travail. Avec HR Pulse, les employés peuvent facilement partager leurs impressions et suggestions, tandis que les managers peuvent suivre le moral de leur équipe en temps réel grâce à des analyses approfondies.",
};

// frontend/src/app/layout.tsx

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      {/* Ajoute suppressHydrationWarning ici */}
      <body suppressHydrationWarning className={`${geistSans.variable} ${geistMono.variable} antialiased`}>
        {children}
      </body>
    </html>
  );
}