import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'financeIntel | P2P Decision Intelligence Layer',
  description: 'AI-Powered Cross-Document Decision Intelligence for Procure-to-Pay Exceptions',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
