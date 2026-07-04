import type { Metadata } from 'next';import './globals.css';import { Providers } from '@/components/providers';
export const metadata: Metadata = { title: 'Odoo HRMS — Every workday aligned', description: 'A production-grade Human Resource Management System dashboard for employees and HR admins.' };
export default function RootLayout({ children }: { children: React.ReactNode }) { return <html lang="en" className="dark"><body><Providers>{children}</Providers></body></html>; }
