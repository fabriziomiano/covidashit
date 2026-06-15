import { useEffect, useState } from 'react';

export interface AsyncState<T> {
  data: T | null;
  error: Error | null;
  loading: boolean;
}

export function useAsync<T>(factory: () => Promise<T>, deps: unknown[]): AsyncState<T> {
  const [state, setState] = useState<AsyncState<T>>({ data: null, error: null, loading: true });

  useEffect(() => {
    let alive = true;
    queueMicrotask(() => {
      if (alive) setState({ data: null, error: null, loading: true });
    });
    factory()
      .then((data) => {
        if (alive) setState({ data, error: null, loading: false });
      })
      .catch((error: Error) => {
        if (alive) setState({ data: null, error, loading: false });
      });
    return () => {
      alive = false;
    };
    // The caller owns the dependency list, similar to React's built-in hooks.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);

  return state;
}
