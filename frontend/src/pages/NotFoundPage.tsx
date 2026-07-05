import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/Button';

export default function NotFoundPage() {
  return (
    <div className="min-h-screen bg-background flex flex-col items-center justify-center p-4 text-center">
      <div className="text-9xl font-black text-accent/10 absolute select-none pointer-events-none -translate-y-1/2 top-1/2">
        404
      </div>
      <div className="relative z-10">
        <h1 className="text-4xl font-bold tracking-tight mb-2">Page not found</h1>
        <p className="text-primary/60 max-w-md mx-auto mb-8">
          Sorry, we couldn't find the page you're looking for. It might have been moved or deleted.
        </p>
        <Link to="/">
          <Button>Return Home</Button>
        </Link>
      </div>
    </div>
  );
}
