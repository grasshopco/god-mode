// Define metadata for the app (server component)
export const metadata = {
  title: 'God Mode Web UI',
  description: 'A modern web interface for the God Mode system',
};

// Client component wrapper
import ClientLayout from './client-layout';
import './globals.css';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <title>God Mode Web UI</title>
        <meta
          name="description"
          content="A modern web interface for the God Mode system"
        />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </head>
      <body>
        <ClientLayout>
          {children}
        </ClientLayout>
      </body>
    </html>
  );
}
