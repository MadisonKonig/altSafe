// Custom useInterval Hook
import { useEffect } from "react";

function useInterval(callback, delay) {
  useEffect(() => {
    if (delay === null) return;

    const intervalId = setInterval(callback, delay);
    return () => clearInterval(intervalId);
  }, [callback, delay]);
}

export default useInterval;
