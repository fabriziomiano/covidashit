import { useEffect, useState } from 'react';

export interface AsyncState<T> {
  data: T | null;
  error: Error | null;
  loading: boolean;
}

export function useAsync<T>(factory: (signal?: AbortSignal) => Promise<T>, deps: unknown[]): AsyncState<T> {
  const [state, setState] = useState<AsyncState<T>>({ data: null, error: null, loading: true });

  useEffect(() => {
    const controller = new AbortController();
    setState((current) => ({ data: current.data, error: null, loading: true }));

    factory(controller.signal)
      .then((data) => {
        setState({ data, error: null, loading: false });
      })
      .catch((error: Error) => {
        if (controller.signal.aborted) return;
        setState({ data: null, error, loading: false });
      });

    return () => controller.abort();
    // The caller owns the dependency list, similar to React's built-in hooks.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);

  return state;
}
